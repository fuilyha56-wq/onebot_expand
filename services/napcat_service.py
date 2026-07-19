"""NapCat 扩展功能服务。

封装 NapCat 扩展 API，提供消息表情回应、精华消息、
在线客户端、Cookies、状态查询、重启、缓存清理等扩展功能。

API 列表 (15):
    - set_msg_emoji_like: 对消息添加/取消表情回应
    - get_essence_msg_list: 获取群精华消息列表
    - get_online_clients: 获取在线客户端列表
    - get_cookies: 获取 Cookies
    - get_csrf_token: 获取 CSRF Token
    - get_status: 获取协议端运行状态
    - set_restart: 重启协议端
    - clean_cache: 清理协议端缓存
    - can_send_image: 检查是否支持发送图片
    - can_send_record: 检查是否支持发送语音
    - get_version_info: 获取协议端版本信息
    - set_essence_msg: 设置精华消息（go-cqhttp兼容）
    - delete_essence_msg: 删除精华消息（go-cqhttp兼容）
    - get_group_at_all_remain: 获取@全体剩余次数（go-cqhttp兼容）
    - fetch_ptt_text: 获取语音转文字（扩展）
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..emoji_tables import get_emoji_by_id
from ..message_utils import MessageId
from ..tools import _call_onebot_api

__all__ = ["NapcatExtService"]


class NapcatExtService(BaseService):
    """NapCat 扩展功能服务。

    封装全部 NapCat 扩展 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    set_msg_emoji_like 方法会使用 emoji_tables 验证 emoji_id 的有效性。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "napcat_ext_service"
    service_description: str = "NapCat 扩展功能服务"
    version: str = "1.0.0"

    def _is_reaction_emoji_enabled(self, emoji_id: int) -> bool:
        """检查表情回应功能及指定表情 ID 是否启用。

        需同时满足以下条件：
        1. 配置中表情回应功能已启用 (emoji.enable_reaction_emoji)
        2. 表情 ID 在启用的回应表情 ID 白名单中（空列表表示全部启用）

        Args:
            emoji_id: 表情 ID。

        Returns:
            True 表示启用，False 表示禁用。
        """
        config = self.plugin.config
        if config is None:
            return True
        emoji_cfg = getattr(config, "emoji", None)
        if emoji_cfg is None:
            return True
        if not getattr(emoji_cfg, "enable_reaction_emoji", True):
            return False
        enabled_ids = getattr(emoji_cfg, "reaction_emoji_enabled_ids", [])
        if not enabled_ids:
            return True
        return emoji_id in enabled_ids

    async def set_msg_emoji_like(
        self,
        message_id: MessageId,
        emoji_id: int,
        set: bool = True,
    ) -> dict[str, Any]:
        """对消息添加/取消表情回应。

        对应 NapCat 扩展 API: ``set_msg_emoji_like``。
        会使用 emoji_tables 验证 emoji_id 是否为合法的回应表情。

        Args:
            message_id: 消息 ID。
            emoji_id: 表情 ID（需在表情回应表中存在）。
            set: True 添加回应，False 取消回应，默认为 True。

        Returns:
            适配器返回的响应字典。
        """

        # 使用 emoji_tables 验证 emoji_id 是否为合法的回应表情
        entry = get_emoji_by_id(emoji_id, table_type="reaction")
        if entry is None:
            return {
                "status": "error",
                "retcode": -1,
                "msg": f"无效的回应表情 ID: {emoji_id}，该 ID 不在表情回应表中",
            }

        # 检查表情回应功能及该表情是否启用
        if not self._is_reaction_emoji_enabled(emoji_id):
            return {
                "status": "error",
                "retcode": -1,
                "msg": f"表情回应功能或表情 ID {emoji_id}（{entry.describe}）已被禁用",
            }

        params: dict[str, Any] = {
            "message_id": message_id,
            "emoji_id": emoji_id,
            "set": set,
        }
        return await _call_onebot_api("set_msg_emoji_like", params)

    async def get_essence_msg_list(self, group_id: int) -> dict[str, Any]:
        """获取群精华消息列表。

        对应 NapCat 扩展 API: ``get_essence_msg_list``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典，包含精华消息列表。
        """
        params: dict[str, Any] = {"group_id": group_id}
        return await _call_onebot_api("get_essence_msg_list", params)


    async def get_online_clients(self) -> dict[str, Any]:
        """获取在线客户端列表。

        对应 NapCat 扩展 API: ``get_online_clients``。

        Returns:
            适配器返回的响应字典，包含在线客户端列表。
        """
        return await _call_onebot_api("get_online_clients", {})

    async def get_cookies(self, domain: str = "") -> dict[str, Any]:
        """获取 Cookies。

        对应 NapCat 扩展 API: ``get_cookies``。

        Args:
            domain: 目标域名，默认为空字符串（获取默认域名的 Cookies）。

        Returns:
            适配器返回的响应字典，包含 Cookies 信息。
        """
        params: dict[str, Any] = {"domain": domain}
        return await _call_onebot_api("get_cookies", params)

    async def get_csrf_token(self) -> dict[str, Any]:
        """获取 CSRF Token。

        对应 NapCat 扩展 API: ``get_csrf_token``。

        Returns:
            适配器返回的响应字典，包含 CSRF Token。
        """
        return await _call_onebot_api("get_csrf_token", {})

    async def get_status(self) -> dict[str, Any]:
        """获取协议端运行状态。

        对应 NapCat 扩展 API: ``get_status``。

        Returns:
            适配器返回的响应字典，包含运行状态信息。
        """
        return await _call_onebot_api("get_status", {})

    async def set_restart(self, delay: int = 0) -> dict[str, Any]:
        """重启协议端。

        对应 NapCat 扩展 API: ``set_restart``。

        Args:
            delay: 延迟重启时间（毫秒），默认为 0（立即重启）。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"delay": delay}
        return await _call_onebot_api("set_restart", params)

    async def clean_cache(self) -> dict[str, Any]:
        """清理协议端缓存。

        对应 NapCat 扩展 API: ``clean_cache``。

        Returns:
            适配器返回的响应字典。
        """
        return await _call_onebot_api("clean_cache", {})

    async def can_send_image(self) -> dict[str, Any]:
        """检查是否支持发送图片。

        对应 NapCat 扩展 API: ``can_send_image``。

        Returns:
            适配器返回的响应字典，包含是否支持发送图片的布尔值。
        """
        return await _call_onebot_api("can_send_image", {})

    async def can_send_record(self) -> dict[str, Any]:
        """检查是否支持发送语音。

        对应 NapCat 扩展 API: ``can_send_record``。

        Returns:
            适配器返回的响应字典，包含是否支持发送语音的布尔值。
        """
        return await _call_onebot_api("can_send_record", {})

    async def get_version_info(self) -> dict[str, Any]:
        """获取协议端版本信息。

        对应 NapCat 扩展 API: ``get_version_info``。

        Returns:
            适配器返回的响应字典，包含协议端版本信息。
        """
        return await _call_onebot_api("get_version_info", {})

    async def set_essence_msg(self, message_id: MessageId) -> dict[str, Any]:
        """设置精华消息（go-cqhttp 兼容）。

        对应 go-cqhttp 兼容 API: ``set_essence_msg``。

        Args:
            message_id: 要设置精华的消息 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"message_id": message_id}
        return await _call_onebot_api("set_essence_msg", params)

    async def delete_essence_msg(self, message_id: MessageId) -> dict[str, Any]:
        """删除精华消息（go-cqhttp 兼容）。

        对应 go-cqhttp 兼容 API: ``delete_essence_msg``。

        Args:
            message_id: 要删除精华的消息 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"message_id": message_id}
        return await _call_onebot_api("delete_essence_msg", params)

    async def get_group_at_all_remain(self, group_id: int) -> dict[str, Any]:
        """获取@全体剩余次数（go-cqhttp 兼容）。

        对应 go-cqhttp 兼容 API: ``get_group_at_all_remain``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典，包含@全体剩余次数信息。
        """
        params: dict[str, Any] = {"group_id": group_id}
        return await _call_onebot_api("get_group_at_all_remain", params)

    async def fetch_ptt_text(self, message_id: MessageId) -> dict[str, Any]:
        """获取语音转文字（扩展）。

        对应扩展 API: ``fetch_ptt_text``。

        Args:
            message_id: 语音消息 ID。

        Returns:
            适配器返回的响应字典，包含语音转文字结果。
        """
        params: dict[str, Any] = {"message_id": message_id}
        return await _call_onebot_api("fetch_ptt_text", params)
