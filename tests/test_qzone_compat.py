"""QZone 兼容请求与响应归一化契约测试。"""

from __future__ import annotations

from urllib.parse import parse_qs, urlsplit

from ..qzone_compat import (
    QzoneCompatibilityClient,
    build_qzone_comment_reply_request,
    build_qzone_user_feeds_request,
    normalize_qzone_msg_detail,
    normalize_qzone_user_feeds,
    parse_qzone_json,
)
from ..services import qzone_service


def test_normalize_qzone_detail_preserves_global_comment_ids() -> None:
    """详情响应必须保留可用于楼中楼回复的全局评论 ID。"""
    detail = normalize_qzone_msg_detail(
        {
            "code": 0,
            "tid": "post-1",
            "uin": "10000",
            "content": "自己的说说",
            "created_time": 1_700_000_000,
            "commentnum": 2,
            "commentlist": [
                {
                    "tid": "root-comment-id",
                    "uin": "20001",
                    "name": "Alice",
                    "content": "一级评论",
                    "list_3": [
                        {
                            "tid": "child-comment-id",
                            "uin": "20002",
                            "name": "Bob",
                            "content": "楼中楼回复",
                        }
                    ],
                }
            ],
        }
    )

    assert detail["tid"] == "post-1"
    assert detail["uin"] == 10000
    assert detail["comment_num"] == 2
    assert detail["commentlist"] == [
        {
            "comment_id": "root-comment-id",
            "uin": 20001,
            "nickname": "Alice",
            "content": "一级评论",
            "list_3": [
                {
                    "comment_id": "child-comment-id",
                    "parent_comment_id": "root-comment-id",
                    "uin": 20002,
                    "nickname": "Bob",
                    "content": "楼中楼回复",
                    "list_3": [],
                }
            ],
        }
    ]


def test_reply_request_matches_qzone_thread_reply_contract() -> None:
    """楼中楼回复必须使用顶层评论 ID、操作者 QQ 和 QZone @ 语法。"""
    request = build_qzone_comment_reply_request(
        self_uin=10000,
        host_uin=10000,
        tid="post-1",
        root_comment_id="root-comment-id",
        target_uin=20001,
        target_name="Alice",
        content="收到啦",
    )
    payload = parse_qs(request.body, keep_blank_values=True)

    assert request.url.startswith(
        "https://user.qzone.qq.com/proxy/domain/taotao.qzone.qq.com/"
        "cgi-bin/emotion_cgi_re_feeds?g_tk="
    )
    assert request.headers == {
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
        "Referer": "https://user.qzone.qq.com/10000",
    }
    assert payload == {
        "topicId": ["10000_post-1__1"],
        "feedsType": ["100"],
        "inCharset": ["utf-8"],
        "outCharset": ["utf-8"],
        "plat": ["qzone"],
        "source": ["ic"],
        "hostUin": ["10000"],
        "isSignIn": [""],
        "platformid": ["52"],
        "uin": ["10000"],
        "format": ["fs"],
        "ref": ["feeds"],
        "content": ["@{uin:20001,nick:Alice,auto:1} 收到啦"],
        "commentId": ["root-comment-id"],
        "commentUin": ["10000"],
        "richval": [""],
        "richtype": [""],
        "private": ["0"],
        "paramstr": ["1"],
        "qzreferrer": ["https://user.qzone.qq.com/10000"],
    }


def test_parse_qzone_json_skips_unrelated_script_objects() -> None:
    """QZone 外层脚本对象不应破坏内部 JSONP 响应解析。"""
    response = (
        'try { window.__qzone_state = {loading:true}; } catch (error) {}'
        'callback({"code":0,"commentid":"new-comment"});'
    )

    assert parse_qzone_json(response) == {
        "code": 0,
        "commentid": "new-comment",
    }


def test_parse_qzone_json_accepts_explicit_plain_text_success() -> None:
    """部分 QZone 回复响应只返回明确的 code=0 状态文本。"""
    assert parse_qzone_json("code=0; message=success") == {
        "code": 0,
        "raw_response": "code=0; message=success",
    }


