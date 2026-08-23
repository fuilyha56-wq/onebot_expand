"""SnowLuma QZone 摘要接口的详情与楼中楼回复兼容层。

SnowLuma 的 ``get_qzone_msg_list`` 为了稳定的 OneBot 输出会裁剪
``commentlist``。本模块复用协议端提供的 QZone Cookie，以原版 QZone CGI
请求补回完整评论树，并严格构造楼中楼回复所需的表单字段。
"""

from __future__ import annotations

import asyncio
import json
import re
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from typing import Any, Literal
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

QZONE_DETAIL_URL = (
    "https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/"
    "cgi-bin/emotion_cgi_msgdetail_v6"
)
QZONE_USER_FEEDS_URL = (
    "https://user.qzone.qq.com/proxy/domain/taotao.qq.com/"
    "cgi-bin/emotion_cgi_msglist_v6"
)
QZONE_REPLY_URL = (
    "https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/"
    "cgi-bin/emotion_cgi_re_feeds"
)
QZONE_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/138.0.0.0 Safari/537.36"
)


class QzoneCompatibilityError(RuntimeError):
    """QZone 详情或楼中楼兼容请求无法安全完成时抛出。"""


@dataclass(frozen=True, slots=True)
class QzoneHttpRequest:
    """一条不含 Cookie 的 QZone HTTP 请求描述。"""

    url: str
    method: Literal["GET", "POST"]
    body: str
    headers: dict[str, str]


QzoneRequester = Callable[[QzoneHttpRequest], Awaitable[str]]


def parse_qzone_cookie_string(cookie_string: str) -> dict[str, str]:
    """把协议端返回的 Cookie 字符串解析为键值字典。"""
    cookies: dict[str, str] = {}
    for segment in str(cookie_string).split(";"):
        key, separator, value = segment.strip().partition("=")
        if separator and key and value:
            cookies[key] = value
    return cookies


def calculate_qzone_gtk(p_skey: str) -> str:
    """按 QZone 规则从 ``p_skey`` 计算请求使用的 ``g_tk``。"""
    if not p_skey:
        raise QzoneCompatibilityError("QZone Cookie 缺少 p_skey。")
    value = 5381
    for character in p_skey:
        value += (value << 5) + ord(character)
    return str(value & 0x7FFFFFFF)


def _first_value(item: Mapping[str, Any], keys: tuple[str, ...]) -> Any:
    """返回字段别名中的第一个非空值。"""
    for key in keys:
        value = item.get(key)
        if value is not None and value != "":
            return value
    return None


def _as_int(value: Any) -> int:
    """把协议中的数字或数字字符串安全转换为整数。"""
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _as_text(value: Any) -> str:
    """把协议字段收敛为去除首尾空白的字符串。"""
    return str(value).strip() if value is not None else ""


def _as_dict_list(value: Any) -> list[dict[str, Any]]:
    """从未知值中提取字典列表。"""
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _normalize_qzone_comment(
    comment: Mapping[str, Any],
    parent_comment_id: str | None = None,
) -> dict[str, Any]:
    """归一化一条 QZone 评论及其明确的楼中楼子评论。"""
    comment_id = _as_text(
        _first_value(comment, ("tid", "commentid", "comment_id", "commentId"))
    )
    normalized: dict[str, Any] = {
        "comment_id": comment_id,
        "uin": _as_int(_first_value(comment, ("uin", "user_id", "userId"))),
        "nickname": _as_text(_first_value(comment, ("name", "nickname", "nick"))),
        "content": _as_text(_first_value(comment, ("content", "text", "comment"))),
        "list_3": [],
    }
    if parent_comment_id:
        normalized["parent_comment_id"] = parent_comment_id
    normalized["list_3"] = [
        _normalize_qzone_comment(child, comment_id or parent_comment_id)
        for child in _as_dict_list(
            _first_value(comment, ("list_3", "reply_list", "sub_comments"))
        )
    ]
    return normalized


