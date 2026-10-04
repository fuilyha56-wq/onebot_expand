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

原样透传铁律（SKILL.md §11.1）：参数与协议端响应均原样透传，
message 参数直接接收 OneBot 消息段（或协议端支持的字符串/CQ 码格式），
不做文本→消息段构造、合并转发节点改写等任何参数变换；
响应完整返回协议端的整个响应字典。
Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from ..message_utils import MessageId
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


class SendGroupMsgTool(BaseTool):
    """发送群聊消息的 Tool。

    对应 OneBot API: ``send_group_msg``。
    """

    name = "send_group_msg"
    description = "向指定QQ群发送消息"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        message: Annotated[
            str | list[dict[str, Any]],
            "消息内容，OneBot 消息段列表或字符串（CQ 码），原样发送",
        ],
        auto_escape: Annotated[bool, "是否不解析 CQ 码"] = False,
    ) -> tuple[bool, dict[str, Any]]:
        """执行发送群消息。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "message": message,
            "auto_escape": auto_escape,
        }
        result = await _call_onebot_api("send_group_msg", params)
        return result.get("status") == "ok", result


class SendPrivateMsgTool(BaseTool):
    """发送私聊消息的 Tool。

    对应 OneBot API: ``send_private_msg``。
    """

    name = "send_private_msg"
    description = "向指定用户发送私聊消息"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        message: Annotated[
            str | list[dict[str, Any]],
            "消息内容，OneBot 消息段列表或字符串（CQ 码），原样发送",
        ],
        auto_escape: Annotated[bool, "是否不解析 CQ 码"] = False,
    ) -> tuple[bool, dict[str, Any]]:
        """执行发送私聊消息。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "message": message,
            "auto_escape": auto_escape,
        }
        result = await _call_onebot_api("send_private_msg", params)
        return result.get("status") == "ok", result


class DeleteMsgTool(BaseTool):
    """撤回消息的 Tool。

    对应 OneBot API: ``delete_msg``。
    """

    name = "delete_msg"
    description = "撤回指定消息"

    async def execute(
        self,
        message_id: Annotated[MessageId, "要撤回的消息ID"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行撤回消息。"""
        params: dict[str, Any] = {"message_id": message_id}
        result = await _call_onebot_api("delete_msg", params)
        return result.get("status") == "ok", result


class GetMsgTool(BaseTool):
    """获取消息详情的 Tool。

    对应 OneBot API: ``get_msg``。
    返回协议端的完整响应。
    """

    name = "get_msg"
    description = "获取指定消息的详情信息"

    async def execute(
        self,
        message_id: Annotated[MessageId, "消息ID"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行获取消息详情。"""
        params: dict[str, Any] = {"message_id": message_id}
        result = await _call_onebot_api("get_msg", params)
        return result.get("status") == "ok", result


class GetForwardMsgTool(BaseTool):
    """获取合并转发消息内容的 Tool。

    对应 OneBot API: ``get_forward_msg``。
    根据合并转发消息的 ID 获取其内容。
    """

    name = "get_forward_msg"
    description = "获取合并转发消息的内容"

    async def execute(
        self,
        id: Annotated[str, "合并转发消息的ID（res_id）"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行获取合并转发消息内容。"""
        params: dict[str, Any] = {"id": id}
        result = await _call_onebot_api("get_forward_msg", params)
        return result.get("status") == "ok", result


class SendLikeTool(BaseTool):
    """发送名片点赞的 Tool。

    对应 OneBot API: ``send_like``。
    对指定用户发送名片点赞，每天次数有限。
    """

    name = "send_like"
    description = "对指定用户发送名片点赞"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        times: Annotated[int, "点赞次数（1-10）"] = 1,
    ) -> tuple[bool, dict[str, Any]]:
        """执行发送名片点赞。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "times": times,
        }
        result = await _call_onebot_api("send_like", params)
        return result.get("status") == "ok", result


class SendPokeTool(BaseTool):
    """发送戳一戳的 Tool（NapCat 扩展）。

    对应 NapCat API: ``send_poke``。
    可对群内成员或私聊用户发送戳一戳。
    """

    name = "send_poke"
    description = "发送戳一戳（NapCat扩展），可对群成员或私聊用户发送"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        group_id: Annotated[int, "目标群号（0表示私聊戳一戳）"] = 0,
    ) -> tuple[bool, dict[str, Any]]:
        """执行发送戳一戳。"""
        params: dict[str, Any] = {"user_id": user_id}
        if group_id:
            params["group_id"] = group_id

        result = await _call_onebot_api("send_poke", params)
        return result.get("status") == "ok", result


class SendForwardMsgTool(BaseTool):
    """发送合并转发消息的 Tool（NapCat 扩展）。

    对应 NapCat API: ``send_forward_msg``。
    发送合并转发消息，可指定群聊或私聊目标。
    messages 直接接收协议端支持的合并转发节点格式，原样发送。
    """

    name = "send_forward_msg"
    description = "发送合并转发消息（NapCat扩展），支持自定义多条消息内容"

    async def execute(
        self,
        messages: Annotated[
            list[dict[str, Any]], "合并转发节点列表（协议端原始格式，原样发送）"
        ],
        group_id: Annotated[int, "目标群号（0表示私聊）"] = 0,
        user_id: Annotated[int, "目标用户QQ号（私聊时必填）"] = 0,
    ) -> tuple[bool, dict[str, Any]]:
        """执行发送合并转发消息。"""
        params: dict[str, Any] = {"messages": messages}
        if group_id:
            params["group_id"] = group_id
        if user_id:
            params["user_id"] = user_id

        result = await _call_onebot_api("send_forward_msg", params)
        return result.get("status") == "ok", result


class SendGroupForwardMsgTool(BaseTool):
    """发送群合并转发消息的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``send_group_forward_msg``。
    向指定群发送合并转发消息，messages 原样发送。
    """

    name = "send_group_forward_msg"
    description = "发送群合并转发消息（go-cqhttp兼容）"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        messages: Annotated[
            list[dict[str, Any]], "合并转发节点列表（协议端原始格式，原样发送）"
        ],
    ) -> tuple[bool, dict[str, Any]]:
        """执行发送群合并转发消息。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "messages": messages,
        }
        result = await _call_onebot_api("send_group_forward_msg", params)
        return result.get("status") == "ok", result


class SendPrivateForwardMsgTool(BaseTool):
    """发送私聊合并转发消息的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``send_private_forward_msg``。
    向指定用户发送合并转发消息，messages 原样发送。
    """

    name = "send_private_forward_msg"
    description = "发送私聊合并转发消息（go-cqhttp兼容）"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        messages: Annotated[
            list[dict[str, Any]], "合并转发节点列表（协议端原始格式，原样发送）"
        ],
    ) -> tuple[bool, dict[str, Any]]:
        """执行发送私聊合并转发消息。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "messages": messages,
        }
        result = await _call_onebot_api("send_private_forward_msg", params)
        return result.get("status") == "ok", result


