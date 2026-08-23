"""OneBot 入站消息预处理器。

订阅 ``BEFORE_MESSAGE_RECEIVED`` 事件，在消息信封进入核心转换器之前，
将机器人自身 ID（``self_id``）写入 ``envelope.message_info.extra``，
并丢弃机器人被单独或全体禁言期间到达的群消息。

设计要点：
    - 仅处理来自 ``onebot_adapter`` 的信封，其他适配器原样放行。
    - ``self_id`` 通过调用 OneBot ``get_login_info`` API 获取并缓存。
    - **绝不阻塞消息流**：缓存命中时同步注入；缓存未命中时后台异步
      刷新，当前消息立即放行。这避免了在 WebSocket 接收循环的同一协程
      里发起同步 API 请求导致的死锁（接收循环等待 handler 完成，handler
      又在等待通过同一 WebSocket 返回的 API 响应）。
        - 禁言状态来自 OneBot 入站事件，不在 WebSocket 接收循环中调用 API。
        - 仅明确识别为群消息且命中禁言状态时返回 ``EventDecision.STOP``。
            私聊、其他 notice、未知字段和其他适配器消息均放行。
"""

from __future__ import annotations

import asyncio
import time
from typing import Any

from src.app.plugin_system.base import BaseEventHandler
from src.app.plugin_system.types import EventType
from src.kernel.event import EventDecision
from src.kernel.logger import get_logger

logger = get_logger("onebot_expand.event_handler")

# self_id 缓存有效期（秒）。OneBot 登录号在运行期通常不变，
# 但缓存可避免长时间持有过期值（如适配器重连切换账号）。
_SELF_ID_TTL: float = 300.0


