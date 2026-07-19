"""OneBot 消息 ID 与消息段辅助函数。"""

from __future__ import annotations

from typing import Any, TypeAlias

MessageId: TypeAlias = int | str


def normalize_message_id(message_id: MessageId) -> MessageId:
    """将主程序保存的平台消息 ID 规范化为 OneBot 可接受的值。"""
    if isinstance(message_id, bool):
        raise ValueError("message_id 不能是布尔值")
    if isinstance(message_id, int):
        return message_id

    normalized = message_id.strip()
    if not normalized:
        raise ValueError("message_id 不能为空")
    try:
        return int(normalized)
    except ValueError:
        return normalized


def build_text_message(
    text: str,
    reply_to_message_id: MessageId | None = None,
) -> list[dict[str, Any]]:
    """构造文本消息，并可在首段添加 OneBot 引用回复。"""
    message: list[dict[str, Any]] = []
    if reply_to_message_id is not None:
        message.append(
            {
                "type": "reply",
                "data": {"id": normalize_message_id(reply_to_message_id)},
            }
        )
    message.append({"type": "text", "data": {"text": text}})
    return message


def normalize_message_ids(value: Any) -> Any:
    """递归规范化 OneBot 参数中的所有 ``message_id`` 字段。"""
    if isinstance(value, dict):
        return {
            key: (
                normalize_message_id(item)
                if key == "message_id" and isinstance(item, int | str)
                else normalize_message_ids(item)
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [normalize_message_ids(item) for item in value]
    return value