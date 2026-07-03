"""群操作 API 的 Tool 组件。

包含 10 个群操作 Tool，对应 OneBot v11 标准群操作 API：
    - set_group_kick: 踢出群成员
    - set_group_ban: 禁言群成员
    - set_group_anonymous_ban: 禁言匿名群成员
    - set_group_whole_ban: 全体禁言
    - set_group_admin: 设置/取消管理员
    - set_group_anonymous: 开启/关闭匿名聊天
    - set_group_card: 设置群名片
    - set_group_name: 设置群名
    - set_group_leave: 退出群聊
    - set_group_special_title: 设置专属头衔

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "SetGroupKickTool",
    "SetGroupBanTool",
    "SetGroupAnonymousBanTool",
    "SetGroupWholeBanTool",
    "SetGroupAdminTool",
    "SetGroupAnonymousTool",
    "SetGroupCardTool",
    "SetGroupNameTool",
    "SetGroupLeaveTool",
    "SetGroupSpecialTitleTool",
]


class SetGroupKickTool(BaseTool):
    """踢出群成员的 Tool。

    对应 OneBot API: ``set_group_kick``。
    将指定群成员移出群聊，可选是否拒绝再次加群请求。
    """

    tool_name = "set_group_kick"
    tool_description = "踢出指定群成员"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        user_id: Annotated[int, "要踢出的成员QQ号"],
        reject_add_request: Annotated[bool, "是否拒绝此人再次加群请求"] = False,
    ) -> tuple[bool, str]:
        """执行踢出群成员。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
            "reject_add_request": reject_add_request,
        }
        result = await _call_onebot_api("set_group_kick", params)
        if result.get("status") == "ok":
            return True, f"已踢出群 {group_id} 中的成员 {user_id}"
        return False, f"踢出群成员失败: {result.get('msg', '未知错误')}"


class SetGroupBanTool(BaseTool):
    """禁言群成员的 Tool。

    对应 OneBot API: ``set_group_ban``。
    对指定群成员设置禁言时长，duration 为 0 表示解除禁言。
    """

    tool_name = "set_group_ban"
    tool_description = "禁言指定群成员，duration为0表示解除禁言"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        user_id: Annotated[int, "要禁言的成员QQ号"],
        duration: Annotated[int, "禁言时长（秒），0表示解除禁言"] = 1800,
    ) -> tuple[bool, str]:
        """执行禁言群成员。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration,
        }
        result = await _call_onebot_api("set_group_ban", params)
        if result.get("status") == "ok":
            if duration == 0:
                return True, f"已解除群 {group_id} 中成员 {user_id} 的禁言"
            return True, f"已禁言群 {group_id} 中的成员 {user_id}，时长 {duration} 秒"
        return False, f"禁言群成员失败: {result.get('msg', '未知错误')}"


class SetGroupAnonymousBanTool(BaseTool):
    """禁言匿名群成员的 Tool。

    对应 OneBot API: ``set_group_anonymous_ban``。
    通过匿名标识或匿名 flag 禁言匿名成员。
    需提供 anonymous（匿名对象）或 anonymous_flag（匿名 flag）之一。
    """

    tool_name = "set_group_anonymous_ban"
    tool_description = "禁言匿名群成员，需提供匿名对象或匿名flag"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        anonymous_flag: Annotated[str, "匿名成员的flag标识"],
        duration: Annotated[int, "禁言时长（秒），0表示解除禁言"] = 1800,
        anonymous: Annotated[
            dict[str, Any] | None, "匿名成员对象（可选，与flag二选一）"
        ] = None,
    ) -> tuple[bool, str]:
        """执行禁言匿名群成员。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "duration": duration,
        }
        if anonymous is not None:
            params["anonymous"] = anonymous
        if anonymous_flag:
            params["anonymous_flag"] = anonymous_flag

        result = await _call_onebot_api("set_group_anonymous_ban", params)
        if result.get("status") == "ok":
            if duration == 0:
                return True, f"已解除群 {group_id} 中匿名成员的禁言"
            return True, f"已禁言群 {group_id} 中的匿名成员，时长 {duration} 秒"
        return False, f"禁言匿名成员失败: {result.get('msg', '未知错误')}"


