"""用户信息扩展服务。

封装 NapCat 用户信息扩展 API，提供好友管理、资料设置、
头像设置、个性签名、最近联系人、资料点赞等功能。

API 列表 (9):
    - delete_friend: 删除好友
    - set_friend_remark: 设置好友备注
    - get_friends_with_category: 获取分组好友列表
    - get_unidirectional_friend_list: 获取单向好友列表
    - set_qq_profile: 设置QQ资料
    - set_qq_avatar: 设置QQ头像
    - set_self_longnick: 设置个性签名
    - get_recent_contact: 获取最近联系人
    - get_profile_like: 获取资料点赞
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["UserExtService"]


class UserExtService(BaseService):
    """用户信息扩展服务。

    封装全部用户信息扩展 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "user_ext_service"
    service_description: str = "用户信息扩展服务"
    version: str = "1.0.0"

    async def delete_friend(
        self,
        user_id: int,
        block: bool = False,
    ) -> dict[str, Any]:
        """删除好友。

        对应 NapCat 扩展 API: ``delete_friend``。

        Args:
            user_id: 目标用户 QQ 号。
            block: 是否同时拉黑，默认为 False。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "block": block,
        }
        return await _call_onebot_api("delete_friend", params)

    async def set_friend_remark(
        self,
        user_id: int,
        remark: str,
    ) -> dict[str, Any]:
        """设置好友备注。

        对应 NapCat 扩展 API: ``set_friend_remark``。

        Args:
            user_id: 目标用户 QQ 号。
            remark: 备注名。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "remark": remark,
        }
        return await _call_onebot_api("set_friend_remark", params)

    async def get_friends_with_category(self) -> dict[str, Any]:
        """获取分组好友列表。

        对应 NapCat 扩展 API: ``get_friends_with_category``。

        Returns:
            适配器返回的响应字典，包含分组好友列表。
        """
        return await _call_onebot_api("get_friends_with_category", {})

    async def get_unidirectional_friend_list(self) -> dict[str, Any]:
        """获取单向好友列表。

        对应 NapCat 扩展 API: ``get_unidirectional_friend_list``。

        Returns:
            适配器返回的响应字典，包含单向好友列表。
        """
        return await _call_onebot_api("get_unidirectional_friend_list", {})

    async def set_qq_profile(
        self,
        nickname: str = "",
        personal_note: str = "",
    ) -> dict[str, Any]:
        """设置QQ资料。

        对应 NapCat 扩展 API: ``set_qq_profile``。

        Args:
            nickname: 昵称，默认为空字符串（不修改）。
            personal_note: 个人说明，默认为空字符串（不修改）。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {}
        if nickname:
            params["nickname"] = nickname
        if personal_note:
            params["personal_note"] = personal_note
        return await _call_onebot_api("set_qq_profile", params)

    async def set_qq_avatar(self, file: str) -> dict[str, Any]:
        """设置QQ头像。

        对应 NapCat 扩展 API: ``set_qq_avatar``。

        Args:
            file: 头像图片路径或 URL。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"file": file}
        return await _call_onebot_api("set_qq_avatar", params)

    async def set_self_longnick(self, long_nick: str) -> dict[str, Any]:
        """设置个性签名。

        对应 NapCat 扩展 API: ``set_self_longnick``。

        Args:
            long_nick: 个性签名内容。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"long_nick": long_nick}
        return await _call_onebot_api("set_self_longnick", params)

    async def get_recent_contact(self, count: int = 10) -> dict[str, Any]:
        """获取最近联系人。

        对应 NapCat 扩展 API: ``get_recent_contact``。

        Args:
            count: 获取数量，默认为 10。

        Returns:
            适配器返回的响应字典，包含最近联系人列表。
        """
        params: dict[str, Any] = {"count": count}
        return await _call_onebot_api("get_recent_contact", params)

    async def get_profile_like(
        self,
        user_id: int,
        start: int = 0,
        count: int = 10,
    ) -> dict[str, Any]:
        """获取资料点赞。

        对应 NapCat 扩展 API: ``get_profile_like``。

        Args:
            user_id: 目标用户 QQ 号。
            start: 起始位置，默认为 0。
            count: 获取数量，默认为 10。

        Returns:
            适配器返回的响应字典，包含资料点赞信息。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "start": start,
            "count": count,
        }
        return await _call_onebot_api("get_profile_like", params)

    async def GetProfileLikeMe(
        self,
        start: int,
        count: int,
    ) -> dict[str, Any]:
        """获取自身被点赞列表。

        对应 OneBot API: ``get_profile_like_me``。
        """
        params: dict[str, Any] = {
            "start": start,
            "count": count,
        }
        return await _call_onebot_api("get_profile_like_me", params)

    async def GetProfileLikeCount(
        self,
        user_id: int,
    ) -> dict[str, Any]:
        """获取用户点赞总数。

        对应 OneBot API: ``get_profile_like_count``。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
        }
        return await _call_onebot_api("get_profile_like_count", params)

    async def GetQQAvatar(
        self,
        user_id: int,
        group_id: int,
    ) -> dict[str, Any]:
        """获取QQ头像URL。

        对应 OneBot API: ``get_qq_avatar``。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "group_id": group_id,
        }
        return await _call_onebot_api("get_qq_avatar", params)

    async def SetFriendCategory(
        self,
        user_id: int,
        category_id: int,
    ) -> dict[str, Any]:
        """设置好友分类。

        对应 OneBot API: ``set_friend_category``。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "category_id": category_id,
        }
        return await _call_onebot_api("set_friend_category", params)

