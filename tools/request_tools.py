"""请求处理相关 API 的 Tool 组件。

包含 6 个请求处理 Tool，对应 OneBot v11 标准请求 API 和扩展请求 API：
    - set_friend_add_request: 处理好友添加请求 (OB11标准)
    - set_group_add_request: 处理加群请求 (OB11标准)
    - get_group_system_msg: 获取群系统消息 (go-cqhttp兼容)
    - get_group_add_request: 获取群添加请求 (NapCat扩展)
    - get_doubt_friends_add_request: 获取可疑好友申请 (扩展)
    - set_doubt_friends_add_request: 处理可疑好友申请 (扩展)

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "SetFriendAddRequestTool",
    "SetGroupAddRequestTool",
    "GetGroupSystemMsgTool",
    "GetGroupAddRequestTool",
    "GetDoubtFriendsAddRequestTool",
    "SetDoubtFriendsAddRequestTool",
]


class SetFriendAddRequestTool(BaseTool):
    """处理好友添加请求的 Tool。

    对应 OneBot API: ``set_friend_add_request``。
    通过请求的 flag 和是否同意来处理好友添加请求。
    """

    tool_name = "set_friend_add_request"
    tool_description = "处理好友添加请求，可同意或拒绝"

    async def execute(
        self,
        flag: Annotated[str, "好友添加请求的 flag"],
        approve: Annotated[bool, "是否同意请求"],
        remark: Annotated[str, "好友备注（可选）"] = "",
    ) -> tuple[bool, str]:
        """执行处理好友添加请求。"""
        params: dict[str, Any] = {
            "flag": flag,
            "approve": approve,
        }
        if remark:
            params["remark"] = remark

        result = await _call_onebot_api("set_friend_add_request", params)
        if result.get("status") == "ok":
            action = "同意" if approve else "拒绝"
            return True, f"已{action}好友添加请求"
        return False, f"处理好友添加请求失败: {result.get('msg', '未知错误')}"


class SetGroupAddRequestTool(BaseTool):
    """处理加群请求的 Tool。

    对应 OneBot API: ``set_group_add_request``。
    通过请求的 flag、子类型和是否同意来处理加群请求。
    """

    tool_name = "set_group_add_request"
    tool_description = "处理加群请求，可同意或拒绝"

    async def execute(
        self,
        flag: Annotated[str, "加群请求的 flag"],
        sub_type: Annotated[str, "请求子类型（add 或 invite）"],
        approve: Annotated[bool, "是否同意请求"],
        reason: Annotated[str, "拒绝理由（可选）"] = "",
    ) -> tuple[bool, str]:
        """执行处理加群请求。"""
        params: dict[str, Any] = {
            "flag": flag,
            "sub_type": sub_type,
            "approve": approve,
        }
        if reason:
            params["reason"] = reason

        result = await _call_onebot_api("set_group_add_request", params)
        if result.get("status") == "ok":
            action = "同意" if approve else "拒绝"
            return True, f"已{action}加群请求"
        return False, f"处理加群请求失败: {result.get('msg', '未知错误')}"


class GetGroupSystemMsgTool(BaseTool):
    """获取群系统消息的 Tool。

    对应 go-cqhttp 兼容 API: ``get_group_system_msg``。
    获取群系统消息列表，包括加群请求、被邀请入群等。
    """

    tool_name = "get_group_system_msg"
    tool_description = "获取群系统消息列表（go-cqhttp兼容）"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群系统消息。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_group_system_msg", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群系统消息失败: {result.get('msg', '未知错误')}"


class GetGroupAddRequestTool(BaseTool):
    """获取群添加请求的 Tool。

    对应 NapCat 扩展 API: ``get_group_add_request``。
    获取群添加请求列表。
    """

    tool_name = "get_group_add_request"
    tool_description = "获取群添加请求列表（NapCat扩展）"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群添加请求。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_group_add_request", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群添加请求失败: {result.get('msg', '未知错误')}"


class GetDoubtFriendsAddRequestTool(BaseTool):
    """获取可疑好友申请的 Tool。

    对应扩展 API: ``get_doubt_friends_add_request``。
    获取可疑的好友添加请求列表。
    """

    tool_name = "get_doubt_friends_add_request"
    tool_description = "获取可疑好友申请列表（扩展）"

    async def execute(
        self,
        count: Annotated[int, "获取数量（默认20）"] = 20,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取可疑好友申请。"""
        params: dict[str, Any] = {"count": count}
        result = await _call_onebot_api("get_doubt_friends_add_request", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取可疑好友申请失败: {result.get('msg', '未知错误')}"


class SetDoubtFriendsAddRequestTool(BaseTool):
    """处理可疑好友申请的 Tool。

    对应扩展 API: ``set_doubt_friends_add_request``。
    通过请求的 flag 和是否同意来处理可疑好友申请。
    """

    tool_name = "set_doubt_friends_add_request"
    tool_description = "处理可疑好友申请，可同意或拒绝（扩展）"

    async def execute(
        self,
        flag: Annotated[str, "可疑好友申请的 flag"],
        approve: Annotated[bool, "是否同意请求"],
    ) -> tuple[bool, str]:
        """执行处理可疑好友申请。"""
        params: dict[str, Any] = {
            "flag": flag,
            "approve": approve,
        }
        result = await _call_onebot_api("set_doubt_friends_add_request", params)
        if result.get("status") == "ok":
            action = "同意" if approve else "拒绝"
            return True, f"已{action}可疑好友申请"
        return False, f"处理可疑好友申请失败: {result.get('msg', '未知错误')}"