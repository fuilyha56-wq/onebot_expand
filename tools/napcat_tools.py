"""NapCat 扩展 API 的 Tool 组件。

包含 15 个 NapCat 扩展 Tool，对应 NapCat 专属扩展 API：
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

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from ..message_utils import MessageId
from . import _call_onebot_api

__all__ = [
    "SetMsgEmojiLikeTool",
    "GetEssenceMsgListTool",

    "GetOnlineClientsTool",
    "GetCookiesTool",
    "GetCsrfTokenTool",
    "GetStatusTool",
    "SetRestartTool",
    "CleanCacheTool",
    "CanSendImageTool",
    "CanSendRecordTool",
    "GetVersionInfoTool",
    "SetEssenceMsgTool",
    "DeleteEssenceMsgTool",
    "GetGroupAtAllRemainTool",
    "FetchPttTextTool",
]


class SetMsgEmojiLikeTool(BaseTool):
    """对消息添加/取消表情回应的 Tool（NapCat 扩展）。

    对应 NapCat API: ``set_msg_emoji_like``。
    对指定消息添加或取消表情回应（贴表情）。
    """

    name = "set_msg_emoji_like"
    description = "对消息添加或取消表情回应（贴表情）"

    async def execute(
        self,
        message_id: Annotated[MessageId, "目标消息ID"],
        emoji_id: Annotated[int, "表情ID（QQNT回应表情ID）"],
        set_like: Annotated[bool, "True为添加回应，False为取消回应"] = True,
    ) -> tuple[bool, dict[str, Any]]:
        """执行对消息设置表情回应。"""
        params: dict[str, Any] = {
            "message_id": message_id,
            "emoji_id": emoji_id,
            "set": set_like,
        }
        result = await _call_onebot_api("set_msg_emoji_like", params)
        return result.get("status") == "ok", result


class GetEssenceMsgListTool(BaseTool):
    """获取群精华消息列表的 Tool（NapCat 扩展）。

    对应 NapCat API: ``get_essence_msg_list``。
    返回指定群的精华消息列表。
    """

    name = "get_essence_msg_list"
    description = "获取指定群的精华消息列表（NapCat扩展）"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群精华消息列表。"""
        params: dict[str, Any] = {"group_id": group_id}
        result = await _call_onebot_api("get_essence_msg_list", params)
        return result.get("status") == "ok", result



class GetOnlineClientsTool(BaseTool):
    """获取在线客户端列表的 Tool（NapCat 扩展）。

    对应 NapCat API: ``get_online_clients``。
    返回当前 Bot 在各平台的在线客户端列表。
    """

    name = "get_online_clients"
    description = "获取当前Bot的在线客户端列表（NapCat扩展）"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取在线客户端列表。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_online_clients", params)
        return result.get("status") == "ok", result


class GetCookiesTool(BaseTool):
    """获取 Cookies 的 Tool（NapCat 扩展）。

    对应 NapCat API: ``get_cookies``。
    获取当前 Bot 在指定域名的 Cookies。
    """

    name = "get_cookies"
    description = "获取当前Bot在指定域名的Cookies（NapCat扩展）"

    async def execute(
        self,
        domain: Annotated[str, "目标域名（如 'qun.qq.com'）"] = "",
    ) -> tuple[bool, dict[str, Any]]:
        """执行获取 Cookies。"""
        params: dict[str, Any] = {}
        if domain:
            params["domain"] = domain

        result = await _call_onebot_api("get_cookies", params)
        return result.get("status") == "ok", result


