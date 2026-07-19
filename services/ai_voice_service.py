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

    封装全部 AI 语音 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    name: str = "ai_voice_service"
    description: str = "AI语音服务"
    version: str = "1.0.0"

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
        params: dict[str, Any] = {
            "group_id": group_id,
            "character": character,
            "text": text,
        }
        return await _call_onebot_api("send_group_ai_record", params)