class GetGroupMsgHistoryTool(BaseTool):
    """获取群消息历史的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``get_group_msg_history``。
    获取指定群的消息历史记录。
    """

    name = "get_group_msg_history"
    description = "获取群消息历史记录（go-cqhttp兼容）"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        message_seq: Annotated[int, "起始消息序号（可选，0表示从最新开始）"] = 0,
        count: Annotated[int, "获取消息数量（默认20）"] = 20,
    ) -> tuple[bool, dict[str, Any]]:
        """执行获取群消息历史。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "count": count,
        }
        if message_seq:
            params["message_seq"] = message_seq

        result = await _call_onebot_api("get_group_msg_history", params)
        return result.get("status") == "ok", result


class GetFriendMsgHistoryTool(BaseTool):
    """获取好友消息历史的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``get_friend_msg_history``。
    获取指定好友的消息历史记录。
    """

    name = "get_friend_msg_history"
    description = "获取好友消息历史记录（go-cqhttp兼容）"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        message_seq: Annotated[int, "起始消息序号（可选，0表示从最新开始）"] = 0,
        count: Annotated[int, "获取消息数量（默认20）"] = 20,
    ) -> tuple[bool, dict[str, Any]]:
        """执行获取好友消息历史。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "count": count,
        }
        if message_seq:
            params["message_seq"] = message_seq

        result = await _call_onebot_api("get_friend_msg_history", params)
        return result.get("status") == "ok", result