class GetCsrfTokenTool(BaseTool):
    """获取 CSRF Token 的 Tool（NapCat 扩展）。

    对应 NapCat API: ``get_csrf_token``。
    获取当前 Bot 的 CSRF Token。
    """

    name = "get_csrf_token"
    description = "获取当前Bot的CSRF Token（NapCat扩展）"

    async def execute(
        self,
    ) -> tuple[bool, dict[str, Any]]:
        """执行获取 CSRF Token。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_csrf_token", params)
        return result.get("status") == "ok", result


class GetStatusTool(BaseTool):
    """获取协议端运行状态的 Tool。

    对应 NapCat API: ``get_status``。
    返回协议端的运行状态信息（在线状态、资源占用等）。
    """

    name = "get_status"
    description = "获取协议端的运行状态信息"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取协议端运行状态。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_status", params)
        return result.get("status") == "ok", result


class SetRestartTool(BaseTool):
    """重启协议端的 Tool（NapCat 扩展）。

    对应 NapCat API: ``set_restart``。
    重启协议端，延迟时间后生效。请谨慎使用。
    """

    name = "set_restart"
    description = "重启协议端，延迟指定秒数后生效（请谨慎使用）"

    async def execute(
        self,
        delay: Annotated[int, "延迟重启时间（秒）"] = 0,
    ) -> tuple[bool, dict[str, Any]]:
        """执行重启协议端。"""
        params: dict[str, Any] = {"delay": delay}
        result = await _call_onebot_api("set_restart", params)
        return result.get("status") == "ok", result


class CleanCacheTool(BaseTool):
    """清理协议端缓存的 Tool（NapCat 扩展）。

    对应 NapCat API: ``clean_cache``。
    清理协议端的缓存数据。
    """

    name = "clean_cache"
    description = "清理协议端的缓存数据（NapCat扩展）"

    async def execute(
        self,
    ) -> tuple[bool, dict[str, Any]]:
        """执行清理协议端缓存。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("clean_cache", params)
        return result.get("status") == "ok", result


class CanSendImageTool(BaseTool):
    """检查是否支持发送图片的 Tool。

    对应 NapCat API: ``can_send_image``。
    检查当前协议端是否支持发送图片。
    """

    name = "can_send_image"
    description = "检查当前协议端是否支持发送图片"

    async def execute(
        self,
    ) -> tuple[bool, dict[str, Any]]:
        """执行检查是否支持发送图片。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("can_send_image", params)
        return result.get("status") == "ok", result


class CanSendRecordTool(BaseTool):
    """检查是否支持发送语音的 Tool。

    对应 NapCat API: ``can_send_record``。
    检查当前协议端是否支持发送语音。
    """

    name = "can_send_record"
    description = "检查当前协议端是否支持发送语音"

    async def execute(
        self,
    ) -> tuple[bool, dict[str, Any]]:
        """执行检查是否支持发送语音。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("can_send_record", params)
        return result.get("status") == "ok", result


class GetVersionInfoTool(BaseTool):
    """获取协议端版本信息的 Tool。

    对应 NapCat API: ``get_version_info``。
    返回协议端的版本信息（版本号、协议类型等）。
    """

    name = "get_version_info"
    description = "获取协议端的版本信息"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取协议端版本信息。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_version_info", params)
        return result.get("status") == "ok", result


class SetEssenceMsgTool(BaseTool):
    """设置精华消息的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``set_essence_msg``。
    将指定消息设置为群精华消息。
    """

    name = "set_essence_msg"
    description = "设置精华消息（go-cqhttp兼容）"

    async def execute(
        self,
        message_id: Annotated[MessageId, "要设置精华的消息ID"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行设置精华消息。"""
        params: dict[str, Any] = {"message_id": message_id}
        result = await _call_onebot_api("set_essence_msg", params)
        return result.get("status") == "ok", result


class DeleteEssenceMsgTool(BaseTool):
    """删除精华消息的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``delete_essence_msg``。
    将指定消息从群精华消息中移除。
    """

    name = "delete_essence_msg"
    description = "删除精华消息（go-cqhttp兼容）"

    async def execute(
        self,
        message_id: Annotated[MessageId, "要删除精华的消息ID"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行删除精华消息。"""
        params: dict[str, Any] = {"message_id": message_id}
        result = await _call_onebot_api("delete_essence_msg", params)
        return result.get("status") == "ok", result


class GetGroupAtAllRemainTool(BaseTool):
    """获取@全体剩余次数的 Tool（go-cqhttp 兼容）。

    对应 go-cqhttp 兼容 API: ``get_group_at_all_remain``。
    获取在指定群中@全体的剩余次数。
    """

    name = "get_group_at_all_remain"
    description = "获取@全体剩余次数（go-cqhttp兼容）"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取@全体剩余次数。"""
        params: dict[str, Any] = {"group_id": group_id}
        result = await _call_onebot_api("get_group_at_all_remain", params)
        return result.get("status") == "ok", result


class FetchPttTextTool(BaseTool):
    """获取语音转文字的 Tool（扩展）。

    对应扩展 API: ``fetch_ptt_text``。
    将指定语音消息转换为文字。
    """

    name = "fetch_ptt_text"
    description = "获取语音转文字（扩展）"

    async def execute(
        self,
        message_id: Annotated[MessageId, "语音消息ID"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取语音转文字。"""
        params: dict[str, Any] = {"message_id": message_id}
        result = await _call_onebot_api("fetch_ptt_text", params)
        return result.get("status") == "ok", result
