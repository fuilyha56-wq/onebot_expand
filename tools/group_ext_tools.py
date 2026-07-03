"""群管理扩展 API 的 Tool 组件。

包含 11 个群管理扩展 Tool：
    - set_group_portrait: 设置群头像
    - set_group_remark: 设置群备注
    - set_group_add_option: 设置加群选项
    - set_group_search: 允许群被搜索
    - set_group_robot_add_option: 设置群机器人加群选项
    - set_group_kick_members: 批量踢出群成员
    - get_group_shut_list: 获取群禁言列表
    - get_group_ignored_notifies: 获取被过滤的入群请求
    - get_group_ignore_add_request: 获取被忽略的入群请求
    - get_group_info_ex: 获取群信息扩展
    - set_group_sign: 群签到

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "SetGroupPortraitTool",
    "SetGroupRemarkTool",
    "SetGroupAddOptionTool",
    "SetGroupSearchTool",
    "SetGroupRobotAddOptionTool",
    "SetGroupKickMembersTool",
    "GetGroupShutListTool",
    "GetGroupIgnoredNotifiesTool",
    "GetGroupIgnoreAddRequestTool",
    "GetGroupInfoExTool",
    "SetGroupSignTool",
]


class SetGroupPortraitTool(BaseTool):
    """设置群头像的 Tool。

    对应 API: ``set_group_portrait``。
    设置指定群的群头像。
    """

    tool_name = "set_group_portrait"
    tool_description = "设置群头像"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        file: Annotated[str, "图片路径或URL"],
    ) -> tuple[bool, str]:
        """执行设置群头像。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "file": file,
        }
        result = await _call_onebot_api("set_group_portrait", params)
        if result.get("status") == "ok":
            return True, f"已设置群 {group_id} 的头像"
        return False, f"设置群头像失败: {result.get('msg', '未知错误')}"


class SetGroupRemarkTool(BaseTool):
    """设置群备注的 Tool。

    对应 API: ``set_group_remark``。
    设置指定群的群备注。
    """

    tool_name = "set_group_remark"
    tool_description = "设置群备注"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        remark: Annotated[str, "群备注内容"],
    ) -> tuple[bool, str]:
        """执行设置群备注。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "remark": remark,
        }
        result = await _call_onebot_api("set_group_remark", params)
        if result.get("status") == "ok":
            return True, f'已设置群 {group_id} 的备注为 "{remark}"'
        return False, f"设置群备注失败: {result.get('msg', '未知错误')}"


class SetGroupAddOptionTool(BaseTool):
    """设置加群选项的 Tool。

    对应 API: ``set_group_add_option``。
    设置指定群的加群方式选项。
    """

    tool_name = "set_group_add_option"
    tool_description = "设置加群选项"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        add_type: Annotated[int, "加群方式（0:允许任何人,1:需要验证,2:不允许任何人）"],
    ) -> tuple[bool, str]:
        """执行设置加群选项。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "add_type": add_type,
        }
        result = await _call_onebot_api("set_group_add_option", params)
        if result.get("status") == "ok":
            type_names = {0: "允许任何人", 1: "需要验证", 2: "不允许任何人"}
            type_desc = type_names.get(add_type, f"类型{add_type}")
            return True, f"已设置群 {group_id} 的加群方式为: {type_desc}"
        return False, f"设置加群选项失败: {result.get('msg', '未知错误')}"


class SetGroupSearchTool(BaseTool):
    """允许群被搜索的 Tool。

    对应 API: ``set_group_search``。
    设置指定群是否允许被搜索。
    """

    tool_name = "set_group_search"
    tool_description = "允许群被搜索"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str]:
        """执行允许群被搜索。"""
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        result = await _call_onebot_api("set_group_search", params)
        if result.get("status") == "ok":
            return True, f"已设置群 {group_id} 允许被搜索"
        return False, f"设置群搜索失败: {result.get('msg', '未知错误')}"


