"""群公告管理服务。

封装群公告相关 API，提供统一的群公告操作接口。

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

    封装全部群公告 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "group_notice_service"
    service_description: str = "群公告管理服务"
    version: str = "1.0.0"

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
        params: dict[str, Any] = {
            "group_id": group_id,
            "notice_id": notice_id,
        }
        return await _call_onebot_api("_del_group_notice", params)