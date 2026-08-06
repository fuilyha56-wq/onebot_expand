"""新增上游 action 的调用参数契约测试。"""

from types import SimpleNamespace
from typing import Any

import pytest

from onebot_expand import api_client
from onebot_expand.config import OnebotExpandConfig
from onebot_expand.services import (
    file_service,
    group_file_service,
    group_service,
    misc_service,
    user_ext_service,
)
from onebot_expand.tools import (
    file_tools,
    group_file_tools,
    group_tools,
    misc_tools,
    user_ext_tools,
)


@pytest.mark.asyncio
async def test_api_client_blocks_snowluma_incompatible_action(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SnowLuma 后端应在本地拒绝 NapCat 专属 action。"""
    config = OnebotExpandConfig()
    config.adapter.backend = "snowluma"
    calls: list[tuple[str, str, dict[str, Any], float]] = []

    async def fake_send(
        adapter_sign: str,
        command_name: str,
        command_data: dict[str, Any],
        timeout: float,
    ) -> dict[str, Any]:
        calls.append((adapter_sign, command_name, command_data, timeout))
        return {"status": "ok", "data": {}}

    monkeypatch.setattr(api_client, "get_config", lambda _name: config)
    monkeypatch.setattr(api_client, "send_adapter_command", fake_send)

    blocked = await api_client._call_onebot_api(
        "send_online_file",
        {"user_id": 10001, "file_path": "file.txt"},
    )
    await api_client._call_onebot_api("get_group_root_files", {"group_id": 10001})

    assert blocked["status"] == "failed"
    assert blocked["retcode"] == 1404
    assert calls == [
        (
            "onebot_adapter:adapter:onebot_adapter",
            "get_group_root_files",
            {"group_id": 10001},
            30.0,
        )
    ]


@pytest.mark.asyncio
async def test_api_client_rejects_snowluma_record_conversion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """SnowLuma 不应把被忽略的 out_format 冒充为已执行的转码。"""
    config = OnebotExpandConfig()
    config.adapter.backend = "snowluma"
    calls: list[tuple[str, str, dict[str, Any], float]] = []

    async def fake_send(
        adapter_sign: str,
        command_name: str,
        command_data: dict[str, Any],
        timeout: float,
    ) -> dict[str, Any]:
        calls.append((adapter_sign, command_name, command_data, timeout))
        return {"status": "ok", "data": {}}

    monkeypatch.setattr(api_client, "get_config", lambda _name: config)
    monkeypatch.setattr(api_client, "send_adapter_command", fake_send)

    rejected = await api_client._call_onebot_api(
        "download_file_record_stream",
        {"file_id": "record-id", "out_format": "mp3"},
    )
    original = await api_client._call_onebot_api(
        "download_file_record_stream",
        {"file_id": "record-id"},
    )
    config.adapter.backend = "napcat"
    converted = await api_client._call_onebot_api(
        "download_file_record_stream",
        {"file_id": "record-id", "out_format": "mp3"},
    )

    assert rejected["status"] == "failed"
    assert rejected["retcode"] == 1400
    assert "不支持 out_format 转码" in rejected["msg"]
    assert original["status"] == "ok"
    assert converted["status"] == "ok"
    assert calls == [
        (
            "onebot_adapter:adapter:onebot_adapter",
            "download_file_record_stream",
            {"file_id": "record-id"},
            30.0,
        ),
        (
            "onebot_adapter:adapter:onebot_adapter",
            "download_file_record_stream",
            {"file_id": "record-id", "out_format": "mp3"},
            30.0,
        ),
    ]


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
async def test_file_service_sends_exact_get_file_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """文件服务不应把响应字段 url 当作 get_file 请求参数发送。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "ok", "data": {}}

    monkeypatch.setattr(file_service, "_call_onebot_api", fake_call)

    await file_service.FileService(plugin=None).get_file("napcat-file-id")

    assert calls == [("get_file", {"file_id": "napcat-file-id"})]


