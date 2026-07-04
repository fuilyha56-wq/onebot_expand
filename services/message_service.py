"""消息发送与管理服务。

封装 OneBot v11 消息相关 API 和 NapCat 消息扩展 API，提供统一的消息操作接口。

API 列表 (18):
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
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["MessageService"]


class MessageService(BaseService):
    """消息发送与管理服务。

    封装全部消息相关 OneBot API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "message_service"
    service_description: str = "消息发送与管理服务"
    version: str = "1.0.0"

    async def send_group_msg(
        self,
        group_id: int,
        message: list[dict[str, Any]],
        auto_escape: bool = False,
    ) -> dict[str, Any]:
        """发送群聊消息。

        对应 OneBot API: ``send_group_msg``。

        Args:
            group_id: 群号。
            message: OneBot 消息段列表。
            auto_escape: 是否不解析 CQ 码，默认为 False。

        Returns:
            适配器返回的响应字典，通常包含 ``message_id``。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "message": message,
            "auto_escape": auto_escape,
        }
        return await _call_onebot_api("send_group_msg", params)

    async def send_private_msg(
        self,
        user_id: int,
        message: list[dict[str, Any]],
        auto_escape: bool = False,
    ) -> dict[str, Any]:
        """发送私聊消息。

        对应 OneBot API: ``send_private_msg``。

        Args:
            user_id: 用户 QQ 号。
            message: OneBot 消息段列表。
            auto_escape: 是否不解析 CQ 码，默认为 False。

        Returns:
            适配器返回的响应字典，通常包含 ``message_id``。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "message": message,
            "auto_escape": auto_escape,
        }
        return await _call_onebot_api("send_private_msg", params)

    async def delete_msg(self, message_id: int) -> dict[str, Any]:
        """撤回消息。

        对应 OneBot API: ``delete_msg``。

        Args:
            message_id: 消息 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"message_id": message_id}
        return await _call_onebot_api("delete_msg", params)

    async def get_msg(self, message_id: int) -> dict[str, Any]:
        """获取消息详情。

        对应 OneBot API: ``get_msg``。

        Args:
            message_id: 消息 ID。

        Returns:
            适配器返回的响应字典，包含消息详情。
        """
        params: dict[str, Any] = {"message_id": message_id}
        return await _call_onebot_api("get_msg", params)

    async def get_forward_msg(self, message_id: str) -> dict[str, Any]:
        """获取合并转发消息内容。

        对应 OneBot API: ``get_forward_msg``。

        Args:
            message_id: 合并转发消息的 ID。

        Returns:
            适配器返回的响应字典，包含合并转发消息内容。
        """
        params: dict[str, Any] = {"id": message_id}
        return await _call_onebot_api("get_forward_msg", params)

    async def send_like(self, user_id: int, times: int = 1) -> dict[str, Any]:
        """发送名片点赞。

        对应 OneBot API: ``send_like``。

        Args:
            user_id: 目标用户 QQ 号。
            times: 点赞次数，默认为 1（上限通常为 10）。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"user_id": user_id, "times": times}
        return await _call_onebot_api("send_like", params)

    async def send_poke(
        self,
        user_id: int,
        group_id: int | None = None,
    ) -> dict[str, Any]:
        """发送戳一戳（NapCat 扩展）。

        对应 NapCat 扩展 API: ``send_poke``。

        Args:
            user_id: 目标用户 QQ 号。
            group_id: 群号，为 None 时发送私聊戳一戳。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"user_id": user_id}
        if group_id is not None:
            params["group_id"] = group_id
        return await _call_onebot_api("send_poke", params)

    async def send_forward_msg(
        self,
        group_id: int | None = None,
        user_id: int | None = None,
        messages: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        """发送合并转发消息（NapCat 扩展）。

        对应 NapCat 扩展 API: ``send_forward_msg``。
        需指定 group_id 或 user_id 之一。

        Args:
            group_id: 群号，发送到群聊时指定。
            user_id: 用户 QQ 号，发送到私聊时指定。
            messages: 合并转发消息内容列表，每个元素为一条消息的节点。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {}
        if group_id is not None:
            params["group_id"] = group_id
        if user_id is not None:
            params["user_id"] = user_id
        if messages is not None:
            params["messages"] = messages
        return await _call_onebot_api("send_forward_msg", params)

    async def send_group_forward_msg(
        self,
        group_id: int,
        messages: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """发送群合并转发消息（go-cqhttp 兼容）。

        对应 go-cqhttp 兼容 API: ``send_group_forward_msg``。

        Args:
            group_id: 群号。
            messages: 合并转发消息内容列表，每个元素为一条消息的节点。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "messages": messages,
        }
        return await _call_onebot_api("send_group_forward_msg", params)

    async def send_private_forward_msg(
        self,
        user_id: int,
        messages: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """发送私聊合并转发消息（go-cqhttp 兼容）。

        对应 go-cqhttp 兼容 API: ``send_private_forward_msg``。

        Args:
            user_id: 用户 QQ 号。
            messages: 合并转发消息内容列表，每个元素为一条消息的节点。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "messages": messages,
        }
        return await _call_onebot_api("send_private_forward_msg", params)

    async def get_group_msg_history(
        self,
        group_id: int,
        message_seq: int | None = None,
        count: int = 20,
    ) -> dict[str, Any]:
        """获取群消息历史（go-cqhttp 兼容）。

        对应 go-cqhttp 兼容 API: ``get_group_msg_history``。

        Args:
            group_id: 群号。
            message_seq: 起始消息序号，为 None 时从最新开始。
            count: 获取消息数量，默认为 20。

        Returns:
            适配器返回的响应字典，包含群消息历史。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "count": count,
        }
        if message_seq is not None:
            params["message_seq"] = message_seq
        return await _call_onebot_api("get_group_msg_history", params)

    async def get_friend_msg_history(
        self,
        user_id: int,
        message_seq: int | None = None,
        count: int = 20,
    ) -> dict[str, Any]:
        """获取好友消息历史（go-cqhttp 兼容）。

        对应 go-cqhttp 兼容 API: ``get_friend_msg_history``。

        Args:
            user_id: 用户 QQ 号。
            message_seq: 起始消息序号，为 None 时从最新开始。
            count: 获取消息数量，默认为 20。

        Returns:
            适配器返回的响应字典，包含好友消息历史。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "count": count,
        }
        if message_seq is not None:
            params["message_seq"] = message_seq
        return await _call_onebot_api("get_friend_msg_history", params)

    async def forward_friend_single_msg(
        self,
        message_id: int,
        user_id: int,
    ) -> dict[str, Any]:
        """转发单条消息给好友（扩展）。

        对应扩展 API: ``forward_friend_single_msg``。

        Args:
            message_id: 要转发的消息 ID。
            user_id: 目标用户 QQ 号。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "message_id": message_id,
            "user_id": user_id,
        }
        return await _call_onebot_api("forward_friend_single_msg", params)

    async def forward_group_single_msg(
        self,
        message_id: int,
        group_id: int,
    ) -> dict[str, Any]:
        """转发单条消息到群（扩展）。

        对应扩展 API: ``forward_group_single_msg``。

        Args:
            message_id: 要转发的消息 ID。
            group_id: 目标群号。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "message_id": message_id,
            "group_id": group_id,
        }
        return await _call_onebot_api("forward_group_single_msg", params)

    async def mark_msg_as_read(
        self,
        message_id: int,
        target_id: int | None = None,
    ) -> dict[str, Any]:
        """标记消息已读（go-cqhttp 兼容）。

        对应 go-cqhttp 兼容 API: ``mark_msg_as_read``。

        Args:
            message_id: 要标记已读的消息 ID。
            target_id: 目标 ID（群号或用户 QQ 号），为 None 时不指定。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"message_id": message_id}
        if target_id is not None:
            params["target_id"] = target_id
        return await _call_onebot_api("mark_msg_as_read", params)

    async def mark_group_msg_as_read(
        self,
        message_id: int,
        group_id: int | None = None,
    ) -> dict[str, Any]:
        """标记群消息已读（扩展）。

        对应扩展 API: ``mark_group_msg_as_read``。

        Args:
            message_id: 要标记已读的消息 ID。
            group_id: 群号，为 None 时不指定。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"message_id": message_id}
        if group_id is not None:
            params["group_id"] = group_id
        return await _call_onebot_api("mark_group_msg_as_read", params)

    async def mark_private_msg_as_read(
        self,
        message_id: int,
        user_id: int | None = None,
    ) -> dict[str, Any]:
        """标记私聊消息已读（扩展）。

        对应扩展 API: ``mark_private_msg_as_read``。

        Args:
            message_id: 要标记已读的消息 ID。
            user_id: 用户 QQ 号，为 None 时不指定。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"message_id": message_id}
        if user_id is not None:
            params["user_id"] = user_id
        return await _call_onebot_api("mark_private_msg_as_read", params)

    async def _mark_all_as_read(self) -> dict[str, Any]:
        """标记全部已读（扩展）。

        对应扩展 API: ``_mark_all_as_read``。

        Returns:
            适配器返回的响应字典。
        """
        return await _call_onebot_api("_mark_all_as_read", {})
