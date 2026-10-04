"""用户信息扩展 API 的 Tool 组件。

包含 15 个用户信息扩展 Tool，对应 NapCat、SnowLuma 与 LLBot 扩展 API：
    - delete_friend: 删除好友
    - set_friend_remark: 设置好友备注
    - get_friends_with_category: 获取分组好友列表
    - get_unidirectional_friend_list: 获取单向好友列表
    - set_qq_profile: 设置QQ资料
    - set_qq_avatar: 设置QQ头像
    - set_self_longnick: 设置个性签名
    - get_recent_contact: 获取最近联系人
    - get_profile_like: 获取资料点赞
    - get_profile_like_me: 获取自身被点赞列表
    - get_profile_like_count: 获取用户点赞总数
    - get_qq_avatar: 获取QQ头像URL
    - set_friend_category: 按分类 ID 设置好友分类（LLBot 扩展）
    - set_friends_category: 按分类 ID 或名称设置好友分类（SnowLuma 扩展）
    - _get_friend_dress: 获取好友个性装扮（SnowLuma 扩展）

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
    "SetFriendsCategoryTool",
    "GetFriendDressTool",
]


class DeleteFriendTool(BaseTool):
    """删除好友的 Tool。

    对应 NapCat API: ``delete_friend``。
    删除指定好友，可选是否同时拉黑。
    """

    name = "delete_friend"
    description = "删除指定好友，可选是否同时拉黑"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        block: Annotated[bool, "是否同时拉黑该好友"] = False,
    ) -> tuple[bool, dict[str, Any]]:
        """执行删除好友。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "block": block,
        }
        result = await _call_onebot_api("delete_friend", params)
        return result.get("status") == "ok", result


class SetFriendRemarkTool(BaseTool):
    """设置好友备注的 Tool。

    对应 NapCat API: ``set_friend_remark``。
    设置指定好友的备注名。
    """

    name = "set_friend_remark"
    description = "设置指定好友的备注名"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        remark: Annotated[str, "备注名"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行设置好友备注。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "remark": remark,
        }
        result = await _call_onebot_api("set_friend_remark", params)
        return result.get("status") == "ok", result


class GetFriendsWithCategoryTool(BaseTool):
    """获取分组好友列表的 Tool。

    对应 NapCat API: ``get_friends_with_category``。
    返回按分组分类的好友列表。
    """

    name = "get_friends_with_category"
    description = "获取按分组分类的好友列表"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取分组好友列表。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_friends_with_category", params)
        return result.get("status") == "ok", result


class GetUnidirectionalFriendListTool(BaseTool):
    """获取单向好友列表的 Tool。

    对应 NapCat API: ``get_unidirectional_friend_list``。
    返回单向好友列表（对方加了自己但自己未加对方）。
    """

    name = "get_unidirectional_friend_list"
    description = "获取单向好友列表"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取单向好友列表。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_unidirectional_friend_list", params)
        return result.get("status") == "ok", result


class SetQQProfileTool(BaseTool):
    """设置QQ资料的 Tool。

    对应 NapCat API: ``set_qq_profile``。
    设置当前 Bot 的 QQ 资料（昵称、个人说明等）。
    """

    name = "set_qq_profile"
    description = "设置当前Bot的QQ资料（昵称、个人说明等）"

    async def execute(
        self,
        nickname: Annotated[str, "昵称"] = "",
        personal_note: Annotated[str, "个人说明"] = "",
    ) -> tuple[bool, dict[str, Any]]:
        """执行设置QQ资料。"""
        params: dict[str, Any] = {}
        if nickname:
            params["nickname"] = nickname
        if personal_note:
            params["personal_note"] = personal_note
        result = await _call_onebot_api("set_qq_profile", params)
        return result.get("status") == "ok", result


