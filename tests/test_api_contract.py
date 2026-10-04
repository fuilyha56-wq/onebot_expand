"""onebot_expand API 注册表同步契约测试。"""

import json
from pathlib import Path

from ..api_defs import ALL_APIS, APICategory, resolve_action
from ..config import OnebotExpandConfig
from ..tools import ALL_TOOLS

EXPECTED_ACTIONS = {
    "download_file_record_stream": {
        "file": "str",
        "file_id": "str",
        "chunk_size": "int",
        "out_format": "str",
    },
    "get_file": {"file_id": "str"},
    "move_group_file": {
        "group_id": "int",
        "file_id": "str",
        "parent_directory": "str",
        "target_directory": "str",
    },
    "get_private_file_url": {
        "user_id": "int",
        "file_id": "str",
        "file_hash": "str",
    },
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
    "get_group_admin_settings": {"group_id": "int"},
    "get_group_share_link": {
        "group_id": "int | str",
        "need_short_url": "bool | str",
        "src_id": "int | str",
        "additional_param": "str",
    },
    "get_msg_emoji_likes": {"message_id": "int | str"},
    "send_tuwen_ark": {
        "user_id": "int",
        "group_id": "int",
        "title": "str",
        "desc": "str",
        "summary": "str",
        "preview_url": "str",
        "jump_url": "str",
    },
}


def test_api_registry_has_expected_upstream_actions() -> None:
    """上游新增 action 应以精确参数契约注册。"""
    assert len(ALL_APIS) == 220
    for action, params in EXPECTED_ACTIONS.items():
        assert ALL_APIS[action].params == params


def test_super_face_action_describes_boolean_result() -> None:
    """超级表情 action 应准确描述其布尔判断结果。"""
    assert ALL_APIS["fetch_super_face_id"].description == (
        "判断系统表情是否使用超级表情格式（SnowLuma 扩展）"
    )


def test_current_snowluma_actions_are_marked_compatible() -> None:
    """SnowLuma 当前已注册的 action 不应被本地兼容层拦截。"""
    actions = {
        "fetch_custom_face_detail",
        "set_group_member_invite_policy",
        "set_group_member_permissions",
        "set_group_new_member_history_visibility",
    }

    assert all(ALL_APIS[action].snowluma_compat for action in actions)
    assert all(not ALL_APIS[action].napcat_only for action in actions)
    assert not ALL_APIS["get_word_slices"].snowluma_compat
    assert not ALL_APIS["send_pb"].snowluma_compat


def test_unregistered_snowluma_actions_are_marked_incompatible() -> None:
    """SnowLuma 未注册的 action 不应依赖默认值被误判为兼容。"""
    actions = {
        "batch_delete_group_member",
        "create_group_album",
        "delete_group_album",
        "get_config",
        "get_event",
        "get_guild_list",
        "get_profile_like_count",
        "get_profile_like_me",
        "get_qq_avatar",
        "get_recommend_face",
        "llonebot_debug",
        "scan_qrcode",
        "set_config",
        "set_friend_category",
        "set_group_msg_mask",
        "unset_msg_emoji_like",
    }

    assert all(not ALL_APIS[action].snowluma_compat for action in actions)


def test_record_stream_registry_describes_backend_conversion_limit() -> None:
    """语音流注册描述必须明确 SnowLuma 不执行 out_format 转码。"""
    description = ALL_APIS["download_file_record_stream"].description

    assert "NapCat 支持 out_format 转码" in description
    assert "SnowLuma 仅下载原始格式" in description


def test_api_tools_switches_and_aliases_are_one_to_one() -> None:
    """主 action、Tool 与独立开关应严格一一对应且别名不冲突。"""
    tool_names = [tool.name for tool in ALL_TOOLS]
    aliases = [alias for api in ALL_APIS.values() for alias in api.aliases]
    switch_fields = {
        field_name.removeprefix("enable_")
        for group_field in OnebotExpandConfig.ApiSwitchesSection.model_fields.values()
        for field_name in group_field.annotation.model_fields
        if field_name != "enable_all_tools"
    }

    assert len(ALL_TOOLS) == len(ALL_APIS) == len(tool_names) == 220
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
        not getattr(group, field_name)
        for group_name in OnebotExpandConfig.ApiSwitchesSection.model_fields
        for group in [getattr(switches, group_name)]
        for field_name in type(group).model_fields
    )


def test_api_switches_are_grouped_for_generic_webui() -> None:
    """工具开关应由配置模型按 API 分类暴露为 WebUI 子页面。"""
    switches = OnebotExpandConfig.ApiSwitchesSection()
    expected_groups = {"registration", *(category.value for category in APICategory)}

    assert set(type(switches).model_fields) == expected_groups
    assert set(type(switches.registration).model_fields) == {"enable_all_tools"}

    for category in APICategory:
        group = getattr(switches, category.value)
        expected_fields = {
            f"enable_{action}"
            for action, api_def in ALL_APIS.items()
            if api_def.category is category
        }
        assert set(type(group).model_fields) == expected_fields

    switches.enable_send_group_msg = True
    switches.message.enable_send_private_msg = True

    assert switches.message.enable_send_group_msg
    assert switches.enable_send_private_msg
    assert (
        type(switches.message)
        .model_fields["enable_send_group_msg"]
        .json_schema_extra["label"]
        == "发送群消息"
    )


def test_legacy_flat_api_switches_migrate_without_losing_values(
    tmp_path: Path,
) -> None:
    """旧版平铺工具开关应在加载时无损迁移到分类子节。"""
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        "[api_switches]\n"
        "enable_all_tools = true\n"
        "enable_send_group_msg = true\n"
        "enable_get_login_info = true\n",
        encoding="utf-8",
    )

    config = OnebotExpandConfig.load(config_path, auto_update=True)
    migrated_text = config_path.read_text(encoding="utf-8")

    assert config.api_switches.enable_all_tools
    assert config.api_switches.enable_send_group_msg
    assert config.api_switches.enable_get_login_info
    assert "[api_switches.registration]" in migrated_text
    assert "[api_switches.message]" in migrated_text
    assert "[api_switches.account]" in migrated_text


def test_manifest_statically_includes_services_only() -> None:
    """动态组件不应在 manifest 中重复静态注册。"""
    manifest_path = Path(__file__).parents[1] / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert len(manifest["include"]) == 23
    assert {item["component_type"] for item in manifest["include"]} == {"service"}