class SelfIdInjectHandler(BaseEventHandler):
    """向入站信封注入元数据并过滤机器人禁言期间的消息。

    在 ``BEFORE_MESSAGE_RECEIVED`` 阶段读取 ``adapter_signature``，
    若来自 OneBot 适配器，则将 ``self_id`` 写入
    ``envelope["message_info"]["extra"]["self_id"]``，并根据 OneBot
    ``group_ban`` / ``group_whole_ban`` 事件维护禁言状态。
    """

    name: str = "self_id_inject_handler"
    description: str = "向 OneBot 入站消息注入 self_id，供兼容桥推断 @机器人 唤醒"
    weight: int = 50
    intercept_message: bool = True
    init_subscribe: list[EventType | str] = [EventType.BEFORE_MESSAGE_RECEIVED]

    def __init__(self, plugin: Any) -> None:
        """初始化处理器并建立 self_id 缓存。

        Args:
            plugin: 所属插件实例
        """
        super().__init__(plugin)
        self._self_id: str = ""
        self._self_id_refreshed_at: float = 0.0
        self._refresh_lock: asyncio.Lock = asyncio.Lock()
        self._refreshing: bool = False
        self._muted_until: dict[str, float] = {}
        self._whole_muted_groups: set[str] = set()

    async def execute(
        self, event_name: str, params: dict[str, Any]
    ) -> tuple[EventDecision, dict[str, Any]]:
        """在消息进入核心前注入 ``self_id``。

        缓存命中时同步注入；缓存未命中时触发后台刷新并立即放行当前消息，
        避免在 WebSocket 接收循环里同步等待 API 响应造成死锁。

        Args:
            event_name: 触发的事件名称
            params: 事件参数，含 ``envelope`` 与 ``adapter_signature``

        Returns:
            禁言期间返回 ``EventDecision.STOP``，其他情况返回
            ``EventDecision.SUCCESS`` 与（可能已修改的）params
        """
        adapter_signature = str(params.get("adapter_signature") or "")
        if not adapter_signature.startswith("onebot_adapter:"):
            return EventDecision.SUCCESS, params

        envelope = params.get("envelope")
        if not isinstance(envelope, dict):
            return EventDecision.SUCCESS, params

        message_info = envelope.get("message_info")
        if not isinstance(message_info, dict):
            return EventDecision.SUCCESS, params

        self._update_mute_state(envelope, message_info)
        if self._is_message_muted(envelope, message_info):
            return EventDecision.STOP, params

        self_id = self._cached_self_id()
        if not self_id:
            # 缓存未命中：同步从 adapter 配置读取 bot_id（不走 WebSocket，
            # 不会阻塞接收循环），失败则后台调 get_login_info 兜底刷新。
            self_id = await self._fetch_self_id_from_config(message_info)
        if self_id:
            self._write_self_id(message_info, self_id)
        else:
            # 配置也拿不到：后台刷新，不阻塞当前消息流。
            self._trigger_background_refresh()

        params["envelope"] = envelope
        return EventDecision.SUCCESS, params

    def _cached_self_id(self) -> str:
        """返回未过期的缓存 self_id，否则空串。"""
        if (
            self._self_id
            and (time.monotonic() - self._self_id_refreshed_at) < _SELF_ID_TTL
        ):
            return self._self_id
        return ""

    def _update_mute_state(
        self, envelope: dict[str, Any], message_info: dict[str, Any]
    ) -> None:
        """从 OneBot 禁言通知记录当前群的禁言状态。"""
        event = self._extract_onebot_event(envelope, message_info)
        if str(event.get("post_type") or "") != "notice":
            return
        notice_type = str(event.get("notice_type") or "")
        group_id = self._as_key(event.get("group_id"))
        if not group_id:
            return

        if notice_type in {"group_whole_ban", "group_whole_ban_status"}:
            if self._as_bool(event.get("enable")):
                self._whole_muted_groups.add(group_id)
            else:
                self._whole_muted_groups.discard(group_id)
            return

        if notice_type != "group_ban":
            return

        user_id = self._as_key(event.get("user_id"))
        self_id = self._as_key(event.get("self_id")) or self._self_id
        if not user_id or not self_id or user_id != self_id:
            return

        duration = max(0.0, self._as_float(event.get("duration")))
        if str(event.get("sub_type") or "") == "lift_ban" or duration == 0:
            self._muted_until.pop(group_id, None)
            return
        self._muted_until[group_id] = time.monotonic() + duration

    def _is_message_muted(
        self, envelope: dict[str, Any], message_info: dict[str, Any]
    ) -> bool:
        """判断普通群消息是否仍处于机器人禁言窗口内。"""
        message_type = str(message_info.get("message_type") or "")
        if message_type not in {"group", "message"}:
            return False
        group_info = message_info.get("group_info")
        group_id = self._as_key(message_info.get("group_id"))
        if not group_id and isinstance(group_info, dict):
            group_id = self._as_key(group_info.get("group_id"))
        if not group_id:
            group_id = self._as_key(envelope.get("group_id"))
        if not group_id:
            return False
        if group_id in self._whole_muted_groups:
            return True
        muted_until = self._muted_until.get(group_id, 0.0)
        if muted_until > time.monotonic():
            return True
        self._muted_until.pop(group_id, None)
        return False

    @staticmethod
    def _extract_onebot_event(
        envelope: dict[str, Any], message_info: dict[str, Any]
    ) -> dict[str, Any]:
        """兼容 adapter 直挂、extra 和 raw_event 三种事件承载位置。"""
        candidates = (
            envelope.get("raw_event"),
            message_info.get("raw_event"),
            message_info.get("extra"),
            message_info,
        )
        for candidate in candidates:
            if isinstance(candidate, dict) and candidate.get("post_type"):
                return candidate
        return {}

    @staticmethod
    def _as_key(value: Any) -> str:
        return str(value) if value is not None and str(value) else ""

    @staticmethod
    def _as_float(value: Any) -> float:
        try:
            return float(value or 0)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def _as_bool(value: Any) -> bool:
        """解析 OneBot 可能以布尔值、数字或字符串传递的开关。"""
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        return str(value or "").strip().lower() in {"1", "true", "yes", "on", "enable"}

    @staticmethod
    def _write_self_id(message_info: dict[str, Any], self_id: str) -> None:
        """将 self_id 写入 message_info.extra（已有值时不覆盖）。"""
        extra = message_info.get("extra")
        if not isinstance(extra, dict):
            extra = {}
            message_info["extra"] = extra
        if not extra.get("self_id"):
            extra["self_id"] = self_id

    async def _fetch_self_id_from_config(self, message_info: dict[str, Any]) -> str:
        """从 adapter 配置同步读取 bot_id 作为 self_id。

        通过 ``get_bot_info_by_platform`` 读取 adapter 已加载的配置
        （不经过 WebSocket），避免在接收循环里同步等待 API 响应导致死锁。
        成功时顺带更新缓存，后续消息可直接命中缓存。

        Args:
            message_info: 信封的 message_info，用于提取 platform

        Returns:
            bot_id 字符串，获取失败返回空串
        """
        platform = str(message_info.get("platform") or "")
        if not platform:
            return ""
        try:
            from src.app.plugin_system.api.adapter_api import get_bot_info_by_platform

            bot_info = await get_bot_info_by_platform(platform)
            if isinstance(bot_info, dict):
                bot_id = str(bot_info.get("bot_id") or bot_info.get("user_id") or "")
                if bot_id:
                    import time

                    self._self_id = bot_id
                    self._self_id_refreshed_at = time.monotonic()
                    logger.debug(f"从配置读取 self_id: {bot_id}")
                    return bot_id
        except Exception as e:
            logger.warning(f"从配置读取 self_id 失败: {e}")
        return ""

    def _trigger_background_refresh(self) -> None:
        """在后台触发一次 self_id 刷新，不阻塞当前协程。

        通过标志位避免重复派发刷新任务；已在刷新中则直接返回。
        """
        if self._refreshing:
            return
        self._refreshing = True
        asyncio.create_task(self._refresh_self_id_background())

    async def _refresh_self_id_background(self) -> None:
        """后台刷新 self_id 并更新缓存。"""
        try:
            await self._do_refresh()
        except Exception as e:
            logger.warning(f"后台刷新 self_id 失败: {e}")
        finally:
            self._refreshing = False

    async def _do_refresh(self) -> None:
        """实际执行 get_login_info 调用并更新缓存。

        通过锁串行化避免并发重复请求。
        """
        import time

        async with self._refresh_lock:
            now = time.monotonic()
            if self._self_id and (now - self._self_id_refreshed_at) < _SELF_ID_TTL:
                return
            try:
                from .api_client import _call_onebot_api

                response = await _call_onebot_api("get_login_info", {})
                data = response.get("data") if isinstance(response, dict) else None
                user_id = ""
                if isinstance(data, dict):
                    user_id = str(data.get("user_id", "") or "")
                if user_id:
                    self._self_id = user_id
                    self._self_id_refreshed_at = now
                    logger.debug(f"已刷新 self_id: {user_id}")
                else:
                    logger.warning("get_login_info 未返回 user_id，沿用旧缓存")
            except Exception as e:
                logger.warning(f"获取 self_id 失败: {e}")