class SetQQAvatarTool(BaseTool):
    """设置QQ头像的 Tool。

    对应 NapCat API: ``set_qq_avatar``。
    设置当前 Bot 的 QQ 头像。
    """

    name = "set_qq_avatar"
    description = "设置当前Bot的QQ头像"

    async def execute(
        self,
        file: Annotated[str, "头像图片路径或URL"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行设置QQ头像。"""
        params: dict[str, Any] = {"file": file}
        result = await _call_onebot_api("set_qq_avatar", params)
        return result.get("status") == "ok", result


class SetSelfLongnickTool(BaseTool):
    """设置个性签名的 Tool。

    对应 NapCat API: ``set_self_longnick``。
    设置当前 Bot 的个性签名。
    """

    name = "set_self_longnick"
    description = "设置当前Bot的个性签名"

    async def execute(
        self,
        long_nick: Annotated[str, "个性签名内容"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行设置个性签名。"""
        params: dict[str, Any] = {"long_nick": long_nick}
        result = await _call_onebot_api("set_self_longnick", params)
        return result.get("status") == "ok", result


class GetRecentContactTool(BaseTool):
    """获取最近联系人的 Tool。

    对应 NapCat API: ``get_recent_contact``。
    返回最近联系人列表。
    """

    name = "get_recent_contact"
    description = "获取最近联系人列表"

    async def execute(
        self,
        count: Annotated[int, "获取数量"] = 10,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取最近联系人。"""
        params: dict[str, Any] = {"count": count}
        result = await _call_onebot_api("get_recent_contact", params)
        return result.get("status") == "ok", result


class GetProfileLikeTool(BaseTool):
    """获取资料点赞的 Tool。

    对应 NapCat API: ``get_profile_like``。
    获取指定用户的资料点赞信息。
    """

    name = "get_profile_like"
    description = "获取指定用户的资料点赞信息"

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
        return result.get("status") == "ok", result


class GetProfileLikeMeTool(BaseTool):
    """获取自身被点赞列表的 Tool。

    对应 API: ``get_profile_like_me``。
    """

    name = "get_profile_like_me"
    description = "获取自身被点赞列表"

    async def execute(
        self,
        start: Annotated[int, "起始位置(默认0)"],
        count: Annotated[int, "数量(默认20,最多30)"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行获取自身被点赞列表。"""
        params: dict[str, Any] = {
            "start": start,
            "count": count,
        }
        result = await _call_onebot_api("get_profile_like_me", params)
        return result.get("status") == "ok", result


class GetProfileLikeCountTool(BaseTool):
    """获取用户点赞总数的 Tool。

    对应 API: ``get_profile_like_count``。
    """

    name = "get_profile_like_count"
    description = "获取用户点赞总数"

    async def execute(
        self,
        user_id: Annotated[int, "目标QQ号"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行获取用户点赞总数。"""
        params: dict[str, Any] = {
            "user_id": user_id,
        }
        result = await _call_onebot_api("get_profile_like_count", params)
        return result.get("status") == "ok", result


class GetQQAvatarTool(BaseTool):
    """获取QQ头像URL的 Tool。

    对应 API: ``get_qq_avatar``。
    """

    name = "get_qq_avatar"
    description = "获取QQ头像URL"

    async def execute(
        self,
        user_id: Annotated[int, "目标QQ号(与group_id二选一)"],
        group_id: Annotated[int, "目标群号(与user_id二选一)"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行获取QQ头像URL。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "group_id": group_id,
        }
        result = await _call_onebot_api("get_qq_avatar", params)
        return result.get("status") == "ok", result


class SetFriendCategoryTool(BaseTool):
    """设置好友分类的 Tool。

    对应 API: ``set_friend_category``。
    """

    name = "set_friend_category"
    description = "设置好友分类"

    async def execute(
        self,
        user_id: Annotated[int, "目标QQ号"],
        category_id: Annotated[int, "分类ID"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行设置好友分类。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "category_id": category_id,
        }
        result = await _call_onebot_api("set_friend_category", params)
        return result.get("status") == "ok", result


class SetFriendsCategoryTool(BaseTool):
    """按分类 ID 或名称设置好友分类的 Tool。"""

    name = "set_friends_category"
    description = "按分类 ID 或名称设置好友分类（SnowLuma 扩展）"

    async def execute(
        self,
        uin: Annotated[int, "目标QQ号"],
        category_id: Annotated[int | None, "分类ID"] = None,
        category_name: Annotated[str | None, "分类名称"] = None,
    ) -> tuple[bool, dict[str, Any]]:
        """执行设置好友分类。"""
        params: dict[str, Any] = {"uin": uin}
        if category_id is not None:
            params["categoryId"] = category_id
        if category_name is not None:
            params["categoryName"] = category_name
        result = await _call_onebot_api("set_friends_category", params)
        return result.get("status") == "ok", result


class GetFriendDressTool(BaseTool):
    """获取好友个性装扮的 Tool。

    对应 API: ``_get_friend_dress``（SnowLuma 扩展）。
    获取指定 QQ 号正在使用的个性装扮（挂件/名片/来电/输入状态等）。
    """

    name = "_get_friend_dress"
    description = "获取指定QQ号的个性装扮（挂件/名片/来电/输入状态等）"

    async def execute(
        self,
        user_id: Annotated[int, "目标QQ号"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行获取好友个性装扮。"""
        params: dict[str, Any] = {
            "user_id": user_id,
        }
        result = await _call_onebot_api("_get_friend_dress", params)
        return result.get("status") == "ok", result
