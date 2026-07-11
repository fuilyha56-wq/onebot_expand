"""NapCat 测试适配器。

通过 WebSocket 连接 ws://127.0.0.1:5326（NapCat 反向 WS 服务端），
提供同步式 API 调用接口，供 SKILL.md Step 8 测试使用。

使用方式：
    from tests.napcat_test_adapter import call_napcat
    result = call_napcat("send_msg", {"message_type": "private", "user_id": 10000, "message": [{"type": "text", "data": {"text": "hi"}}]})

协议：
    客户端发: {"action": "<name>", "params": {...}, "echo": "<uuid>"}
    服务端回: {"status": "ok"|"failed"|"async", "retcode": 0, "data": {...}, "echo": "<uuid>"}

需要安装 websockets：``pip install websockets``
NapCat 必须启用反向 WebSocket 服务端，监听 127.0.0.1:5326。
"""

from __future__ import annotations

import asyncio
import json
import uuid
from typing import Any

import websockets

DEFAULT_URL = "ws://127.0.0.1:5326"
DEFAULT_TIMEOUT = 30.0


async def _call_async(
    action: str,
    params: dict[str, Any] | None = None,
    *,
    url: str = DEFAULT_URL,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """异步调用 NapCat API。"""
    echo = uuid.uuid4().hex
    payload = json.dumps({"action": action, "params": params or {}, "echo": echo}, ensure_ascii=False)
    async with websockets.connect(url, max_size=64 * 1024 * 1024) as ws:
        await ws.send(payload)
        while True:
            raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
            try:
                msg = json.loads(raw)
            except (TypeError, ValueError):
                continue
            if not isinstance(msg, dict):
                continue
            # 跳过事件上报（无 echo 或 echo 不匹配）
            if msg.get("echo") != echo:
                continue
            return msg


def call_napcat(
    action: str,
    params: dict[str, Any] | None = None,
    *,
    url: str = DEFAULT_URL,
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """同步调用 NapCat API。

    Args:
        action: API action 名（主名或别名，NapCat 会自行解析）。
        params: API 参数字典。
        url: NapCat 反向 WS 服务端地址，默认 ws://127.0.0.1:5326。
        timeout: 单次响应超时（秒）。

    Returns:
        NapCat 返回的响应字典，包含 ``status``、``retcode``、``data``、``echo``。
        连接或超时失败时返回 ``{"status": "error", "retcode": -1, "msg": "<原因>"}``。
    """
    try:
        return asyncio.run(_call_async(action, params, url=url, timeout=timeout))
    except (OSError, asyncio.TimeoutError, websockets.exceptions.WebSocketException) as exc:
        return {"status": "error", "retcode": -1, "msg": f"{type(exc).__name__}: {exc}"}
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "retcode": -1, "msg": f"{type(exc).__name__}: {exc}"}


def is_available(url: str = DEFAULT_URL, timeout: float = 3.0) -> bool:
    """检查 NapCat 测试服务端是否可达。"""
    try:
        result = call_napcat("get_login_info", {}, url=url, timeout=timeout)
        return result.get("status") == "ok"
    except Exception:  # noqa: BLE001
        return False


if __name__ == "__main__":
    import sys

    action = sys.argv[1] if len(sys.argv) > 1 else "get_login_info"
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    result = call_napcat(action, params)
    print(json.dumps(result, ensure_ascii=False, indent=2))
