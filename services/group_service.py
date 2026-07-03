"""群管理操作服务。

封装 OneBot v11 群操作相关 API，提供统一的群管理接口。
所有方法在执行前会检查对应的配置开关，禁用时返回错误提示。

API 列表 (10):
    - kick: 踢出群成员
    - ban: 禁言群成员
    - anonymous_ban: 禁言匿名群成员
    - whole_ban: 全体禁言
    - set_admin: 设置/取消管理员
    - set_anonymous: 开启/关闭匿名聊天
    - set_card: 设置群名片
    - set_group_name: 设置群名
    - leave: 退出群聊
    - set_special_title: 设置专属头衔
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["GroupService"]


class GroupService(BaseService):
    """群管理操作服务。

    封装全部群操作 OneBot API 调用，提供配置开关检查和统一调用入口。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "group_service"
    service_description: str = "群管理操作服务"
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

    async def kick(
        self,
        group_id: int,
        user_id: int,
        reject_add_request: bool = False,
    ) -> dict[str, Any]:
        """踢出群成员。

        对应 OneBot API: ``set_group_kick``。

        Args:
            group_id: 群号。
            user_id: 被踢成员 QQ 号。
            reject_add_request: 是否拒绝此人再次加群请求，默认为 False。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("set_group_kick"):
            return self._disabled_response("set_group_kick")
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
            "reject_add_request": reject_add_request,
        }
        return await _call_onebot_api("set_group_kick", params)

    async def ban(
        self,
        group_id: int,
        user_id: int,
        duration: int = 1800,
    ) -> dict[str, Any]:
        """禁言群成员。

        对应 OneBot API: ``set_group_ban``。

        Args:
            group_id: 群号。
            user_id: 被禁言成员 QQ 号。
            duration: 禁言时长（秒），0 表示解除禁言，默认为 1800（30 分钟）。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("set_group_ban"):
            return self._disabled_response("set_group_ban")
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
            "duration": duration,
        }
        return await _call_onebot_api("set_group_ban", params)

    async def anonymous_ban(
        self,
        group_id: int,
        anonymous: dict[str, Any] | None = None,
        anonymous_flag: str | None = None,
        duration: int = 1800,
    ) -> dict[str, Any]:
        """禁言匿名群成员。

        对应 OneBot API: ``set_group_anonymous_ban``。
        需提供 anonymous 对象或 anonymous_flag 之一。

        Args:
            group_id: 群号。
            anonymous: 匿名用户对象（从消息事件中获取），可选。
            anonymous_flag: 匿名用户 flag（从消息事件中获取），可选。
            duration: 禁言时长（秒），默认为 1800（30 分钟）。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("set_group_anonymous_ban"):
            return self._disabled_response("set_group_anonymous_ban")
        params: dict[str, Any] = {
            "group_id": group_id,
            "duration": duration,
        }
        if anonymous is not None:
            params["anonymous"] = anonymous
        if anonymous_flag is not None:
            params["anonymous_flag"] = anonymous_flag
        return await _call_onebot_api("set_group_anonymous_ban", params)

    async def whole_ban(
        self,
        group_id: int,
        enable: bool = True,
    ) -> dict[str, Any]:
        """全体禁言。

        对应 OneBot API: ``set_group_whole_ban``。

        Args:
            group_id: 群号。
            enable: 是否开启全体禁言，默认为 True。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("set_group_whole_ban"):
            return self._disabled_response("set_group_whole_ban")
        params: dict[str, Any] = {
            "group_id": group_id,
            "enable": enable,
        }
        return await _call_onebot_api("set_group_whole_ban", params)

    async def set_admin(
        self,
        group_id: int,
        user_id: int,
        enable: bool = True,
    ) -> dict[str, Any]:
        """设置/取消群管理员。

        对应 OneBot API: ``set_group_admin``。

        Args:
            group_id: 群号。
            user_id: 目标用户 QQ 号。
            enable: True 设置为管理员，False 取消管理员，默认为 True。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("set_group_admin"):
            return self._disabled_response("set_group_admin")
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
            "enable": enable,
        }
        return await _call_onebot_api("set_group_admin", params)

    async def set_anonymous(
        self,
        group_id: int,
        enable: bool = True,
    ) -> dict[str, Any]:
        """开启/关闭匿名聊天。

        对应 OneBot API: ``set_group_anonymous``。

        Args:
            group_id: 群号。
            enable: True 开启匿名聊天，False 关闭，默认为 True。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("set_group_anonymous"):
            return self._disabled_response("set_group_anonymous")
        params: dict[str, Any] = {
            "group_id": group_id,
            "enable": enable,
        }
        return await _call_onebot_api("set_group_anonymous", params)

    async def set_card(
        self,
        group_id: int,
        user_id: int,
        card: str = "",
    ) -> dict[str, Any]:
        """设置群名片。

        对应 OneBot API: ``set_group_card``。

        Args:
            group_id: 群号。
            user_id: 目标用户 QQ 号。
            card: 群名片内容，空字符串表示删除名片，默认为空。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("set_group_card"):
            return self._disabled_response("set_group_card")
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
            "card": card,
        }
        return await _call_onebot_api("set_group_card", params)

    async def set_group_name(
        self,
        group_id: int,
        group_name: str,
    ) -> dict[str, Any]:
        """设置群名。

        对应 OneBot API: ``set_group_name``。

        Args:
            group_id: 群号。
            group_name: 新的群名称。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("set_group_name"):
            return self._disabled_response("set_group_name")
        params: dict[str, Any] = {
            "group_id": group_id,
            "group_name": group_name,
        }
        return await _call_onebot_api("set_group_name", params)

    async def leave(
        self,
        group_id: int,
        is_dismiss: bool = False,
    ) -> dict[str, Any]:
        """退出群聊。

        对应 OneBot API: ``set_group_leave``。

        Args:
            group_id: 群号。
            is_dismiss: 是否解散群聊（仅群主可操作），默认为 False。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("set_group_leave"):
            return self._disabled_response("set_group_leave")
        params: dict[str, Any] = {
            "group_id": group_id,
            "is_dismiss": is_dismiss,
        }
        return await _call_onebot_api("set_group_leave", params)

    async def set_special_title(
        self,
        group_id: int,
        user_id: int,
        special_title: str = "",
        duration: int = -1,
    ) -> dict[str, Any]:
        """设置专属头衔。

        对应 OneBot API: ``set_group_special_title``。

        Args:
            group_id: 群号。
            user_id: 目标用户 QQ 号。
            special_title: 专属头衔内容，空字符串表示删除头衔，默认为空。
            duration: 专属头衔有效期（秒），-1 表示永久，默认为 -1。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("set_group_special_title"):
            return self._disabled_response("set_group_special_title")
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
            "special_title": special_title,
            "duration": duration,
        }
        return await _call_onebot_api("set_group_special_title", params)
