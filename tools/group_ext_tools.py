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
    "GetGroupSignedListTool",
"BatchDeleteGroupMemberTool",
    "SetGroupMsgMaskTool",
]


class SetGroupPortraitTool(BaseTool):
    """设置群头像的 Tool。

    对应 API: ``set_group_portrait``。
    设置指定群的群头像。
    """

    name = "set_group_portrait"
    description = "设置群头像"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        file: Annotated[str, "图片路径或URL"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行设置群头像。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "file": file,
        }
        result = await _call_onebot_api("set_group_portrait", params)
        return result.get("status") == "ok", result


class SetGroupRemarkTool(BaseTool):
    """设置群备注的 Tool。

    对应 API: ``set_group_remark``。
    设置指定群的群备注。
    """

    name = "set_group_remark"
    description = "设置群备注"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        remark: Annotated[str, "群备注内容"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行设置群备注。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "remark": remark,
        }
        result = await _call_onebot_api("set_group_remark", params)
        return result.get("status") == "ok", result


class SetGroupAddOptionTool(BaseTool):
    """设置加群选项的 Tool。

    对应 API: ``set_group_add_option``。
    设置指定群的加群方式选项。
    """

    name = "set_group_add_option"
    description = "设置加群选项"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        add_type: Annotated[int, "加群方式（0:允许任何人,1:需要验证,2:不允许任何人）"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行设置加群选项。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "add_type": add_type,
        }
        result = await _call_onebot_api("set_group_add_option", params)
        return result.get("status") == "ok", result


class SetGroupSearchTool(BaseTool):
    """允许群被搜索的 Tool。

    对应 API: ``set_group_search``。
    设置指定群是否允许被搜索。
    """

    name = "set_group_search"
    description = "允许群被搜索"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行允许群被搜索。"""
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        result = await _call_onebot_api("set_group_search", params)
        return result.get("status") == "ok", result


class SetGroupRobotAddOptionTool(BaseTool):
    """设置群机器人加群选项的 Tool。

    对应 API: ``set_group_robot_add_option``。
    设置群机器人是否允许加群。
    """

    name = "set_group_robot_add_option"
    description = "设置群机器人加群选项"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        robot_member_switch: Annotated[bool, "是否允许机器人加群"] = True,
    ) -> tuple[bool, dict[str, Any]]:
        """执行设置群机器人加群选项。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "robot_member_switch": robot_member_switch,
        }
        result = await _call_onebot_api("set_group_robot_add_option", params)
        return result.get("status") == "ok", result


class SetGroupKickMembersTool(BaseTool):
    """批量踢出群成员的 Tool。

    对应 API: ``set_group_kick_members``。
    批量将指定群成员移出群聊，可选是否拒绝再次加群请求。
    """

    name = "set_group_kick_members"
    description = "批量踢出群成员"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        user_id_list: Annotated[list[int], "要踢出的成员QQ号列表"],
        reject_add_request: Annotated[bool, "是否拒绝这些人再次加群请求"] = False,
    ) -> tuple[bool, dict[str, Any]]:
        """执行批量踢出群成员。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id_list": user_id_list,
            "reject_add_request": reject_add_request,
        }
        result = await _call_onebot_api("set_group_kick_members", params)
        return result.get("status") == "ok", result


class GetGroupShutListTool(BaseTool):
    """获取群禁言列表的 Tool。

    对应 API: ``get_group_shut_list``。
    获取指定群中被禁言的成员列表。
    """

    name = "get_group_shut_list"
    description = "获取群禁言列表"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群禁言列表。"""
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        result = await _call_onebot_api("get_group_shut_list", params)
        return result.get("status") == "ok", result


class GetGroupIgnoredNotifiesTool(BaseTool):
    """获取被过滤的入群请求的 Tool。

    对应 API: ``get_group_ignored_notifies``。
    获取被过滤的入群请求列表。
    """

    name = "get_group_ignored_notifies"
    description = "获取被过滤的入群请求"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取被过滤的入群请求。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_group_ignored_notifies", params)
        return result.get("status") == "ok", result


class GetGroupIgnoreAddRequestTool(BaseTool):
    """获取被忽略的入群请求的 Tool。

    对应 API: ``get_group_ignore_add_request``。
    获取被忽略的入群请求列表。
    """

    name = "get_group_ignore_add_request"
    description = "获取被忽略的入群请求"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取被忽略的入群请求。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_group_ignore_add_request", params)
        return result.get("status") == "ok", result


class GetGroupInfoExTool(BaseTool):
    """获取群信息扩展的 Tool。

    对应 API: ``get_group_info_ex``。
    获取指定群的扩展信息。
    """

    name = "get_group_info_ex"
    description = "获取群信息扩展"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群信息扩展。"""
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        result = await _call_onebot_api("get_group_info_ex", params)
        return result.get("status") == "ok", result


class SetGroupSignTool(BaseTool):
    """群签到的 Tool。

    对应 API: ``set_group_sign``。
    在指定群中进行签到。
    """

    name = "set_group_sign"
    description = "群签到"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行群签到。"""
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        result = await _call_onebot_api("set_group_sign", params)
        return result.get("status") == "ok", result


class GetGroupSignedListTool(BaseTool):
    """获取群今日打卡列表的 Tool。

    对应 API: ``get_group_signed_list``。
    获取指定群今日已签到的成员列表。
    """

    name = "get_group_signed_list"
    description = "获取群今日打卡列表"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群今日打卡列表。"""
        params: dict[str, Any] = {"group_id": group_id}
        result = await _call_onebot_api("get_group_signed_list", params)
        return result.get("status") == "ok", result


class BatchDeleteGroupMemberTool(BaseTool):
    """批量踢出群成员的 Tool。

    对应 API: ``batch_delete_group_member``。
    """

    name = "batch_delete_group_member"
    description = "批量踢出群成员"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        user_ids: Annotated[list[int], "要踢出的QQ号列表"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行批量踢出群成员。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_ids": user_ids,
        }
        result = await _call_onebot_api("batch_delete_group_member", params)
        return result.get("status") == "ok", result



class SetGroupMsgMaskTool(BaseTool):
    """设置群消息屏蔽的 Tool。

    对应 API: ``set_group_msg_mask``。
    """

    name = "set_group_msg_mask"
    description = "设置群消息屏蔽"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        mask: Annotated[int, "屏蔽等级(1-4)"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行设置群消息屏蔽。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "mask": mask,
        }
        result = await _call_onebot_api("set_group_msg_mask", params)
        return result.get("status") == "ok", result


