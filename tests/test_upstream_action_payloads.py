"""新增上游 action 的调用参数契约测试。"""

from types import SimpleNamespace
from typing import Any

import pytest

from .. import api_client
from ..config import OnebotExpandConfig
from ..services import (
    ark_service,
    emoji_ext_service,
    file_service,
    group_file_service,
    group_ext_service,
    group_service,
    group_todo_service,
    misc_service,
    user_ext_service,
)
from ..tools import (
    emoji_ext_tools,
    file_tools,
    group_file_tools,
    group_ext_tools,
    group_tools,
    misc_tools,
    user_ext_tools,
)


@pytest.mark.asyncio
async def test_new_snowluma_action_payloads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """新增 SnowLuma 动作应传递与上游 schema 一致的参数。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "ok", "data": {}}

    monkeypatch.setattr(emoji_ext_service, "_call_onebot_api", fake_call)
    monkeypatch.setattr(group_todo_service, "_call_onebot_api", fake_call)

    emoji = emoji_ext_service.EmojiExtService(plugin=None)
    todo = group_todo_service.GroupTodoService(plugin=None)
    await emoji.fetch_sys_faces()
    await emoji.fetch_face_entity(14, refresh=True)
    await emoji.search_sys_faces("开心")
    await emoji.fetch_super_face_id(14)
    await todo.get_group_todo_list(10001)

    assert calls == [
        ("fetch_sys_faces", {"refresh": False}),
        ("fetch_face_entity", {"face_id": 14, "refresh": True}),
        ("search_sys_faces", {"query": "开心"}),
        ("fetch_super_face_id", {"face_id": 14, "refresh": False}),
        ("get_group_todo_list", {"group_id": 10001}),
    ]


@pytest.mark.asyncio
async def test_20260827_new_action_payloads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """2026-08-27 新增的 SnowLuma action 应传递与上游 schema 一致的参数。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "ok", "data": {}}

    monkeypatch.setattr(group_service, "_call_onebot_api", fake_call)
    monkeypatch.setattr(emoji_ext_service, "_call_onebot_api", fake_call)
    monkeypatch.setattr(ark_service, "_call_onebot_api", fake_call)

    group = group_service.GroupService(plugin=None)
    emoji = emoji_ext_service.EmojiExtService(plugin=None)
    ark = ark_service.ArkService(plugin=None)
    await group.get_admin_settings(10001)
    await emoji.get_msg_emoji_likes(-123456)
    await ark.send_tuwen_ark(
        title="标题",
        desc="描述",
        jump_url="https://example.com",
        group_id=10001,
    )
    # 原样透传：不指定目标也照发，由协议端返回错误
    await ark.send_tuwen_ark(title="t", desc="d", jump_url="u")

    assert calls == [
        ("get_group_admin_settings", {"group_id": 10001}),
        ("get_msg_emoji_likes", {"message_id": -123456}),
        (
            "send_tuwen_ark",
            {
                "title": "标题",
                "desc": "描述",
                "summary": "[分享]",
                "preview_url": "https://tangram-1251316161.file.myqcloud.com/files/20210721/e50a8e37e08f29bf1ffc7466e1950690.png",
                "jump_url": "https://example.com",
                "group_id": 10001,
            },
        ),
        (
            "send_tuwen_ark",
            {
                "title": "t",
                "desc": "d",
                "summary": "[分享]",
                "preview_url": "https://tangram-1251316161.file.myqcloud.com/files/20210721/e50a8e37e08f29bf1ffc7466e1950690.png",
                "jump_url": "u",
            },
        ),
    ]


