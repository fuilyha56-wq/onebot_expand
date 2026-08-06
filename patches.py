"""SnowLuma 文件消息 ``file_hash`` 透传补丁。

背景：
    SnowLuma 在私聊/群文件的 OneBot 段 ``data`` 中会携带 ``file_hash``
    字段（``element-codecs.ts`` 的 ``toSegment`` 输出 ``file_hash:
    element.fileHash ?? ''``），而 ``get_private_file_url`` 需要
    ``file_id`` + ``file_hash`` 才能解析出下载地址。

    neo-mofox 主程序在两处把 ``file_hash`` 丢弃：
      - ``onebot_adapter`` 的 ``MessageHandler._handle_file_message``
        只提取 ``file``/``file_size``/``file_id``；
      - 核心 ``MessageConverter._handle_file`` 生成占位符
        ``[文件:名称]``，不带 ``id=``/``hash=``。

    本插件（onebot_expand）的 ``GetPrivateFileUrlTool`` 依赖占位符里的
    ``id=... hash=...`` 取值，因此需要在不改动主程序文件的前提下补齐。

实现方式：
    onebot_expand 的 ``manifest.json`` 已声明依赖 ``onebot_adapter``，
    加载器保证本插件在其之后加载。这里在 import 时对上述两个方法做
    模块级替换：保留原始返回值结构，仅把 ``file_hash`` 透传进
    ``data``，并把占位符富化为 ``[文件:名称 id=... hash=...]``。

    纯 Python 运行时补丁，不修改、不覆盖任何主程序源文件；卸载或
    移除本插件后，主程序文件保持原样（进程重启即恢复原行为）。
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.api.log_api import get_logger

logger = get_logger("onebot_expand.patches")

_applied: bool = False


def _build_file_data(file_name: Any, file_size: Any, file_id: Any, file_hash: Any) -> dict[str, Any]:
    """构造透传 ``file_hash`` 的文件数据字典。

    仅在确实取到 ``file_hash`` 时写入，避免向后端塞入空串字段。
    """
    data: dict[str, Any] = {
        "name": file_name,
        "size": file_size,
        "id": file_id,
    }
    if file_hash:
        data["hash"] = file_hash
    return data


def _build_placeholder(file_name: str, file_id: Any, file_hash: Any) -> str:
    """生成带 ``id=``/``hash=`` 的文件占位符。

    与原 ``[文件:名称]`` 保持同一前缀；仅在取到值时追加对应片段，
    供 ``GetPrivateFileUrlTool`` 按约定解析。
    """
    placeholder = f"[文件:{file_name}"
    if file_id:
        placeholder += f" id={file_id}"
    if file_hash:
        placeholder += f" hash={file_hash}"
    placeholder += "]"
    return placeholder


def _patch_adapter_file_message() -> None:
    """替换 ``MessageHandler._handle_file_message``，透传 ``file_hash``。

    原始实现位于
    ``plugins/onebot_adapter/src/handlers/to_core/message_handler.py``，
    只取 ``file``/``file_size``/``file_id``。补丁版在此基础上追加
    SnowLuma 下发的 ``file_hash``，产出结构保持 ``{"type": "file",
    "data": {...}}`` 不变。
    """
    from onebot_adapter.src.handlers.to_core.message_handler import MessageHandler

    async def _handle_file_message_patched(self: Any, segment: dict) -> dict | None:
        """处理文件消息（补丁版，透传 ``file_hash``）。"""
        message_data = segment.get("data", {})
        if not message_data:
            return None

        file_name = message_data.get("file")
        file_size = message_data.get("file_size")
        file_id = message_data.get("file_id")
        # SnowLuma 在文件段 data 中附带 file_hash，原始实现将其丢弃。
        file_hash = message_data.get("file_hash")

        file_data = _build_file_data(file_name, file_size, file_id, file_hash)
        return {"type": "file", "data": file_data}

    MessageHandler._handle_file_message = _handle_file_message_patched  # type: ignore[method-assign]


def _patch_converter_file() -> None:
    """替换 ``MessageConverter._handle_file``，富化占位符并透传 ``file_hash``。

    原始实现位于
    ``src/core/transport/message_receive/converter.py``，占位符为
    ``[文件:名称]`` 且丢弃 ``hash``。补丁版把 ``hash`` 写进 ``media``
    的 ``data``，并把占位符富化为 ``[文件:名称 id=... hash=...]``。
    """
    from src.core.transport.message_receive.converter import MessageConverter

    @staticmethod
    def _handle_file_patched(data: Any, result: Any) -> None:
        """处理文件段（补丁版，透传 ``file_hash`` 并富化占位符）。"""
        from src.core.transport.message_receive.utils import safe_json_loads

        parsed = data
        if isinstance(data, str):
            parsed = safe_json_loads(data)

        if isinstance(parsed, dict):
            file_name = parsed.get("name") or parsed.get("file", "")
            file_size = parsed.get("size") or parsed.get("file_size")
            file_id = parsed.get("id") or parsed.get("file_id")
            file_hash = parsed.get("hash") or parsed.get("file_hash")

            result.media.append({
                "type": "file",
                "data": _build_file_data(file_name, file_size, file_id, file_hash),
            })
            display_name = file_name or "文件"
            result.text_parts.append(_build_placeholder(display_name, file_id, file_hash))
        else:
            # 无法解析结构，保留原始信息
            result.media.append({"type": "file", "data": parsed})
            result.text_parts.append("[文件]")

    MessageConverter._handle_file = _handle_file_patched  # type: ignore[method-assign]


def apply_file_hash_patches() -> bool:
    """应用 ``file_hash`` 透传补丁（幂等）。

    对 ``onebot_adapter`` 与核心转换器各打一次补丁；重复调用直接
    返回已应用状态，不重复替换。

    Returns:
        补丁是否处于已应用状态。任一步骤失败时返回 ``False`` 并记录
        错误，不影响插件其余组件的注册。
    """
    global _applied
    if _applied:
        return True

    try:
        _patch_adapter_file_message()
        _patch_converter_file()
    except Exception as exc:  # pragma: no cover - 防御性兜底
        logger.error(f"应用 file_hash 透传补丁失败: {exc}", exc_info=True)
        return False

    _applied = True
    logger.info("已应用 file_hash 透传补丁（adapter 文件消息 + 核心占位符富化）")
    return True


# 模块 import 时立即应用补丁。onebot_expand 依赖 onebot_adapter，
# 加载顺序保证此处 import 时两个目标模块均已就绪。
apply_file_hash_patches()
