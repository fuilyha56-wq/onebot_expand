"""表情/收藏扩展服务。

封装 NapCat 表情/收藏扩展 API，提供收藏表情管理、
表情回应查询等功能。

API 列表 (5):
    - fetch_custom_face: 获取收藏表情
    - add_custom_face: 添加收藏表情
    - delete_custom_face: 删除收藏表情
    - fetch_emoji_like: 获取表情回应分页
    - get_emoji_likes: 获取表情回应用户
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["EmojiExtService"]


class EmojiExtService(BaseService):
    """表情/收藏扩展服务。

    封装全部表情/收藏扩展 API 调用，提供配置开关检查和统一调用入口。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "emoji_ext_service"
    service_description: str = "表情/收藏扩展服务"
    version: str = "1.0.0"

    def _is_api_enabled(self, api_name: str) -> bool:
        """检查 API 是否在配置中启用。

        1.3.0 起支持别名：传入别名时会先解析为主名再查询配置开关。
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
        """构造 API 禁用时的标准响应。"""
        return {"status": "error", "retcode": -1, "msg": f"API {api_name} 已禁用"}

    async def fetch_custom_face(self, count: int = 48) -> dict[str, Any]:
        """获取收藏表情。

        对应 NapCat 扩展 API: ``fetch_custom_face``。

        Args:
            count: 获取数量，默认为 48。

        Returns:
            适配器返回的响应字典，包含收藏表情列表。
        """
        if not self._is_api_enabled("fetch_custom_face"):
            return self._disabled_response("fetch_custom_face")
        params: dict[str, Any] = {"count": count}
        return await _call_onebot_api("fetch_custom_face", params)

    async def add_custom_face(self, file: str) -> dict[str, Any]:
        """添加收藏表情。

        对应 NapCat 扩展 API: ``add_custom_face``。

        Args:
            file: 表情图片路径或 URL。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("add_custom_face"):
            return self._disabled_response("add_custom_face")
        params: dict[str, Any] = {"file": file}
        return await _call_onebot_api("add_custom_face", params)

    async def delete_custom_face(self, emoji_id: str) -> dict[str, Any]:
        """删除收藏表情。

        对应 NapCat 扩展 API: ``delete_custom_face``。

        Args:
            emoji_id: 表情 ID。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("delete_custom_face"):
            return self._disabled_response("delete_custom_face")
        params: dict[str, Any] = {"emoji_id": emoji_id}
        return await _call_onebot_api("delete_custom_face", params)

    async def fetch_emoji_like(
        self,
        message_id: int,
        emoji_id: int = 0,
        count: int = 30,
    ) -> dict[str, Any]:
        """获取表情回应分页。

        对应 NapCat 扩展 API: ``fetch_emoji_like``。

        Args:
            message_id: 消息 ID。
            emoji_id: 表情 ID，默认为 0。
            count: 获取数量，默认为 30。

        Returns:
            适配器返回的响应字典，包含表情回应分页数据。
        """
        if not self._is_api_enabled("fetch_emoji_like"):
            return self._disabled_response("fetch_emoji_like")
        params: dict[str, Any] = {
            "message_id": message_id,
            "emoji_id": emoji_id,
            "count": count,
        }
        return await _call_onebot_api("fetch_emoji_like", params)

    async def get_emoji_likes(
        self,
        message_id: int,
        emoji_id: int,
    ) -> dict[str, Any]:
        """获取表情回应用户。

        对应 NapCat 扩展 API: ``get_emoji_likes``。

        Args:
            message_id: 消息 ID。
            emoji_id: 表情 ID。

        Returns:
            适配器返回的响应字典，包含表情回应用户列表。
        """
        if not self._is_api_enabled("get_emoji_likes"):
            return self._disabled_response("get_emoji_likes")
        params: dict[str, Any] = {
            "message_id": message_id,
            "emoji_id": emoji_id,
        }
        return await _call_onebot_api("get_emoji_likes", params)