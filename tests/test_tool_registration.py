"""onebot_expand 工具动态注册测试。"""

from __future__ import annotations

from types import SimpleNamespace

from onebot_expand.config import OnebotExpandConfig
from onebot_expand.event_handler import SelfIdInjectHandler
from onebot_expand.plugin import OnebotExpandPlugin
from onebot_expand.services import ALL_SERVICES
from onebot_expand.tools import (
    SendGroupMsgTool,
    SendOnlineFileTool,
    SendPrivateMsgTool,
    UploadFileStreamTool,
    _is_tool_independently_enabled,
    _is_tool_master_switch_on,
)

ALWAYS_ON_COMPONENTS = ALL_SERVICES + [SelfIdInjectHandler]


def test_missing_config_registers_services_only() -> None:
    """配置缺失时不应暴露任何工具。"""
    plugin = OnebotExpandPlugin(config=None)

    assert plugin.get_components() == ALWAYS_ON_COMPONENTS
    assert not _is_tool_master_switch_on(plugin)


def test_master_switch_off_registers_services_only() -> None:
    """总开关关闭时独立开关不应触发工具注册。"""
    config = OnebotExpandConfig()
    config.api_switches.enable_send_group_msg = True
    plugin = OnebotExpandPlugin(config=config)

    assert plugin.get_components() == ALWAYS_ON_COMPONENTS


def test_only_explicitly_enabled_tools_are_registered() -> None:
    """总开关开启后只注册独立开关为真的工具。"""
    config = OnebotExpandConfig()
    config.api_switches.enable_all_tools = True
    config.api_switches.enable_send_group_msg = True
    config.api_switches.enable_send_private_msg = True
    plugin = OnebotExpandPlugin(config=config)

    assert plugin.get_components() == ALWAYS_ON_COMPONENTS + [
        SendGroupMsgTool,
        SendPrivateMsgTool,
    ]

    enabled_tools = plugin._get_enabled_tools()
    assert enabled_tools == [SendGroupMsgTool, SendPrivateMsgTool]


def test_snowluma_backend_filters_incompatible_tools() -> None:
    """SnowLuma 后端不应向模型注册协议端不支持的 Tool。"""
    config = OnebotExpandConfig()
    config.protocol.backend = "snowluma"
    config.api_switches.enable_all_tools = True
    config.api_switches.enable_send_online_file = True
    config.api_switches.enable_upload_file_stream = True
    plugin = OnebotExpandPlugin(config=config)

    enabled_tools = plugin._get_enabled_tools()

    assert UploadFileStreamTool in enabled_tools
    assert SendOnlineFileTool not in enabled_tools


def test_wrapper_defaults_missing_switch_to_disabled() -> None:
    """包装器遇到缺失独立开关时应严格默认关闭。"""
    plugin = SimpleNamespace(
        config=SimpleNamespace(
            api_switches=SimpleNamespace(enable_all_tools=True),
        )
    )

    assert _is_tool_master_switch_on(plugin)
    assert not _is_tool_independently_enabled(plugin, "unknown_action")
