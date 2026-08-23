"""OneBot 入站消息元数据注入契约测试。"""

from __future__ import annotations

import time

import pytest

from ..event_handler import SelfIdInjectHandler
from src.app.plugin_system.types import EventType
from src.kernel.event import EventDecision


@pytest.mark.asyncio
async def test_handler_injects_self_id_before_message_conversion() -> None:
    """处理器应在消息转换前把 self_id 注入 envelope。"""
    assert SelfIdInjectHandler.init_subscribe == [EventType.BEFORE_MESSAGE_RECEIVED]

    handler = SelfIdInjectHandler(plugin=None)
    handler._self_id = "123456"
    handler._self_id_refreshed_at = time.monotonic()
    envelope = {"message_info": {"platform": "qq", "extra": {}}}
    params = {
        "envelope": envelope,
        "adapter_signature": "onebot_adapter:adapter:onebot_adapter",
    }

    decision, updated_params = await handler.execute(
        EventType.BEFORE_MESSAGE_RECEIVED.value,
        params,
    )

    assert decision is EventDecision.SUCCESS
    assert updated_params["envelope"]["message_info"]["extra"]["self_id"] == "123456"