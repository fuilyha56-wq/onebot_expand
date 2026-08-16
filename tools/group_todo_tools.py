"""群待办 API 的 Tool 组件。

包含 4 个群待办 Tool，对应 NapCat/SnowLuma 群待办 API：
    - set_group_todo: 设置群待办
    - complete_group_todo: 完成群待办
    - cancel_group_todo: 取消群待办
    - get_group_todo_list: 获取群待办列表（SnowLuma 扩展）

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from ..message_utils import MessageId
from . import _call_onebot_api

__all__ = [
    "SetGroupTodoTool",
    "CompleteGroupTodoTool",
    "CancelGroupTodoTool",
    "GetGroupTodoListTool",
]


class GetGroupTodoListTool(BaseTool):
    """获取群待办列表的 Tool（SnowLuma 扩展）。"""

    name = "get_group_todo_list"
    description = "获取指定群的待办列表（SnowLuma扩展）"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        result = await _call_onebot_api("get_group_todo_list", {"group_id": group_id})
        if result.get("status") == "ok":
            return True, result.get("data", {})
        return False, f"获取群待办列表失败: {result.get('msg', '未知错误')}"


class SetGroupTodoTool(BaseTool):
    """设置群待办的 Tool。

    对应 NapCat API: ``set_group_todo``。
    在指定群中设置待办事项。
    """

    name = "set_group_todo"
    description = "在指定群中设置待办事项"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        message_id: Annotated[MessageId, "消息ID"],
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

    name = "complete_group_todo"
    description = "完成指定群中的待办事项"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        message_id: Annotated[MessageId, "消息ID"],
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

    name = "cancel_group_todo"
    description = "取消指定群中的待办事项"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        message_id: Annotated[MessageId, "消息ID"],
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
