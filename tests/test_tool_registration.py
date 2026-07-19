"""onebot_expand 工具动态注册测试。"""

from __future__ import annotations

from types import SimpleNamespace

from onebot_expand.config import OnebotExpandConfig
from onebot_expand.plugin import OnebotExpandPlugin
from onebot_expand.services import ALL_SERVICES
from onebot_expand.tools import (
    ALL_TOOLS,
    SendGroupMsgTool,
    SendPrivateMsgTool,
    _is_tool_independently_enabled,
    _is_tool_master_switch_on,
)


def test_missing_config_registers_services_only() -> None:
    """配置缺失时不应暴露任何工具。"""
    plugin = OnebotExpandPlugin(config=None)

    assert plugin.get_components() == ALL_SERVICES
    assert not _is_tool_master_switch_on(plugin)


def test_master_switch_off_registers_services_only() -> None:
    """总开关关闭时独立开关不应触发工具注册。"""
    config = OnebotExpandConfig()
    config.api_switches.enable_send_group_msg = True
    plugin = OnebotExpandPlugin(config=config)

    assert plugin.get_components() == ALL_SERVICES


def test_only_explicitly_enabled_tools_are_registered() -> None:
    """总开关开启后只注册独立开关为真的工具。"""
    config = OnebotExpandConfig()
    config.api_switches.enable_all_tools = True
    config.api_switches.enable_send_group_msg = True
    config.api_switches.enable_send_private_msg = True
    plugin = OnebotExpandPlugin(config=config)

    components = plugin.get_components()
    registered_tools = [component for component in components if component in ALL_TOOLS]

    assert registered_tools == [SendGroupMsgTool, SendPrivateMsgTool]
    assert components[-len(ALL_SERVICES):] == ALL_SERVICES


def test_wrapper_defaults_missing_switch_to_disabled() -> None:
    """包装器遇到缺失独立开关时应严格默认关闭。"""
    plugin = SimpleNamespace(
        config=SimpleNamespace(
            api_switches=SimpleNamespace(enable_all_tools=True),
        )
    )

    assert _is_tool_master_switch_on(plugin)
    assert not _is_tool_independently_enabled(plugin, "unknown_action")
