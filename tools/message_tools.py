"""消息相关 API 的 Tool 组件。

包含 18 个消息操作 Tool，对应 OneBot v11 标准消息 API 和 NapCat 消息扩展 API：
    - send_group_msg: 发送群聊消息
    - send_private_msg: 发送私聊消息
    - delete_msg: 撤回消息
    - get_msg: 获取消息详情
    - get_forward_msg: 获取合并转发消息内容
    - send_like: 发送名片点赞
    - send_poke: 发送戳一戳（NapCat 扩展）
    - send_forward_msg: 发送合并转发消息（NapCat 扩展）
    - send_group_forward_msg: 发送群合并转发消息（go-cqhttp兼容）
    - send_private_forward_msg: 发送私聊合并转发消息（go-cqhttp兼容）
    - get_group_msg_history: 获取群消息历史（go-cqhttp兼容）
    - get_friend_msg_history: 获取好友消息历史（go-cqhttp兼容）
    - forward_friend_single_msg: 转发单条消息给好友（扩展）
    - forward_group_single_msg: 转发单条消息到群（扩展）
    - mark_msg_as_read: 标记消息已读（go-cqhttp兼容）
    - mark_group_msg_as_read: 标记群消息已读（扩展）
    - mark_private_msg_as_read: 标记私聊消息已读（扩展）
    - _mark_all_as_read: 标记全部已读（扩展）

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [

    "SendGroupMsgTool",
    "SendPrivateMsgTool",
    "SendMsgTool",
    "DeleteMsgTool",
    "GetMsgTool",
    "GetForwardMsgTool",
    "SendLikeTool",
    "SendPokeTool",
    "SendForwardMsgTool",
    "SendGroupForwardMsgTool",
    "SendPrivateForwardMsgTool",
    "GetGroupMsgHistoryTool",
    "GetFriendMsgHistoryTool",
    "ForwardFriendSingleMsgTool",
    "ForwardGroupSingleMsgTool",
    "MarkMsgAsReadTool",
    "MarkGroupMsgAsReadTool",
    "MarkPrivateMsgAsReadTool",
    "MarkAllAsReadTool",
    "UploadForwardMsgTool",
]


def _build_text_message(text: str) -> list[dict[str, Any]]:
    """将纯文本构造成 OneBot 消息段列表。

    Args:
        text: 纯文本消息内容。

    Returns:
        OneBot 消息段列表，格式为 ``[{"type": "text", "data": {"text": ...}}]``。
    """
    return [{"type": "text", "data": {"text": text}}]


def _extract_message_id(result: dict[str, Any]) -> str:
    """从 API 响应中提取消息 ID。

    Args:
        result: OneBot API 响应字典。

    Returns:
        消息 ID 字符串，未找到时返回空字符串。
    """
    data = result.get("data")
    if isinstance(data, dict):
        msg_id = data.get("message_id")
        if msg_id is not None:
            return str(msg_id)
    return ""



class SendGroupMsgTool(BaseTool):
    """发送群聊消息的 Tool。

    对应 OneBot API: ``send_group_msg``。
    """

    tool_name = "send_group_msg"
    tool_description = "向指定QQ群发送消息"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        message: Annotated[str, "消息内容文本"],
    ) -> tuple[bool, str]:
        """执行发送群消息。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "message": _build_text_message(message),
        }
        result = await _call_onebot_api("send_group_msg", params)
        if result.get("status") == "ok":
            msg_id = _extract_message_id(result)
            return (
                True,
                f"群消息发送成功，message_id={msg_id}" if msg_id else "群消息发送成功",
            )
        return False, f"群消息发送失败: {result.get('msg', '未知错误')}"


