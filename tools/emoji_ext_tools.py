"""表情/收藏扩展 API 的 Tool 组件。

包含 5 个表情/收藏扩展 Tool，对应 NapCat 表情/收藏扩展 API：
    - fetch_custom_face: 获取收藏表情
    - add_custom_face: 添加收藏表情
    - delete_custom_face: 删除收藏表情
    - fetch_emoji_like: 获取表情回应分页
    - get_emoji_likes: 获取表情回应用户

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "FetchCustomFaceTool",
    "AddCustomFaceTool",
    "DeleteCustomFaceTool",
    "FetchEmojiLikeTool",
    "GetEmojiLikesTool",
]


class FetchCustomFaceTool(BaseTool):
    """获取收藏表情的 Tool。

    对应 NapCat API: ``fetch_custom_face``。
    获取当前 Bot 的收藏表情列表。
    """

    tool_name = "fetch_custom_face"
    tool_description = "获取当前Bot的收藏表情列表"

    async def execute(
        self,
        count: Annotated[int, "获取数量"] = 48,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取收藏表情。"""
        params: dict[str, Any] = {"count": count}
        result = await _call_onebot_api("fetch_custom_face", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取收藏表情失败: {result.get('msg', '未知错误')}"


class AddCustomFaceTool(BaseTool):
    """添加收藏表情的 Tool。

    对应 NapCat API: ``add_custom_face``。
    添加表情到收藏列表。
    """

    tool_name = "add_custom_face"
    tool_description = "添加表情到收藏列表"

    async def execute(
        self,
        file: Annotated[str, "表情图片路径或URL"],
    ) -> tuple[bool, str]:
        """执行添加收藏表情。"""
        params: dict[str, Any] = {"file": file}
        result = await _call_onebot_api("add_custom_face", params)
        if result.get("status") == "ok":
            return True, "收藏表情添加成功"
        return False, f"添加收藏表情失败: {result.get('msg', '未知错误')}"


class DeleteCustomFaceTool(BaseTool):
    """删除收藏表情的 Tool。

    对应 NapCat API: ``delete_custom_face``。
    从收藏列表中删除指定表情。
    """

    tool_name = "delete_custom_face"
    tool_description = "从收藏列表中删除指定表情"

    async def execute(
        self,
        emoji_id: Annotated[str, "表情ID"],
    ) -> tuple[bool, str]:
        """执行删除收藏表情。"""
        params: dict[str, Any] = {"emoji_id": emoji_id}
        result = await _call_onebot_api("delete_custom_face", params)
        if result.get("status") == "ok":
            return True, f"已删除收藏表情 {emoji_id}"
        return False, f"删除收藏表情失败: {result.get('msg', '未知错误')}"


class FetchEmojiLikeTool(BaseTool):
    """获取表情回应分页的 Tool。

    对应 NapCat API: ``fetch_emoji_like``。
    获取指定消息的表情回应分页数据。
    """

    tool_name = "fetch_emoji_like"
    tool_description = "获取指定消息的表情回应分页数据"

    async def execute(
        self,
        message_id: Annotated[int, "目标消息ID"],
        emoji_id: Annotated[int, "表情ID"] = 0,
        count: Annotated[int, "获取数量"] = 30,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取表情回应分页。"""
        params: dict[str, Any] = {
            "message_id": message_id,
            "emoji_id": emoji_id,
            "count": count,
        }
        result = await _call_onebot_api("fetch_emoji_like", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取表情回应分页失败: {result.get('msg', '未知错误')}"


class GetEmojiLikesTool(BaseTool):
    """获取表情回应用户的 Tool。

    对应 NapCat API: ``get_emoji_likes``。
    获取指定消息上某表情的回应用户列表。
    """

    tool_name = "get_emoji_likes"
    tool_description = "获取指定消息上某表情的回应用户列表"

    async def execute(
        self,
        message_id: Annotated[int, "目标消息ID"],
        emoji_id: Annotated[int, "表情ID"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取表情回应用户。"""
        params: dict[str, Any] = {
            "message_id": message_id,
            "emoji_id": emoji_id,
        }
        result = await _call_onebot_api("get_emoji_likes", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取表情回应用户失败: {result.get('msg', '未知错误')}"