def _extract_detail_record(payload: Mapping[str, Any]) -> Mapping[str, Any]:
    """从根对象、data 包装或 msglist 包装中抽取单条说说详情。"""
    data = payload.get("data")
    container = data if isinstance(data, dict) else payload
    msglist = _as_dict_list(container.get("msglist"))
    if msglist:
        return msglist[0]
    return container


def _ensure_qzone_success(payload: Mapping[str, Any]) -> None:
    """在 QZone CGI 声明失败时抛出不暴露 Cookie 的错误。"""
    for key in ("subcode", "code"):
        value = payload.get(key)
        if value is None or value == "":
            continue
        numeric_value = _as_int(value)
        if numeric_value != 0:
            message = _as_text(
                _first_value(payload, ("message", "msg", "wording"))
            )
            suffix = f": {message}" if message else ""
            raise QzoneCompatibilityError(f"QZone 请求失败（{key}={numeric_value}）{suffix}")


def _normalize_qzone_record(
    record: Mapping[str, Any],
    *,
    fallback_uin: int = 0,
) -> dict[str, Any]:
    """归一化单条 QZone 说说及其结构化评论树。"""
    tid = _as_text(_first_value(record, ("tid", "id", "key")))
    if not tid:
        raise QzoneCompatibilityError("QZone 说说详情响应缺少 tid。")

    images: list[str] = []
    for picture in _as_dict_list(_first_value(record, ("pic", "pictotal"))):
        image_url = _as_text(
            _first_value(picture, ("url3", "url2", "url1", "smallurl"))
        )
        if image_url:
            images.append(image_url)

    comments = [
        _normalize_qzone_comment(comment)
        for comment in _as_dict_list(
            _first_value(record, ("commentlist", "comment_list", "comments"))
        )
    ]
    normalized_uin = _as_int(
        _first_value(record, ("uin", "user_id", "owner_uin"))
    )
    return {
        "tid": tid,
        "uin": normalized_uin or fallback_uin,
        "content": _as_text(_first_value(record, ("content", "text", "summary"))),
        "created_time": _as_int(
            _first_value(record, ("created_time", "time", "abstime"))
        ),
        "comment_num": _as_int(
            _first_value(
                record,
                ("commentnum", "cmtnum", "comment_num", "comment_count"),
            )
        ),
        "images": images,
        "commentlist": comments,
    }


def normalize_qzone_msg_detail(payload: Mapping[str, Any]) -> dict[str, Any]:
    """将 ``msgdetail_v6`` 原始结果变为稳定的完整评论树。"""
    _ensure_qzone_success(payload)
    record = _extract_detail_record(payload)
    _ensure_qzone_success(record)
    return _normalize_qzone_record(record)


def normalize_qzone_user_feeds(
    payload: Mapping[str, Any],
    *,
    host_uin: int,
) -> list[dict[str, Any]]:
    """将 ``msglist_v6`` 原始结果归一化为可跨插件使用的说说列表。"""
    if host_uin <= 0:
        raise QzoneCompatibilityError("QZone 说说列表请求缺少有效目标 QQ。")
    _ensure_qzone_success(payload)
    data = payload.get("data")
    container = data if isinstance(data, Mapping) else payload
    feeds: list[dict[str, Any]] = []
    for record in _as_dict_list(container.get("msglist")):
        try:
            feeds.append(_normalize_qzone_record(record, fallback_uin=host_uin))
        except QzoneCompatibilityError:
            continue
    return feeds


def _json_object_candidates(text: str) -> list[str]:
    """提取脚本或 JSONP 响应中的平衡对象候选。"""
    candidates: list[str] = []
    starts: list[int] = []
    in_string = False
    escaped = False
    depth = 0
    start = -1

    for index, character in enumerate(text):
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
            continue
        if character == "{":
            if depth == 0:
                start = index
            starts.append(index)
            depth += 1
            continue
        if character != "}" or depth == 0:
            continue
        depth -= 1
        starts.pop()
        if depth == 0 and start >= 0:
            candidates.append(text[start : index + 1])
            start = -1
    return candidates