class SetGroupWholeBanTool(BaseTool):
    """全体禁言的 Tool。

    对应 OneBot API: ``set_group_whole_ban``。
    开启或关闭群的全员禁言状态。
    """

    tool_name = "set_group_whole_ban"
    tool_description = "开启或关闭群的全员禁言"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        enable: Annotated[bool, "True为开启全体禁言，False为关闭"] = True,
    ) -> tuple[bool, str]:
        """执行全体禁言。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "enable": enable,
        }
        result = await _call_onebot_api("set_group_whole_ban", params)
        if result.get("status") == "ok":
            action = "开启" if enable else "关闭"
            return True, f"已{action}群 {group_id} 的全体禁言"
        return False, f"全体禁言设置失败: {result.get('msg', '未知错误')}"


class SetGroupAdminTool(BaseTool):
    """设置/取消群管理员的 Tool。

    对应 OneBot API: ``set_group_admin``。
    设置或取消指定群成员的管理员身份。
    """

    tool_name = "set_group_admin"
    tool_description = "设置或取消群成员的管理员身份"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        user_id: Annotated[int, "目标成员QQ号"],
        enable: Annotated[bool, "True为设置管理员，False为取消管理员"] = True,
    ) -> tuple[bool, str]:
        """执行设置/取消管理员。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
            "enable": enable,
        }
        result = await _call_onebot_api("set_group_admin", params)
        if result.get("status") == "ok":
            action = "设置" if enable else "取消"
            return True, f"已{action}群 {group_id} 中成员 {user_id} 的管理员身份"
        return False, f"设置管理员失败: {result.get('msg', '未知错误')}"


class SetGroupAnonymousTool(BaseTool):
    """开启/关闭匿名聊天的 Tool。

    对应 OneBot API: ``set_group_anonymous``。
    开启或关闭群的匿名聊天功能。
    """

    tool_name = "set_group_anonymous"
    tool_description = "开启或关闭群的匿名聊天功能"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        enable: Annotated[bool, "True为开启匿名聊天，False为关闭"] = True,
    ) -> tuple[bool, str]:
        """执行开启/关闭匿名聊天。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "enable": enable,
        }
        result = await _call_onebot_api("set_group_anonymous", params)
        if result.get("status") == "ok":
            action = "开启" if enable else "关闭"
            return True, f"已{action}群 {group_id} 的匿名聊天"
        return False, f"匿名聊天设置失败: {result.get('msg', '未知错误')}"


class SetGroupCardTool(BaseTool):
    """设置群名片的 Tool。

    对应 OneBot API: ``set_group_card``。
    修改指定群成员的群名片（群昵称）。
    """

    tool_name = "set_group_card"
    tool_description = "设置群成员的群名片（群昵称）"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        user_id: Annotated[int, "目标成员QQ号"],
        card: Annotated[str, "群名片内容，空字符串表示清空名片"] = "",
    ) -> tuple[bool, str]:
        """执行设置群名片。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
            "card": card,
        }
        result = await _call_onebot_api("set_group_card", params)
        if result.get("status") == "ok":
            card_desc = f'"{card}"' if card else "（已清空）"
            return True, f"已设置群 {group_id} 中成员 {user_id} 的名片为 {card_desc}"
        return False, f"设置群名片失败: {result.get('msg', '未知错误')}"


class SetGroupNameTool(BaseTool):
    """设置群名的 Tool。

    对应 OneBot API: ``set_group_name``。
    修改指定群的群名称。
    """

    tool_name = "set_group_name"
    tool_description = "修改群名称"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        group_name: Annotated[str, "新的群名称"],
    ) -> tuple[bool, str]:
        """执行设置群名。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "group_name": group_name,
        }
        result = await _call_onebot_api("set_group_name", params)
        if result.get("status") == "ok":
            return True, f'已修改群 {group_id} 的名称为 "{group_name}"'
        return False, f"设置群名失败: {result.get('msg', '未知错误')}"


class SetGroupLeaveTool(BaseTool):
    """退出群聊的 Tool。

    对应 OneBot API: ``set_group_leave``。
    退出指定群聊，可选是否解散群（仅群主可解散）。
    """

    tool_name = "set_group_leave"
    tool_description = "退出群聊，可选是否解散群（仅群主可解散）"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        is_dismiss: Annotated[bool, "是否解散群（仅群主有效）"] = False,
    ) -> tuple[bool, str]:
        """执行退出群聊。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "is_dismiss": is_dismiss,
        }
        result = await _call_onebot_api("set_group_leave", params)
        if result.get("status") == "ok":
            action = "解散" if is_dismiss else "退出"
            return True, f"已{action}群 {group_id}"
        return False, f"退出群聊失败: {result.get('msg', '未知错误')}"


class SetGroupSpecialTitleTool(BaseTool):
    """设置专属头衔的 Tool。

    对应 OneBot API: ``set_group_special_title``。
    修改指定群成员的专属头衔。
    """

    tool_name = "set_group_special_title"
    tool_description = "设置群成员的专属头衔"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        user_id: Annotated[int, "目标成员QQ号"],
        special_title: Annotated[str, "专属头衔内容，空字符串表示清空"],
        duration: Annotated[int, "头衔有效期（秒），-1表示永久"] = -1,
    ) -> tuple[bool, str]:
        """执行设置专属头衔。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title,
            "duration": duration,
        }
        result = await _call_onebot_api("set_group_special_title", params)
        if result.get("status") == "ok":
            title_desc = f'"{special_title}"' if special_title else "（已清空）"
            return True, f"已设置群 {group_id} 中成员 {user_id} 的头衔为 {title_desc}"
        return False, f"设置专属头衔失败: {result.get('msg', '未知错误')}"
