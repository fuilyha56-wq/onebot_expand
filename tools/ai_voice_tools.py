"""AI语音 API 的 Tool 组件。

包含 3 个 AI 语音 Tool，对应 NapCat AI 语音 API：
    - get_ai_characters: 获取AI语音角色
    - get_ai_record: 生成AI语音
    - send_group_ai_record: 发送群AI语音

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "GetAiCharactersTool",
    "GetAiRecordTool",
    "SendGroupAiRecordTool",
]


class GetAiCharactersTool(BaseTool):
    """获取AI语音角色的 Tool。

    对应 NapCat API: ``get_ai_characters``。
    获取可用的 AI 语音角色列表。
    """

    name = "get_ai_characters"
    description = "获取可用的AI语音角色列表"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号（可选）"] = 0,
        chat_type: Annotated[int, "聊天类型（可选）"] = 0,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取AI语音角色。"""
        params: dict[str, Any] = {}
        if group_id:
            params["group_id"] = group_id
        if chat_type:
            params["chat_type"] = chat_type
        result = await _call_onebot_api("get_ai_characters", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取AI语音角色失败: {result.get('msg', '未知错误')}"


class GetAiRecordTool(BaseTool):
    """生成AI语音的 Tool。

    对应 NapCat API: ``get_ai_record``。
    使用指定 AI 角色生成语音。
    """

    name = "get_ai_record"
    description = "使用指定AI角色生成语音"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        character: Annotated[str, "语音角色名称"],
        text: Annotated[str, "语音合成文本内容"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行生成AI语音。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "character": character,
            "text": text,
        }
        result = await _call_onebot_api("get_ai_record", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"生成AI语音失败: {result.get('msg', '未知错误')}"


class SendGroupAiRecordTool(BaseTool):
    """发送群AI语音的 Tool。

    对应 NapCat API: ``send_group_ai_record``。
    使用指定 AI 角色生成语音并发送到群聊。
    """

    name = "send_group_ai_record"
    description = "使用指定AI角色生成语音并发送到群聊"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        character: Annotated[str, "语音角色名称"],
        text: Annotated[str, "语音合成文本内容"],
    ) -> tuple[bool, str]:
        """执行发送群AI语音。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "character": character,
            "text": text,
        }
        result = await _call_onebot_api("send_group_ai_record", params)
        if result.get("status") == "ok":
            return True, f"AI语音已发送到群 {group_id}"
        return False, f"发送群AI语音失败: {result.get('msg', '未知错误')}"