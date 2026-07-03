"""群待办 API 的 Tool 组件。

包含 3 个群待办 Tool，对应 NapCat 群待办 API：
    - set_group_todo: 设置群待办
    - complete_group_todo: 完成群待办
    - cancel_group_todo: 取消群待办

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "SetGroupTodoTool",
    "CompleteGroupTodoTool",
    "CancelGroupTodoTool",
]


class SetGroupTodoTool(BaseTool):
    """设置群待办的 Tool。

    对应 NapCat API: ``set_group_todo``。
    在指定群中设置待办事项。
    """

    tool_name = "set_group_todo"
    tool_description = "在指定群中设置待办事项"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        message_id: Annotated[int, "消息ID"],
    ) -> tuple[bool, str]:
        """执行设置群待办。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "message_id": message_id,
        }
        result = await _call_onebot_api("set_group_todo", params)
        if result.get("status") == "ok":
            return True, f"已在群 {group_id} 设置待办"
        return False, f"设置群待办失败: {result.get('msg', '未知错误')}"


class CompleteGroupTodoTool(BaseTool):
    """完成群待办的 Tool。

    对应 NapCat API: ``complete_group_todo``。
    完成指定群中的待办事项。
    """

    tool_name = "complete_group_todo"
    tool_description = "完成指定群中的待办事项"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        message_id: Annotated[int, "消息ID"],
    ) -> tuple[bool, str]:
        """执行完成群待办。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "message_id": message_id,
        }
        result = await _call_onebot_api("complete_group_todo", params)
        if result.get("status") == "ok":
            return True, f"已完成群 {group_id} 的待办"
        return False, f"完成群待办失败: {result.get('msg', '未知错误')}"


class CancelGroupTodoTool(BaseTool):
    """取消群待办的 Tool。

    对应 NapCat API: ``cancel_group_todo``。
    取消指定群中的待办事项。
    """

    tool_name = "cancel_group_todo"
    tool_description = "取消指定群中的待办事项"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        message_id: Annotated[int, "消息ID"],
    ) -> tuple[bool, str]:
        """执行取消群待办。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "message_id": message_id,
        }
        result = await _call_onebot_api("cancel_group_todo", params)
        if result.get("status") == "ok":
            return True, f"已取消群 {group_id} 的待办"
        return False, f"取消群待办失败: {result.get('msg', '未知错误')}"