def test_parse_qzone_json_extracts_format_fs_frame_callback() -> None:
    """评论接口的 frame 桥接 HTML 应解析出真实 QZone code。"""
    response = (
        '<html><script>frameElement.callback('
        '{"code":0,"commentid":"new-comment","extra":undefined}'
        ')</script></html>'
    )

    assert parse_qzone_json(response) == {
        "code": 0,
        "commentid": "new-comment",
        "extra": None,
    }


def test_send_qzone_request_rejects_non_whitelisted_url() -> None:
    """SSRF 防护：非 QZone CGI 白名单 URL 必须被拒绝，白名单 URL 放行。"""
    import pytest

    from ..qzone_compat import (
        QZONE_DETAIL_URL,
        QzoneCompatibilityError,
        QzoneHttpRequest,
        _send_qzone_request,
    )

    # 白名单内的 URL（带查询串）放行（用一个必然失败的端口超时验证不被 URL 校验拦截）
    good = QzoneHttpRequest(
        url=f"{QZONE_DETAIL_URL}?g_tk=1&uin=10000",
        method="GET",
        body="",
        headers={},
    )
    # 黑名单地址一律在发送前被拒绝
    for malicious in [
        "https://evil.example.com/cgi-bin/emotion_cgi_msgdetail_v6",
        "http://127.0.0.1:8080/admin",
        "https://user.qzone.qq.com.evil.example.com/proxy/domain/taotao.qq.com/",
    ]:
        bad = QzoneHttpRequest(url=malicious, method="GET", body="", headers={})
        with pytest.raises(QzoneCompatibilityError):
            _send_qzone_request(bad, "uin=o1; skey=abc", 5.0)

    # 白名单地址不应触发 URL 校验异常（网络层失败与 URL 校验是不同异常）
    try:
        _send_qzone_request(good, "uin=o1; skey=abc", 0.1)
    except QzoneCompatibilityError as error:
        assert "白名单" not in str(error)


def test_user_feed_request_and_normalization_need_no_browser() -> None:
    """任意 QQ 说说读取应是带 Cookie 的出站 HTTPS 请求且保留评论树。"""
    request = build_qzone_user_feeds_request(
        self_uin=10000,
        host_uin=20000,
        pos=2,
        num=3,
        gtk="gtk-value",
    )

    assert request.method == "GET"
    assert request.body == ""
    assert request.url.startswith(
        "https://user.qzone.qq.com/proxy/domain/taotao.qq.com/"
        "cgi-bin/emotion_cgi_msglist_v6?"
    )
    assert parse_qs(urlsplit(request.url).query) == {
        "g_tk": ["gtk-value"],
        "uin": ["20000"],
        "ftype": ["0"],
        "sort": ["0"],
        "pos": ["2"],
        "num": ["3"],
        "replynum": ["999"],
        "code_version": ["1"],
        "format": ["json"],
        "need_comment": ["1"],
    }
    assert request.headers == {
        "Accept": "*/*",
        "Origin": "https://user.qzone.qq.com",
        "Referer": "https://user.qzone.qq.com/10000",
    }
    assert normalize_qzone_user_feeds(
        {
            "code": 0,
            "msglist": [
                {
                    "tid": "friend-post",
                    "content": "好友说说",
                    "created_time": 1_700_000_000,
                    "commentnum": 1,
                    "pic": [{"url1": "https://example.test/image.jpg"}],
                    "commentlist": [
                        {
                            "tid": "global-root-comment-id",
                            "uin": "20001",
                            "name": "访客",
                            "content": "一级评论",
                            "list_3": [
                                {
                                    "tid": "child-comment-id",
                                    "uin": "20002",
                                    "name": "回复者",
                                    "content": "楼中楼",
                                }
                            ],
                        }
                    ],
                }
            ],
        },
        host_uin=20000,
    ) == [
        {
            "tid": "friend-post",
            "uin": 20000,
            "content": "好友说说",
            "created_time": 1_700_000_000,
            "comment_num": 1,
            "images": ["https://example.test/image.jpg"],
            "commentlist": [
                {
                    "comment_id": "global-root-comment-id",
                    "uin": 20001,
                    "nickname": "访客",
                    "content": "一级评论",
                    "list_3": [
                        {
                            "comment_id": "child-comment-id",
                            "parent_comment_id": "global-root-comment-id",
                            "uin": 20002,
                            "nickname": "回复者",
                            "content": "楼中楼",
                            "list_3": [],
                        }
                    ],
                }
            ],
        }
    ]


