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

from ..tools import _call_onebot_api

__all__ = ["GroupTodoService"]


class GroupTodoService(BaseService):
    """群待办服务。

    封装全部群待办 API 调用，提供配置开关检查和统一调用入口。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "group_todo_service"
    service_description: str = "群待办服务"
    version: str = "1.0.0"

    def _is_api_enabled(self, api_name: str) -> bool:
        """检查 API 是否在配置中启用。

        1.3.0 起支持别名：传入别名时会先解析为主名再查询配置开关。
        """
        from ..api_defs import resolve_action

        config = self.plugin.config
        if config is None:
            return True
        switches = getattr(config, "api_switches", None)
        if switches is None:
            return True
        primary = resolve_action(api_name) or api_name
        return getattr(switches, f"enable_{primary}", True)

    @staticmethod
    def _disabled_response(api_name: str) -> dict[str, Any]:
        """构造 API 禁用时的标准响应。"""
        return {"status": "error", "retcode": -1, "msg": f"API {api_name} 已禁用"}

    async def set_group_todo(
        self,
        group_id: int,
        message_id: int,
    ) -> dict[str, Any]:
        """设置群待办。

        对应 NapCat 扩展 API: ``set_group_todo``。

        Args:
            group_id: 群号。
            message_id: 消息 ID。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("set_group_todo"):
            return self._disabled_response("set_group_todo")
        params: dict[str, Any] = {
            "group_id": group_id,
            "message_id": message_id,
        }
        return await _call_onebot_api("set_group_todo", params)

    async def complete_group_todo(
        self,
        group_id: int,
        message_id: int,
    ) -> dict[str, Any]:
        """完成群待办。

        对应 NapCat 扩展 API: ``complete_group_todo``。

        Args:
            group_id: 群号。
            message_id: 消息 ID。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("complete_group_todo"):
            return self._disabled_response("complete_group_todo")
        params: dict[str, Any] = {
            "group_id": group_id,
            "message_id": message_id,
        }
        return await _call_onebot_api("complete_group_todo", params)

    async def cancel_group_todo(
        self,
        group_id: int,
        message_id: int,
    ) -> dict[str, Any]:
        """取消群待办。

        对应 NapCat 扩展 API: ``cancel_group_todo``。

        Args:
            group_id: 群号。
            message_id: 消息 ID。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("cancel_group_todo"):
            return self._disabled_response("cancel_group_todo")
        params: dict[str, Any] = {
            "group_id": group_id,
            "message_id": message_id,
        }
        return await _call_onebot_api("cancel_group_todo", params)