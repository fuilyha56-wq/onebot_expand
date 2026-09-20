"""戳一拍 API 的 Tool 组件。

包含 2 个戳一拍 Tool，对应 NapCat 戳一拍 API：
    - friend_poke: 好友戳一戳
    - group_poke: 群戳一戳

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "FriendPokeTool",
    "GroupPokeTool",
]


class FriendPokeTool(BaseTool):
    """好友戳一戳的 Tool。

    对应 NapCat API: ``friend_poke``。
    向指定好友发送戳一戳。
    """

    name = "friend_poke"
    description = "向指定好友发送戳一戳"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        target_id: Annotated[int, "被戳目标QQ号（可选）"] = 0,
    ) -> tuple[bool, dict[str, Any]]:
        """执行好友戳一戳。"""
        params: dict[str, Any] = {"user_id": user_id}
        if target_id:
            params["target_id"] = target_id
        result = await _call_onebot_api("friend_poke", params)
        return result.get("status") == "ok", result


class GroupPokeTool(BaseTool):
    """群戳一戳的 Tool。

    对应 NapCat API: ``group_poke``。
    在指定群中向指定成员发送戳一戳。
    """

    name = "group_poke"
    description = "在指定群中向指定成员发送戳一戳"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        user_id: Annotated[int, "目标成员QQ号"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行群戳一戳。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "user_id": user_id,
        }
        result = await _call_onebot_api("group_poke", params)
        return result.get("status") == "ok", result