async def test_user_feeds_replace_summary_comments_with_detail_and_keep_fallback() -> None:
    """列表读取应逐条补详情，且单条详情失败不得丢弃摘要结果。"""
    requests: list[object] = []

    async def requester(request: object) -> str:
        requests.append(request)
        url = str(getattr(request, "url"))
        query = parse_qs(urlsplit(url).query)
        if "emotion_cgi_msglist_v6" in url:
            return (
                '{"code":0,"msglist":['
                '{"tid":"post-success","commentnum":1,'
                '"commentlist":[{"tid":"summary-root","content":"摘要评论"}]},'
                '{"tid":"post-fallback","commentnum":1,'
                '"commentlist":[{"tid":"fallback-root","content":"保留摘要"}]}'
                ']}'
            )
        if query["tid"] == ["post-success"]:
            return (
                '{"code":0,"tid":"post-success","commentnum":2,'
                '"commentlist":[{"tid":"detail-root","content":"完整评论"}]}'
            )
        return '{"code":-1,"message":"详情不可用"}'

    client = QzoneCompatibilityClient("p_skey=test-p-skey", requester=requester)

    feeds = await client.get_user_feeds(self_uin=10000, host_uin=20000, num=2)

    assert [str(getattr(request, "url")) for request in requests] == [
        str(getattr(requests[0], "url")),
        str(getattr(requests[1], "url")),
        str(getattr(requests[2], "url")),
    ]
    assert "emotion_cgi_msglist_v6" in str(getattr(requests[0], "url"))
    assert [parse_qs(urlsplit(str(getattr(request, "url"))).query)["tid"] for request in requests[1:]] == [
        ["post-success"],
        ["post-fallback"],
    ]
    assert feeds[0]["comment_num"] == 2
    assert feeds[0]["commentlist"][0]["comment_id"] == "detail-root"
    assert feeds[1]["comment_num"] == 1
    assert feeds[1]["commentlist"][0]["comment_id"] == "fallback-root"