@pytest.mark.asyncio
async def test_get_group_share_link_payloads(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """NapCat 群分享链接 API 应只透传调用方显式提供的字段。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "ok", "retcode": 0, "data": {"url": "https://qm.qq.com/q/x"}}

    monkeypatch.setattr(group_ext_service, "_call_onebot_api", fake_call)
    monkeypatch.setattr(group_ext_tools, "_call_onebot_api", fake_call)

    service = group_ext_service.GroupExtService(plugin=None)
    await service.get_group_share_link("10001")
    await service.get_group_share_link(
        "10001",
        need_short_url="false",
        src_id="73",
        additional_param="from-test",
    )

    config = OnebotExpandConfig()
    config.api_switches.enable_all_tools = True
    config.api_switches.enable_get_group_share_link = True
    plugin = SimpleNamespace(config=config)
    success, result = await group_ext_tools.GetGroupShareLinkTool(plugin=plugin).execute(
        10001,
        need_short_url=False,
        src_id=73,
        additional_param="from-tool",
    )

    assert success is True
    assert result["data"]["url"] == "https://qm.qq.com/q/x"
    assert calls == [
        ("get_group_share_link", {"group_id": "10001"}),
        (
            "get_group_share_link",
            {
                "group_id": "10001",
                "need_short_url": "false",
                "src_id": "73",
                "additional_param": "from-test",
            },
        ),
        (
            "get_group_share_link",
            {
                "group_id": 10001,
                "need_short_url": False,
                "src_id": 73,
                "additional_param": "from-tool",
            },
        ),
    ]


@pytest.mark.asyncio
async def test_fetch_face_entity_tool_preserves_null_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """表情编号不存在时 Tool 应原样透传 SnowLuma 的完整响应。"""

    async def fake_call(_action: str, _params: dict[str, Any]) -> dict[str, Any]:
        return {"status": "ok", "retcode": 0, "data": None, "echo": "e-1"}

    monkeypatch.setattr(emoji_ext_tools, "_call_onebot_api", fake_call)
    plugin = SimpleNamespace(
        config=SimpleNamespace(
            api_switches=SimpleNamespace(
                enable_all_tools=True,
                enable_fetch_face_entity=True,
            )
        )
    )
    tool = emoji_ext_tools.FetchFaceEntityTool(plugin=plugin)

    success, result = await tool.execute(999999)

    assert success is True
    assert result == {"status": "ok", "retcode": 0, "data": None, "echo": "e-1"}


@pytest.mark.asyncio
async def test_api_client_passes_through_snowluma_incompatible_action(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """原样透传铁律：SnowLuma 后端也不得本地拦截，照发协议端。"""
    calls: list[tuple[str, str, dict[str, Any], float]] = []

    async def fake_send(
        adapter_sign: str,
        command_name: str,
        command_data: dict[str, Any],
        timeout: float,
    ) -> dict[str, Any]:
        calls.append((adapter_sign, command_name, command_data, timeout))
        return {"status": "failed", "retcode": 1404, "data": None, "msg": "不支持"}

    monkeypatch.setattr(api_client, "send_adapter_command", fake_send)

    sent = await api_client._call_onebot_api(
        "send_online_file",
        {"user_id": 10001, "file_path": "file.txt"},
    )
    sent_pb = await api_client._call_onebot_api(
        "send_pb",
        {"cmd": "trpc.test", "hex": "0a00"},
    )
    passed = await api_client._call_onebot_api("get_group_root_files", {"group_id": 10001})

    # 全部照发协议端，协议端的失败响应原样透传回来
    assert sent["status"] == "failed"
    assert sent_pb["status"] == "failed"
    assert passed["status"] == "failed"
    assert [c[1] for c in calls] == [
        "send_online_file",
        "send_pb",
        "get_group_root_files",
    ]


@pytest.mark.asyncio
async def test_api_client_passes_through_out_format(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """原样透传铁律：out_format 不在本地拦截，由协议端自行处理。"""
    calls: list[tuple[str, str, dict[str, Any], float]] = []

    async def fake_send(
        adapter_sign: str,
        command_name: str,
        command_data: dict[str, Any],
        timeout: float,
    ) -> dict[str, Any]:
        calls.append((adapter_sign, command_name, command_data, timeout))
        return {"status": "ok", "data": {}}

    monkeypatch.setattr(api_client, "send_adapter_command", fake_send)

    with_format = await api_client._call_onebot_api(
        "download_file_record_stream",
        {"file_id": "record-id", "out_format": "mp3"},
    )
    without_format = await api_client._call_onebot_api(
        "download_file_record_stream",
        {"file_id": "record-id"},
    )

    assert with_format["status"] == "ok"
    assert without_format["status"] == "ok"
    assert calls == [
        (
            "onebot_adapter:adapter:onebot_adapter",
            "download_file_record_stream",
            {"file_id": "record-id", "out_format": "mp3"},
            30.0,
        ),
        (
            "onebot_adapter:adapter:onebot_adapter",
            "download_file_record_stream",
            {"file_id": "record-id"},
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
async def test_group_service_passes_through_empty_member_permissions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """原样透传铁律：空权限请求也照发协议端，由协议端返回错误。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "failed", "retcode": 1200, "data": None}

    monkeypatch.setattr(group_service, "_call_onebot_api", fake_call)
    service = group_service.GroupService(plugin=None)

    result = await service.set_member_permissions("10001")

    assert result["status"] == "failed"
    assert calls == [("set_group_member_permissions", {"group_id": "10001"})]


