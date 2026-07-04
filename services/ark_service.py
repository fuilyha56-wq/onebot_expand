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

from ..tools import _call_onebot_api

__all__ = ["ArkService"]


class ArkService(BaseService):
    """Ark分享服务。

    封装全部 Ark 分享 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "ark_service"
    service_description: str = "Ark分享服务"
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