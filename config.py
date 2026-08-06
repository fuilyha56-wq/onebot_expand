"""onebot_expand 插件配置。

定义 OneBot v11 标准 API 与 NapCat 扩展 API 的全部配置项，包括：
    - 插件启用与版本
    - 适配器签名与协议端
    - 每个 API 的独立开关
    - 表情发送与回应的开关
    - 文件传输模式（路径映射/base64/共享卷）
    - 协议端后端类型

配置文件默认路径: ``config/plugins/onebot_expand/config.toml``

起：API 开关按主名生成；旧配置中可能出现的别名开关（如
``enable_nc_get_rkey``）会在加载时通过 :func:`_normalize_config_key`
映射到主名（如 ``enable_get_rkey``），向后兼容。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar, Self, cast
import tomllib

from pydantic import create_model

from src.app.plugin_system.base import BaseConfig, Field, SectionBase, config_section

from .api_defs import ALL_APIS, APICategory

__all__ = ["OnebotExpandConfig"]


def _normalize_config_key(key: str) -> str:
    """将别名配置键映射到主名配置键。

    所有 API 开关按主名生成。若旧配置文件使用别名键
    （如 ``enable_nc_get_rkey``），加载时会被映射到主名键
    （如 ``enable_get_rkey``），保证旧配置仍然生效。

    未识别的键原样返回。

    Args:
        key: 原始配置键名。

    Returns:
        规范化后的配置键名。
    """
    # 延迟导入避免循环依赖
    from .api_defs import resolve_action

    if not key.startswith("enable_"):
        return key
    action = key[7:]
    primary = resolve_action(action)
    if primary is None:
        return key
    return f"enable_{primary}"


_API_CATEGORY_TITLES: dict[APICategory, str] = {
    APICategory.MESSAGE: "消息工具",
    APICategory.GROUP: "群管理工具",
    APICategory.FILE: "文件工具",
    APICategory.ACCOUNT: "账号信息工具",
    APICategory.NAPCAT_EXT: "NapCat 扩展工具",
    APICategory.GROUP_FILE: "群文件工具",
    APICategory.GROUP_NOTICE: "群公告工具",
    APICategory.GROUP_EXT: "群管理扩展工具",
    APICategory.REQUEST: "请求处理工具",
    APICategory.USER_EXT: "用户信息工具",
    APICategory.STATUS: "在线状态工具",
    APICategory.POKE: "戳一戳工具",
    APICategory.EMOJI_EXT: "表情与收藏工具",
    APICategory.AI_VOICE: "AI 语音工具",
    APICategory.CRED: "凭证与安全工具",
    APICategory.MISC: "其他工具",
    APICategory.FLASH: "闪传工具",
    APICategory.GROUP_ALBUM: "群相册工具",
    APICategory.GROUP_TODO: "群待办工具",
    APICategory.QZONE: "QQ 空间工具",
    APICategory.ARK: "Ark 分享工具",
}

_API_SWITCH_LABEL_OVERRIDES = {
    "send_msg": "发送通用消息",
    "send_group_msg": "发送群消息",
    "send_private_msg": "发送私聊消息",
}

_API_SWITCH_FIELD_TO_GROUP = {
    "enable_all_tools": "registration",
    **{
        f"enable_{action}": api_def.category.value
        for action, api_def in ALL_APIS.items()
    },
}


class _GroupedApiSwitchesBase(SectionBase):
    """按类别组织工具开关，并兼容原有平铺属性访问。"""

    _field_to_group: ClassVar[dict[str, str]] = _API_SWITCH_FIELD_TO_GROUP

    def __getattr__(self, name: str) -> Any:
        """读取旧式平铺开关属性。

        Args:
            name: 属性名称。

        Returns:
            对应分类子节中的字段值。
        """
        group_name = type(self)._field_to_group.get(name)
        if group_name is not None:
            group = object.__getattribute__(self, group_name)
            return getattr(group, name)
        return super().__getattr__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """写入旧式平铺开关属性。

        Args:
            name: 属性名称。
            value: 新字段值。
        """
        group_name = type(self)._field_to_group.get(name)
        if group_name is not None and name not in type(self).model_fields:
            group = object.__getattribute__(self, group_name)
            setattr(group, name, value)
            return
        super().__setattr__(name, value)


def _build_grouped_api_switches_section(
    flat_model: type[SectionBase],
) -> type[_GroupedApiSwitchesBase]:
    """从平铺开关模型生成按 API 类别分组的配置节。

    Args:
        flat_model: 包含全部工具开关字段的平铺模型。

    Returns:
        可由通用 WebUI 解析器直接渲染的分组配置节模型。

    Raises:
        RuntimeError: 平铺开关与 API 注册表不一致。
    """
    expected_fields = set(_API_SWITCH_FIELD_TO_GROUP)
    actual_fields = set(flat_model.model_fields)
    if actual_fields != expected_fields:
        missing_fields = sorted(expected_fields - actual_fields)
        extra_fields = sorted(actual_fields - expected_fields)
        raise RuntimeError(
            "onebot_expand 工具开关与 API 注册表不一致: "
            f"缺少={missing_fields}, 多余={extra_fields}"
        )

    section_models: dict[str, type[SectionBase]] = {}
    registration_field = flat_model.model_fields["enable_all_tools"]
    registration_model = cast(
        type[SectionBase],
        create_model(
            "RegistrationSwitchesSection",
            __base__=SectionBase,
            __module__=__name__,
            enable_all_tools=(
                registration_field.annotation,
                Field(
                    default=False,
                    description=registration_field.description or "",
                    label="启用工具注册",
                    input_type="switch",
                ),
            ),
        ),
    )
    section_models["registration"] = config_section(
        "registration",
        title="工具注册",
        description="开启总开关后，只有对应分类中启用的工具会被注册。",
        tag="plugin",
    )(registration_model)

    for category in APICategory:
        field_definitions: dict[str, tuple[Any, Any]] = {}
        for action, api_def in ALL_APIS.items():
            if api_def.category is not category:
                continue
            field_name = f"enable_{action}"
            source_field = flat_model.model_fields[field_name]
            field_definitions[field_name] = (
                source_field.annotation,
                Field(
                    default=False,
                    description=source_field.description or "",
                    label=_API_SWITCH_LABEL_OVERRIDES.get(action, api_def.description),
                    input_type="switch",
                ),
            )

        model_name = "".join(part.title() for part in category.value.split("_"))
        category_model = cast(
            type[SectionBase],
            create_model(
                f"{model_name}SwitchesSection",
                __base__=SectionBase,
                __module__=__name__,
                **field_definitions,
            ),
        )
        section_models[category.value] = config_section(
            category.value,
            title=_API_CATEGORY_TITLES[category],
            description="开启需要注册的工具；保存后按 WebUI 设置决定是否热重载。",
            tag="plugin",
        )(category_model)

    grouped_fields: dict[str, tuple[Any, Any]] = {
        group_name: (
            section_model,
            Field(
                default_factory=section_model,
                description=getattr(section_model, "__config_section_description__", "")
                or "",
            ),
        )
        for group_name, section_model in section_models.items()
    }
    grouped_model = cast(
        type[_GroupedApiSwitchesBase],
        create_model(
            "ApiSwitchesSection",
            __base__=_GroupedApiSwitchesBase,
            __module__=__name__,
            **grouped_fields,
        ),
    )
    return config_section(
        "api_switches",
        title="工具开关",
        description="按功能分类控制可供 LLM 调用的 OneBot 工具。",
        tag="plugin",
    )(grouped_model)


def _migrate_legacy_api_switches(
    data: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    """把旧版平铺 api_switches 转换为分类子节。

    Args:
        data: 完整配置数据。

    Returns:
        迁移后的配置数据，以及是否发生迁移。
    """
    raw_switches = data.get("api_switches")
    if not isinstance(raw_switches, dict):
        return data, False

    flat_keys = [
        key
        for key in raw_switches
        if isinstance(key, str) and key.startswith("enable_")
    ]
    if not flat_keys:
        return data, False

    grouped_switches: dict[str, Any] = {
        key: dict(value) if isinstance(value, dict) else value
        for key, value in raw_switches.items()
        if key not in flat_keys
    }
    for key in flat_keys:
        normalized_key = _normalize_config_key(key)
        group_name = _API_SWITCH_FIELD_TO_GROUP.get(normalized_key)
        if group_name is None:
            grouped_switches[key] = raw_switches[key]
            continue
        group_data = grouped_switches.setdefault(group_name, {})
        if not isinstance(group_data, dict):
            group_data = {}
            grouped_switches[group_name] = group_data
        group_data[normalized_key] = raw_switches[key]

    migrated = dict(data)
    migrated["api_switches"] = grouped_switches
    return migrated, True


class OnebotExpandConfig(BaseConfig):
    """onebot_expand 插件配置。

    配置文件路径: ``config/plugins/onebot_expand/config.toml``

    配置节:
        - plugin: 插件启用与版本
        - adapter: 适配器签名、默认超时、协议端
        - api_switches: 每个 API 的独立开关
        - emoji: 表情发送与回应开关
        - file_transfer: 文件传输模式配置
        - protocol: 协议端后端与兼容模式
    """

    name: ClassVar[str] = "config"
    description: ClassVar[str] = "OneBot Expand 插件配置"

    # ==================== plugin 节 ====================
    @config_section("plugin")
    class PluginSection(SectionBase):
        """插件基本配置。"""

        enabled: bool = Field(
            default=True,
            description="是否启用 onebot_expand 插件",
        )
        config_version: str = Field(
            default="1.0.0",
            description="配置文件版本号，用于版本追踪与迁移",
        )

    # ==================== adapter 节 ====================
    @config_section("adapter")
    class AdapterSection(SectionBase):
        """适配器与协议端配置。"""

        adapter_signature: str = Field(
            default="onebot_adapter:adapter:onebot_adapter",
            description="onebot_adapter 适配器签名，用于 adapter_api.get_adapter() 定位适配器实例",
        )
        default_timeout: float = Field(
            default=30.0,
            description="API 调用默认超时时间（秒），超时后返回超时错误",
            ge=1.0,
        )
        protocol: str = Field(
            default="napcat",
            description="协议端类型: napcat 或 snowluma",
        )

    # ==================== api_switches 节 ====================
    class _FlatApiSwitchesSection(SectionBase):
        """API 级独立开关的字段权威定义。

        每个 API 拥有独立的布尔开关，格式为 ``enable_<api_name>``，默认全部 False。
        工具注册受总开关 ``enable_all_tools`` 和独立开关双重控制（见下）。
        服务不受这些开关影响，始终注册并可调用。

        ``enable_all_tools`` 是工具总开关（默认 False）：
        - True：只注册独立开关为 True 的工具。
        - False（默认）：不注册任何工具，无论独立开关如何。
        服务不受此开关影响，始终注册，供其他插件调用。
        """

        # --- 工具总开关 ---
        enable_all_tools: bool = Field(
            default=False,
            description="工具总开关。开启时只注册独立开关为真的工具；关闭时不注册任何工具。服务不受影响。",
        )

        # --- 消息类 API (18) ---
        enable_send_group_msg: bool = Field(
            default=False,
            description="是否启用 send_group_msg API（发送群聊消息）",
        )
        enable_send_private_msg: bool = Field(
            default=False,
            description="是否启用 send_private_msg API（发送私聊消息）",
        )
        enable_send_msg: bool = Field(
            default=False,
            description="是否启用 send_msg API（通用发消息，按 message_type 自动路由）",
        )
        enable_delete_msg: bool = Field(
            default=False,
            description="是否启用 delete_msg API（撤回消息）",
        )
        enable_get_msg: bool = Field(
            default=False,
            description="是否启用 get_msg API（获取消息详情）",
        )
        enable_get_forward_msg: bool = Field(
            default=False,
            description="是否启用 get_forward_msg API（获取合并转发消息内容）",
        )
        enable_send_like: bool = Field(
            default=False,
            description="是否启用 send_like API（发送名片点赞）",
        )
        enable_send_poke: bool = Field(
            default=False,
            description="是否启用 send_poke API（发送戳一戳，NapCat 扩展）",
        )
        enable_send_forward_msg: bool = Field(
            default=False,
            description="是否启用 send_forward_msg API（发送合并转发消息，NapCat 扩展）",
        )
        enable_send_group_forward_msg: bool = Field(
            default=False,
            description="是否启用 send_group_forward_msg API（发送群合并转发消息，go-cqhttp兼容）",
        )
        enable_send_private_forward_msg: bool = Field(
            default=False,
            description="是否启用 send_private_forward_msg API（发送私聊合并转发消息，go-cqhttp兼容）",
        )
        enable_get_group_msg_history: bool = Field(
            default=False,
            description="是否启用 get_group_msg_history API（获取群消息历史，go-cqhttp兼容）",
        )
        enable_get_friend_msg_history: bool = Field(
            default=False,
            description="是否启用 get_friend_msg_history API（获取好友消息历史，go-cqhttp兼容）",
        )
        enable_forward_friend_single_msg: bool = Field(
            default=False,
            description="是否启用 forward_friend_single_msg API（转发单条消息给好友，扩展）",
        )
        enable_forward_group_single_msg: bool = Field(
            default=False,
            description="是否启用 forward_group_single_msg API（转发单条消息到群，扩展）",
        )
        enable_mark_msg_as_read: bool = Field(
            default=False,
            description="是否启用 mark_msg_as_read API（标记消息已读，go-cqhttp兼容）",
        )
        enable_mark_group_msg_as_read: bool = Field(
            default=False,
            description="是否启用 mark_group_msg_as_read API（标记群消息已读，扩展）",
        )
        enable_mark_private_msg_as_read: bool = Field(
            default=False,
            description="是否启用 mark_private_msg_as_read API（标记私聊消息已读，扩展）",
        )
        enable__mark_all_as_read: bool = Field(
            default=False,
            description="是否启用 _mark_all_as_read API（标记全部已读，扩展）",
        )
        enable_upload_forward_msg: bool = Field(
            default=False,
            description="是否启用 upload_forward_msg API（上传合并转发消息，扩展）",
        )

        # --- 群操作类 API (13) ---
        enable_set_group_kick: bool = Field(
            default=False,
            description="是否启用 set_group_kick API（群成员踢出）",
        )
        enable_set_group_ban: bool = Field(
            default=False,
            description="是否启用 set_group_ban API（单人禁言）",
        )
        enable_set_group_anonymous_ban: bool = Field(
            default=False,
            description="是否启用 set_group_anonymous_ban API（匿名禁言）",
        )
        enable_set_group_whole_ban: bool = Field(
            default=False,
            description="是否启用 set_group_whole_ban API（全体禁言）",
        )
        enable_set_group_admin: bool = Field(
            default=False,
            description="是否启用 set_group_admin API（设置管理员）",
        )
        enable_set_group_anonymous: bool = Field(
            default=False,
            description="是否启用 set_group_anonymous API（匿名聊天开关）",
        )
        enable_set_group_card: bool = Field(
            default=False,
            description="是否启用 set_group_card API（设置群名片）",
        )
        enable_set_group_name: bool = Field(
            default=False,
            description="是否启用 set_group_name API（设置群名）",
        )
        enable_set_group_leave: bool = Field(
            default=False,
            description="是否启用 set_group_leave API（退出群聊）",
        )
        enable_set_group_special_title: bool = Field(
            default=False,
            description="是否启用 set_group_special_title API（设置专属头衔）",
        )
        enable_set_group_member_invite_policy: bool = Field(
            default=False,
            description="是否启用 set_group_member_invite_policy API（设置群成员邀请策略，NapCat 扩展）",
        )
        enable_set_group_member_permissions: bool = Field(
            default=False,
            description="是否启用 set_group_member_permissions API（设置群成员功能权限，NapCat 扩展）",
        )
        enable_set_group_new_member_history_visibility: bool = Field(
            default=False,
            description="是否启用 set_group_new_member_history_visibility API（设置新成员历史消息可见性，NapCat 扩展）",
        )

        # --- 文件类 API (5) ---
        enable_upload_group_file: bool = Field(
            default=False,
            description="是否启用 upload_group_file API（上传群文件）",
        )
        enable_upload_private_file: bool = Field(
            default=False,
            description="是否启用 upload_private_file API（上传私聊文件）",
        )
        enable_get_file: bool = Field(
            default=False,
            description="是否启用 get_file API（获取文件信息，NapCat 扩展）",
        )
        enable_get_image: bool = Field(
            default=False,
            description="是否启用 get_image API（获取图片信息）",
        )
        enable_get_record: bool = Field(
            default=False,
            description="是否启用 get_record API（获取语音文件信息）",
        )
        enable_send_online_file: bool = Field(
            default=False,
            description="是否启用 send_online_file API（发送在线文件，NapCat 扩展）",
        )
        enable_send_online_folder: bool = Field(
            default=False,
            description="是否启用 send_online_folder API（发送在线文件夹，NapCat 扩展）",
        )
        enable_get_online_file_msg: bool = Field(
            default=False,
            description="是否启用 get_online_file_msg API（获取在线文件消息列表，NapCat 扩展）",
        )
        enable_receive_online_file: bool = Field(
            default=False,
            description="是否启用 receive_online_file API（接收在线文件，NapCat 扩展）",
        )
        enable_refuse_online_file: bool = Field(
            default=False,
            description="是否启用 refuse_online_file API（拒绝在线文件，NapCat 扩展）",
        )
        enable_cancel_online_file: bool = Field(
            default=False,
            description="是否启用 cancel_online_file API（取消已发送在线文件，NapCat 扩展）",
        )
        enable_clean_stream_temp_file: bool = Field(
            default=False,
            description="是否启用 clean_stream_temp_file API（清理流式传输临时文件）",
        )
        enable_upload_file_stream: bool = Field(
            default=False,
            description="是否启用 upload_file_stream API（流式上传文件）",
        )
        enable_download_file_stream: bool = Field(
            default=False,
            description="是否启用 download_file_stream API（流式下载文件）",
        )
        enable_download_file_record_stream: bool = Field(
            default=False,
            description="是否启用 download_file_record_stream API（流式下载语音文件）",
        )
        enable_download_file_image_stream: bool = Field(
            default=False,
            description="是否启用 download_file_image_stream API（流式下载图片文件）",
        )

        # --- 账号类 API (9) ---
        enable_get_login_info: bool = Field(
            default=False,
            description="是否启用 get_login_info API（获取登录号信息）",
        )
        enable_get_stranger_info: bool = Field(
            default=False,
            description="是否启用 get_stranger_info API（获取陌生人信息）",
        )
        enable_get_friend_list: bool = Field(
            default=False,
            description="是否启用 get_friend_list API（获取好友列表）",
        )
        enable_get_group_list: bool = Field(
            default=False,
            description="是否启用 get_group_list API（获取群列表）",
        )
        enable_get_group_member_list: bool = Field(
            default=False,
            description="是否启用 get_group_member_list API（获取群成员列表）",
        )
        enable_get_group_member_info: bool = Field(
            default=False,
            description="是否启用 get_group_member_info API（获取群成员信息）",
        )
        enable_get_group_info: bool = Field(
            default=False,
            description="是否启用 get_group_info API（获取群信息）",
        )
        enable_get_group_detail_info: bool = Field(
            default=False,
            description="是否启用 get_group_detail_info API（获取群详细信息，NapCat 扩展）",
        )
        enable_get_group_honor_info: bool = Field(
            default=False,
            description="是否启用 get_group_honor_info API（获取群荣誉信息）",
        )
        enable_get_robot_uin_range: bool = Field(
            default=False,
            description="是否启用 get_robot_uin_range API（获取机器人 UIN 范围，NapCat 扩展）",
        )

        # --- NapCat 扩展类 API (15) ---
        enable_set_msg_emoji_like: bool = Field(
            default=False,
            description="是否启用 set_msg_emoji_like API（消息表情回应，NapCat 扩展）",
        )
        enable_get_essence_msg_list: bool = Field(
            default=False,
            description="是否启用 get_essence_msg_list API（获取精华消息列表，NapCat 扩展）",
        )

        enable_get_online_clients: bool = Field(
            default=False,
            description="是否启用 get_online_clients API（获取在线客户端，NapCat 扩展）",
        )
        enable_get_cookies: bool = Field(
            default=False,
            description="是否启用 get_cookies API（获取 Cookies，NapCat 扩展）",
        )
        enable_get_csrf_token: bool = Field(
            default=False,
            description="是否启用 get_csrf_token API（获取 CSRF Token，NapCat 扩展）",
        )
        enable_get_status: bool = Field(
            default=False,
            description="是否启用 get_status API（获取运行状态）",
        )
        enable_set_restart: bool = Field(
            default=False,
            description="是否启用 set_restart API（重启协议端，NapCat 扩展）",
        )
        enable_clean_cache: bool = Field(
            default=False,
            description="是否启用 clean_cache API（清理缓存，NapCat 扩展）",
        )
        enable_can_send_image: bool = Field(
            default=False,
            description="是否启用 can_send_image API（是否支持发送图片）",
        )
        enable_can_send_record: bool = Field(
            default=False,
            description="是否启用 can_send_record API（是否支持发送语音）",
        )
        enable_get_version_info: bool = Field(
            default=False,
            description="是否启用 get_version_info API（获取版本信息）",
        )
        enable_set_essence_msg: bool = Field(
            default=False,
            description="是否启用 set_essence_msg API（设置精华消息，go-cqhttp兼容）",
        )
        enable_delete_essence_msg: bool = Field(
            default=False,
            description="是否启用 delete_essence_msg API（删除精华消息，go-cqhttp兼容）",
        )
        enable_get_group_at_all_remain: bool = Field(
            default=False,
            description="是否启用 get_group_at_all_remain API（获取@全体剩余次数，go-cqhttp兼容）",
        )
        enable_fetch_ptt_text: bool = Field(
            default=False,
            description="是否启用 fetch_ptt_text API（获取语音转文字，扩展）",
        )

        # --- 群文件管理类 API (11) ---
        enable_get_group_file_url: bool = Field(
            default=False,
            description="是否启用 get_group_file_url API（获取群文件下载链接，go-cqhttp 兼容）",
        )
        enable_get_group_root_files: bool = Field(
            default=False,
            description="是否启用 get_group_root_files API（获取群根目录文件，go-cqhttp 兼容）",
        )
        enable_get_group_files_by_folder: bool = Field(
            default=False,
            description="是否启用 get_group_files_by_folder API（获取群子目录文件，go-cqhttp 兼容）",
        )
        enable_delete_group_file: bool = Field(
            default=False,
            description="是否启用 delete_group_file API（删除群文件，go-cqhttp 兼容）",
        )
        enable_create_group_file_folder: bool = Field(
            default=False,
            description="是否启用 create_group_file_folder API（创建群文件夹，go-cqhttp 兼容）",
        )
        enable_delete_group_folder: bool = Field(
            default=False,
            description="是否启用 delete_group_folder API（删除群文件夹，go-cqhttp 兼容）",
        )
        enable_get_group_file_system_info: bool = Field(
            default=False,
            description="是否启用 get_group_file_system_info API（获取群文件系统信息，go-cqhttp 兼容）",
        )
        enable_move_group_file: bool = Field(
            default=False,
            description="是否启用 move_group_file API（移动群文件，扩展）",
        )
        enable_rename_group_file: bool = Field(
            default=False,
            description="是否启用 rename_group_file API（重命名群文件，扩展）",
        )
        enable_rename_group_file_folder: bool = Field(
            default=False,
            description="是否启用 rename_group_file_folder API（重命名群文件夹，SnowLuma 扩展）",
        )
        enable_trans_group_file: bool = Field(
            default=False,
            description="是否启用 trans_group_file API（转存群文件，扩展）",
        )
        enable_get_private_file_url: bool = Field(
            default=False,
            description="是否启用 get_private_file_url API（获取私聊文件下载链接，扩展）",
        )

        # --- 群公告类 API (3) ---
        enable__send_group_notice: bool = Field(
            default=False,
            description="是否启用 _send_group_notice API（发送群公告）",
        )
        enable__get_group_notice: bool = Field(
            default=False,
            description="是否启用 _get_group_notice API（获取群公告）",
        )
        enable__del_group_notice: bool = Field(
            default=False,
            description="是否启用 _del_group_notice API（删除群公告）",
        )

        # --- 群管理扩展类 API (11) ---
        enable_set_group_portrait: bool = Field(
            default=False,
            description="是否启用 set_group_portrait API（设置群头像）",
        )
        enable_set_group_remark: bool = Field(
            default=False,
            description="是否启用 set_group_remark API（设置群备注）",
        )
        enable_set_group_add_option: bool = Field(
            default=False,
            description="是否启用 set_group_add_option API（设置加群选项）",
        )
        enable_set_group_search: bool = Field(
            default=False,
            description="是否启用 set_group_search API（允许群被搜索）",
        )
        enable_set_group_robot_add_option: bool = Field(
            default=False,
            description="是否启用 set_group_robot_add_option API（设置群机器人加群选项）",
        )
        enable_set_group_kick_members: bool = Field(
            default=False,
            description="是否启用 set_group_kick_members API（批量踢出群成员）",
        )
        enable_get_group_shut_list: bool = Field(
            default=False,
            description="是否启用 get_group_shut_list API（获取群禁言列表）",
        )
        enable_get_group_ignored_notifies: bool = Field(
            default=False,
            description="是否启用 get_group_ignored_notifies API（获取被过滤的入群请求）",
        )
        enable_get_group_ignore_add_request: bool = Field(
            default=False,
            description="是否启用 get_group_ignore_add_request API（获取被忽略的入群请求）",
        )
        enable_get_group_info_ex: bool = Field(
            default=False,
            description="是否启用 get_group_info_ex API（获取群信息扩展）",
        )
        enable_set_group_sign: bool = Field(
            default=False,
            description="是否启用 set_group_sign API（群签到）",
        )
        enable_get_group_signed_list: bool = Field(
            default=False,
            description="是否启用 get_group_signed_list API（获取群今日打卡列表）",
        )

        # --- 请求处理类 API (5) ---
        enable_set_friend_add_request: bool = Field(
            default=False,
            description="是否启用 set_friend_add_request API（处理好友添加请求，OB11标准）",
        )
        enable_set_group_add_request: bool = Field(
            default=False,
            description="是否启用 set_group_add_request API（处理加群请求，OB11标准）",
        )
        enable_get_group_system_msg: bool = Field(
            default=False,
            description="是否启用 get_group_system_msg API（获取群系统消息，go-cqhttp兼容）",
        )
        enable_get_doubt_friends_add_request: bool = Field(
            default=False,
            description="是否启用 get_doubt_friends_add_request API（获取可疑好友申请，扩展）",
        )
        enable_set_doubt_friends_add_request: bool = Field(
            default=False,
            description="是否启用 set_doubt_friends_add_request API（处理可疑好友申请，扩展）",
        )

        # --- 用户信息扩展类 API (10) ---
        enable_delete_friend: bool = Field(
            default=False,
            description="是否启用 delete_friend API（删除好友）",
        )
        enable_set_friend_remark: bool = Field(
            default=False,
            description="是否启用 set_friend_remark API（设置好友备注）",
        )
        enable_get_friends_with_category: bool = Field(
            default=False,
            description="是否启用 get_friends_with_category API（获取分组好友列表）",
        )
        enable_get_unidirectional_friend_list: bool = Field(
            default=False,
            description="是否启用 get_unidirectional_friend_list API（获取单向好友列表）",
        )
        enable_set_qq_profile: bool = Field(
            default=False,
            description="是否启用 set_qq_profile API（设置QQ资料）",
        )
        enable_set_qq_avatar: bool = Field(
            default=False,
            description="是否启用 set_qq_avatar API（设置QQ头像）",
        )
        enable_set_self_longnick: bool = Field(
            default=False,
            description="是否启用 set_self_longnick API（设置个性签名）",
        )
        enable_get_recent_contact: bool = Field(
            default=False,
            description="是否启用 get_recent_contact API（获取最近联系人）",
        )
        enable_get_profile_like: bool = Field(
            default=False,
            description="是否启用 get_profile_like API（获取资料点赞）",
        )
        enable__get_friend_dress: bool = Field(
            default=False,
            description="是否启用 _get_friend_dress API（获取好友个性装扮，SnowLuma 扩展）",
        )

        # --- 在线状态类 API (4) ---
        enable_set_online_status: bool = Field(
            default=False,
            description="是否启用 set_online_status API（设置在线状态）",
        )
        enable_set_diy_online_status: bool = Field(
            default=False,
            description="是否启用 set_diy_online_status API（设置自定义在线状态）",
        )
        enable_set_input_status: bool = Field(
            default=False,
            description="是否启用 set_input_status API（设置输入状态）",
        )
        enable_nc_get_user_status: bool = Field(
            default=False,
            description="是否启用 nc_get_user_status API（获取用户状态）",
        )

        # --- 戳一拍类 API (2) ---
        enable_friend_poke: bool = Field(
            default=False,
            description="是否启用 friend_poke API（好友戳一戳）",
        )
        enable_group_poke: bool = Field(
            default=False,
            description="是否启用 group_poke API（群戳一戳）",
        )

        # --- 表情/收藏扩展类 API (10) ---
        enable_fetch_custom_face: bool = Field(
            default=False,
            description="是否启用 fetch_custom_face API（获取收藏表情）",
        )
        enable_fetch_custom_face_detail: bool = Field(
            default=False,
            description="是否启用 fetch_custom_face_detail API（获取收藏表情详情列表，NapCat 扩展）",
        )
        enable_add_custom_face: bool = Field(
            default=False,
            description="是否启用 add_custom_face API（添加收藏表情）",
        )
        enable_delete_custom_face: bool = Field(
            default=False,
            description="是否启用 delete_custom_face API（删除收藏表情）",
        )
        enable_set_custom_face_desc: bool = Field(
            default=False,
            description="是否启用 set_custom_face_desc API（修改收藏表情描述，NapCat 扩展）",
        )
        enable_modify_custom_face: bool = Field(
            default=False,
            description="是否启用 modify_custom_face API（修改收藏表情备注，SnowLuma 扩展）",
        )
        enable_move_custom_face_to_front: bool = Field(
            default=False,
            description="是否启用 move_custom_face_to_front API（收藏表情移到最前，SnowLuma 扩展）",
        )
        enable_fetch_emoji_like: bool = Field(
            default=False,
            description="是否启用 fetch_emoji_like API（获取表情回应分页）",
        )
        enable_get_emoji_likes: bool = Field(
            default=False,
            description="是否启用 get_emoji_likes API（获取表情回应用户）",
        )
        enable_set_group_reaction: bool = Field(
            default=False,
            description="是否启用 set_group_reaction API（群聊消息表情回应，SnowLuma 扩展）",
        )

        # --- AI语音类 API (3) ---
        enable_get_ai_characters: bool = Field(
            default=False,
            description="是否启用 get_ai_characters API（获取AI语音角色）",
        )
        enable_get_ai_record: bool = Field(
            default=False,
            description="是否启用 get_ai_record API（生成AI语音）",
        )
        enable_send_group_ai_record: bool = Field(
            default=False,
            description="是否启用 send_group_ai_record API（发送群AI语音）",
        )

        # --- 凭证/安全/下载类 API (6) ---
        enable_get_clientkey: bool = Field(
            default=False,
            description="是否启用 get_clientkey API（获取clientkey）",
        )
        enable_get_credentials: bool = Field(
            default=False,
            description="是否启用 get_credentials API（获取凭证）",
        )
        enable_get_rkey: bool = Field(
            default=False,
            description="是否启用 get_rkey API（获取rkey）",
        )
        enable_get_rkey_server: bool = Field(
            default=False,
            description="是否启用 get_rkey_server API（获取rkey服务器信息）",
        )
        enable_check_url_safely: bool = Field(
            default=False,
            description="是否启用 check_url_safely API（检查链接安全性）",
        )
        enable_ocr_image: bool = Field(
            default=False,
            description="是否启用 ocr_image API（OCR图片）",
        )
        enable_download_file: bool = Field(
            default=False,
            description="是否启用 download_file API（下载文件）",
        )
        enable_request_decrypt_key: bool = Field(
            default=False,
            description="是否启用 request_decrypt_key API（请求数据库解密密钥，SnowLuma 扩展）",
        )

        # --- 机型/其他类 API (13) ---
        enable__get_model_show: bool = Field(
            default=False,
            description="是否启用 _get_model_show API（获取机型展示）",
        )
        enable__set_model_show: bool = Field(
            default=False,
            description="是否启用 _set_model_show API（设置机型展示）",
        )
        enable_bot_exit: bool = Field(
            default=False,
            description="是否启用 bot_exit API（退出机器人）",
        )
        enable_nc_get_packet_status: bool = Field(
            default=False,
            description="是否启用 nc_get_packet_status API（获取packet状态）",
        )
        enable_click_inline_keyboard_button: bool = Field(
            default=False,
            description="是否启用 click_inline_keyboard_button API（点击内联键盘按钮）",
        )
        enable_get_mini_app_ark: bool = Field(
            default=False,
            description="是否启用 get_mini_app_ark API（获取小程序卡片）",
        )
        enable_translate_en2zh: bool = Field(
            default=False,
            description="是否启用 translate_en2zh API（英译中）",
        )
        enable_create_collection: bool = Field(
            default=False,
            description="是否启用 create_collection API（创建收藏）",
        )
        enable_get_collection_list: bool = Field(
            default=False,
            description="是否启用 get_collection_list API（获取收藏列表）",
        )
        enable_send_packet: bool = Field(
            default=False,
            description="是否启用 send_packet API（发送原始SSO包）",
        )
        enable_send_pb: bool = Field(
            default=False,
            description="是否启用 send_pb API（发送原始 Protobuf 数据，LLBot 扩展）",
        )
        enable_handle_quick_operation: bool = Field(
            default=False,
            description="是否启用 handle_quick_operation API（go-cqhttp 快速操作，别名 .handle_quick_operation）",
        )
        enable_get_word_slices: bool = Field(
            default=False,
            description="是否启用 get_word_slices API（go-cqhttp 分词，别名 .get_word_slices，仅 NapCat 支持）",
        )

        # --- 闪传类 API (8) ---
        enable_create_flash_task: bool = Field(
            default=False,
            description="是否启用 create_flash_task API（创建闪传任务）",
        )
        enable_send_flash_msg: bool = Field(
            default=False,
            description="是否启用 send_flash_msg API（发送闪传消息）",
        )
        enable_get_flash_file_list: bool = Field(
            default=False,
            description="是否启用 get_flash_file_list API（获取闪传文件列表）",
        )
        enable_get_flash_file_url: bool = Field(
            default=False,
            description="是否启用 get_flash_file_url API（获取闪传文件URL）",
        )
        enable_get_share_link: bool = Field(
            default=False,
            description="是否启用 get_share_link API（获取文件分享链接）",
        )
        enable_download_fileset: bool = Field(
            default=False,
            description="是否启用 download_fileset API（下载文件集）",
        )
        enable_get_fileset_info: bool = Field(
            default=False,
            description="是否启用 get_fileset_info API（获取文件集信息）",
        )
        enable_get_fileset_id: bool = Field(
            default=False,
            description="是否启用 get_fileset_id API（从分享码获取fileset_id）",
        )
        enable_list_filesets: bool = Field(
            default=False,
            description="是否启用 list_filesets API（列出所有闪传文件集，SnowLuma 扩展）",
        )
        enable_delete_flash_file: bool = Field(
            default=False,
            description="是否启用 delete_flash_file API（删除闪传文件，SnowLuma 扩展）",
        )
        enable_rename_flash_file: bool = Field(
            default=False,
            description="是否启用 rename_flash_file API（重命名闪传文件，SnowLuma 扩展）",
        )

        # --- 群相册类 API (7) ---
        enable_get_qun_album_list: bool = Field(
            default=False,
            description="是否启用 get_qun_album_list API（获取群相册列表）",
        )
        enable_upload_image_to_qun_album: bool = Field(
            default=False,
            description="是否启用 upload_image_to_qun_album API（上传图片到群相册）",
        )
        enable_get_group_album_media_list: bool = Field(
            default=False,
            description="是否启用 get_group_album_media_list API（获取群相册媒体列表）",
        )
        enable_do_group_album_comment: bool = Field(
            default=False,
            description="是否启用 do_group_album_comment API（评论群相册）",
        )
        enable_set_group_album_media_like: bool = Field(
            default=False,
            description="是否启用 set_group_album_media_like API（点赞群相册）",
        )
        enable_cancel_group_album_media_like: bool = Field(
            default=False,
            description="是否启用 cancel_group_album_media_like API（取消点赞群相册）",
        )
        enable_del_group_album_media: bool = Field(
            default=False,
            description="是否启用 del_group_album_media API（删除群相册媒体）",
        )

        # --- 群待办类 API (3) ---
        enable_set_group_todo: bool = Field(
            default=False,
            description="是否启用 set_group_todo API（设置群待办）",
        )
        enable_complete_group_todo: bool = Field(
            default=False,
            description="是否启用 complete_group_todo API（完成群待办）",
        )
        enable_cancel_group_todo: bool = Field(
            default=False,
            description="是否启用 cancel_group_todo API（取消群待办）",
        )

        # --- QQ空间类 API (7) ---
        enable_get_qzone_msg_list: bool = Field(
            default=False,
            description="是否启用 get_qzone_msg_list API（获取QQ空间说说列表）",
        )
        enable_get_qzone_feeds: bool = Field(
            default=False,
            description="是否启用 get_qzone_feeds API（获取QQ空间好友动态）",
        )
        enable_send_qzone_msg: bool = Field(
            default=False,
            description="是否启用 send_qzone_msg API（发表说说）",
        )
        enable_delete_qzone_msg: bool = Field(
            default=False,
            description="是否启用 delete_qzone_msg API（删除说说）",
        )
        enable_like_qzone: bool = Field(
            default=False,
            description="是否启用 like_qzone API（给说说点赞）",
        )
        enable_unlike_qzone: bool = Field(
            default=False,
            description="是否启用 unlike_qzone API（取消点赞）",
        )
        enable_comment_qzone: bool = Field(
            default=False,
            description="是否启用 comment_qzone API（评论说说）",
        )
        enable_set_qzone_ban: bool = Field(
            default=False,
            description="是否启用 set_qzone_ban API（QQ空间拉黑/解除拉黑，SnowLuma 扩展）",
        )
        enable_set_qzone_msg_right: bool = Field(
            default=False,
            description="是否启用 set_qzone_msg_right API（修改说说查看权限，SnowLuma 扩展）",
        )

        # --- Ark分享类 API (4) ---
        enable_share_peer: bool = Field(
            default=False,
            description="是否启用 share_peer API（分享用户/群Ark卡片）",
        )
        enable_send_ark_share: bool = Field(
            default=False,
            description="是否启用 send_ark_share API（分享Ark卡片）",
        )
        enable_share_group_ex: bool = Field(
            default=False,
            description="是否启用 share_group_ex API（分享群Ark卡片）",
        )
        enable_send_group_ark_share: bool = Field(
            default=False,
            description="是否启用 send_group_ark_share API（发送群Ark分享）",
        )

        # --- LLBot 扩展类 API (21) ---
        enable_batch_delete_group_member: bool = Field(
            default=False,
            description="是否启用 batch_delete_group_member API（批量踢出群成员，LLBot 扩展）",
        )
        enable_set_group_msg_mask: bool = Field(
            default=False,
            description="是否启用 set_group_msg_mask API（设置群消息屏蔽，LLBot 扩展）",
        )
        enable_create_group_album: bool = Field(
            default=False,
            description="是否启用 create_group_album API（创建群相册，LLBot 扩展）",
        )
        enable_delete_group_album: bool = Field(
            default=False,
            description="是否启用 delete_group_album API（删除群相册，LLBot 扩展）",
        )
        enable_get_flash_file_download_urls: bool = Field(
            default=False,
            description="是否启用 get_flash_file_download_urls API（获取闪传文件集下载URL，LLBot 扩展）",
        )
        enable_upload_flash_file: bool = Field(
            default=False,
            description="是否启用 upload_flash_file API（上传闪传文件，LLBot 扩展）",
        )
        enable_reshare_flash_file: bool = Field(
            default=False,
            description="是否启用 reshare_flash_file API（重新分享闪传文件，LLBot 扩展）",
        )
        enable_set_group_file_forever: bool = Field(
            default=False,
            description="是否启用 set_group_file_forever API（设置群文件永久保存，LLBot 扩展）",
        )
        enable_get_profile_like_me: bool = Field(
            default=False,
            description="是否启用 get_profile_like_me API（获取自身被点赞列表，LLBot 扩展）",
        )
        enable_get_profile_like_count: bool = Field(
            default=False,
            description="是否启用 get_profile_like_count API（获取用户点赞总数，LLBot 扩展）",
        )
        enable_get_qq_avatar: bool = Field(
            default=False,
            description="是否启用 get_qq_avatar API（获取QQ头像URL，LLBot 扩展）",
        )
        enable_set_friend_category: bool = Field(
            default=False,
            description="是否启用 set_friend_category API（设置好友分类，LLBot 扩展）",
        )
        enable_set_friends_category: bool = Field(
            default=False,
            description="是否启用 set_friends_category API（按分类 ID 或名称设置好友分类，SnowLuma 扩展）",
        )
        enable_get_recommend_face: bool = Field(
            default=False,
            description="是否启用 get_recommend_face API（获取推荐表情，LLBot 扩展）",
        )
        enable_unset_msg_emoji_like: bool = Field(
            default=False,
            description="是否启用 unset_msg_emoji_like API（取消消息表情回应，LLBot 扩展）",
        )
        enable_get_config: bool = Field(
            default=False,
            description="是否启用 get_config API（获取协议端配置，LLBot 扩展）",
        )
        enable_set_config: bool = Field(
            default=False,
            description="是否启用 set_config API（设置协议端配置，LLBot 扩展）",
        )
        enable_get_event: bool = Field(
            default=False,
            description="是否启用 get_event API（获取事件，LLBot 扩展）",
        )
        enable_llonebot_debug: bool = Field(
            default=False,
            description="是否启用 llonebot_debug API（调试接口，调用内部API，LLBot 扩展）",
        )
        enable_scan_qrcode: bool = Field(
            default=False,
            description="是否启用 scan_qrcode API（扫码登录，LLBot 扩展）",
        )
        enable_get_guild_list: bool = Field(
            default=False,
            description="是否启用 get_guild_list API（获取频道列表，NapCat/LLBot 扩展）",
        )

    ApiSwitchesSection: ClassVar[type[_GroupedApiSwitchesBase]] = (
        _build_grouped_api_switches_section(_FlatApiSwitchesSection)
    )

    # ==================== emoji 节 ====================
    @config_section("emoji")
    class EmojiSection(SectionBase):
        """表情发送与回应配置。"""

        enable_send_emoji: bool = Field(
            default=True,
            description="是否启用发送表情功能（通过 face 消息段发送原生 QQ 表情）",
        )
        enable_reaction_emoji: bool = Field(
            default=True,
            description="是否启用表情回应功能（通过 set_msg_emoji_like 添加表情回应）",
        )
        send_emoji_enabled_ids: list[int] = Field(
            default_factory=list,
            description="启用的发送表情 ID 列表，空列表表示全部启用",
        )
        reaction_emoji_enabled_ids: list[int] = Field(
            default_factory=list,
            description="启用的回应表情 ID 列表，空列表表示全部启用",
        )

    # ==================== file_transfer 节 ====================
    @config_section("file_transfer")
    class FileTransferSection(SectionBase):
        """文件传输模式配置。

        支持三种传输模式，按优先级: 路径映射 > 共享卷 > base64。
        多种模式同时启用时按优先级顺序尝试。
        """

        enable_path_mapping: bool = Field(
            default=False,
            description="是否启用路径映射模式（将本地路径前缀替换为协议端可访问路径）",
        )
        enable_base64_transfer: bool = Field(
            default=True,
            description="是否启用 base64 传输模式（读取文件内容编码为 base64 传输）",
        )
        enable_shared_volume: bool = Field(
            default=False,
            description="是否启用共享卷模式（直接使用原始路径发送，适用于同一文件系统）",
        )
        path_mappings: list[str] = Field(
            default_factory=list,
            description='路径映射规则列表，格式为 "host_path|container_path"，例如 "/app/data|/mnt/shared"',
        )
        shared_volume_root: str = Field(
            default="",
            description="共享卷根目录，共享卷模式下文件路径的基准目录",
        )
        auto_detect_mode: bool = Field(
            default=False,
            description="是否自动检测最佳传输模式（根据文件路径和可访问性自动选择）",
        )
        max_base64_size_mb: int = Field(
            default=10,
            description="base64 传输最大文件大小（MB），超过此大小则拒绝 base64 传输",
            ge=1,
        )

    # ==================== protocol 节 ====================
    @config_section("protocol")
    class ProtocolSection(SectionBase):
        """协议端后端配置。"""

        backend: str = Field(
            default="napcat",
            description="协议端类型: napcat 或 snowluma",
        )
        snowluma_compat_mode: bool = Field(
            default=False,
            description='强制启用 SnowLuma 兼容过滤；backend="snowluma" 时会自动启用',
        )

    # ==================== 字段声明 ====================
    plugin: PluginSection = Field(default_factory=PluginSection)
    adapter: AdapterSection = Field(default_factory=AdapterSection)
    api_switches: ApiSwitchesSection = Field(default_factory=ApiSwitchesSection)
    emoji: EmojiSection = Field(default_factory=EmojiSection)
    file_transfer: FileTransferSection = Field(default_factory=FileTransferSection)
    protocol: ProtocolSection = Field(default_factory=ProtocolSection)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """从字典加载配置并兼容旧版平铺工具开关。

        Args:
            data: 原始配置数据。

        Returns:
            完成兼容迁移的配置实例。
        """
        migrated, _ = _migrate_legacy_api_switches(data)
        return super().from_dict(migrated)

    @classmethod
    def load(
        cls,
        path: str | Path,
        *,
        auto_update: bool = False,
    ) -> Self:
        """加载配置，并在自动更新时持久化旧开关分组迁移。

        Args:
            path: TOML 配置文件路径。
            auto_update: 是否按当前配置模型更新文件签名。

        Returns:
            加载完成的配置实例。
        """
        config_path = Path(path)
        if config_path.exists():
            with config_path.open("rb") as file:
                raw_data = tomllib.load(file)
            migrated, changed = _migrate_legacy_api_switches(raw_data)
            if changed:
                if not auto_update:
                    return cls.from_dict(migrated)

                from src.kernel.config.core import (
                    _merge_with_model_defaults,
                    _render_toml_with_signature,
                )

                merged = _merge_with_model_defaults(cls, migrated)
                config_path.write_text(
                    _render_toml_with_signature(cls, merged),
                    encoding="utf-8",
                )
                return cls.from_dict(merged)

        return super().load(config_path, auto_update=auto_update)