@pytest.mark.asyncio
async def test_user_service_passes_through_friend_category_selector(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """原样透传铁律：分类选择参数不做本地校验，全部照发。"""
    calls: list[tuple[str, dict[str, Any]]] = []

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        calls.append((action, params))
        return {"status": "ok", "data": None}

    monkeypatch.setattr(user_ext_service, "_call_onebot_api", fake_call)
    service = user_ext_service.UserExtService(plugin=None)

    await service.set_friends_category(10002, category_id=3)
    await service.set_friends_category(10002, category_name="同事")
    # 透传：零个或两个选择参数都照发，由协议端处理
    await service.set_friends_category(10002)
    await service.set_friends_category(10002, category_id=3, category_name="同事")

    assert calls == [
        ("set_friends_category", {"uin": 10002, "categoryId": 3}),
        ("set_friends_category", {"uin": 10002, "categoryName": "同事"}),
        ("set_friends_category", {"uin": 10002}),
        (
            "set_friends_category",
            {"uin": 10002, "categoryId": 3, "categoryName": "同事"},
        ),
    ]


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
    # 原样透传：返回协议端的完整响应字典而非 data 子集
    assert result == {
        "status": "ok",
        "data": {"url": "http://file.example/download"},
    }
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
    monkeypatch.setattr(file_tools, "_call_onebot_api", fake_call)

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
        await file_tools.UploadFileStreamTool(plugin=plugin)
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
    """原样透传：流式上传的完整响应（含 data 内本地文件信息）逐字段返回。"""
    completion_data = {
        "type": "response",
        "file_path": "C:/Temp/snowluma-stream/upload/audit.txt",
        "file_size": 38,
        "sha256": "0123456789abcdef",
    }
    full_response = {
        "status": "ok",
        "retcode": 0,
        "data": completion_data,
        "echo": "echo-1",
    }

    async def fake_call(action: str, params: dict[str, Any]) -> dict[str, Any]:
        assert action == "upload_file_stream"
        assert params == {
            "stream_id": "stream-id",
            "file_retention": 60000,
            "is_complete": True,
        }
        return full_response

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
    assert result == full_response


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

    # 原样透传铁律：本地不做参数形态校验，缺参数也照发协议端
    await group_tools.SetGroupMemberPermissionsTool(plugin=plugin).execute("10001")
    await user_ext_tools.SetFriendsCategoryTool(plugin=plugin).execute(10002)
    assert calls[-2:] == [
        ("set_group_member_permissions", {"group_id": "10001"}),
        ("set_friends_category", {"uin": 10002}),
    ]
