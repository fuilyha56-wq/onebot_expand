"""QQ空间服务。

封装 NapCat QQ 空间 API，提供说说列表查询、好友动态、
发表说说、删除说说、点赞、取消点赞、评论等功能。

API 列表 (7):
    - get_qzone_msg_list: 获取QQ空间说说列表
    - get_qzone_feeds: 获取QQ空间好友动态
    - send_qzone_msg: 发表说说
    - delete_qzone_msg: 删除说说
    - like_qzone: 给说说点赞
    - unlike_qzone: 取消点赞
    - comment_qzone: 评论说说
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["QzoneService"]


class QzoneService(BaseService):
    """QQ空间服务。

    封装全部 QQ 空间 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    name: str = "qzone_service"
    description: str = "QQ空间服务"
    version: str = "1.0.0"

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

    async def send_qzone_msg(self, content: str) -> dict[str, Any]:
        """发表说说。

        对应 NapCat 扩展 API: ``send_qzone_msg``。

        Args:
            content: 说说内容。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"content": content}
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
    ) -> dict[str, Any]:
        """评论说说。

        对应 NapCat 扩展 API: ``comment_qzone``。

        Args:
            tid: 说说 ID。
            content: 评论内容。
            target_uin: 说说发布者 QQ 号，默认为 None。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "tid": tid,
            "content": content,
        }
        if target_uin is not None:
            params["target_uin"] = target_uin
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
