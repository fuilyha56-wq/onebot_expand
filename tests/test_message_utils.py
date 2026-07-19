"""消息 ID 与引用消息段辅助函数测试。"""

from __future__ import annotations

import pytest

from message_utils import build_text_message, normalize_message_id, normalize_message_ids
from tools.message_tools import _normalize_forward_messages


def test_normalize_message_id_accepts_core_message_table_values() -> None:
    """主程序消息表中的字符串 ID 应转换为 OneBot 可接受的值。"""
    assert normalize_message_id(" 12345 ") == 12345
    assert normalize_message_id("platform-message-id") == "platform-message-id"
    assert normalize_message_id(12345) == 12345


@pytest.mark.parametrize("message_id", ["", "   ", True])
def test_normalize_message_id_rejects_invalid_values(message_id: int | str) -> None:
    """空 ID 与布尔值不应被发送到 OneBot。"""
    with pytest.raises(ValueError):
        normalize_message_id(message_id)


def test_normalize_message_ids_handles_nested_message_payloads() -> None:
    """合并转发等嵌套消息中的 message_id 也应被规范化。"""
    params = {
        "message_id": "100",
        "messages": [{"data": {"message_id": "nested-id"}}],
    }

    assert normalize_message_ids(params) == {
        "message_id": 100,
        "messages": [{"data": {"message_id": "nested-id"}}],
    }
    assert params["message_id"] == "100"


def test_build_text_message_prepends_reply_segment() -> None:
    """引用回复段必须位于文本段之前。"""
    assert build_text_message("hello", "12345") == [
        {"type": "reply", "data": {"id": 12345}},
        {"type": "text", "data": {"text": "hello"}},
    ]


def test_normalize_forward_messages_wraps_short_nodes() -> None:
    """合并转发的简写节点应转换为 OneBot 标准 node 段。"""
    assert _normalize_forward_messages(
        [{"uin": "10001", "nick": "Alice", "content": "你好"}]
    ) == [
        {
            "type": "node",
            "data": {"uin": "10001", "name": "Alice", "content": "你好"},
        }
    ]


def test_normalize_forward_messages_rejects_incomplete_short_node() -> None:
    """不完整的合并转发简写节点应在调用 OneBot 前被拒绝。"""
    with pytest.raises(ValueError, match="uin、nick（或 name）和 content"):
        _normalize_forward_messages([{"uin": "10001", "content": "你好"}])
