"""请求处理服务。

封装 OneBot v11 请求相关 API 和扩展请求 API，提供统一的请求处理接口。

API 列表 (5):
    - set_friend_add_request: 处理好友添加请求 (OB11标准)
    - set_group_add_request: 处理加群请求 (OB11标准)
    - get_group_system_msg: 获取群系统消息 (go-cqhttp兼容)
    - get_doubt_friends_add_request: 获取可疑好友申请 (扩展)
    - set_doubt_friends_add_request: 处理可疑好友申请 (扩展)
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["RequestService"]


class RequestService(BaseService):
    """请求处理服务。

    封装全部请求处理相关 OneBot API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    name: str = "request_service"
    description: str = "请求处理服务"
    version: str = "1.0.0"

    async def set_friend_add_request(
        self,
        flag: str,
        approve: bool = True,
        remark: str = "",
    ) -> dict[str, Any]:
        """处理好友添加请求。

        对应 OneBot API: ``set_friend_add_request``。

        Args:
            flag: 好友添加请求的 flag。
            approve: 是否同意请求，默认为 True。
            remark: 好友备注，默认为空字符串。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "flag": flag,
            "approve": approve,
        }
        if remark:
            params["remark"] = remark
        return await _call_onebot_api("set_friend_add_request", params)

    async def set_group_add_request(
        self,
        flag: str,
        sub_type: str,
        approve: bool = True,
        reason: str = "",
    ) -> dict[str, Any]:
        """处理加群请求。

        对应 OneBot API: ``set_group_add_request``。

        Args:
            flag: 加群请求的 flag。
            sub_type: 请求子类型（"add" 或 "invite"）。
            approve: 是否同意请求，默认为 True。
            reason: 拒绝理由，默认为空字符串。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "flag": flag,
            "sub_type": sub_type,
            "approve": approve,
        }
        if reason:
            params["reason"] = reason
        return await _call_onebot_api("set_group_add_request", params)

    async def get_group_system_msg(self) -> dict[str, Any]:
        """获取群系统消息。

        对应 go-cqhttp 兼容 API: ``get_group_system_msg``。

        Returns:
            适配器返回的响应字典，包含群系统消息列表。
        """
        return await _call_onebot_api("get_group_system_msg", {})

    async def get_doubt_friends_add_request(
        self,
        count: int = 20,
    ) -> dict[str, Any]:
        """获取可疑好友申请。

        对应扩展 API: ``get_doubt_friends_add_request``。

        Args:
            count: 获取数量，默认为 20。

        Returns:
            适配器返回的响应字典，包含可疑好友申请列表。
        """
        params: dict[str, Any] = {"count": count}
        return await _call_onebot_api("get_doubt_friends_add_request", params)

    async def set_doubt_friends_add_request(
        self,
        flag: str,
        approve: bool = True,
    ) -> dict[str, Any]:
        """处理可疑好友申请。

        对应扩展 API: ``set_doubt_friends_add_request``。

        Args:
            flag: 可疑好友申请的 flag。
            approve: 是否同意请求，默认为 True。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "flag": flag,
            "approve": approve,
        }
        return await _call_onebot_api("set_doubt_friends_add_request", params)