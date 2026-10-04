"""消息 ID 类型别名测试（原样透传铁律版）。

历史上的 normalize_message_id / normalize_message_ids / build_text_message
参数改写辅助函数已按 SKILL.md §11.1 原样透传铁律移除；
本文件验证类型别名仍可用，且改写函数确实不存在。
"""

from __future__ import annotations

import pytest

from .. import message_utils
from ..message_utils import MessageId


def test_message_id_type_alias_accepts_int_and_str() -> None:
    """MessageId 类型别名应同时容纳 int 与 str（运行时不做转换）。"""
    a: MessageId = 12345
    b: MessageId = "platform-message-id"
    assert a == 12345
    assert b == "platform-message-id"


def test_param_transform_helpers_are_removed() -> None:
    """参数改写辅助函数必须已被移除（原样透传铁律）。"""
    assert not hasattr(message_utils, "normalize_message_id")
    assert not hasattr(message_utils, "normalize_message_ids")
    assert not hasattr(message_utils, "build_text_message")


def test_forward_node_normalizer_is_removed() -> None:
    """合并转发节点改写函数必须已被移除（参数原样透传）。"""
    from ..tools import message_tools

    assert not hasattr(message_tools, "_normalize_forward_messages")
    assert not hasattr(message_tools, "_extract_message_id")
    assert not hasattr(message_tools, "ForwardNode")


def test_api_client_does_not_rewrite_params() -> None:
    """api_client 不得再引用参数改写函数。"""
    import inspect

    from .. import api_client

    source = inspect.getsource(api_client)
    assert "normalize_message_ids" not in source
    assert "snowluma_compat" not in source  # 兼容性标记不得用于调用期拦截
