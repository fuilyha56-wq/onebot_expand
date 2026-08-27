"""QQ空间服务。

封装 NapCat QQ 空间 API，提供说说列表查询、好友动态、
发表说说、删除说说、点赞、取消点赞、评论等功能。

公开 OneBot action (9):
    - get_qzone_msg_list: 获取QQ空间说说列表
    - get_qzone_feeds: 获取QQ空间好友动态
    - send_qzone_msg: 发表说说
    - delete_qzone_msg: 删除说说
    - like_qzone: 给说说点赞
    - unlike_qzone: 取消点赞
    - comment_qzone: 评论说说
    - set_qzone_ban: 设置空间黑名单
    - set_qzone_msg_right: 修改说说查看权限

内部 Service 能力（不注册为 OneBot action 或 Tool）:
    - get_qzone_msg_detail: 补全单条说说的完整评论树
    - get_qzone_user_feeds: 读取指定 QQ 可见的说说列表
    - reply_qzone_comment: 使用详情确认的顶层评论 ID 发送楼中楼回复
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

from src.app.plugin_system.base import BaseService

from ..api_client import _call_onebot_api
from ..qzone_compat import QzoneCompatibilityClient, QzoneCompatibilityError

__all__ = ["QzoneService"]

#: 兼容层 Cookie 缓存有效期（秒）。QZone Cookie 通常数小时有效，
#: 短 TTL 缓存可避免一轮轮询内重复请求 ``get_cookies`` 触发风控。
_COOKIE_CACHE_TTL_SECONDS = 300.0

#: 类级共享 Cookie 缓存：``(cookie 字符串, 到期时间戳)``。
#:
#: Service 每次构造新实例（非单例），实例级缓存无法跨调用复用；
#: Cookie 对同一 Bot 账号全局一致，因此放在类级并配合并发去重锁。
_SHARED_COOKIE_CACHE: tuple[str, float] | None = None
_COOKIE_FETCH_LOCK = asyncio.Lock()


class QzoneService(BaseService):
    """QQ空间服务。

    封装全部 QQ 空间 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    name: str = "qzone_service"
    description: str = "QQ空间服务"
    version: str = "1.0.1"

    @staticmethod
    def _compatibility_failure(error: Exception) -> dict[str, Any]:
        """把本地 QZone 兼容层异常收敛为标准 OneBot 失败响应。"""
        message = str(error) or "QZone 兼容请求失败。"
        return {
            "status": "failed",
            "retcode": -1,
            "data": None,
            "msg": message,
            "wording": message,
        }

    @classmethod
    def _invalidate_cookie_cache(cls) -> None:
        """清除类级共享 Cookie 缓存，下次请求重新拉取。"""
        global _SHARED_COOKIE_CACHE
        _SHARED_COOKIE_CACHE = None

    async def _get_compatibility_client(self) -> QzoneCompatibilityClient:
        """经协议端获取当前 QZone Cookie 并创建短生命周期兼容客户端。

        Cookie 使用类级缓存（TTL 内直接复用），并发调用在锁内去重，
        避免一轮轮询对协议端发起数十次 ``get_cookies`` 请求。
        """
        global _SHARED_COOKIE_CACHE
        async with _COOKIE_FETCH_LOCK:
            now = time.monotonic()
            if _SHARED_COOKIE_CACHE is not None:
                cookie_string, expires_at = _SHARED_COOKIE_CACHE
                if now < expires_at:
                    return QzoneCompatibilityClient(cookie_string)
            response = await _call_onebot_api(
                "get_cookies",
                {"domain": "qzone.qq.com"},
            )
            if str(response.get("status", "")).lower() != "ok":
                message = str(
                    response.get("msg")
                    or response.get("wording")
                    or "协议端未返回 QZone Cookie。"
                )
                raise QzoneCompatibilityError(message)
            data = response.get("data")
            cookies = data.get("cookies") if isinstance(data, dict) else None
            if not isinstance(cookies, str) or not cookies.strip():
                raise QzoneCompatibilityError("协议端返回的 QZone Cookie 为空。")
            _SHARED_COOKIE_CACHE = (
                cookies,
                now + _COOKIE_CACHE_TTL_SECONDS,
            )
            return QzoneCompatibilityClient(cookies)

    async def _load_self_uin(self) -> int:
        """通过标准 OneBot 登录信息读取当前 Bot QQ。"""
        response = await _call_onebot_api("get_login_info", {})
        if str(response.get("status", "")).lower() != "ok":
            message = str(
                response.get("msg")
                or response.get("wording")
                or "协议端未返回当前 Bot QQ。"
            )
            raise QzoneCompatibilityError(message)
        data = response.get("data")
        payload = data if isinstance(data, dict) else response
        try:
            self_uin = int(
                payload.get("user_id")
                or payload.get("self_id")
                or payload.get("uin")
            )
        except (TypeError, ValueError) as error:
            raise QzoneCompatibilityError(
                "协议端登录信息缺少有效 Bot QQ。"
            ) from error
        if self_uin <= 0:
            raise QzoneCompatibilityError("协议端登录信息包含无效 Bot QQ。")
        return self_uin

    async def get_qzone_msg_list(
        self,
        pos: int = 0,
        num: int = 10,
    ) -> dict[str, Any]:
        """获取QQ空间说说列表。

        对应 NapCat 扩展 API: ``get_qzone_msg_list``。

        Args:
            pos: 起始位置，默认为 0。
            num: 获取数量，默认为 10。

        Returns:
            适配器返回的响应字典，包含说说列表。
        """
        params: dict[str, Any] = {
            "pos": pos,
            "num": num,
        }
        return await _call_onebot_api("get_qzone_msg_list", params)

    async def get_qzone_feeds(
        self,
        page_num: int = 0,
        count: int = 10,
    ) -> dict[str, Any]:
        """获取QQ空间好友动态。

        对应 NapCat 扩展 API: ``get_qzone_feeds``。

        Args:
            page_num: 页码，默认为 0。
            count: 每页数量，默认为 10。

        Returns:
            适配器返回的响应字典，包含好友动态列表。
        """
        params: dict[str, Any] = {
            "page_num": page_num,
            "count": count,
        }
        return await _call_onebot_api("get_qzone_feeds", params)

    async def get_qzone_msg_detail(
        self,
        tid: str,
        host_uin: int,
    ) -> dict[str, Any]:
        """获取单条说说详情及其完整评论树。

        SnowLuma 的列表 action 为稳定输出会裁剪评论树；该方法仅复用其
        ``get_cookies`` 会话，再按 QZone 的 ``msgdetail_v6`` 契约补全详情。
        """
        try:
            client = await self._get_compatibility_client()
            detail = await client.get_msg_detail(int(host_uin), str(tid).strip())
        except (QzoneCompatibilityError, TypeError, ValueError) as error:
            return self._compatibility_failure(error)
        return {"status": "ok", "retcode": 0, "data": detail}

    async def get_qzone_user_feeds(
        self,
        *,
        host_uin: int,
        pos: int = 0,
        num: int = 5,
        self_uin: int | None = None,
    ) -> dict[str, Any]:
        """读取指定 QQ 可见的说说列表，无需浏览器或本地 HTTP 服务。"""
        try:
            client = await self._get_compatibility_client()
            effective_self_uin = (
                int(self_uin) if self_uin is not None else await self._load_self_uin()
            )
            feeds = await client.get_user_feeds(
                self_uin=effective_self_uin,
                host_uin=int(host_uin),
                pos=int(pos),
                num=int(num),
            )
        except (QzoneCompatibilityError, TypeError, ValueError) as error:
            return self._compatibility_failure(error)
        return {"status": "ok", "retcode": 0, "data": {"msglist": feeds}}

    async def reply_qzone_comment(
        self,
        *,
        tid: str,
        host_uin: int,
        root_comment_id: str,
        target_uin: int,
        target_name: str,
        content: str,
        self_uin: int | None = None,
    ) -> dict[str, Any]:
        """在指定顶层评论下发送一条 QZone 楼中楼回复。

        ``root_comment_id`` 必须来自 :meth:`get_qzone_msg_detail` 返回的
        顶层评论 ID，不能使用摘要列表中可能是局部序号的字段。
        """
        try:
            client = await self._get_compatibility_client()
            effective_self_uin = (
                int(self_uin) if self_uin is not None else await self._load_self_uin()
            )
            data = await client.reply_comment(
                self_uin=effective_self_uin,
                host_uin=int(host_uin),
                tid=str(tid).strip(),
                root_comment_id=str(root_comment_id).strip(),
                target_uin=int(target_uin),
                target_name=str(target_name).strip(),
                content=str(content).strip(),
            )
        except (QzoneCompatibilityError, TypeError, ValueError) as error:
            return self._compatibility_failure(error)
        return {"status": "ok", "retcode": 0, "data": data}

    async def send_qzone_msg(
        self,
        content: str,
        images: list[str] | None = None,
        ugc_right: int = 1,
        target_uins: list[int] | None = None,
    ) -> dict[str, Any]:
        """发表说说。

        对应 NapCat 扩展 API: ``send_qzone_msg``。
        支持纯文字或带图，可设置查看权限。

        Args:
            content: 说说内容。
            images: 图片数组（可选），支持 file:// http(s):// base64://。
            ugc_right: 查看权限（1=所有人可见，4=好友可见，16=部分好友可见，
                64=仅自己可见，128=部分好友不可见），默认为 1。
            target_uins: 权限作用 QQ 号数组；ugc_right=16 时为可见名单，128 时为不可见名单。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"content": content, "ugc_right": ugc_right}
        if images is not None:
            params["images"] = images
        if target_uins is not None:
            params["target_uins"] = target_uins
        return await _call_onebot_api("send_qzone_msg", params)

    async def delete_qzone_msg(self, tid: str) -> dict[str, Any]:
        """删除说说。

        对应 NapCat 扩展 API: ``delete_qzone_msg``。

        Args:
            tid: 说说 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"tid": tid}
        return await _call_onebot_api("delete_qzone_msg", params)

    async def like_qzone(
        self,
        tid: str,
        target_uin: int | None = None,
    ) -> dict[str, Any]:
        """给说说点赞。

        对应 NapCat 扩展 API: ``like_qzone``。

        Args:
            tid: 说说 ID。
            target_uin: 说说发布者 QQ 号，默认为 None。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"tid": tid}
        if target_uin is not None:
            params["target_uin"] = target_uin
        return await _call_onebot_api("like_qzone", params)

    async def unlike_qzone(
        self,
        tid: str,
        target_uin: int | None = None,
    ) -> dict[str, Any]:
        """取消点赞。

        对应 NapCat 扩展 API: ``unlike_qzone``。

        Args:
            tid: 说说 ID。
            target_uin: 说说发布者 QQ 号，默认为 None。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"tid": tid}
        if target_uin is not None:
            params["target_uin"] = target_uin
        return await _call_onebot_api("unlike_qzone", params)

    async def comment_qzone(
        self,
        tid: str,
        content: str,
        target_uin: int | None = None,
        images: list[str] | None = None,
    ) -> dict[str, Any]:
        """评论说说。

        对应 NapCat 扩展 API: ``comment_qzone``。
        支持纯文字或带图。

        Args:
            tid: 说说 ID。
            content: 评论内容。
            target_uin: 说说发布者 QQ 号，默认为 None。
            images: 图片数组（可选），支持 file:// http(s):// base64://。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "tid": tid,
            "content": content,
        }
        if target_uin is not None:
            params["target_uin"] = target_uin
        if images is not None:
            params["images"] = images
        return await _call_onebot_api("comment_qzone", params)

    async def set_qzone_ban(
        self,
        user_id: int,
        enable: bool = True,
    ) -> dict[str, Any]:
        """拉黑或解除拉黑某人（机器人自身 QQ 空间黑名单；SnowLuma 扩展）。

        对应扩展 API: ``set_qzone_ban``。

        Args:
            user_id: 目标 QQ 号。
            enable: True 拉黑，False 解除拉黑。

        Returns:
            适配器返回的响应字典。
        """
        return await _call_onebot_api(
            "set_qzone_ban",
            {"user_id": user_id, "enable": enable},
        )

    async def set_qzone_msg_right(
        self,
        tid: str,
        ugc_right: int,
        target_uins: list[int] | None = None,
    ) -> dict[str, Any]:
        """修改一条已发说说的查看权限（SnowLuma 扩展）。

        对应扩展 API: ``set_qzone_msg_right``。

        Args:
            tid: 说说 tid。
            ugc_right: 查看权限（1=所有人可见，4=好友可见，16=部分好友可见，
                64=仅自己可见，128=部分好友不可见）。
            target_uins: 权限作用 QQ 号数组；ugc_right=16 时为可见名单，128 时为不可见名单。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"tid": tid, "ugc_right": ugc_right}
        if target_uins is not None:
            params["target_uins"] = target_uins
        return await _call_onebot_api("set_qzone_msg_right", params)
