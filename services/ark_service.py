"""Ark分享服务。

封装 NapCat Ark 分享 API，提供用户/群 Ark 卡片分享、
群扩展 Ark 分享等功能。

API 列表 (4):
    - share_peer: 分享用户/群Ark卡片
    - send_ark_share: 分享Ark卡片
    - share_group_ex: 分享群Ark卡片
    - send_group_ark_share: 发送群Ark分享
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..api_client import _call_onebot_api

__all__ = ["ArkService"]


class ArkService(BaseService):
    """Ark分享服务。

    封装全部 Ark 分享 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    name: str = "ark_service"
    description: str = "Ark分享服务"
    version: str = "1.0.0"

    async def share_peer(
        self,
        user_id: int | None = None,
        group_id: int | None = None,
    ) -> dict[str, Any]:
        """分享用户/群Ark卡片。

        对应 NapCat 扩展 API: ``share_peer``。

        Args:
            user_id: 目标用户 QQ 号，默认为 None。
            group_id: 目标群号，默认为 None。

        Returns:
            适配器返回的响应字典，包含 Ark 卡片数据。
        """
        params: dict[str, Any] = {}
        if user_id is not None:
            params["user_id"] = user_id
        if group_id is not None:
            params["group_id"] = group_id
        return await _call_onebot_api("share_peer", params)

    async def send_ark_share(
        self,
        user_id: int | None = None,
        group_id: int | None = None,
    ) -> dict[str, Any]:
        """分享Ark卡片。

        对应 NapCat 扩展 API: ``send_ark_share``。

        Args:
            user_id: 目标用户 QQ 号，默认为 None。
            group_id: 目标群号，默认为 None。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {}
        if user_id is not None:
            params["user_id"] = user_id
        if group_id is not None:
            params["group_id"] = group_id
        return await _call_onebot_api("send_ark_share", params)

    async def share_group_ex(self, group_id: int) -> dict[str, Any]:
        """分享群Ark卡片。

        对应 NapCat 扩展 API: ``share_group_ex``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典，包含群 Ark 卡片数据。
        """
        params: dict[str, Any] = {"group_id": group_id}
        return await _call_onebot_api("share_group_ex", params)

    async def send_group_ark_share(self, group_id: int) -> dict[str, Any]:
        """发送群Ark分享。

        对应 NapCat 扩展 API: ``send_group_ark_share``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"group_id": group_id}
        return await _call_onebot_api("send_group_ark_share", params)

    async def send_tuwen_ark(
        self,
        title: str,
        desc: str,
        jump_url: str,
        user_id: int | None = None,
        group_id: int | None = None,
        summary: str = "[分享]",
        preview_url: str = "https://tangram-1251316161.file.myqcloud.com/files/20210721/e50a8e37e08f29bf1ffc7466e1950690.png",
    ) -> dict[str, Any]:
        """发送图文Ark卡片（SnowLuma 扩展）。

        对应 SnowLuma 扩展 API: ``send_tuwen_ark``。
        发送固定图文 ark 模板到私聊或群聊，返回 null（无法用于撤回/设精华）。

        Args:
            title: 卡片标题。
            desc: 卡片描述。
            jump_url: 跳转链接。
            user_id: 目标用户 QQ 号，与 group_id 二选一。
            group_id: 目标群号，与 user_id 二选一。
            summary: 卡片摘要，默认 "[分享]"。
            preview_url: 预览图 URL，默认为 SnowLuma 内置占位图。

        Returns:
            适配器返回的响应字典（data 为 null）。

        Raises:
            ValueError: user_id 与 group_id 未二选一时抛出。
        """
        if (user_id is None) == (group_id is None):
            raise ValueError("user_id 与 group_id 必须二选一（恰好提供一个）")
        params: dict[str, Any] = {
            "title": title,
            "desc": desc,
            "summary": summary,
            "preview_url": preview_url,
            "jump_url": jump_url,
        }
        if group_id is not None:
            params["group_id"] = group_id
        else:
            params["user_id"] = user_id
        return await _call_onebot_api("send_tuwen_ark", params)