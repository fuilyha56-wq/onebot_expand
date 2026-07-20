"""在线状态 API 的 Tool 组件。

包含 4 个在线状态 Tool，对应 NapCat 在线状态 API：
    - set_online_status: 设置在线状态
    - set_diy_online_status: 设置自定义在线状态
    - set_input_status: 设置输入状态
    - nc_get_user_status: 获取用户状态

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "SetOnlineStatusTool",
    "SetDiyOnlineStatusTool",
    "SetInputStatusTool",
    "NcGetUserStatusTool",
]


class SetOnlineStatusTool(BaseTool):
    """设置在线状态的 Tool。

    对应 NapCat API: ``set_online_status``。
    设置当前 Bot 的在线状态。
    """

    tool_name = "set_online_status"
    tool_description = "设置当前Bot的在线状态"

    async def execute(
        self,
        status: Annotated[int, "在线状态值"],
        ext_status: Annotated[int, "扩展状态值"] = 0,
        battery_status: Annotated[int, "电池状态百分比"] = 0,
    ) -> tuple[bool, str]:
        """执行设置在线状态。"""
        params: dict[str, Any] = {
            "status": status,
            "ext_status": ext_status,
            "battery_status": battery_status,
        }
        result = await _call_onebot_api("set_online_status", params)
        if result.get("status") == "ok":
            return True, f"在线状态已设置为 {status}"
        return False, f"设置在线状态失败: {result.get('msg', '未知错误')}"


class SetDiyOnlineStatusTool(BaseTool):
    """设置自定义在线状态的 Tool。

    对应 NapCat API: ``set_diy_online_status``。
    设置当前 Bot 的自定义在线状态（含表情和文字）。
    """

    tool_name = "set_diy_online_status"
    tool_description = "设置当前Bot的自定义在线状态（含表情和文字）"

    async def execute(
        self,
        face_id: Annotated[int, "表情ID"],
        face_type: Annotated[int, "表情类型"] = 1,
        wording: Annotated[str, "状态文字"] = "",
    ) -> tuple[bool, str]:
        """执行设置自定义在线状态。"""
        params: dict[str, Any] = {
            "face_id": face_id,
            "face_type": face_type,
        }
        if wording:
            params["wording"] = wording
        result = await _call_onebot_api("set_diy_online_status", params)
        if result.get("status") == "ok":
            return True, "自定义在线状态设置成功"
        return False, f"设置自定义在线状态失败: {result.get('msg', '未知错误')}"


class SetInputStatusTool(BaseTool):
    """设置输入状态的 Tool。

    对应 NapCat API: ``set_input_status``。
    向指定用户发送输入状态通知。
    """

    tool_name = "set_input_status"
    tool_description = "向指定用户发送输入状态通知"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        event_type: Annotated[int, "输入状态事件类型（1=正在输入, 0=取消输入）"],
    ) -> tuple[bool, str]:
        """执行设置输入状态。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "event_type": event_type,
        }
        result = await _call_onebot_api("set_input_status", params)
        if result.get("status") == "ok":
            return True, f"已向用户 {user_id} 发送输入状态"
        return False, f"设置输入状态失败: {result.get('msg', '未知错误')}"


class NcGetUserStatusTool(BaseTool):
    """获取用户状态的 Tool。

    对应 NapCat API: ``nc_get_user_status``。
    获取指定用户的在线状态信息。
    """

    tool_name = "nc_get_user_status"
    tool_description = "获取指定用户的在线状态信息"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取用户状态。"""
        params: dict[str, Any] = {"user_id": user_id}
        result = await _call_onebot_api("nc_get_user_status", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取用户状态失败: {result.get('msg', '未知错误')}"