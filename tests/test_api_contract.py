"""onebot_expand API 注册表同步契约测试。"""

import json
from pathlib import Path

from onebot_expand.api_defs import ALL_APIS, resolve_action
from onebot_expand.config import OnebotExpandConfig
from onebot_expand.tools import ALL_TOOLS

EXPECTED_ACTIONS = {
    "send_pb": {"cmd": "str", "hex": "str"},
    "set_friends_category": {
        "uin": "int",
        "categoryId": "int",
        "categoryName": "str",
    },
    "set_group_member_invite_policy": {"group_id": "str", "policy": "str"},
    "set_group_member_permissions": {
        "group_id": "str",
        "allow_member_upload_album": "bool",
        "allow_member_temporary_session": "bool",
        "allow_member_create_group": "bool",
    },
    "set_group_new_member_history_visibility": {
        "group_id": "str",
        "visible": "bool",
    },
}


def test_api_registry_has_expected_upstream_actions() -> None:
    """上游新增 action 应以精确参数契约注册。"""
    assert len(ALL_APIS) == 211
    for action, params in EXPECTED_ACTIONS.items():
        assert ALL_APIS[action].params == params


def test_api_tools_switches_and_aliases_are_one_to_one() -> None:
    """主 action、Tool 与独立开关应严格一一对应且别名不冲突。"""
    tool_names = [tool.tool_name for tool in ALL_TOOLS]
    aliases = [alias for api in ALL_APIS.values() for alias in api.aliases]
    switch_fields = {
        field_name.removeprefix("enable_")
        for field_name in OnebotExpandConfig.ApiSwitchesSection.model_fields
        if field_name.startswith("enable_") and field_name != "enable_all_tools"
    }

    assert len(ALL_TOOLS) == len(ALL_APIS) == len(tool_names) == 211
    assert len(set(tool_names)) == len(tool_names)
    assert set(tool_names) == set(ALL_APIS)
    assert switch_fields == set(ALL_APIS)
    assert len(aliases) == len(set(aliases)) == 18
    assert not set(aliases) & set(ALL_APIS)
    assert all(resolve_action(alias) in ALL_APIS for alias in aliases)


def test_all_tool_switches_default_to_disabled() -> None:
    """总开关和每个 action 开关都必须默认关闭。"""
    switches = OnebotExpandConfig.ApiSwitchesSection()

    assert not switches.enable_all_tools
    assert all(
        not getattr(switches, field_name)
        for field_name in OnebotExpandConfig.ApiSwitchesSection.model_fields
        if field_name.startswith("enable_")
    )


def test_manifest_statically_includes_services_only() -> None:
    """动态组件不应在 manifest 中重复静态注册。"""
    manifest_path = Path(__file__).parents[1] / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert len(manifest["include"]) == 23
    assert {item["component_type"] for item in manifest["include"]} == {"service"}
