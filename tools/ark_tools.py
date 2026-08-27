"""Ark分享 API 的 Tool 组件。

包含 5 个 Ark 分享 Tool，对应 NapCat / SnowLuma Ark 分享 API：
    - share_peer: 分享用户/群Ark卡片
    - send_ark_share: 分享Ark卡片
    - share_group_ex: 分享群Ark卡片
    - send_group_ark_share: 发送群Ark分享
    - send_tuwen_ark: 发送图文Ark卡片（SnowLuma 扩展）

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "SharePeerTool",
    "SendArkShareTool",
    "ShareGroupExTool",
    "SendGroupArkShareTool",
    "SendTuwenArkTool",
]


class SharePeerTool(BaseTool):
    """分享用户/群Ark卡片的 Tool。

    对应 NapCat API: ``share_peer``。
    分享用户或群的 Ark 卡片。
    """

    name = "share_peer"
    description = "分享用户或群的Ark卡片"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号（可选）"] = 0,
        group_id: Annotated[int, "目标群号（可选）"] = 0,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行分享用户/群Ark卡片。"""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if group_id:
            params["group_id"] = group_id
        result = await _call_onebot_api("share_peer", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"分享Ark卡片失败: {result.get('msg', '未知错误')}"


class SendArkShareTool(BaseTool):
    """分享Ark卡片的 Tool。

    对应 NapCat API: ``send_ark_share``。
    发送 Ark 卡片到指定用户或群。
    """

    name = "send_ark_share"
    description = "发送Ark卡片到指定用户或群"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号（可选）"] = 0,
        group_id: Annotated[int, "目标群号（可选）"] = 0,
    ) -> tuple[bool, str]:
        """执行分享Ark卡片。"""
        params: dict[str, Any] = {}
        if user_id:
            params["user_id"] = user_id
        if group_id:
            params["group_id"] = group_id
        result = await _call_onebot_api("send_ark_share", params)
        if result.get("status") == "ok":
            return True, "Ark卡片分享成功"
        return False, f"分享Ark卡片失败: {result.get('msg', '未知错误')}"


class ShareGroupExTool(BaseTool):
    """分享群Ark卡片的 Tool。

    对应 NapCat API: ``share_group_ex``。
    分享群的扩展 Ark 卡片。
    """

    name = "share_group_ex"
    description = "分享群的扩展Ark卡片"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行分享群Ark卡片。"""
        params: dict[str, Any] = {"group_id": group_id}
        result = await _call_onebot_api("share_group_ex", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"分享群Ark卡片失败: {result.get('msg', '未知错误')}"


class SendGroupArkShareTool(BaseTool):
    """发送群Ark分享的 Tool。

    对应 NapCat API: ``send_group_ark_share``。
    向指定群发送 Ark 分享卡片。
    """

    name = "send_group_ark_share"
    description = "向指定群发送Ark分享卡片"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str]:
        """执行发送群Ark分享。"""
        params: dict[str, Any] = {"group_id": group_id}
        result = await _call_onebot_api("send_group_ark_share", params)
        if result.get("status") == "ok":
            return True, f"群 {group_id} Ark分享发送成功"
        return False, f"发送群Ark分享失败: {result.get('msg', '未知错误')}"


class SendTuwenArkTool(BaseTool):
    """发送图文Ark卡片的 Tool（SnowLuma 扩展）。

    对应 SnowLuma API: ``send_tuwen_ark``。
    发送固定图文 ark 模板，返回 null（无法用于撤回/设精华）。
    """

    name = "send_tuwen_ark"
    description = "发送图文Ark卡片（私聊/群聊二选一，SnowLuma扩展）"

    async def execute(
        self,
        title: Annotated[str, "卡片标题"],
        desc: Annotated[str, "卡片描述"],
        jump_url: Annotated[str, "跳转链接"],
        user_id: Annotated[int, "目标用户QQ号（与 group_id 二选一）"] = 0,
        group_id: Annotated[int, "目标群号（与 user_id 二选一）"] = 0,
        summary: Annotated[str, "卡片摘要"] = "[分享]",
        preview_url: Annotated[
            str,
            "预览图 URL，默认为 SnowLuma 内置占位图",
        ] = "https://tangram-1251316161.file.myqcloud.com/files/20210721/e50a8e37e08f29bf1ffc7466e1950690.png",
    ) -> tuple[bool, str]:
        """执行发送图文Ark卡片。"""
        if bool(user_id) == bool(group_id):
            raise ValueError("user_id 与 group_id 必须二选一（恰好提供一个）")
        params: dict[str, Any] = {
            "title": title,
            "desc": desc,
            "summary": summary,
            "preview_url": preview_url,
            "jump_url": jump_url,
        }
        if group_id:
            params["group_id"] = group_id
        else:
            params["user_id"] = user_id
        result = await _call_onebot_api("send_tuwen_ark", params)
        if result.get("status") == "ok":
            return True, "图文Ark卡片发送成功"
        return False, f"发送图文Ark卡片失败: {result.get('msg', '未知错误')}"