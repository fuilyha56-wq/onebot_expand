"""用户信息扩展 API 的 Tool 组件。

包含 9 个用户信息扩展 Tool，对应 NapCat 用户信息扩展 API：
    - delete_friend: 删除好友
    - set_friend_remark: 设置好友备注
    - get_friends_with_category: 获取分组好友列表
    - get_unidirectional_friend_list: 获取单向好友列表
    - set_qq_profile: 设置QQ资料
    - set_qq_avatar: 设置QQ头像
    - set_self_longnick: 设置个性签名
    - get_recent_contact: 获取最近联系人
    - get_profile_like: 获取资料点赞

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "DeleteFriendTool",
    "SetFriendRemarkTool",
    "GetFriendsWithCategoryTool",
    "GetUnidirectionalFriendListTool",
    "SetQQProfileTool",
    "SetQQAvatarTool",
    "SetSelfLongnickTool",
    "GetRecentContactTool",
    "GetProfileLikeTool",
"GetProfileLikeMeTool",
    "GetProfileLikeCountTool",
    "GetQQAvatarTool",
    "SetFriendCategoryTool",
]


class DeleteFriendTool(BaseTool):
    """删除好友的 Tool。

    对应 NapCat API: ``delete_friend``。
    删除指定好友，可选是否同时拉黑。
    """

    tool_name = "delete_friend"
    tool_description = "删除指定好友，可选是否同时拉黑"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        block: Annotated[bool, "是否同时拉黑该好友"] = False,
    ) -> tuple[bool, str]:
        """执行删除好友。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "block": block,
        }
        result = await _call_onebot_api("delete_friend", params)
        if result.get("status") == "ok":
            block_msg = "并已拉黑" if block else ""
            return True, f"已删除好友 {user_id}{block_msg}"
        return False, f"删除好友失败: {result.get('msg', '未知错误')}"