def _frame_callback_candidates(text: str) -> list[str]:
    """提取 ``frameElement.callback({...})`` 中的对象文本。"""
    candidates: list[str] = []
    marker = re.compile(r"frameElement\.callback\s*\(")
    for match in marker.finditer(text):
        start = text.find("{", match.end())
        if start < 0:
            continue
        nested = _json_object_candidates(text[start:])
        if nested:
            candidates.append(nested[0])
    return candidates


def _parse_json_candidates(candidates: list[str]) -> list[dict[str, Any]]:
    """解析 JSON/JavaScript 对象候选，兼容 QZone 的 ``undefined``。"""
    parsed_payloads: list[dict[str, Any]] = []
    for candidate in candidates:
        normalized_candidate = re.sub(r"\bundefined\b", "null", candidate)
        try:
            payload = json.loads(normalized_candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict):
            parsed_payloads.append(payload)
    return parsed_payloads


def parse_qzone_json(text: str) -> dict[str, Any]:
    """解析 QZone 返回的 JSON 或 JSONP 对象，拒绝非对象响应。

    部分 QZone CGI 会在 JSONP 外层附加 JavaScript。不能简单取第一个
    ``{`` 到最后一个 ``}``，否则脚本中的其他对象会与真实响应拼接成非法 JSON。
    """
    normalized_text = text.lstrip("\ufeff").strip()
    if not normalized_text:
        raise QzoneCompatibilityError("QZone 响应为空。")

    parsed_payloads = _parse_json_candidates(
        _frame_callback_candidates(normalized_text)
        + _json_object_candidates(normalized_text)
    )

    response_keys = frozenset(
        {
            "code",
            "subcode",
            "retcode",
            "status",
            "commentid",
            "comment_id",
            "msglist",
            "message",
            "msg",
            "wording",
        }
    )
    for payload in parsed_payloads:
        if response_keys.intersection(payload):
            return payload
    if parsed_payloads:
        return parsed_payloads[0]

    if "{" not in normalized_text or "}" not in normalized_text:
        if re.search(
            r"(?:^|[\s;&])(?:code|subcode|retcode|ret)\s*[=:]\s*0"
            r"(?:$|[\s;&])",
            normalized_text,
            flags=re.IGNORECASE,
        ):
            return {"code": 0, "raw_response": normalized_text[:160]}
        preview = " ".join(normalized_text.split())[:160]
        detail = f"响应摘要={preview!r}" if preview else "响应摘要为空"
        raise QzoneCompatibilityError(f"QZone 响应不包含 JSON 对象（{detail}）。")
    preview = " ".join(normalized_text.split())[:160]
    detail = f"响应摘要={preview!r}" if preview else "响应摘要为空"
    raise QzoneCompatibilityError(f"QZone 响应 JSON 解析失败（{detail}）。")


def build_qzone_msg_detail_request(
    *,
    host_uin: int,
    tid: str,
    gtk: str,
) -> QzoneHttpRequest:
    """构造原版 FoxZone 已验证的单条说说详情请求。"""
    if host_uin <= 0 or not str(tid).strip():
        raise QzoneCompatibilityError("QZone 详情请求缺少有效说说主人或 tid。")
    query = urlencode(
        {
            "uin": str(host_uin),
            "tid": str(tid).strip(),
            "format": "jsonp",
            "g_tk": str(gtk),
        }
    )
    return QzoneHttpRequest(
        url=f"{QZONE_DETAIL_URL}?{query}",
        method="GET",
        body="",
        headers={
            "Accept": "*/*",
            "Referer": (
                "https://h5.qzone.qq.com/mqzone/index?_proxy=1"
                f"&hostuin={host_uin}"
            ),
        },
    )