class SendPrivateMsgTool(BaseTool):
    """发送私聊消息的 Tool。

    对应 OneBot API: ``send_private_msg``。
    """

    tool_name = "send_private_msg"
    tool_description = "向指定用户发送私聊消息"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        message: Annotated[str, "消息内容文本"],
    ) -> tuple[bool, str]:
        """执行发送私聊消息。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "message": _build_text_message(message),
        }
        result = await _call_onebot_api("send_private_msg", params)
        if result.get("status") == "ok":
            msg_id = _extract_message_id(result)
            return (
                True,
                f"私聊消息发送成功，message_id={msg_id}"
                if msg_id
                else "私聊消息发送成功",
            )
        return False, f"私聊消息发送失败: {result.get('msg', '未知错误')}"


class DeleteMsgTool(BaseTool):
    """撤回消息的 Tool。

    对应 OneBot API: ``delete_msg``。
    """

    tool_name = "delete_msg"
    tool_description = "撤回指定消息"

    async def execute(
        self,
        message_id: Annotated[int, "要撤回的消息ID"],
    ) -> tuple[bool, str]:
        """执行撤回消息。"""
        params: dict[str, Any] = {"message_id": message_id}
        result = await _call_onebot_api("delete_msg", params)
        if result.get("status") == "ok":
            return True, "消息撤回成功"
        return False, f"消息撤回失败: {result.get('msg', '未知错误')}"


class GetMsgTool(BaseTool):
    """获取消息详情的 Tool。

    对应 OneBot API: ``get_msg``。
    返回消息的元信息和内容。
    """

    tool_name = "get_msg"
    tool_description = "获取指定消息的详情信息"

    async def execute(
        self,
        message_id: Annotated[int, "消息ID"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取消息详情。"""
        params: dict[str, Any] = {"message_id": message_id}
        result = await _call_onebot_api("get_msg", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取消息失败: {result.get('msg', '未知错误')}"


class GetForwardMsgTool(BaseTool):
    """获取合并转发消息内容的 Tool。

    对应 OneBot API: ``get_forward_msg``。
    根据合并转发消息的 ID 获取其内容。
    """

    tool_name = "get_forward_msg"
    tool_description = "获取合并转发消息的内容"

    async def execute(
        self,
        id: Annotated[str, "合并转发消息的ID（res_id）"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取合并转发消息内容。"""
        params: dict[str, Any] = {"id": id}
        result = await _call_onebot_api("get_forward_msg", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取合并转发消息失败: {result.get('msg', '未知错误')}"


class SendLikeTool(BaseTool):
    """发送名片点赞的 Tool。

    对应 OneBot API: ``send_like``。
    对指定用户发送名片点赞，每天次数有限。
    """

    tool_name = "send_like"
    tool_description = "对指定用户发送名片点赞"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        times: Annotated[int, "点赞次数（1-10）"] = 1,
    ) -> tuple[bool, str]:
        """执行发送名片点赞。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "times": times,
        }
        result = await _call_onebot_api("send_like", params)
        if result.get("status") == "ok":
            return True, f"名片点赞成功，点赞 {times} 次"
        return False, f"名片点赞失败: {result.get('msg', '未知错误')}"


class SendPokeTool(BaseTool):
    """发送戳一戳的 Tool（NapCat 扩展）。

    对应 NapCat API: ``send_poke``。
    可对群内成员或私聊用户发送戳一戳。
    """

    tool_name = "send_poke"
    tool_description = "发送戳一戳（NapCat扩展），可对群成员或私聊用户发送"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        group_id: Annotated[int, "目标群号（0表示私聊戳一戳）"] = 0,
    ) -> tuple[bool, str]:
        """执行发送戳一戳。"""
        params: dict[str, Any] = {"user_id": user_id}
        if group_id:
            params["group_id"] = group_id

        result = await _call_onebot_api("send_poke", params)
        if result.get("status") == "ok":
            target = (
                f"群 {group_id} 中的用户 {user_id}" if group_id else f"用户 {user_id}"
            )
            return True, f"戳一戳发送成功，目标: {target}"
        return False, f"戳一戳发送失败: {result.get('msg', '未知错误')}"


class SendForwardMsgTool(BaseTool):
    """发送合并转发消息的 Tool（NapCat 扩展）。

    对应 NapCat API: ``send_forward_msg``。
    发送合并转发消息，可指定群聊或私聊目标。
    messages 参数为自定义消息段列表，每条消息需包含 uin、nick、content 等字段。
    """

    tool_name = "send_forward_msg"
    tool_description = "发送合并转发消息（NapCat扩展），支持自定义多条消息内容"

    async def execute(
        self,
        messages: Annotated[
            list[dict[str, Any]], "合并转发消息段列表，每条包含 uin/nick/content"
        ],
        group_id: Annotated[int, "目标群号（0表示私聊）"] = 0,
        user_id: Annotated[int, "目标用户QQ号（私聊时必填）"] = 0,
    ) -> tuple[bool, str]:
        """执行发送合并转发消息。"""
        params: dict[str, Any] = {"messages": messages}
        if group_id:
            params["group_id"] = group_id
        if user_id:
            params["user_id"] = user_id

        result = await _call_onebot_api("send_forward_msg", params)
        if result.get("status") == "ok":
            msg_id = _extract_message_id(result)
            return (
                True,
                f"合并转发消息发送成功，message_id={msg_id}"
                if msg_id
                else "合并转发消息发送成功",
            )
        return False, f"合并转发消息发送失败: {result.get('msg', '未知错误')}"


class SendGroupForwardMsgTool(BaseTool):
    """发送群合并转发消息的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``send_group_forward_msg``。
    向指定群发送合并转发消息，messages 为自定义消息节点列表。
    """

    tool_name = "send_group_forward_msg"
    tool_description = "发送群合并转发消息（go-cqhttp兼容）"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        messages: Annotated[
            list[dict[str, Any]], "合并转发消息段列表，每条包含 uin/nick/content"
        ],
    ) -> tuple[bool, str]:
        """执行发送群合并转发消息。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "messages": messages,
        }
        result = await _call_onebot_api("send_group_forward_msg", params)
        if result.get("status") == "ok":
            msg_id = _extract_message_id(result)
            return (
                True,
                f"群合并转发消息发送成功，message_id={msg_id}"
                if msg_id
                else "群合并转发消息发送成功",
            )
        return False, f"群合并转发消息发送失败: {result.get('msg', '未知错误')}"


class SendPrivateForwardMsgTool(BaseTool):
    """发送私聊合并转发消息的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``send_private_forward_msg``。
    向指定用户发送合并转发消息，messages 为自定义消息节点列表。
    """

    tool_name = "send_private_forward_msg"
    tool_description = "发送私聊合并转发消息（go-cqhttp兼容）"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        messages: Annotated[
            list[dict[str, Any]], "合并转发消息段列表，每条包含 uin/nick/content"
        ],
    ) -> tuple[bool, str]:
        """执行发送私聊合并转发消息。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "messages": messages,
        }
        result = await _call_onebot_api("send_private_forward_msg", params)
        if result.get("status") == "ok":
            msg_id = _extract_message_id(result)
            return (
                True,
                f"私聊合并转发消息发送成功，message_id={msg_id}"
                if msg_id
                else "私聊合并转发消息发送成功",
            )
        return False, f"私聊合并转发消息发送失败: {result.get('msg', '未知错误')}"