class SetFriendRemarkTool(BaseTool):
    """设置好友备注的 Tool。

    对应 NapCat API: ``set_friend_remark``。
    设置指定好友的备注名。
    """

    tool_name = "set_friend_remark"
    tool_description = "设置指定好友的备注名"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        remark: Annotated[str, "备注名"],
    ) -> tuple[bool, str]:
        """执行设置好友备注。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "remark": remark,
        }
        result = await _call_onebot_api("set_friend_remark", params)
        if result.get("status") == "ok":
            return True, f"已设置好友 {user_id} 的备注为: {remark}"
        return False, f"设置好友备注失败: {result.get('msg', '未知错误')}"


class GetFriendsWithCategoryTool(BaseTool):
    """获取分组好友列表的 Tool。

    对应 NapCat API: ``get_friends_with_category``。
    返回按分组分类的好友列表。
    """

    tool_name = "get_friends_with_category"
    tool_description = "获取按分组分类的好友列表"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取分组好友列表。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_friends_with_category", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取分组好友列表失败: {result.get('msg', '未知错误')}"


class GetUnidirectionalFriendListTool(BaseTool):
    """获取单向好友列表的 Tool。

    对应 NapCat API: ``get_unidirectional_friend_list``。
    返回单向好友列表（对方加了自己但自己未加对方）。
    """

    tool_name = "get_unidirectional_friend_list"
    tool_description = "获取单向好友列表"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取单向好友列表。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_unidirectional_friend_list", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取单向好友列表失败: {result.get('msg', '未知错误')}"


class SetQQProfileTool(BaseTool):
    """设置QQ资料的 Tool。

    对应 NapCat API: ``set_qq_profile``。
    设置当前 Bot 的 QQ 资料（昵称、个人说明等）。
    """

    tool_name = "set_qq_profile"
    tool_description = "设置当前Bot的QQ资料（昵称、个人说明等）"

    async def execute(
        self,
        nickname: Annotated[str, "昵称"] = "",
        personal_note: Annotated[str, "个人说明"] = "",
    ) -> tuple[bool, str]:
        """执行设置QQ资料。"""
        params: dict[str, Any] = {}
        if nickname:
            params["nickname"] = nickname
        if personal_note:
            params["personal_note"] = personal_note
        result = await _call_onebot_api("set_qq_profile", params)
        if result.get("status") == "ok":
            return True, "QQ资料设置成功"
        return False, f"设置QQ资料失败: {result.get('msg', '未知错误')}"


class SetQQAvatarTool(BaseTool):
    """设置QQ头像的 Tool。

    对应 NapCat API: ``set_qq_avatar``。
    设置当前 Bot 的 QQ 头像。
    """

    tool_name = "set_qq_avatar"
    tool_description = "设置当前Bot的QQ头像"

    async def execute(
        self,
        file: Annotated[str, "头像图片路径或URL"],
    ) -> tuple[bool, str]:
        """执行设置QQ头像。"""
        params: dict[str, Any] = {"file": file}
        result = await _call_onebot_api("set_qq_avatar", params)
        if result.get("status") == "ok":
            return True, "QQ头像设置成功"
        return False, f"设置QQ头像失败: {result.get('msg', '未知错误')}"


class SetSelfLongnickTool(BaseTool):
    """设置个性签名的 Tool。

    对应 NapCat API: ``set_self_longnick``。
    设置当前 Bot 的个性签名。
    """

    tool_name = "set_self_longnick"
    tool_description = "设置当前Bot的个性签名"

    async def execute(
        self,
        long_nick: Annotated[str, "个性签名内容"],
    ) -> tuple[bool, str]:
        """执行设置个性签名。"""
        params: dict[str, Any] = {"long_nick": long_nick}
        result = await _call_onebot_api("set_self_longnick", params)
        if result.get("status") == "ok":
            return True, "个性签名设置成功"
        return False, f"设置个性签名失败: {result.get('msg', '未知错误')}"


class GetRecentContactTool(BaseTool):
    """获取最近联系人的 Tool。

    对应 NapCat API: ``get_recent_contact``。
    返回最近联系人列表。
    """

    tool_name = "get_recent_contact"
    tool_description = "获取最近联系人列表"

    async def execute(
        self,
        count: Annotated[int, "获取数量"] = 10,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取最近联系人。"""
        params: dict[str, Any] = {"count": count}
        result = await _call_onebot_api("get_recent_contact", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取最近联系人失败: {result.get('msg', '未知错误')}"


class GetProfileLikeTool(BaseTool):
    """获取资料点赞的 Tool。

    对应 NapCat API: ``get_profile_like``。
    获取指定用户的资料点赞信息。
    """

    tool_name = "get_profile_like"
    tool_description = "获取指定用户的资料点赞信息"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        start: Annotated[int, "起始位置"] = 0,
        count: Annotated[int, "获取数量"] = 10,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取资料点赞。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "start": start,
            "count": count,
        }
        result = await _call_onebot_api("get_profile_like", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取资料点赞失败: {result.get('msg', '未知错误')}"


class GetProfileLikeMeTool(BaseTool):
    """获取自身被点赞列表的 Tool。

    对应 API: ``get_profile_like_me``。
    """

    tool_name = "get_profile_like_me"
    tool_description = "获取自身被点赞列表"

    async def execute(
        self,
        start: Annotated[int, "起始位置(默认0)"],
        count: Annotated[int, "数量(默认20,最多30)"],
    ) -> tuple[bool, str]:
        """执行获取自身被点赞列表。"""
        params: dict[str, Any] = {
            "start": start,
            "count": count,
        }
        result = await _call_onebot_api("get_profile_like_me", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"获取自身被点赞列表失败: {result.get('msg', '未知错误')}"



class GetProfileLikeCountTool(BaseTool):
    """获取用户点赞总数的 Tool。

    对应 API: ``get_profile_like_count``。
    """

    tool_name = "get_profile_like_count"
    tool_description = "获取用户点赞总数"

    async def execute(
        self,
        user_id: Annotated[int, "目标QQ号"],
    ) -> tuple[bool, str]:
        """执行获取用户点赞总数。"""
        params: dict[str, Any] = {
            "user_id": user_id,
        }
        result = await _call_onebot_api("get_profile_like_count", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"获取用户点赞总数失败: {result.get('msg', '未知错误')}"



class GetQQAvatarTool(BaseTool):
    """获取QQ头像URL的 Tool。

    对应 API: ``get_qq_avatar``。
    """

    tool_name = "get_qq_avatar"
    tool_description = "获取QQ头像URL"

    async def execute(
        self,
        user_id: Annotated[int, "目标QQ号(与group_id二选一)"],
        group_id: Annotated[int, "目标群号(与user_id二选一)"],
    ) -> tuple[bool, str]:
        """执行获取QQ头像URL。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "group_id": group_id,
        }
        result = await _call_onebot_api("get_qq_avatar", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"获取QQ头像URL失败: {result.get('msg', '未知错误')}"



class SetFriendCategoryTool(BaseTool):
    """设置好友分类的 Tool。

    对应 API: ``set_friend_category``。
    """

    tool_name = "set_friend_category"
    tool_description = "设置好友分类"

    async def execute(
        self,
        user_id: Annotated[int, "目标QQ号"],
        category_id: Annotated[int, "分类ID"],
    ) -> tuple[bool, str]:
        """执行设置好友分类。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "category_id": category_id,
        }
        result = await _call_onebot_api("set_friend_category", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"设置好友分类失败: {result.get('msg', '未知错误')}"


