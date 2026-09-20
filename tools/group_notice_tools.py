"""群公告 API 的 Tool 组件。

包含 3 个群公告 Tool：
    - _send_group_notice: 发送群公告
    - _get_group_notice: 获取群公告
    - _del_group_notice: 删除群公告

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "SendGroupNoticeTool",
    "GetGroupNoticeTool",
    "DelGroupNoticeTool",
]


class SendGroupNoticeTool(BaseTool):
    """发送群公告的 Tool。

    对应 API: ``_send_group_notice``。
    向指定群发送群公告，可附带图片。
    """

    name = "_send_group_notice"
    description = "发送群公告"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        content: Annotated[str, "公告内容"],
        image: Annotated[str, "公告图片（可选，图片路径或URL）"] = "",
    ) -> tuple[bool, dict[str, Any]]:
        """执行发送群公告。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "content": content,
        }
        if image:
            params["image"] = image
        result = await _call_onebot_api("_send_group_notice", params)
        return result.get("status") == "ok", result


class GetGroupNoticeTool(BaseTool):
    """获取群公告的 Tool。

    对应 API: ``_get_group_notice``。
    获取指定群的群公告列表。
    """

    name = "_get_group_notice"
    description = "获取群公告列表"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群公告。"""
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        result = await _call_onebot_api("_get_group_notice", params)
        return result.get("status") == "ok", result


class DelGroupNoticeTool(BaseTool):
    """删除群公告的 Tool。

    对应 API: ``_del_group_notice``。
    删除指定群中的群公告。
    """

    name = "_del_group_notice"
    description = "删除群公告"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        notice_id: Annotated[str, "公告ID"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行删除群公告。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "notice_id": notice_id,
        }
        result = await _call_onebot_api("_del_group_notice", params)
        return result.get("status") == "ok", result
