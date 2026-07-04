"""群管理扩展服务。

封装群管理扩展相关 API，提供统一的群管理扩展操作接口。

API 列表 (12):
    - set_group_portrait: 设置群头像
    - set_group_remark: 设置群备注
    - set_group_add_option: 设置加群选项
    - set_group_search: 允许群被搜索
    - set_group_robot_add_option: 设置群机器人加群选项
    - set_group_kick_members: 批量踢出群成员
    - get_group_shut_list: 获取群禁言列表
    - get_group_ignored_notifies: 获取被过滤的入群请求
    - get_group_ignore_add_request: 获取被忽略的入群请求
    - get_group_info_ex: 获取群信息扩展
    - set_group_sign: 群签到
    - get_group_signed_list: 获取群今日打卡列表
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["GroupExtService"]


class GroupExtService(BaseService):
    """群管理扩展服务。

    封装全部群管理扩展 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "group_ext_service"
    service_description: str = "群管理扩展服务"
    version: str = "1.0.0"

    async def set_group_portrait(
        self,
        group_id: int,
        file: str,
    ) -> dict[str, Any]:
        """设置群头像。

        对应 API: ``set_group_portrait``。

        Args:
            group_id: 群号。
            file: 图片路径或 URL。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "file": file,
        }
        return await _call_onebot_api("set_group_portrait", params)

    async def set_group_remark(
        self,
        group_id: int,
        remark: str,
    ) -> dict[str, Any]:
        """设置群备注。

        对应 API: ``set_group_remark``。

        Args:
            group_id: 群号。
            remark: 群备注内容。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "remark": remark,
        }
        return await _call_onebot_api("set_group_remark", params)

    async def set_group_add_option(
        self,
        group_id: int,
        add_type: int,
    ) -> dict[str, Any]:
        """设置加群选项。

        对应 API: ``set_group_add_option``。

        Args:
            group_id: 群号。
            add_type: 加群方式（0:允许任何人, 1:需要验证, 2:不允许任何人）。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "add_type": add_type,
        }
        return await _call_onebot_api("set_group_add_option", params)

    async def set_group_search(
        self,
        group_id: int,
    ) -> dict[str, Any]:
        """允许群被搜索。

        对应 API: ``set_group_search``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        return await _call_onebot_api("set_group_search", params)

    async def set_group_robot_add_option(
        self,
        group_id: int,
        robot_member_switch: bool = True,
    ) -> dict[str, Any]:
        """设置群机器人加群选项。

        对应 API: ``set_group_robot_add_option``。

        Args:
            group_id: 群号。
            robot_member_switch: 是否允许机器人加群，默认为 True。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "robot_member_switch": robot_member_switch,
        }
        return await _call_onebot_api("set_group_robot_add_option", params)

    async def set_group_kick_members(
        self,
        group_id: int,
        user_id_list: list[int],
        reject_add_request: bool = False,
    ) -> dict[str, Any]:
        """批量踢出群成员。

        对应 API: ``set_group_kick_members``。

        Args:
            group_id: 群号。
            user_id_list: 要踢出的成员 QQ 号列表。
            reject_add_request: 是否拒绝这些人再次加群请求，默认为 False。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id_list": user_id_list,
            "reject_add_request": reject_add_request,
        }
        return await _call_onebot_api("set_group_kick_members", params)

    async def get_group_shut_list(
        self,
        group_id: int,
    ) -> dict[str, Any]:
        """获取群禁言列表。

        对应 API: ``get_group_shut_list``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典，包含禁言成员列表。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        return await _call_onebot_api("get_group_shut_list", params)

    async def get_group_ignored_notifies(
        self,
    ) -> dict[str, Any]:
        """获取被过滤的入群请求。

        对应 API: ``get_group_ignored_notifies``。

        Returns:
            适配器返回的响应字典，包含被过滤的入群请求列表。
        """
        params: dict[str, Any] = {}
        return await _call_onebot_api("get_group_ignored_notifies", params)

    async def get_group_ignore_add_request(
        self,
    ) -> dict[str, Any]:
        """获取被忽略的入群请求。

        对应 API: ``get_group_ignore_add_request``。

        Returns:
            适配器返回的响应字典，包含被忽略的入群请求列表。
        """
        params: dict[str, Any] = {}
        return await _call_onebot_api("get_group_ignore_add_request", params)

    async def get_group_info_ex(
        self,
        group_id: int,
    ) -> dict[str, Any]:
        """获取群信息扩展。

        对应 API: ``get_group_info_ex``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典，包含群扩展信息。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        return await _call_onebot_api("get_group_info_ex", params)

    async def set_group_sign(
        self,
        group_id: int,
    ) -> dict[str, Any]:
        """群签到。

        对应 API: ``set_group_sign``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        return await _call_onebot_api("set_group_sign", params)

    async def get_group_signed_list(self, group_id: int) -> dict[str, Any]:
        """获取群今日打卡列表。

        对应 API: ``get_group_signed_list``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典，包含群今日已签到成员列表。
        """
        params: dict[str, Any] = {"group_id": group_id}
        return await _call_onebot_api("get_group_signed_list", params)