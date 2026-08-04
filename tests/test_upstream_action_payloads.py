"""新增上游 action 的调用参数契约测试。"""

from types import SimpleNamespace
from typing import Any

import pytest

from onebot_expand.config import OnebotExpandConfig
from onebot_expand.services import group_service, misc_service, user_ext_service
from onebot_expand.tools import group_tools, misc_tools, user_ext_tools


@pytest.mark.asyncio
async def test_group_service_maps_new_action_payloads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """群服务应发送精确 wire 参数并省略未设置权限。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "ok", "data": None}

    monkeypatch.setattr(group_service, "_call_onebot_api", fake_call)
    service = group_service.GroupService(plugin=None)

    await service.set_member_invite_policy("10001", "require_approval")
    await service.set_member_permissions(
        "10001",
        allow_member_upload_album=False,
    )
    await service.set_new_member_history_visibility("10001", True)

    assert calls == [
        (
            "set_group_member_invite_policy",
            {"group_id": "10001", "policy": "require_approval"},
        ),
        (
            "set_group_member_permissions",
            {"group_id": "10001", "allow_member_upload_album": False},
        ),
        (
            "set_group_new_member_history_visibility",
            {"group_id": "10001", "visible": True},
        ),
    ]


@pytest.mark.asyncio
async def test_group_service_rejects_empty_member_permissions() -> None:
    """群服务不应发送没有任何权限项的请求。"""
    service = group_service.GroupService(plugin=None)

    with pytest.raises(ValueError, match="至少需要提供一个群成员功能权限"):
        await service.set_member_permissions("10001")


@pytest.mark.asyncio
async def test_user_service_requires_one_friend_category_selector(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """好友分类服务应要求分类 ID 与名称恰好提供一个。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "ok", "data": None}

    monkeypatch.setattr(user_ext_service, "_call_onebot_api", fake_call)
    service = user_ext_service.UserExtService(plugin=None)

    await service.set_friends_category(10002, category_id=3)
    await service.set_friends_category(10002, category_name="同事")

    assert calls == [
        ("set_friends_category", {"uin": 10002, "categoryId": 3}),
        ("set_friends_category", {"uin": 10002, "categoryName": "同事"}),
    ]
    with pytest.raises(ValueError, match="恰好提供一个"):
        await service.set_friends_category(10002)
    with pytest.raises(ValueError, match="恰好提供一个"):
        await service.set_friends_category(10002, category_id=3, category_name="同事")


@pytest.mark.asyncio
async def test_misc_service_maps_hex_data_to_wire_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """PB 服务应将 Python 参数 hex_data 映射为 wire 键 hex。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "ok", "data": {}}

    monkeypatch.setattr(misc_service, "_call_onebot_api", fake_call)

    await misc_service.MiscService(plugin=None).send_pb("trpc.test", "0a00")

    assert calls == [("send_pb", {"cmd": "trpc.test", "hex": "0a00"})]


@pytest.mark.asyncio
async def test_new_tools_map_payloads_and_validate_optional_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """新增 Tool 应复用与 Service 相同的 wire 参数契约。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "ok", "data": None}

    monkeypatch.setattr(group_tools, "_call_onebot_api", fake_call)
    monkeypatch.setattr(user_ext_tools, "_call_onebot_api", fake_call)
    monkeypatch.setattr(misc_tools, "_call_onebot_api", fake_call)

    config = OnebotExpandConfig()
    config.api_switches.enable_all_tools = True
    config.api_switches.enable_set_group_member_invite_policy = True
    config.api_switches.enable_set_group_member_permissions = True
    config.api_switches.enable_set_group_new_member_history_visibility = True
    config.api_switches.enable_set_friends_category = True
    config.api_switches.enable_send_pb = True
    plugin = SimpleNamespace(config=config)

    await group_tools.SetGroupMemberInvitePolicyTool(plugin=plugin).execute(
        "10001", "disabled"
    )
    await group_tools.SetGroupMemberPermissionsTool(plugin=plugin).execute(
        "10001",
        allow_member_temporary_session=True,
    )
    await group_tools.SetGroupNewMemberHistoryVisibilityTool(plugin=plugin).execute(
        "10001", False
    )
    await user_ext_tools.SetFriendsCategoryTool(plugin=plugin).execute(
        10002, category_name="同事"
    )
    await misc_tools.SendPBTool(plugin=plugin).execute("trpc.test", "0a00")

    assert calls == [
        (
            "set_group_member_invite_policy",
            {"group_id": "10001", "policy": "disabled"},
        ),
        (
            "set_group_member_permissions",
            {"group_id": "10001", "allow_member_temporary_session": True},
        ),
        (
            "set_group_new_member_history_visibility",
            {"group_id": "10001", "visible": False},
        ),
        ("set_friends_category", {"uin": 10002, "categoryName": "同事"}),
        ("send_pb", {"cmd": "trpc.test", "hex": "0a00"}),
    ]

    with pytest.raises(ValueError, match="至少需要提供一个群成员功能权限"):
        await group_tools.SetGroupMemberPermissionsTool(plugin=plugin).execute("10001")
    with pytest.raises(ValueError, match="恰好提供一个"):
        await user_ext_tools.SetFriendsCategoryTool(plugin=plugin).execute(10002)
