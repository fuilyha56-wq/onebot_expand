"""账号信息查询 API 的 Tool 组件。

包含 10 个账号信息查询 Tool，对应 OneBot v11 账号 API 和 NapCat 账号扩展 API：
    - get_login_info: 获取 Bot 登录信息
    - get_stranger_info: 获取陌生人信息
    - get_friend_list: 获取好友列表
    - get_group_list: 获取群列表
    - get_group_member_list: 获取群成员列表
    - get_group_member_info: 获取群成员详情
    - get_group_info: 获取群信息
    - get_group_detail_info: 获取群详细信息（NapCat 扩展）
    - get_group_honor_info: 获取群荣誉信息
    - get_robot_uin_range: 获取机器人 UIN 范围（NapCat 扩展）

Tool 不检查配置开关，配置开关由 Service 层统一检查。
这些 Tool 偏信息获取，返回值为 ``(bool, str | dict)`` 格式，查询成功时返回数据字典。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "GetLoginInfoTool",
    "GetStrangerInfoTool",
    "GetFriendListTool",
    "GetGroupListTool",
    "GetGroupMemberListTool",
    "GetGroupMemberInfoTool",
    "GetGroupInfoTool",
    "GetGroupDetailInfoTool",
    "GetGroupHonorInfoTool",
    "GetRobotUinRangeTool",
]


class GetLoginInfoTool(BaseTool):
    """获取 Bot 登录信息的 Tool。

    对应 OneBot API: ``get_login_info``。
    返回当前 Bot 的 QQ 号和昵称。
    """

    name = "get_login_info"
    description = "获取当前Bot的登录信息（QQ号和昵称）"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取 Bot 登录信息。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_login_info", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取登录信息失败: {result.get('msg', '未知错误')}"


class GetStrangerInfoTool(BaseTool):
    """获取陌生人信息的 Tool。

    对应 OneBot API: ``get_stranger_info``。
    根据 QQ 号获取陌生人的资料信息。
    """

    name = "get_stranger_info"
    description = "获取陌生人信息（根据QQ号查询用户资料）"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        no_cache: Annotated[bool, "是否不使用缓存"] = False,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取陌生人信息。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "no_cache": no_cache,
        }
        result = await _call_onebot_api("get_stranger_info", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取陌生人信息失败: {result.get('msg', '未知错误')}"


class GetFriendListTool(BaseTool):
    """获取好友列表的 Tool。

    对应 OneBot API: ``get_friend_list``。
    返回当前 Bot 的全部好友列表。
    """

    name = "get_friend_list"
    description = "获取当前Bot的全部好友列表"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取好友列表。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_friend_list", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取好友列表失败: {result.get('msg', '未知错误')}"


class GetGroupListTool(BaseTool):
    """获取群列表的 Tool。

    对应 OneBot API: ``get_group_list``。
    返回当前 Bot 加入的全部群列表。
    """

    name = "get_group_list"
    description = "获取当前Bot加入的全部群列表"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群列表。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_group_list", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取群列表失败: {result.get('msg', '未知错误')}"


class GetGroupMemberListTool(BaseTool):
    """获取群成员列表的 Tool。

    对应 OneBot API: ``get_group_member_list``。
    返回指定群的全部成员列表。
    """

    name = "get_group_member_list"
    description = "获取指定群的全部成员列表"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        no_cache: Annotated[bool, "是否不使用缓存"] = False,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群成员列表。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "no_cache": no_cache,
        }
        result = await _call_onebot_api("get_group_member_list", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取群成员列表失败: {result.get('msg', '未知错误')}"


class GetGroupMemberInfoTool(BaseTool):
    """获取群成员详情的 Tool。

    对应 OneBot API: ``get_group_member_info``。
    返回指定群中指定成员的详细信息。
    """

    name = "get_group_member_info"
    description = "获取指定群中指定成员的详细信息"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        user_id: Annotated[int, "目标成员QQ号"],
        no_cache: Annotated[bool, "是否不使用缓存"] = False,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群成员详情。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
            "no_cache": no_cache,
        }
        result = await _call_onebot_api("get_group_member_info", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群成员信息失败: {result.get('msg', '未知错误')}"


class GetGroupInfoTool(BaseTool):
    """获取群信息的 Tool。

    对应 OneBot API: ``get_group_info``。
    返回指定群的基本信息（群名、群主、群人数等）。
    """

    name = "get_group_info"
    description = "获取指定群的基本信息"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        no_cache: Annotated[bool, "是否不使用缓存"] = False,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群信息。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "no_cache": no_cache,
        }
        result = await _call_onebot_api("get_group_info", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群信息失败: {result.get('msg', '未知错误')}"


class GetGroupDetailInfoTool(BaseTool):
    """获取群详细信息的 Tool（NapCat 扩展）。

    对应 NapCat API: ``get_group_detail_info``。
    返回指定群的详细信息（比标准 get_group_info 更多字段）。
    """

    name = "get_group_detail_info"
    description = "获取指定群的详细信息（NapCat扩展，比标准API更多字段）"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群详细信息。"""
        params: dict[str, Any] = {"group_id": group_id}
        result = await _call_onebot_api("get_group_detail_info", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群详细信息失败: {result.get('msg', '未知错误')}"


class GetGroupHonorInfoTool(BaseTool):
    """获取群荣誉信息的 Tool。

    对应 OneBot API: ``get_group_honor_info``。
    返回指定群的荣誉信息（龙王、群聊之火等）。
    type 参数指定荣誉类型: talkative（龙王）、performer（群聊之火）、legend（群聊之焰）、
    strong_newbie（冒尖小春笋）、emotion（快乐之源）、all（全部）。
    """

    name = "get_group_honor_info"
    description = "获取指定群的荣誉信息（龙王、群聊之火等）"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        type: Annotated[
            str, "荣誉类型: talkative/performer/legend/strong_newbie/emotion/all"
        ] = "all",
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群荣誉信息。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "type": type,
        }
        result = await _call_onebot_api("get_group_honor_info", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群荣誉信息失败: {result.get('msg', '未知错误')}"


class GetRobotUinRangeTool(BaseTool):
    """获取机器人 UIN 范围的 Tool（NapCat 扩展）。

    对应 NapCat API: ``get_robot_uin_range``。
    返回当前可用的机器人 UIN 范围列表。
    """

    name = "get_robot_uin_range"
    description = "获取机器人 UIN 范围（NapCat扩展）"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取机器人 UIN 范围。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_robot_uin_range", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取机器人 UIN 范围失败: {result.get('msg', '未知错误')}"
