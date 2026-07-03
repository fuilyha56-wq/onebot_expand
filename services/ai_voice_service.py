"""AI语音服务。

封装 NapCat AI 语音 API，提供 AI 语音角色查询、
语音生成、群 AI 语音发送等功能。

API 列表 (3):
    - get_ai_characters: 获取AI语音角色
    - get_ai_record: 生成AI语音
    - send_group_ai_record: 发送群AI语音
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["AiVoiceService"]


class AiVoiceService(BaseService):
    """AI语音服务。

    封装全部 AI 语音 API 调用，提供配置开关检查和统一调用入口。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "ai_voice_service"
    service_description: str = "AI语音服务"
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

    async def get_ai_characters(
        self,
        group_id: int | None = None,
        chat_type: int | None = None,
    ) -> dict[str, Any]:
        """获取AI语音角色。

        对应 NapCat 扩展 API: ``get_ai_characters``。

        Args:
            group_id: 群号，默认为 None。
            chat_type: 聊天类型，默认为 None。

        Returns:
            适配器返回的响应字典，包含 AI 语音角色列表。
        """
        if not self._is_api_enabled("get_ai_characters"):
            return self._disabled_response("get_ai_characters")
        params: dict[str, Any] = {}
        if group_id is not None:
            params["group_id"] = group_id
        if chat_type is not None:
            params["chat_type"] = chat_type
        return await _call_onebot_api("get_ai_characters", params)

    async def get_ai_record(
        self,
        group_id: int,
        character: str,
        text: str,
    ) -> dict[str, Any]:
        """生成AI语音。

        对应 NapCat 扩展 API: ``get_ai_record``。

        Args:
            group_id: 群号。
            character: 语音角色名称。
            text: 语音合成文本内容。

        Returns:
            适配器返回的响应字典，包含生成的语音数据。
        """
        if not self._is_api_enabled("get_ai_record"):
            return self._disabled_response("get_ai_record")
        params: dict[str, Any] = {
            "group_id": group_id,
            "character": character,
            "text": text,
        }
        return await _call_onebot_api("get_ai_record", params)

    async def send_group_ai_record(
        self,
        group_id: int,
        character: str,
        text: str,
    ) -> dict[str, Any]:
        """发送群AI语音。

        对应 NapCat 扩展 API: ``send_group_ai_record``。

        Args:
            group_id: 群号。
            character: 语音角色名称。
            text: 语音合成文本内容。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("send_group_ai_record"):
            return self._disabled_response("send_group_ai_record")
        params: dict[str, Any] = {
            "group_id": group_id,
            "character": character,
            "text": text,
        }
        return await _call_onebot_api("send_group_ai_record", params)