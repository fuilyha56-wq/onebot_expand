"""群公告管理服务。

封装群公告相关 API，提供统一的群公告操作接口。
所有方法在执行前会检查对应的配置开关，禁用时返回错误提示。

API 列表 (3):
    - send_group_notice: 发送群公告
    - get_group_notice: 获取群公告
    - del_group_notice: 删除群公告
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["GroupNoticeService"]


class GroupNoticeService(BaseService):
    """群公告管理服务。

    封装全部群公告 API 调用，提供配置开关检查和统一调用入口。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "group_notice_service"
    service_description: str = "群公告管理服务"
    version: str = "1.0.0"

    def _is_api_enabled(self, api_name: str) -> bool:
        """检查 API 是否在配置中启用。

        1.3.0 起支持别名：传入别名时会先解析为主名再查询配置开关，
        保证主名与别名共用同一开关。

        Args:
            api_name: API 名称（主名或别名，对应配置中 ``enable_<api_name>`` 字段）。

        Returns:
            True 表示启用，False 表示禁用。无配置时默认启用。
        """
        from ..api_defs import resolve_action

        config = self.plugin.config
        if config is None:
            return True
        switches = getattr(config, "api_switches", None)
        if switches is None:
            return True
        primary = resolve_action(api_name) or api_name
        return getattr(switches, f"enable_{primary}", True)

    @staticmethod
    def _disabled_response(api_name: str) -> dict[str, Any]:
        """构造 API 禁用时的标准响应。

        Args:
            api_name: 被禁用的 API 名称。

        Returns:
            包含错误状态和提示信息的字典。
        """
        return {"status": "error", "retcode": -1, "msg": f"API {api_name} 已禁用"}

    async def send_group_notice(
        self,
        group_id: int,
        content: str,
        image: str = "",
    ) -> dict[str, Any]:
        """发送群公告。

        对应 API: ``_send_group_notice``。

        Args:
            group_id: 群号。
            content: 公告内容。
            image: 公告图片路径或 URL，可选。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("_send_group_notice"):
            return self._disabled_response("_send_group_notice")
        params: dict[str, Any] = {
            "group_id": group_id,
            "content": content,
        }
        if image:
            params["image"] = image
        return await _call_onebot_api("_send_group_notice", params)

    async def get_group_notice(
        self,
        group_id: int,
    ) -> dict[str, Any]:
        """获取群公告。

        对应 API: ``_get_group_notice``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典，包含群公告列表。
        """
        if not self._is_api_enabled("_get_group_notice"):
            return self._disabled_response("_get_group_notice")
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        return await _call_onebot_api("_get_group_notice", params)

    async def del_group_notice(
        self,
        group_id: int,
        notice_id: str,
    ) -> dict[str, Any]:
        """删除群公告。

        对应 API: ``_del_group_notice``。

        Args:
            group_id: 群号。
            notice_id: 公告 ID。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("_del_group_notice"):
            return self._disabled_response("_del_group_notice")
        params: dict[str, Any] = {
            "group_id": group_id,
            "notice_id": notice_id,
        }
        return await _call_onebot_api("_del_group_notice", params)