class GetGroupMsgHistoryTool(BaseTool):
    """获取群消息历史的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``get_group_msg_history``。
    获取指定群的消息历史记录。
    """

    tool_name = "get_group_msg_history"
    tool_description = "获取群消息历史记录（go-cqhttp兼容）"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        message_seq: Annotated[int, "起始消息序号（可选，0表示从最新开始）"] = 0,
        count: Annotated[int, "获取消息数量（默认20）"] = 20,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群消息历史。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "count": count,
        }
        if message_seq:
            params["message_seq"] = message_seq

        result = await _call_onebot_api("get_group_msg_history", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群消息历史失败: {result.get('msg', '未知错误')}"


class GetFriendMsgHistoryTool(BaseTool):
    """获取好友消息历史的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``get_friend_msg_history``。
    获取指定好友的消息历史记录。
    """

    tool_name = "get_friend_msg_history"
    tool_description = "获取好友消息历史记录（go-cqhttp兼容）"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        message_seq: Annotated[int, "起始消息序号（可选，0表示从最新开始）"] = 0,
        count: Annotated[int, "获取消息数量（默认20）"] = 20,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取好友消息历史。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "count": count,
        }
        if message_seq:
            params["message_seq"] = message_seq

        result = await _call_onebot_api("get_friend_msg_history", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取好友消息历史失败: {result.get('msg', '未知错误')}"


class ForwardFriendSingleMsgTool(BaseTool):
    """转发单条消息给好友的 Tool（扩展）。

    对应扩展 API: ``forward_friend_single_msg``。
    将指定消息转发给好友。
    """

    tool_name = "forward_friend_single_msg"
    tool_description = "转发单条消息给好友（扩展）"

    async def execute(
        self,
        message_id: Annotated[int, "要转发的消息ID"],
        user_id: Annotated[int, "目标用户QQ号"],
    ) -> tuple[bool, str]:
        """执行转发单条消息给好友。"""
        params: dict[str, Any] = {
            "message_id": message_id,
            "user_id": user_id,
        }
        result = await _call_onebot_api("forward_friend_single_msg", params)
        if result.get("status") == "ok":
            return True, f"消息已转发给好友 {user_id}"
        return False, f"转发消息给好友失败: {result.get('msg', '未知错误')}"


class ForwardGroupSingleMsgTool(BaseTool):
    """转发单条消息到群的 Tool（扩展）。

    对应扩展 API: ``forward_group_single_msg``。
    将指定消息转发到群。
    """

    tool_name = "forward_group_single_msg"
    tool_description = "转发单条消息到群（扩展）"

    async def execute(
        self,
        message_id: Annotated[int, "要转发的消息ID"],
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str]:
        """执行转发单条消息到群。"""
        params: dict[str, Any] = {
            "message_id": message_id,
            "group_id": group_id,
        }
        result = await _call_onebot_api("forward_group_single_msg", params)
        if result.get("status") == "ok":
            return True, f"消息已转发到群 {group_id}"
        return False, f"转发消息到群失败: {result.get('msg', '未知错误')}"


class MarkMsgAsReadTool(BaseTool):
    """标记消息已读的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``mark_msg_as_read``。
    标记指定消息为已读。
    """

    tool_name = "mark_msg_as_read"
    tool_description = "标记指定消息为已读（go-cqhttp兼容）"

    async def execute(
        self,
        message_id: Annotated[int, "要标记已读的消息ID"],
        target_id: Annotated[int, "目标ID（可选，群号或用户QQ号）"] = 0,
    ) -> tuple[bool, str]:
        """执行标记消息已读。"""
        params: dict[str, Any] = {"message_id": message_id}
        if target_id:
            params["target_id"] = target_id

        result = await _call_onebot_api("mark_msg_as_read", params)
        if result.get("status") == "ok":
            return True, f"消息 {message_id} 已标记为已读"
        return False, f"标记消息已读失败: {result.get('msg', '未知错误')}"


class MarkGroupMsgAsReadTool(BaseTool):
    """标记群消息已读的 Tool（扩展）。

    对应扩展 API: ``mark_group_msg_as_read``。
    标记指定群的消息为已读。
    """

    tool_name = "mark_group_msg_as_read"
    tool_description = "标记群消息已读（扩展）"

    async def execute(
        self,
        message_id: Annotated[int, "要标记已读的消息ID"],
        group_id: Annotated[int, "目标群号（可选，0表示当前群）"] = 0,
    ) -> tuple[bool, str]:
        """执行标记群消息已读。"""
        params: dict[str, Any] = {"message_id": message_id}
        if group_id:
            params["group_id"] = group_id

        result = await _call_onebot_api("mark_group_msg_as_read", params)
        if result.get("status") == "ok":
            target = f"群 {group_id}" if group_id else "当前群"
            return True, f"{target} 的消息 {message_id} 已标记为已读"
        return False, f"标记群消息已读失败: {result.get('msg', '未知错误')}"


class MarkPrivateMsgAsReadTool(BaseTool):
    """标记私聊消息已读的 Tool（扩展）。

    对应扩展 API: ``mark_private_msg_as_read``。
    标记指定私聊的消息为已读。
    """

    tool_name = "mark_private_msg_as_read"
    tool_description = "标记私聊消息已读（扩展）"

    async def execute(
        self,
        message_id: Annotated[int, "要标记已读的消息ID"],
        user_id: Annotated[int, "目标用户QQ号（可选，0表示当前私聊）"] = 0,
    ) -> tuple[bool, str]:
        """执行标记私聊消息已读。"""
        params: dict[str, Any] = {"message_id": message_id}
        if user_id:
            params["user_id"] = user_id

        result = await _call_onebot_api("mark_private_msg_as_read", params)
        if result.get("status") == "ok":
            target = f"用户 {user_id}" if user_id else "当前私聊"
            return True, f"{target} 的消息 {message_id} 已标记为已读"
        return False, f"标记私聊消息已读失败: {result.get('msg', '未知错误')}"


class MarkAllAsReadTool(BaseTool):
    """标记全部已读的 Tool（扩展）。

    对应扩展 API: ``_mark_all_as_read``。
    标记所有消息为已读。
    """

    tool_name = "_mark_all_as_read"
    tool_description = "标记全部消息为已读（扩展）"

    async def execute(
        self,
    ) -> tuple[bool, str]:
        """执行标记全部已读。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("_mark_all_as_read", params)
        if result.get("status") == "ok":
            return True, "已标记全部消息为已读"
        return False, f"标记全部已读失败: {result.get('msg', '未知错误')}"


class SendMsgTool(BaseTool):
    """通用发消息 Tool（按 message_type 或 user_id/group_id 自动路由）。

    对应 OneBot API: ``send_msg``。
    """

    tool_name = "send_msg"
    tool_description = "发送消息（通用，按 message_type 自动路由群聊或私聊）"

    async def execute(
        self,
        message: Annotated[str, "消息内容文本"],
        message_type: Annotated[str, "消息类型 private 或 group"] = "",
        user_id: Annotated[int, "目标用户QQ号（私聊时）"] = 0,
        group_id: Annotated[int, "目标群号（群聊时）"] = 0,
    ) -> tuple[bool, str]:
        """执行发送消息。"""
        params: dict[str, Any] = {
            "message": _build_text_message(message),
        }
        if message_type:
            params["message_type"] = message_type
        if user_id:
            params["user_id"] = user_id
        if group_id:
            params["group_id"] = group_id
        result = await _call_onebot_api("send_msg", params)
        if result.get("status") == "ok":
            msg_id = _extract_message_id(result)
            return (
                True,
                f"消息发送成功，message_id={msg_id}" if msg_id else "消息发送成功",
            )
        return False, f"消息发送失败: {result.get('msg', '未知错误')}"


class UploadForwardMsgTool(BaseTool):
    """上传合并转发消息 Tool（返回 res_id）。

    对应扩展 API: ``upload_forward_msg``。
    """

    tool_name = "upload_forward_msg"
    tool_description = "上传合并转发消息，返回 res_id（扩展，SnowLuma 支持）"

    async def execute(
        self,
        messages: Annotated[str, "合并转发消息 JSON 字符串"],
        group_id: Annotated[int, "目标群号（私聊留空）"] = 0,
    ) -> tuple[bool, str]:
        """执行上传合并转发。"""
        import json

        try:
            parsed = json.loads(messages) if isinstance(messages, str) else messages
        except (TypeError, ValueError) as exc:
            return False, f"messages 解析失败: {exc}"
        params: dict[str, Any] = {"messages": parsed}
        if group_id:
            params["group_id"] = group_id
        result = await _call_onebot_api("upload_forward_msg", params)
        if result.get("status") == "ok":
            data = result.get("data") or {}
            res_id = data.get("res_id") or data.get("forward_id") or ""
            return (
                True,
                f"上传成功，res_id={res_id}" if res_id else "上传成功",
            )
        return False, f"上传合并转发失败: {result.get('msg', '未知错误')}"
