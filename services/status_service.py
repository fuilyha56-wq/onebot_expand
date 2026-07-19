"""在线状态服务。

封装 NapCat 在线状态 API，提供在线状态设置、自定义状态、
输入状态、用户状态查询等功能。

API 列表 (4):
    - set_online_status: 设置在线状态
    - set_diy_online_status: 设置自定义在线状态
    - set_input_status: 设置输入状态
    - nc_get_user_status: 获取用户状态
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["StatusService"]


class StatusService(BaseService):
    """在线状态服务。

    封装全部在线状态 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    name: str = "status_service"
    description: str = "在线状态服务"
    version: str = "1.0.0"

    async def set_online_status(
        self,
        status: int,
        ext_status: int = 0,
        battery_status: int = 0,
    ) -> dict[str, Any]:
        """设置在线状态。

        对应 NapCat 扩展 API: ``set_online_status``。

        Args:
            status: 在线状态值。
            ext_status: 扩展状态值，默认为 0。
            battery_status: 电池状态百分比，默认为 0。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "status": status,
            "ext_status": ext_status,
            "battery_status": battery_status,
        }
        return await _call_onebot_api("set_online_status", params)

    async def set_diy_online_status(
        self,
        face_id: int,
        face_type: int = 1,
        wording: str = "",
    ) -> dict[str, Any]:
        """设置自定义在线状态。

        对应 NapCat 扩展 API: ``set_diy_online_status``。

        Args:
            face_id: 表情 ID。
            face_type: 表情类型，默认为 1。
            wording: 状态文字，默认为空字符串。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "face_id": face_id,
            "face_type": face_type,
        }
        if wording:
            params["wording"] = wording
        return await _call_onebot_api("set_diy_online_status", params)

    async def set_input_status(
        self,
        user_id: int,
        event_type: int,
    ) -> dict[str, Any]:
        """设置输入状态。

        对应 NapCat 扩展 API: ``set_input_status``。

        Args:
            user_id: 目标用户 QQ 号。
            event_type: 输入状态事件类型（1=正在输入, 0=取消输入）。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "event_type": event_type,
        }
        return await _call_onebot_api("set_input_status", params)

    async def nc_get_user_status(self, user_id: int) -> dict[str, Any]:
        """获取用户状态。

        对应 NapCat 扩展 API: ``nc_get_user_status``。

        Args:
            user_id: 目标用户 QQ 号。

        Returns:
            适配器返回的响应字典，包含用户在线状态信息。
        """
        params: dict[str, Any] = {"user_id": user_id}
        return await _call_onebot_api("nc_get_user_status", params)