@pytest.mark.asyncio
async def test_private_file_url_service_and_tool_send_snowluma_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """私聊文件 URL 的 Service 与 Tool 都应发送 SnowLuma 所需的 ID 和哈希。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "ok", "data": {"url": "http://file.example/download"}}

    monkeypatch.setattr(group_file_service, "_call_onebot_api", fake_call)
    monkeypatch.setattr(group_file_tools, "_call_onebot_api", fake_call)

    await group_file_service.GroupFileService(plugin=None).get_private_file_url(
        "snowluma-file-id",
        "snowluma-file-hash",
    )

    config = OnebotExpandConfig()
    config.api_switches.enable_all_tools = True
    config.api_switches.enable_get_private_file_url = True
    plugin = SimpleNamespace(config=config)
    success, result = await group_file_tools.GetPrivateFileUrlTool(
        plugin=plugin
    ).execute("snowluma-file-id", "snowluma-file-hash")

    assert success
    assert result == {"url": "http://file.example/download"}
    assert calls == [
        (
            "get_private_file_url",
            {
                "file_id": "snowluma-file-id",
                "file_hash": "snowluma-file-hash",
            },
        ),
        (
            "get_private_file_url",
            {
                "file_id": "snowluma-file-id",
                "file_hash": "snowluma-file-hash",
            },
        ),
    ]


@pytest.mark.asyncio
async def test_move_group_file_service_and_tool_send_snowluma_fields(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """移动群文件应使用 SnowLuma 的 parent_directory wire 字段。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "ok", "data": None}

    monkeypatch.setattr(group_file_service, "_call_onebot_api", fake_call)
    monkeypatch.setattr(group_file_tools, "_call_onebot_api", fake_call)

    await group_file_service.GroupFileService(plugin=None).move_group_file(
        10001,
        "file-id",
        "/source",
        "/target",
    )

    config = OnebotExpandConfig()
    config.api_switches.enable_all_tools = True
    config.api_switches.enable_move_group_file = True
    plugin = SimpleNamespace(config=config)
    success, _ = await group_file_tools.MoveGroupFileTool(plugin=plugin).execute(
        10001,
        "file-id",
        "/source",
        "/target",
    )

    assert success
    assert calls == [
        (
            "move_group_file",
            {
                "group_id": 10001,
                "file_id": "file-id",
                "parent_directory": "/source",
                "target_directory": "/target",
            },
        ),
        (
            "move_group_file",
            {
                "group_id": 10001,
                "file_id": "file-id",
                "parent_directory": "/source",
                "target_directory": "/target",
            },
        ),
    ]


@pytest.mark.asyncio
async def test_upload_file_stream_tool_preserves_zero_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """流式上传首块的索引 0 和显式 False 均不能被省略。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "ok", "data": {"type": "stream"}}

    monkeypatch.setattr(file_service, "_call_onebot_api", fake_call)
    monkeypatch.setattr("onebot_expand.tools.file_tools._call_onebot_api", fake_call)

    config = OnebotExpandConfig()
    config.api_switches.enable_all_tools = True
    config.api_switches.enable_upload_file_stream = True
    plugin = SimpleNamespace(config=config)

    await file_service.FileService(plugin=plugin).upload_file_stream(
        "stream-id",
        chunk_data="",
        chunk_index=0,
        total_chunks=1,
        file_size=0,
        is_complete=False,
        reset=False,
        verify_only=False,
    )
    success, _ = (
        await __import__(
            "onebot_expand.tools.file_tools", fromlist=["UploadFileStreamTool"]
        )
        .UploadFileStreamTool(plugin=plugin)
        .execute(
            "stream-id",
            chunk_data="",
            chunk_index=0,
            total_chunks=1,
            file_size=0,
            is_complete=False,
            reset=False,
            verify_only=False,
        )
    )

    assert success
    expected = {
        "stream_id": "stream-id",
        "file_retention": 0,
        "chunk_data": "",
        "chunk_index": 0,
        "total_chunks": 1,
        "file_size": 0,
        "is_complete": False,
        "reset": False,
        "verify_only": False,
    }
    assert calls == [
        ("upload_file_stream", expected),
        ("upload_file_stream", expected),
    ]


@pytest.mark.asyncio
async def test_upload_file_stream_tool_returns_completion_data(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """流式上传完成响应中的本地文件信息应返回给调用方。"""
    completion_data = {
        "type": "response",
        "file_path": "C:/Temp/snowluma-stream/upload/audit.txt",
        "file_size": 38,
        "sha256": "0123456789abcdef",
    }

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        assert action == "upload_file_stream"
        assert params == {
            "stream_id": "stream-id",
            "file_retention": 60000,
            "is_complete": True,
        }
        return {"status": "ok", "data": completion_data}

    monkeypatch.setattr(file_tools, "_call_onebot_api", fake_call)

    config = OnebotExpandConfig()
    config.api_switches.enable_all_tools = True
    config.api_switches.enable_upload_file_stream = True
    plugin = SimpleNamespace(config=config)
    success, result = await file_tools.UploadFileStreamTool(plugin=plugin).execute(
        "stream-id",
        is_complete=True,
        file_retention=60000,
    )

    assert success
    assert result == completion_data


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
