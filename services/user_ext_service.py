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

    封装全部用户信息扩展 API 调用，提供配置开关检查和统一调用入口。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "user_ext_service"
    service_description: str = "用户信息扩展服务"
    version: str = "1.0.0"

    def _is_api_enabled(self, api_name: str) -> bool:
        """检查 API 是否在配置中启用。

        1.3.0 起支持别名：传入别名时会先解析为主名再查询配置开关，
        保证主名与别名共用同一开关。

        Args:
            api_name: API 名称（主名或别名，对应配置中 ``enable_<api_name>`` 字段）。

        Returns:
            True 表示启用，False 表示禁用。无配置时默认启用。
        """
        from ..api_defs import resolve_action

        config = self.plugin.config
        if config is None:
            return True
        switches = getattr(config, "api_switches", None)
        if switches is None:
            return True
        primary = resolve_action(api_name) or api_name
        return getattr(switches, f"enable_{primary}", True)

    @staticmethod
    def _disabled_response(api_name: str) -> dict[str, Any]:
        """构造 API 禁用时的标准响应。

        Args:
            api_name: 被禁用的 API 名称。

        Returns:
            包含错误状态和提示信息的字典。
        """
        return {"status": "error", "retcode": -1, "msg": f"API {api_name} 已禁用"}

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
        if not self._is_api_enabled("delete_friend"):
            return self._disabled_response("delete_friend")
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
        if not self._is_api_enabled("set_friend_remark"):
            return self._disabled_response("set_friend_remark")
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
        if not self._is_api_enabled("get_friends_with_category"):
            return self._disabled_response("get_friends_with_category")
        return await _call_onebot_api("get_friends_with_category", {})

    async def get_unidirectional_friend_list(self) -> dict[str, Any]:
        """获取单向好友列表。

        对应 NapCat 扩展 API: ``get_unidirectional_friend_list``。

        Returns:
            适配器返回的响应字典，包含单向好友列表。
        """
        if not self._is_api_enabled("get_unidirectional_friend_list"):
            return self._disabled_response("get_unidirectional_friend_list")
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
        if not self._is_api_enabled("set_qq_profile"):
            return self._disabled_response("set_qq_profile")
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
        if not self._is_api_enabled("set_qq_avatar"):
            return self._disabled_response("set_qq_avatar")
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
        if not self._is_api_enabled("set_self_longnick"):
            return self._disabled_response("set_self_longnick")
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
        if not self._is_api_enabled("get_recent_contact"):
            return self._disabled_response("get_recent_contact")
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
        if not self._is_api_enabled("get_profile_like"):
            return self._disabled_response("get_profile_like")
        params: dict[str, Any] = {
            "user_id": user_id,
            "start": start,
            "count": count,
        }
        return await _call_onebot_api("get_profile_like", params)