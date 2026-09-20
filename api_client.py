"""OneBot API 调用客户端（中间通讯层）。

提供 Service 层与 Tool 层共用的底层 OneBot API 调用入口 ``_call_onebot_api``。
本模块是 Service 与 Tool 之间的唯一通讯桥梁，不依赖任何一层，
确保 Tool 层可被整体移除/恢复而不影响 Service 可用性。

架构关系：
    Service / Tool  →  api_client._call_onebot_api  →  onebot_adapter  →  协议端

移除 Tool 层时：Service 改为 ``from ..api_client import _call_onebot_api``，
plugin.py 的 get_components() 不再返回 ALL_TOOLS 即可。
恢复 Tool 层时：plugin.py 的 get_components() 加回 ``+ ALL_TOOLS``。

原样透传铁律（SKILL.md §11.1）：
    本函数是协议端（NapCat/SnowLuma/LLOneBot）的纯透传入口——
    参数不经任何改写原样发出，协议端响应不经任何加工原样返回，
    不做任何本地拦截或本地伪造响应。协议端不支持的 action 也照发，
    由协议端自行返回错误，该错误响应原样透传给调用方。
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.api.adapter_api import send_adapter_command

from .api_defs import (
    ADAPTER_SIGNATURE,
    DEFAULT_TIMEOUT,
    resolve_action,
)

__all__ = ["_call_onebot_api"]


async def _call_onebot_api(
    action: str,
    params: dict[str, Any],
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """调用 OneBot API 的统一入口（纯透传）。

    通过 adapter_api 向 onebot_adapter 适配器发送命令，并等待响应。
    仅做一件事：把 ``params`` 原样发给协议端，把协议端响应原样返回。
    调用前通过 :func:`resolve_action` 将别名解析为主名（§6 别名机制，
    属于 action 命名而非参数改写）；未知名也原样转发，由协议端自行报错。

    Args:
        action: OneBot API action 名称（主名或别名，如 ``"send_group_msg"`` 或 ``"nc_get_rkey"``）。
        params: API 参数字典，原样透传，不做任何改写。
        timeout: 超时时间（秒），默认为 :data:`DEFAULT_TIMEOUT`。

    Returns:
        协议端返回的完整响应字典原样透传（通常包含 ``status``、``retcode``、
        ``data``、``echo``、``msg``、``wording`` 等字段，全部保留）。
    """
    primary = resolve_action(action)
    return await send_adapter_command(
        adapter_sign=ADAPTER_SIGNATURE,
        command_name=primary if primary is not None else action,
        command_data=params,
        timeout=timeout,
    )