def build_qzone_user_feeds_request(
    *,
    self_uin: int,
    host_uin: int,
    pos: int,
    num: int,
    gtk: str,
) -> QzoneHttpRequest:
    """构造无浏览器的 ``msglist_v6`` 任意 QQ 说说列表请求。"""
    if min(self_uin, host_uin) <= 0:
        raise QzoneCompatibilityError("QZone 说说列表请求缺少有效 QQ 号。")
    if pos < 0 or num < 1:
        raise QzoneCompatibilityError("QZone 说说列表分页参数无效。")
    query = urlencode(
        {
            "g_tk": str(gtk),
            "uin": str(host_uin),
            "ftype": "0",
            "sort": "0",
            "pos": str(pos),
            "num": str(num),
            "replynum": "999",
            "code_version": "1",
            "format": "json",
            "need_comment": "1",
        }
    )
    return QzoneHttpRequest(
        url=f"{QZONE_USER_FEEDS_URL}?{query}",
        method="GET",
        body="",
        headers={
            "Accept": "*/*",
            "Origin": "https://user.qzone.qq.com",
            "Referer": f"https://user.qzone.qq.com/{self_uin}",
        },
    )


def build_qzone_comment_reply_request(
    *,
    self_uin: int,
    host_uin: int,
    tid: str,
    root_comment_id: str,
    target_uin: int,
    target_name: str,
    content: str,
    gtk: str = "0",
) -> QzoneHttpRequest:
    """构造 QZone 楼中楼回复的精确表单请求。"""
    if min(self_uin, host_uin, target_uin) <= 0:
        raise QzoneCompatibilityError("QZone 楼中楼回复缺少有效 QQ 号。")
    if not str(tid).strip() or not str(root_comment_id).strip():
        raise QzoneCompatibilityError("QZone 楼中楼回复缺少 tid 或顶层评论 ID。")
    normalized_content = str(content).strip()
    if not normalized_content:
        raise QzoneCompatibilityError("QZone 楼中楼回复正文不能为空。")
    mention = f"@{{uin:{target_uin},nick:{str(target_name).strip()},auto:1}}"
    body = urlencode(
        {
            "topicId": f"{host_uin}_{str(tid).strip()}__1",
            "feedsType": "100",
            "inCharset": "utf-8",
            "outCharset": "utf-8",
            "plat": "qzone",
            "source": "ic",
            "hostUin": str(host_uin),
            "isSignIn": "",
            "platformid": "52",
            "uin": str(self_uin),
            "format": "fs",
            "ref": "feeds",
            "content": f"{mention} {normalized_content}",
            "commentId": str(root_comment_id).strip(),
            "commentUin": str(self_uin),
            "richval": "",
            "richtype": "",
            "private": "0",
            "paramstr": "1",
            "qzreferrer": f"https://user.qzone.qq.com/{self_uin}",
        }
    )
    return QzoneHttpRequest(
        url=f"{QZONE_REPLY_URL}?{urlencode({'g_tk': str(gtk)})}",
        method="POST",
        body=body,
        headers={
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-CH-UA": (
                '"Chromium";v="138", "Not(A:Brand";v="99", '
                '"Google Chrome";v="138"'
            ),
            "Sec-CH-UA-Mobile": "?0",
            "Sec-CH-UA-Platform": '"Windows"',
            "Origin": "https://user.qzone.qq.com",
            "Referer": f"https://user.qzone.qq.com/{self_uin}",
        },
    )


def _send_qzone_request(
    request: QzoneHttpRequest,
    cookie_header: str,
    timeout_seconds: float,
) -> str:
    """在工作线程中发送 HTTP 请求，避免阻塞框架事件循环。"""
    headers = {
        "User-Agent": QZONE_USER_AGENT,
        "Accept-Encoding": "identity",
        "Cookie": cookie_header,
        **request.headers,
    }
    request_data = request.body.encode("utf-8") if request.method == "POST" else None
    raw_request = Request(
        request.url,
        data=request_data,
        headers=headers,
        method=request.method,
    )
    try:
        with urlopen(raw_request, timeout=timeout_seconds) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except HTTPError as error:
        raise QzoneCompatibilityError(
            f"QZone HTTP 请求失败（status={error.code}）。"
        ) from error
    except URLError as error:
        raise QzoneCompatibilityError("QZone HTTP 请求无法连接。") from error


