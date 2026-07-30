"""onebot_expand 插件入口。

OneBot v11 + NapCat 扩展 API 的完整封装插件。
通过 onebot_adapter 的 WebSocket 连接调用全部 206 个 OneBot API。

架构采用 Service + Tool 分离设计：
    - Service 层（23 个）：始终可用，供其他插件程序化调用，通过 api_client 调协议端
    - Tool 层（206 个）：供 LLM 直接调用，默认全部关闭，可按需启用

Tool 层当前已从组件注册中移除，仅保留代码与开关保护逻辑。
恢复 Tool 注册只需在 get_components() 末尾加回 ``+ ALL_TOOLS``。
"""

from __future__ import annotations

from src.app.plugin_system.api.log_api import get_logger
from src.app.plugin_system.base import BasePlugin, register_plugin

from .api_defs import resolve_action
from .config import OnebotExpandConfig
from .services import ALL_SERVICES

logger = get_logger("onebot_expand")


@register_plugin
class OnebotExpandPlugin(BasePlugin):
    """OneBot Expand 插件。

    扩展 onebot_adapter 的能力，提供全部 OneBot v11 + NapCat 扩展 API
    的 Service 组件封装。Tool 层代码保留但默认不注册。

    Attributes:
        plugin_name: 插件名称
        plugin_description: 插件描述
        plugin_version: 插件版本
        configs: 配置类列表
        dependencies: 依赖的其他组件列表
    """

    plugin_name: str = "onebot_expand"
    plugin_description: str = (
        "OneBot v11 + NapCat 扩展 API 完整封装，"
        "提供 23 个 Service 组件（Tool 层已分离，可按需启用）"
    )
    plugin_version: str = "1.0.9"

    configs: list[type] = [OnebotExpandConfig]
    dependencies: list[str] = []

    def _get_enabled_tools(self) -> list[type]:
        """返回配置中明确启用、需要注册的工具类。

        Tool 层当前已从组件注册中移除，本方法保留供未来恢复 Tool 时使用。
        恢复方式：在 get_components() 末尾加回 ``+ self._get_enabled_tools()``。
        """
        from .tools import ALL_TOOLS

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
        """返回需要注册的组件列表。

        当前仅返回 Service 组件（Tool 层已分离）。
        恢复 Tool 注册：将返回值改为 ``self._get_enabled_tools() + ALL_SERVICES``。

        Returns:
            全部 Service 类
        """
        return ALL_SERVICES

    async def on_plugin_loaded(self) -> None:
        """插件加载完成后的初始化。"""
        logger.info(
            f"onebot_expand 插件已加载: 注册 {len(ALL_SERVICES)} 个服务"
            "（Tool 层已分离，未注册）"
        )

    async def on_plugin_unloaded(self) -> None:
        """插件卸载前的清理。"""
        logger.info("onebot_expand 插件已卸载")
