"""原样透传一致性测试（SKILL.md §11.1 铁律的自动化检查）。

扫描全部 Tool / Service / api_client 源码，断言：
1. Tool 层不存在响应加工（中文摘要、data 提取、伪造响应）
2. Tool 层不存在参数改写（normalize/inject/结构重排）
3. api_client 不做本地拦截（snowluma_compat 不参与调用期判断）
4. ALL_TOOLS 与 ALL_APIS 数量一致（去重铁律）
"""

from __future__ import annotations

import glob
import inspect
import io
import re

import pytest

from .. import api_client
from ..api_defs import ALL_APIS
from ..tools import ALL_TOOLS

TOOL_FILES = sorted(glob.glob(str(__import__("pathlib").Path(__file__).parent.parent / "tools" / "*_tools.py")))


def _read(path: str) -> str:
    return io.open(path, encoding="utf-8").read()


def test_all_tool_files_are_passthrough() -> None:
    """全部 Tool 源码不得出现响应加工/参数改写模式。"""
    violations: list[str] = []
    for path in TOOL_FILES:
        src = _read(path)
        name = path.replace("\\", "/").split("/")[-1]
        if re.search(r'return True, f?"', src):
            violations.append(f"{name}: return True 携带字面量摘要")
        if re.search(r"return True, [a-zA-Z_]+$", src, re.M):
            violations.append(f"{name}: return True 携带加工变量")
        if re.search(r'return False, f?"', src):
            violations.append(f"{name}: return False 携带本地错误文案")
        if re.search(r'result\.get\("data"', src):
            violations.append(f"{name}: 提取 data 子集")
        if re.search(r'"status":\s*"(error|failed)"', src):
            violations.append(f"{name}: 本地伪造失败响应")
        if re.search(r'"status":\s*"ok"', src):
            violations.append(f"{name}: 本地伪造成功响应")
        if "normalize_message_id" in src or "build_text_message" in src:
            violations.append(f"{name}: 引用参数改写辅助函数")
        if "raise ValueError" in src:
            violations.append(f"{name}: 本地参数校验拦截")
    assert not violations, "透传违规:\n" + "\n".join(violations)


def test_every_tool_returns_full_response() -> None:
    """每个 Tool 的 execute 都必须以透传双元组收尾。"""
    violations: list[str] = []
    for tool_cls in ALL_TOOLS:
        source = inspect.getsource(tool_cls.execute)
        if 'return result.get("status") == "ok", result' not in source:
            violations.append(tool_cls.name)
    assert not violations, f"未透传完整响应的 Tool: {violations}"


def test_api_client_is_pure_passthrough() -> None:
    """api_client 不得包含本地拦截逻辑。"""
    source = inspect.getsource(api_client)
    assert "snowluma_compat" not in source
    assert "napcat_only" not in source
    assert "enable_reaction" not in source
    assert "normalize_message_ids" not in source
    assert 'return await send_adapter_command(' in source


def test_tool_count_matches_api_count() -> None:
    """去重铁律：Tool 数与 APIDef 数一致。"""
    assert len(ALL_TOOLS) == len(ALL_APIS), (
        f"ALL_TOOLS={len(ALL_TOOLS)} != ALL_APIS={len(ALL_APIS)}"
    )


@pytest.mark.parametrize(
    "service_name",
    ["message_service", "napcat_ext_service", "qzone_service"],
)
def test_services_do_not_gate_calls(service_name: str) -> None:
    """关键 Service 不得在调用前做本地门控/拦截。"""
    import importlib

    from .. import services

    module_name = {
        "message_service": "message_service",
        "napcat_ext_service": "napcat_service",
        "qzone_service": "qzone_service",
    }[service_name]
    module = importlib.import_module(f"..services.{module_name}", __package__)
    source = io.open(inspect.getsourcefile(module), encoding="utf-8").read()

    # OneBot action 方法不得包含本地门控（qzone 内部能力除外）
    if service_name == "napcat_ext_service":
        assert "_is_reaction_emoji_enabled" not in source
        assert "get_emoji_by_id" not in source
    if service_name == "message_service":
        assert "_prepend_reply" not in source
        assert "reply_to_message_id" not in source