class ForwardFriendSingleMsgTool(BaseTool):
    """转发单条消息给好友的 Tool（扩展）。

    对应扩展 API: ``forward_friend_single_msg``。
    将指定消息转发给好友。
    """

    name = "forward_friend_single_msg"
    description = "转发单条消息给好友（扩展）"

    async def execute(
        self,
        message_id: Annotated[MessageId, "要转发的消息ID"],
        user_id: Annotated[int, "目标用户QQ号"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行转发单条消息给好友。"""
        params: dict[str, Any] = {
            "message_id": message_id,
            "user_id": user_id,
        }
        result = await _call_onebot_api("forward_friend_single_msg", params)
        return result.get("status") == "ok", result


class ForwardGroupSingleMsgTool(BaseTool):
    """转发单条消息到群的 Tool（扩展）。

    对应扩展 API: ``forward_group_single_msg``。
    将指定消息转发到群。
    """

    name = "forward_group_single_msg"
    description = "转发单条消息到群（扩展）"

    async def execute(
        self,
        message_id: Annotated[MessageId, "要转发的消息ID"],
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行转发单条消息到群。"""
        params: dict[str, Any] = {
            "message_id": message_id,
            "group_id": group_id,
        }
        result = await _call_onebot_api("forward_group_single_msg", params)
        return result.get("status") == "ok", result


class MarkMsgAsReadTool(BaseTool):
    """标记消息已读的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``mark_msg_as_read``。
    标记指定消息为已读。
    """

    name = "mark_msg_as_read"
    description = "标记指定消息为已读（go-cqhttp兼容）"

    async def execute(
        self,
        message_id: Annotated[MessageId, "要标记已读的消息ID"],
        target_id: Annotated[int, "目标ID（可选，群号或用户QQ号）"] = 0,
    ) -> tuple[bool, dict[str, Any]]:
        """执行标记消息已读。"""
        params: dict[str, Any] = {"message_id": message_id}
        if target_id:
            params["target_id"] = target_id

        result = await _call_onebot_api("mark_msg_as_read", params)
        return result.get("status") == "ok", result


class MarkGroupMsgAsReadTool(BaseTool):
    """标记群消息已读的 Tool（扩展）。

    对应扩展 API: ``mark_group_msg_as_read``。
    标记指定群的消息为已读。
    """

    name = "mark_group_msg_as_read"
    description = "标记群消息已读（扩展）"

    async def execute(
        self,
        message_id: Annotated[MessageId, "要标记已读的消息ID"],
        group_id: Annotated[int, "目标群号（可选，0表示当前群）"] = 0,
    ) -> tuple[bool, dict[str, Any]]:
        """执行标记群消息已读。"""
        params: dict[str, Any] = {"message_id": message_id}
        if group_id:
            params["group_id"] = group_id

        result = await _call_onebot_api("mark_group_msg_as_read", params)
        return result.get("status") == "ok", result


class MarkPrivateMsgAsReadTool(BaseTool):
    """标记私聊消息已读的 Tool（扩展）。

    对应扩展 API: ``mark_private_msg_as_read``。
    标记指定私聊的消息为已读。
    """

    name = "mark_private_msg_as_read"
    description = "标记私聊消息已读（扩展）"

    async def execute(
        self,
        message_id: Annotated[MessageId, "要标记已读的消息ID"],
        user_id: Annotated[int, "目标用户QQ号（可选，0表示当前私聊）"] = 0,
    ) -> tuple[bool, dict[str, Any]]:
        """执行标记私聊消息已读。"""
        params: dict[str, Any] = {"message_id": message_id}
        if user_id:
            params["user_id"] = user_id

        result = await _call_onebot_api("mark_private_msg_as_read", params)
        return result.get("status") == "ok", result


class MarkAllAsReadTool(BaseTool):
    """标记全部已读的 Tool（扩展）。

    对应扩展 API: ``_mark_all_as_read``。
    标记所有消息为已读。
    """

    name = "_mark_all_as_read"
    description = "标记全部消息为已读（扩展）"

    async def execute(
        self,
    ) -> tuple[bool, dict[str, Any]]:
        """执行标记全部已读。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("_mark_all_as_read", params)
        return result.get("status") == "ok", result


class SendMsgTool(BaseTool):
    """通用发消息 Tool（按 message_type 或 user_id/group_id 自动路由）。

    对应 OneBot API: ``send_msg``。
    """

    name = "send_msg"
    description = "发送消息（通用，按 message_type 自动路由群聊或私聊）"

    async def execute(
        self,
        message: Annotated[
            str | list[dict[str, Any]],
            "消息内容，OneBot 消息段列表或字符串（CQ 码），原样发送",
        ],
        message_type: Annotated[str, "消息类型 private 或 group"] = "",
        user_id: Annotated[int, "目标用户QQ号（私聊时）"] = 0,
        group_id: Annotated[int, "目标群号（群聊时）"] = 0,
        auto_escape: Annotated[bool, "是否不解析 CQ 码"] = False,
    ) -> tuple[bool, dict[str, Any]]:
        """执行发送消息。"""
        params: dict[str, Any] = {
            "message": message,
            "auto_escape": auto_escape,
        }
        if message_type:
            params["message_type"] = message_type
        if user_id:
            params["user_id"] = user_id
        if group_id:
            params["group_id"] = group_id
        result = await _call_onebot_api("send_msg", params)
        return result.get("status") == "ok", result


class UploadForwardMsgTool(BaseTool):
    """上传合并转发消息 Tool（返回 res_id）。

    对应扩展 API: ``upload_forward_msg``。
    """

    name = "upload_forward_msg"
    description = "上传合并转发消息，返回 res_id（扩展，SnowLuma 支持）"

    async def execute(
        self,
        messages: Annotated[
            list[dict[str, Any]], "合并转发节点列表（协议端原始格式，原样发送）"
        ],
        group_id: Annotated[int, "目标群号（私聊留空）"] = 0,
    ) -> tuple[bool, dict[str, Any]]:
        """执行上传合并转发。"""
        params: dict[str, Any] = {"messages": messages}
        if group_id:
            params["group_id"] = group_id
        result = await _call_onebot_api("upload_forward_msg", params)
        return result.get("status") == "ok", result
