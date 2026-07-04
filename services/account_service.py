"""账号与群组信息查询服务。

封装 OneBot v11 账号信息查询 API 和 NapCat 账号扩展 API，
提供统一的信息查询接口。

API 列表 (10):
    - get_login_info: 获取 Bot 登录信息
    - get_stranger_info: 获取陌生人信息
    - get_friend_list: 获取好友列表
    - get_group_list: 获取群列表
    - get_group_member_list: 获取群成员列表
    - get_group_member_info: 获取群成员详情
    - get_group_info: 获取群信息
    - get_group_detail_info: 获取群详细信息（NapCat 扩展）
    - get_group_honor_info: 获取群荣誉信息
    - get_robot_uin_range: 获取机器人 UIN 范围（NapCat 扩展）
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["AccountService"]


class AccountService(BaseService):
    """账号与群组信息查询服务。

    封装全部账号信息查询 OneBot API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "account_service"
    service_description: str = "账号与群组信息查询服务"
    version: str = "1.0.0"

    async def get_login_info(self) -> dict[str, Any]:
        """获取 Bot 登录信息。

        对应 OneBot API: ``get_login_info``。

        Returns:
            适配器返回的响应字典，包含登录号的 user_id 和 nickname。
        """
        return await _call_onebot_api("get_login_info", {})

    async def get_stranger_info(
        self,
        user_id: int,
        no_cache: bool = False,
    ) -> dict[str, Any]:
        """获取陌生人信息。

        对应 OneBot API: ``get_stranger_info``。

        Args:
            user_id: 目标用户 QQ 号。
            no_cache: 是否不使用缓存，默认为 False。

        Returns:
            适配器返回的响应字典，包含陌生人信息。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "no_cache": no_cache,
        }
        return await _call_onebot_api("get_stranger_info", params)

    async def get_friend_list(self) -> dict[str, Any]:
        """获取好友列表。

        对应 OneBot API: ``get_friend_list``。

        Returns:
            适配器返回的响应字典，包含好友列表。
        """
        return await _call_onebot_api("get_friend_list", {})

    async def get_group_list(self) -> dict[str, Any]:
        """获取群列表。

        对应 OneBot API: ``get_group_list``。

        Returns:
            适配器返回的响应字典，包含群列表。
        """
        return await _call_onebot_api("get_group_list", {})

    async def get_group_member_list(
        self,
        group_id: int,
        no_cache: bool = False,
    ) -> dict[str, Any]:
        """获取群成员列表。

        对应 OneBot API: ``get_group_member_list``。

        Args:
            group_id: 群号。
            no_cache: 是否不使用缓存，默认为 False。

        Returns:
            适配器返回的响应字典，包含群成员列表。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "no_cache": no_cache,
        }
        return await _call_onebot_api("get_group_member_list", params)

    async def get_group_member_info(
        self,
        group_id: int,
        user_id: int,
        no_cache: bool = False,
    ) -> dict[str, Any]:
        """获取群成员详情。

        对应 OneBot API: ``get_group_member_info``。

        Args:
            group_id: 群号。
            user_id: 目标用户 QQ 号。
            no_cache: 是否不使用缓存，默认为 False。

        Returns:
            适配器返回的响应字典，包含群成员详情。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
            "no_cache": no_cache,
        }
        return await _call_onebot_api("get_group_member_info", params)

    async def get_group_info(
        self,
        group_id: int,
        no_cache: bool = False,
    ) -> dict[str, Any]:
        """获取群信息。

        对应 OneBot API: ``get_group_info``。

        Args:
            group_id: 群号。
            no_cache: 是否不使用缓存，默认为 False。

        Returns:
            适配器返回的响应字典，包含群信息。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "no_cache": no_cache,
        }
        return await _call_onebot_api("get_group_info", params)

    async def get_group_detail_info(self, group_id: int) -> dict[str, Any]:
        """获取群详细信息（NapCat 扩展）。

        对应 NapCat 扩展 API: ``get_group_detail_info``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典，包含群详细信息。
        """
        params: dict[str, Any] = {"group_id": group_id}
        return await _call_onebot_api("get_group_detail_info", params)

    async def get_group_honor_info(
        self,
        group_id: int,
        honor_type: str = "all",
    ) -> dict[str, Any]:
        """获取群荣誉信息。

        对应 OneBot API: ``get_group_honor_info``。

        Args:
            group_id: 群号。
            honor_type: 荣誉类型，可选值:
                - "talkative": 龙王
                - "performer": 群聊之火
                - "legend": 群聊炽焰
                - "strongest_newbie": 冒尖小春笋
                - "emotionless": 快乐之源
                - "all": 全部（默认）

        Returns:
            适配器返回的响应字典，包含群荣誉信息。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "type": honor_type,
        }
        return await _call_onebot_api("get_group_honor_info", params)

    async def get_robot_uin_range(self) -> dict[str, Any]:
        """获取机器人 UIN 范围（NapCat 扩展）。

        对应 NapCat 扩展 API: ``get_robot_uin_range``。

        Returns:
            适配器返回的响应字典，包含机器人 UIN 范围列表。
        """
        return await _call_onebot_api("get_robot_uin_range", {})
