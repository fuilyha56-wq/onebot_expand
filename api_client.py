"""OneBot API 调用客户端（中间通讯层）。

提供 Service 层与 Tool 层共用的底层 OneBot API 调用入口 ``_call_onebot_api``。
本模块是 Service 与 Tool 之间的唯一通讯桥梁，不依赖任何一层，
确保 Tool 层可被整体移除/恢复而不影响 Service 可用性。

架构关系：
    Service / Tool  →  api_client._call_onebot_api  →  onebot_adapter  →  协议端

移除 Tool 层时：Service 改为 ``from ..api_client import _call_onebot_api``，
plugin.py 的 get_components() 不再返回 ALL_TOOLS 即可。
恢复 Tool 层时：plugin.py 的 get_components() 加回 ``+ ALL_TOOLS``。
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.api.adapter_api import send_adapter_command
from src.app.plugin_system.api.config_api import get_config

from .api_defs import (
    ADAPTER_SIGNATURE,
    ALL_APIS,
    DEFAULT_TIMEOUT,
    ExpandAction,
    resolve_action,
)
from .message_utils import normalize_message_ids

__all__ = ["_call_onebot_api"]


async def _call_onebot_api(
    action: str,
    params: dict[str, Any],
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """调用 OneBot API 的统一入口。

    通过 adapter_api 向 onebot_adapter 适配器发送命令，并等待响应。
    调用前会先通过 :func:`resolve_action` 将别名解析为主名，
    保证配置开关、协议端兼容性检查、文档引用的一致性。

    Args:
        action: OneBot API action 名称（主名或别名，如 ``"send_group_msg"`` 或 ``"nc_get_rkey"``）。
        params: API 参数字典。
        timeout: 超时时间（秒），默认为 :data:`DEFAULT_TIMEOUT`。

    Returns:
        适配器返回的响应字典，通常包含 ``status``、``retcode``、``data`` 等字段。
        若 action 名（含别名）无法识别，返回 ``{"status": "error", "retcode": -1, "msg": ...}``。
    """
    primary = resolve_action(action)
    if primary is None:
        return {
            "status": "error",
            "retcode": -1,
            "msg": f"未知 action: {action}",
        }
    config = get_config("onebot_expand")
    adapter = getattr(config, "adapter", None)
    snowluma_backend = bool(
        adapter
        and (
            str(adapter.backend).strip().lower() == "snowluma"
            or bool(adapter.snowluma_compat_mode)
        )
    )
    api_def = ALL_APIS[primary]
    if snowluma_backend and not api_def.snowluma_compat:
        message = f"当前 SnowLuma 后端不支持 action: {primary}"
        return {
            "status": "failed",
            "retcode": 1404,
            "data": None,
            "msg": message,
            "wording": message,
        }
    if (
        snowluma_backend
        and primary == ExpandAction.DOWNLOAD_FILE_RECORD_STREAM
        and params.get("out_format")
    ):
        message = (
            "SnowLuma 的 download_file_record_stream 不支持 out_format 转码；"
            "请省略该参数以下载原始语音文件"
        )
        return {
            "status": "failed",
            "retcode": 1400,
            "data": None,
            "msg": message,
            "wording": message,
        }
    return await send_adapter_command(
        adapter_sign=ADAPTER_SIGNATURE,
        command_name=primary,
        command_data=normalize_message_ids(params),
        timeout=timeout,
    )
