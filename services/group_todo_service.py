"""群待办服务。

封装 NapCat 群待办 API，提供群待办设置、完成、取消等功能。

API 列表 (3):
    - set_group_todo: 设置群待办
    - complete_group_todo: 完成群待办
    - cancel_group_todo: 取消群待办
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..message_utils import MessageId
from ..tools import _call_onebot_api

__all__ = ["GroupTodoService"]


class GroupTodoService(BaseService):
    """群待办服务。

    封装全部群待办 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    name: str = "group_todo_service"
    description: str = "群待办服务"
    version: str = "1.0.0"

    async def set_group_todo(
        self,
        group_id: int,
        message_id: MessageId,
    ) -> dict[str, Any]:
        """设置群待办。

        对应 NapCat 扩展 API: ``set_group_todo``。

        Args:
            group_id: 群号。
            message_id: 消息 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "message_id": message_id,
        }
        return await _call_onebot_api("set_group_todo", params)

    async def complete_group_todo(
        self,
        group_id: int,
        message_id: MessageId,
    ) -> dict[str, Any]:
        """完成群待办。

        对应 NapCat 扩展 API: ``complete_group_todo``。

        Args:
            group_id: 群号。
            message_id: 消息 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "message_id": message_id,
        }
        return await _call_onebot_api("complete_group_todo", params)

    async def cancel_group_todo(
        self,
        group_id: int,
        message_id: MessageId,
    ) -> dict[str, Any]:
        """取消群待办。

        对应 NapCat 扩展 API: ``cancel_group_todo``。

        Args:
            group_id: 群号。
            message_id: 消息 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "message_id": message_id,
        }
        return await _call_onebot_api("cancel_group_todo", params)