async def test_qzone_service_uses_snowluma_cookie_for_detail_and_reply(
    monkeypatch: object,
) -> None:
    """Service 应经现有 get_cookies action 调用详情与楼中楼兼容客户端。

    Cookie 在类级缓存 TTL 内复用：三次兼容调用只触发一次
    ``get_cookies``，避免一轮轮询对协议端发起数十次 Cookie 请求。
    """
    calls: list[tuple[str, dict[str, object]]] = []
    created_cookies: list[str] = []

    class FakeCompatibilityClient:
        """记录由 Service 传入的 Cookie 与详情/回复参数。"""

        def __init__(self, cookie_string: str) -> None:
            created_cookies.append(cookie_string)

        async def get_msg_detail(
            self,
            host_uin: int,
            tid: str,
        ) -> dict[str, object]:
            return {"tid": tid, "uin": host_uin, "commentlist": []}

        async def get_user_feeds(
            self,
            **kwargs: object,
        ) -> list[dict[str, object]]:
            return [{"tid": "friend-post", **kwargs}]

        async def reply_comment(
            self,
            **kwargs: object,
        ) -> dict[str, object]:
            return {"code": 0, "commentid": "new-comment", **kwargs}

    async def fake_call(
        action: str,
        params: dict[str, object],
    ) -> dict[str, object]:
        calls.append((action, params))
        return {
            "status": "ok",
            "retcode": 0,
            "data": {"cookies": "uin=o10000; p_skey=test-p-skey"},
        }

    monkeypatch.setattr(qzone_service, "_call_onebot_api", fake_call)
    monkeypatch.setattr(
        qzone_service,
        "QzoneCompatibilityClient",
        FakeCompatibilityClient,
    )
    qzone_service.QzoneService._invalidate_cookie_cache()
    service = qzone_service.QzoneService(plugin=None)

    detail = await service.get_qzone_msg_detail("post-1", 10000)
    feeds = await service.get_qzone_user_feeds(
        host_uin=20000,
        pos=1,
        num=2,
        self_uin=10000,
    )
    reply = await service.reply_qzone_comment(
        tid="post-1",
        host_uin=10000,
        root_comment_id="root-comment-id",
        target_uin=20001,
        target_name="Alice",
        content="收到啦",
        self_uin=10000,
    )

    assert detail == {
        "status": "ok",
        "retcode": 0,
        "data": {"tid": "post-1", "uin": 10000, "commentlist": []},
    }
    assert feeds == {
        "status": "ok",
        "retcode": 0,
        "data": {
            "msglist": [
                {
                    "tid": "friend-post",
                    "self_uin": 10000,
                    "host_uin": 20000,
                    "pos": 1,
                    "num": 2,
                }
            ]
        },
    }
    assert reply["status"] == "ok"
    assert reply["data"]["commentid"] == "new-comment"
    assert reply["data"]["root_comment_id"] == "root-comment-id"
    assert created_cookies == [
        "uin=o10000; p_skey=test-p-skey",
        "uin=o10000; p_skey=test-p-skey",
        "uin=o10000; p_skey=test-p-skey",
    ]
    # TTL 缓存生效：三次兼容调用仅一次 get_cookies。
    assert calls == [("get_cookies", {"domain": "qzone.qq.com"})]
    qzone_service.QzoneService._invalidate_cookie_cache()


def test_qzone_service_cookie_cache_expires_and_dedupes_concurrent_calls() -> None:
    """Cookie 缓存过期后应重新拉取，并发调用应在锁内去重。"""
    import asyncio

    from ..services import qzone_service as module

    async def scenario() -> tuple[int, int]:
        fetch_count = 0
        client_count = 0

        class FakeClient:
            def __init__(self, cookie_string: str) -> None:
                nonlocal client_count
                client_count += 1

            async def get_msg_detail(
                self,
                host_uin: int,
                tid: str,
            ) -> dict[str, object]:
                return {"tid": tid, "uin": host_uin, "commentlist": []}

        async def fake_call(action: str, params: dict[str, object]) -> dict[str, object]:
            nonlocal fetch_count
            fetch_count += 1
            return {
                "status": "ok",
                "retcode": 0,
                "data": {"cookies": f"uin=o10000; p_skey=k{fetch_count}"},
            }

        module._call_onebot_api = fake_call  # type: ignore[assignment]
        module.QzoneCompatibilityClient = FakeClient  # type: ignore[assignment,misc]
        module.QzoneService._invalidate_cookie_cache()

        service = module.QzoneService(plugin=None)

        async def call_detail() -> None:
            await service.get_qzone_msg_detail("post-1", 10000)

        # 并发 5 个请求：锁内去重后只允许一次真实拉取。
        await asyncio.gather(*(call_detail() for _ in range(5)))
        concurrent_fetches = fetch_count

        # 模拟缓存过期：清空缓存时间戳。
        module._SHARED_COOKIE_CACHE = None
        await call_detail()
        return concurrent_fetches, fetch_count - concurrent_fetches

    concurrent_fetches, refetches = asyncio.run(scenario())
    assert concurrent_fetches == 1
    assert refetches == 1
    module.QzoneService._invalidate_cookie_cache()