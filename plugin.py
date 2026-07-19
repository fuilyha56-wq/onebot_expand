"""onebot_expand 插件入口。

OneBot v11 + NapCat 扩展 API 的完整封装插件。
通过 onebot_adapter 的 WebSocket 连接调用全部 173 个 OneBot API。
所有功能以 Tool + Service 双层组件形式提供。

引入别名机制：5 组纯别名（get_rkey/set_group_sign/send_packet/
ocr_image/fetch_ptt_text）合并为同一开关与同一 handler；同 handler 数组
别名不再作为独立 action 注册。共 173 主名 + 7 别名 action 串。
"""

from __future__ import annotations

from src.app.plugin_system.api.log_api import get_logger
from src.app.plugin_system.base import BasePlugin, register_plugin

from .api_defs import resolve_action
from .config import OnebotExpandConfig
from .services import ALL_SERVICES
from .tools import ALL_TOOLS

logger = get_logger("onebot_expand")


@register_plugin
class OnebotExpandPlugin(BasePlugin):
    """OneBot Expand 插件。

    扩展 onebot_adapter 的能力，提供全部 OneBot v11 + NapCat 扩展 API
    的 Tool 和 Service 组件封装。

    Attributes:
        plugin_name: 插件名称
        plugin_description: 插件描述
        plugin_version: 插件版本
        configs: 配置类列表
        dependent_components: 依赖的其他组件列表
    """

    plugin_name: str = "onebot_expand"
    plugin_description: str = (
        "OneBot v11 + NapCat 扩展 API 完整封装，"
        "提供 185 个 Tool 组件和 23 个 Service 组件，"
        "含 13 个别名机制"
    )
    plugin_version: str = "1.0.6"

    configs: list[type] = [OnebotExpandConfig]
    dependent_components: list[str] = []

    def _get_enabled_tools(self) -> list[type]:
        """返回配置中明确启用、需要注册的工具类。"""
        config = self.config
        if not isinstance(config, OnebotExpandConfig):
            return []

        switches = config.api_switches
        if not switches.enable_all_tools:
            return []

        enabled_tools: list[type] = []
        for tool_cls in ALL_TOOLS:
            tool_name = str(getattr(tool_cls, "tool_name", "") or "")
            if not tool_name:
                continue
            primary_action = resolve_action(tool_name) or tool_name
            if bool(getattr(switches, f"enable_{primary_action}", False)):
                enabled_tools.append(tool_cls)
        return enabled_tools

    def get_components(self) -> list[type]:
        """返回已启用的工具和始终可用的服务组件。

        Returns:
            配置中启用的工具类与全部服务类
        """
        return self._get_enabled_tools() + ALL_SERVICES

    async def on_plugin_loaded(self) -> None:
        """插件加载完成后的初始化。"""
        enabled_tools = self._get_enabled_tools()
        logger.info(
            f"onebot_expand 插件已加载: 注册 {len(enabled_tools)} 个工具, "
            f"{len(ALL_SERVICES)} 个服务"
        )

    async def on_plugin_unloaded(self) -> None:
        """插件卸载前的清理。"""
        logger.info("onebot_expand 插件已卸载")