class SetGroupRobotAddOptionTool(BaseTool):
    """设置群机器人加群选项的 Tool。

    对应 API: ``set_group_robot_add_option``。
    设置群机器人是否允许加群。
    """

    tool_name = "set_group_robot_add_option"
    tool_description = "设置群机器人加群选项"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        robot_member_switch: Annotated[bool, "是否允许机器人加群"] = True,
    ) -> tuple[bool, str]:
        """执行设置群机器人加群选项。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "robot_member_switch": robot_member_switch,
        }
        result = await _call_onebot_api("set_group_robot_add_option", params)
        if result.get("status") == "ok":
            action = "允许" if robot_member_switch else "禁止"
            return True, f"已设置群 {group_id} {action}机器人加群"
        return False, f"设置群机器人加群选项失败: {result.get('msg', '未知错误')}"


class SetGroupKickMembersTool(BaseTool):
    """批量踢出群成员的 Tool。

    对应 API: ``set_group_kick_members``。
    批量将指定群成员移出群聊，可选是否拒绝再次加群请求。
    """

    tool_name = "set_group_kick_members"
    tool_description = "批量踢出群成员"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        user_id_list: Annotated[list[int], "要踢出的成员QQ号列表"],
        reject_add_request: Annotated[bool, "是否拒绝这些人再次加群请求"] = False,
    ) -> tuple[bool, str]:
        """执行批量踢出群成员。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id_list": user_id_list,
            "reject_add_request": reject_add_request,
        }
        result = await _call_onebot_api("set_group_kick_members", params)
        if result.get("status") == "ok":
            return True, f"已批量踢出群 {group_id} 中的 {len(user_id_list)} 名成员"
        return False, f"批量踢出群成员失败: {result.get('msg', '未知错误')}"


class GetGroupShutListTool(BaseTool):
    """获取群禁言列表的 Tool。

    对应 API: ``get_group_shut_list``。
    获取指定群中被禁言的成员列表。
    """

    tool_name = "get_group_shut_list"
    tool_description = "获取群禁言列表"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群禁言列表。"""
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        result = await _call_onebot_api("get_group_shut_list", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群禁言列表失败: {result.get('msg', '未知错误')}"


class GetGroupIgnoredNotifiesTool(BaseTool):
    """获取被过滤的入群请求的 Tool。

    对应 API: ``get_group_ignored_notifies``。
    获取被过滤的入群请求列表。
    """

    tool_name = "get_group_ignored_notifies"
    tool_description = "获取被过滤的入群请求"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取被过滤的入群请求。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_group_ignored_notifies", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取被过滤的入群请求失败: {result.get('msg', '未知错误')}"


class GetGroupIgnoreAddRequestTool(BaseTool):
    """获取被忽略的入群请求的 Tool。

    对应 API: ``get_group_ignore_add_request``。
    获取被忽略的入群请求列表。
    """

    tool_name = "get_group_ignore_add_request"
    tool_description = "获取被忽略的入群请求"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取被忽略的入群请求。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_group_ignore_add_request", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取被忽略的入群请求失败: {result.get('msg', '未知错误')}"


class GetGroupInfoExTool(BaseTool):
    """获取群信息扩展的 Tool。

    对应 API: ``get_group_info_ex``。
    获取指定群的扩展信息。
    """

    tool_name = "get_group_info_ex"
    tool_description = "获取群信息扩展"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群信息扩展。"""
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        result = await _call_onebot_api("get_group_info_ex", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群信息扩展失败: {result.get('msg', '未知错误')}"


class SetGroupSignTool(BaseTool):
    """群签到的 Tool。

    对应 API: ``set_group_sign``。
    在指定群中进行签到。
    """

    tool_name = "set_group_sign"
    tool_description = "群签到"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str]:
        """执行群签到。"""
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        result = await _call_onebot_api("set_group_sign", params)
        if result.get("status") == "ok":
            return True, f"已在群 {group_id} 签到"
        return False, f"群签到失败: {result.get('msg', '未知错误')}"