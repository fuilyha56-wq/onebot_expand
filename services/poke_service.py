"""戳一拍服务。

封装 NapCat 戳一拍 API，提供好友戳一戳和群戳一戳功能。

API 列表 (2):
    - friend_poke: 好友戳一戳
    - group_poke: 群戳一戳
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["PokeService"]


class PokeService(BaseService):
    """戳一拍服务。

    封装全部戳一拍 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    name: str = "poke_service"
    description: str = "戳一拍服务"
    version: str = "1.0.0"

    async def friend_poke(
        self,
        user_id: int,
        target_id: int | None = None,
    ) -> dict[str, Any]:
        """好友戳一戳。

        对应 NapCat 扩展 API: ``friend_poke``。

        Args:
            user_id: 目标用户 QQ 号。
            target_id: 被戳目标 QQ 号，默认为 None。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"user_id": user_id}
        if target_id is not None:
            params["target_id"] = target_id
        return await _call_onebot_api("friend_poke", params)

    async def group_poke(
        self,
        group_id: int,
        user_id: int,
    ) -> dict[str, Any]:
        """群戳一戳。

        对应 NapCat 扩展 API: ``group_poke``。

        Args:
            group_id: 群号。
            user_id: 目标成员 QQ 号。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
        }
        return await _call_onebot_api("group_poke", params)