class QzoneCompatibilityClient:
    """使用协议端 Cookie 发送 QZone 详情和楼中楼兼容请求。"""

    def __init__(
        self,
        cookie_string: str,
        *,
        timeout_seconds: float = 20.0,
        requester: QzoneRequester | None = None,
    ) -> None:
        """初始化 Cookie 上下文与可注入的异步请求器。"""
        self._cookie_header = str(cookie_string).strip()
        self._cookies = parse_qzone_cookie_string(self._cookie_header)
        self._gtk = calculate_qzone_gtk(self._cookies.get("p_skey", ""))
        self._timeout_seconds = max(1.0, float(timeout_seconds))
        self._requester = requester

    async def get_msg_detail(self, host_uin: int, tid: str) -> dict[str, Any]:
        """读取一条说说详情并返回带完整评论树的标准化数据。"""
        request = build_qzone_msg_detail_request(
            host_uin=host_uin,
            tid=tid,
            gtk=self._gtk,
        )
        detail = normalize_qzone_msg_detail(
            parse_qzone_json(await self._request(request))
        )
        if detail["uin"] <= 0:
            detail["uin"] = host_uin
        return detail

    async def get_user_feeds(
        self,
        *,
        self_uin: int,
        host_uin: int,
        pos: int = 0,
        num: int = 5,
        paginate_comments: bool = True,
    ) -> list[dict[str, Any]]:
        """读取指定 QQ 可见的说说列表，并按需补全每条评论树。

        ``msglist_v6`` 返回的 ``commentlist`` 可能被服务端裁剪。默认对每条
        说说再请求 ``msgdetail_v6``，以详情中的完整评论树覆盖摘要；单条详情
        不可用时保留原列表结果，避免一条动态的读取失败影响整个列表。
        """
        request = build_qzone_user_feeds_request(
            self_uin=self_uin,
            host_uin=host_uin,
            pos=pos,
            num=num,
            gtk=self._gtk,
        )
        feeds = normalize_qzone_user_feeds(
            parse_qzone_json(await self._request(request)),
            host_uin=host_uin,
        )
        if not paginate_comments:
            return feeds

        for feed in feeds:
            tid = _as_text(feed.get("tid"))
            if not tid:
                continue
            try:
                detail = await self.get_msg_detail(host_uin, tid)
            except QzoneCompatibilityError:
                continue
            feed["commentlist"] = detail["commentlist"]
            feed["comment_num"] = detail["comment_num"]
        return feeds

    async def reply_comment(
        self,
        *,
        self_uin: int,
        host_uin: int,
        tid: str,
        root_comment_id: str,
        target_uin: int,
        target_name: str,
        content: str,
    ) -> dict[str, Any]:
        """向指定顶层评论中的用户发送一条楼中楼回复。"""
        request = build_qzone_comment_reply_request(
            self_uin=self_uin,
            host_uin=host_uin,
            tid=tid,
            root_comment_id=root_comment_id,
            target_uin=target_uin,
            target_name=target_name,
            content=content,
            gtk=self._gtk,
        )
        payload = parse_qzone_json(await self._request(request))
        _ensure_qzone_success(payload)
        return payload

    async def _request(self, request: QzoneHttpRequest) -> str:
        """通过测试替身或标准库 HTTP 客户端执行请求。"""
        if self._requester is not None:
            return await self._requester(request)
        return await asyncio.to_thread(
            _send_qzone_request,
            request,
            self._cookie_header,
            self._timeout_seconds,
        )


__all__ = [
    "QZONE_DETAIL_URL",
    "QZONE_REPLY_URL",
    "QZONE_USER_FEEDS_URL",
    "QzoneCompatibilityClient",
    "QzoneCompatibilityError",
    "QzoneHttpRequest",
    "build_qzone_comment_reply_request",
    "build_qzone_msg_detail_request",
    "build_qzone_user_feeds_request",
    "calculate_qzone_gtk",
    "normalize_qzone_msg_detail",
    "normalize_qzone_user_feeds",
    "parse_qzone_cookie_string",
    "parse_qzone_json",
]