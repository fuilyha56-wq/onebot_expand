"""OneBot v11 + NapCat 扩展 API 定义模块。

定义全部 185 个 OneBot API 的常量、元数据、分类索引和查询函数。
供 Service 层和 Tool 层引用，确保 API action 名称和参数定义的一致性。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


# ============================================================================
# 枚举定义
# ============================================================================


class APICategory(Enum):
    """API 类别枚举，按功能域分组。"""

    MESSAGE = "message"
    """消息相关 API"""

    GROUP = "group"
    """群操作 API"""

    FILE = "file"
    """文件操作 API"""

    ACCOUNT = "account"
    """账号信息查询 API"""

    NAPCAT_EXT = "napcat_ext"
    """NapCat 扩展 API"""

    GROUP_FILE = "group_file"
    """群文件管理 API"""

    GROUP_NOTICE = "group_notice"
    """群公告 API"""

    GROUP_EXT = "group_ext"
    """群管理扩展 API"""

    REQUEST = "request"
    """请求处理 API"""

    USER_EXT = "user_ext"
    """用户信息扩展 API"""

    STATUS = "status"
    """在线状态 API"""

    POKE = "poke"
    """戳一拍 API"""

    EMOJI_EXT = "emoji_ext"
    """表情/收藏扩展 API"""

    AI_VOICE = "ai_voice"
    """AI语音 API"""

    CRED = "cred"
    """凭证/安全/下载 API"""

    MISC = "misc"
    """机型/其他 API"""

    FLASH = "flash"
    """闪传 API"""

    GROUP_ALBUM = "group_album"
    """群相册 API"""

    GROUP_TODO = "group_todo"
    """群待办 API"""

    QZONE = "qzone"
    """QQ空间 API"""

    ARK = "ark"
    """Ark分享 API"""


class APISource(Enum):
    """API 来源枚举，区分 OneBot v11 标准和 NapCat 扩展。"""

    ONEBOT_V11 = "onebot_v11"
    """OneBot v11 标准 API"""

    NAPCAT_EXT = "napcat_ext"
    """NapCat 扩展 API"""

    GOCQHTTP_COMPAT = "gocqhttp_compat"
    """go-cqhttp 兼容 API"""

    EXPAND = "expand"
    """扩展 API"""


# ============================================================================
# 数据类定义
# ============================================================================


@dataclass(frozen=True, slots=True)
class APIDef:
    """单个 API 的定义元数据。

    Attributes:
        action: API action 名称（如 "send_group_msg"）
        category: API 所属类别
        source: API 来源（OneBot v11 或 NapCat 扩展）
        description: API 中文描述
        params: 参数名到类型描述的映射（如 {"group_id": "int"}）
        napcat_only: 是否为 NapCat 专属 API（SnowLumia 不支持）
        snowluma_compat: 是否兼容 SnowLumia 协议端
        aliases: 同 handler 的别名 action 名元组（不含主名本身）。
            别名不作为 ALL_APIS 的键，只作为主名的 aliases 字段值。
            配置开关与协议端兼容性跟随主名。
    """

    action: str
    category: APICategory
    source: APISource
    description: str
    params: dict[str, str] = field(default_factory=dict)
    napcat_only: bool = False
    snowluma_compat: bool = True
    aliases: tuple[str, ...] = ()


# ============================================================================
# OneBot v11 标准 API action 常量
# ============================================================================


class OneBotAction:
    """OneBot v11 标准 API action 常量。"""

    # 消息相关

    SEND_GROUP_MSG = "send_group_msg"
    SEND_PRIVATE_MSG = "send_private_msg"
    SEND_MSG = "send_msg"
    DELETE_MSG = "delete_msg"
    GET_MSG = "get_msg"
    GET_FORWARD_MSG = "get_forward_msg"
    SEND_LIKE = "send_like"

    # 群操作
    SET_GROUP_KICK = "set_group_kick"
    SET_GROUP_BAN = "set_group_ban"
    SET_GROUP_ANONYMOUS_BAN = "set_group_anonymous_ban"
    SET_GROUP_WHOLE_BAN = "set_group_whole_ban"
    SET_GROUP_ADMIN = "set_group_admin"
    SET_GROUP_ANONYMOUS = "set_group_anonymous"
    SET_GROUP_CARD = "set_group_card"
    SET_GROUP_NAME = "set_group_name"
    SET_GROUP_LEAVE = "set_group_leave"
    SET_GROUP_SPECIAL_TITLE = "set_group_special_title"

    # 文件操作
    UPLOAD_GROUP_FILE = "upload_group_file"
    UPLOAD_PRIVATE_FILE = "upload_private_file"
    GET_IMAGE = "get_image"
    GET_RECORD = "get_record"

    # 账号信息
    GET_LOGIN_INFO = "get_login_info"
    GET_STRANGER_INFO = "get_stranger_info"
    GET_FRIEND_LIST = "get_friend_list"
    GET_GROUP_LIST = "get_group_list"
    GET_GROUP_MEMBER_LIST = "get_group_member_list"
    GET_GROUP_MEMBER_INFO = "get_group_member_info"
    GET_GROUP_INFO = "get_group_info"
    GET_GROUP_HONOR_INFO = "get_group_honor_info"

    # 请求处理（OneBot v11 标准）
    SET_FRIEND_ADD_REQUEST = "set_friend_add_request"
    SET_GROUP_ADD_REQUEST = "set_group_add_request"
    GET_GROUP_SYSTEM_MSG = "get_group_system_msg"


class NapCatAction:
    """NapCat 扩展 API action 常量。"""

    # 消息扩展
    SEND_POKE = "send_poke"
    SEND_FORWARD_MSG = "send_forward_msg"

    # 文件扩展
    GET_FILE = "get_file"

    # 在线文件（NapCat 扩展）
    SEND_ONLINE_FILE = "send_online_file"
    SEND_ONLINE_FOLDER = "send_online_folder"
    GET_ONLINE_FILE_MSG = "get_online_file_msg"
    RECEIVE_ONLINE_FILE = "receive_online_file"
    REFUSE_ONLINE_FILE = "refuse_online_file"
    CANCEL_ONLINE_FILE = "cancel_online_file"

    # 账号扩展
    GET_GROUP_DETAIL_INFO = "get_group_detail_info"

    # NapCat 专属
    SET_MSG_EMOJI_LIKE = "set_msg_emoji_like"

    GET_ONLINE_CLIENTS = "get_online_clients"
    GET_COOKIES = "get_cookies"
    GET_CSRF_TOKEN = "get_csrf_token"
    GET_STATUS = "get_status"
    SET_RESTART = "set_restart"
    CLEAN_CACHE = "clean_cache"
    CAN_SEND_IMAGE = "can_send_image"
    CAN_SEND_RECORD = "can_send_record"
    GET_VERSION_INFO = "get_version_info"


class GoCqhttpCompatAction:
    """go-cqhttp 兼容 API action 常量。"""

    # 消息相关
    SEND_GROUP_FORWARD_MSG = "send_group_forward_msg"
    SEND_PRIVATE_FORWARD_MSG = "send_private_forward_msg"
    GET_GROUP_MSG_HISTORY = "get_group_msg_history"
    GET_FRIEND_MSG_HISTORY = "get_friend_msg_history"
    MARK_MSG_AS_READ = "mark_msg_as_read"
    SET_ESSENCE_MSG = "set_essence_msg"
    DELETE_ESSENCE_MSG = "delete_essence_msg"
    GET_ESSENCE_MSG_LIST = "get_essence_msg_list"
    GET_GROUP_AT_ALL_REMAIN = "get_group_at_all_remain"

    # 群文件管理
    GET_GROUP_FILE_URL = "get_group_file_url"
    GET_GROUP_ROOT_FILES = "get_group_root_files"
    GET_GROUP_FILES_BY_FOLDER = "get_group_files_by_folder"
    DELETE_GROUP_FILE = "delete_group_file"
    CREATE_GROUP_FILE_FOLDER = "create_group_file_folder"
    DELETE_GROUP_FOLDER = "delete_group_folder"
    GET_GROUP_FILE_SYSTEM_INFO = "get_group_file_system_info"

    # 用户/资料
    SET_QQ_PROFILE = "set_qq_profile"

    # 凭证/识别
    OCR_IMAGE = "ocr_image"

    # go-cqhttp 快速操作
    HANDLE_QUICK_OPERATION = "handle_quick_operation"

    # go-cqhttp 分词
    GET_WORD_SLICES = "get_word_slices"


class ExpandAction:
    """扩展 API action 常量。"""

    # 消息扩展
    FORWARD_FRIEND_SINGLE_MSG = "forward_friend_single_msg"
    FORWARD_GROUP_SINGLE_MSG = "forward_group_single_msg"
    MARK_GROUP_MSG_AS_READ = "mark_group_msg_as_read"
    MARK_PRIVATE_MSG_AS_READ = "mark_private_msg_as_read"
    MARK_ALL_AS_READ = "_mark_all_as_read"
    FETCH_PTT_TEXT = "fetch_ptt_text"

    # 请求处理扩展
    GET_DOUBT_FRIENDS_ADD_REQUEST = "get_doubt_friends_add_request"
    SET_DOUBT_FRIENDS_ADD_REQUEST = "set_doubt_friends_add_request"

    # 群文件扩展
    MOVE_GROUP_FILE = "move_group_file"
    RENAME_GROUP_FILE = "rename_group_file"
    RENAME_GROUP_FILE_FOLDER = "rename_group_file_folder"
    TRANS_GROUP_FILE = "trans_group_file"
    GET_PRIVATE_FILE_URL = "get_private_file_url"

    # 群公告
    SEND_GROUP_NOTICE = "_send_group_notice"
    GET_GROUP_NOTICE = "_get_group_notice"
    DEL_GROUP_NOTICE = "_del_group_notice"

    # 群管理扩展
    SET_GROUP_PORTRAIT = "set_group_portrait"
    SET_GROUP_REMARK = "set_group_remark"
    SET_GROUP_ADD_OPTION = "set_group_add_option"
    SET_GROUP_SEARCH = "set_group_search"
    SET_GROUP_ROBOT_ADD_OPTION = "set_group_robot_add_option"
    SET_GROUP_KICK_MEMBERS = "set_group_kick_members"
    GET_GROUP_SHUT_LIST = "get_group_shut_list"
    GET_GROUP_IGNORED_NOTIFIES = "get_group_ignored_notifies"
    GET_GROUP_IGNORE_ADD_REQUEST = "get_group_ignore_add_request"
    GET_GROUP_INFO_EX = "get_group_info_ex"
    SET_GROUP_SIGN = "set_group_sign"
    GET_GROUP_SIGNED_LIST = "get_group_signed_list"
    GET_ROBOT_UIN_RANGE = "get_robot_uin_range"

    # 用户信息扩展
    DELETE_FRIEND = "delete_friend"
    SET_FRIEND_REMARK = "set_friend_remark"
    GET_FRIENDS_WITH_CATEGORY = "get_friends_with_category"
    GET_UNIDIRECTIONAL_FRIEND_LIST = "get_unidirectional_friend_list"
    SET_QQ_AVATAR = "set_qq_avatar"
    SET_SELF_LONGNICK = "set_self_longnick"
    GET_RECENT_CONTACT = "get_recent_contact"
    GET_PROFILE_LIKE = "get_profile_like"

    # 在线状态
    SET_ONLINE_STATUS = "set_online_status"
    SET_DIY_ONLINE_STATUS = "set_diy_online_status"
    SET_INPUT_STATUS = "set_input_status"
    NC_GET_USER_STATUS = "nc_get_user_status"

    # 戳一拍
    FRIEND_POKE = "friend_poke"
    GROUP_POKE = "group_poke"

    # 表情/收藏扩展
    FETCH_CUSTOM_FACE = "fetch_custom_face"
    FETCH_CUSTOM_FACE_DETAIL = "fetch_custom_face_detail"
    ADD_CUSTOM_FACE = "add_custom_face"
    DELETE_CUSTOM_FACE = "delete_custom_face"
    SET_CUSTOM_FACE_DESC = "set_custom_face_desc"
    MODIFY_CUSTOM_FACE = "modify_custom_face"
    MOVE_CUSTOM_FACE_TO_FRONT = "move_custom_face_to_front"
    FETCH_EMOJI_LIKE = "fetch_emoji_like"
    GET_EMOJI_LIKES = "get_emoji_likes"
    SET_GROUP_REACTION = "set_group_reaction"

    # AI语音
    GET_AI_CHARACTERS = "get_ai_characters"
    GET_AI_RECORD = "get_ai_record"
    SEND_GROUP_AI_RECORD = "send_group_ai_record"

    # 凭证/安全/下载
    GET_CLIENTKEY = "get_clientkey"
    GET_CREDENTIALS = "get_credentials"
    GET_RKEY = "get_rkey"
    GET_RKEY_SERVER = "get_rkey_server"
    CHECK_URL_SAFELY = "check_url_safely"
    DOWNLOAD_FILE = "download_file"
    REQUEST_DECRYPT_KEY = "request_decrypt_key"

    # 流式文件传输
    CLEAN_STREAM_TEMP_FILE = "clean_stream_temp_file"
    UPLOAD_FILE_STREAM = "upload_file_stream"
    DOWNLOAD_FILE_STREAM = "download_file_stream"
    DOWNLOAD_FILE_RECORD_STREAM = "download_file_record_stream"
    DOWNLOAD_FILE_IMAGE_STREAM = "download_file_image_stream"

    # 机型/其他
    GET_MODEL_SHOW = "_get_model_show"
    SET_MODEL_SHOW = "_set_model_show"
    BOT_EXIT = "bot_exit"
    NC_GET_PACKET_STATUS = "nc_get_packet_status"
    CLICK_INLINE_KEYBOARD_BUTTON = "click_inline_keyboard_button"
    GET_MINI_APP_ARK = "get_mini_app_ark"
    TRANSLATE_EN2ZH = "translate_en2zh"
    CREATE_COLLECTION = "create_collection"
    GET_COLLECTION_LIST = "get_collection_list"
    SEND_PACKET = "send_packet"

    # 闪传
    CREATE_FLASH_TASK = "create_flash_task"
    SEND_FLASH_MSG = "send_flash_msg"
    GET_FLASH_FILE_LIST = "get_flash_file_list"
    GET_FLASH_FILE_URL = "get_flash_file_url"
    GET_SHARE_LINK = "get_share_link"
    DOWNLOAD_FILESET = "download_fileset"
    GET_FILESET_INFO = "get_fileset_info"
    GET_FILESET_ID = "get_fileset_id"
    LIST_FILESETS = "list_filesets"
    DELETE_FLASH_FILE = "delete_flash_file"
    RENAME_FLASH_FILE = "rename_flash_file"

    # 群相册
    GET_QUN_ALBUM_LIST = "get_qun_album_list"
    UPLOAD_IMAGE_TO_QUN_ALBUM = "upload_image_to_qun_album"
    GET_GROUP_ALBUM_MEDIA_LIST = "get_group_album_media_list"
    DO_GROUP_ALBUM_COMMENT = "do_group_album_comment"
    SET_GROUP_ALBUM_MEDIA_LIKE = "set_group_album_media_like"
    CANCEL_GROUP_ALBUM_MEDIA_LIKE = "cancel_group_album_media_like"
    DEL_GROUP_ALBUM_MEDIA = "del_group_album_media"

    # 群待办
    SET_GROUP_TODO = "set_group_todo"
    COMPLETE_GROUP_TODO = "complete_group_todo"
    CANCEL_GROUP_TODO = "cancel_group_todo"

    # QQ空间
    GET_QZONE_MSG_LIST = "get_qzone_msg_list"
    GET_QZONE_FEEDS = "get_qzone_feeds"
    SEND_QZONE_MSG = "send_qzone_msg"
    DELETE_QZONE_MSG = "delete_qzone_msg"
    LIKE_QZONE = "like_qzone"
    UNLIKE_QZONE = "unlike_qzone"
    COMMENT_QZONE = "comment_qzone"
    SET_QZONE_BAN = "set_qzone_ban"
    SET_QZONE_MSG_RIGHT = "set_qzone_msg_right"

    # 上传合并转发
    UPLOAD_FORWARD_MSG = "upload_forward_msg"

    # Ark分享
    SHARE_PEER = "share_peer"
    SEND_ARK_SHARE = "send_ark_share"
    SHARE_GROUP_EX = "share_group_ex"
    SEND_GROUP_ARK_SHARE = "send_group_ark_share"

    # LLBot 扩展
    BATCH_DELETE_GROUP_MEMBER = "batch_delete_group_member"
    SET_GROUP_MSG_MASK = "set_group_msg_mask"
    CREATE_GROUP_ALBUM = "create_group_album"
    DELETE_GROUP_ALBUM = "delete_group_album"
    GET_FLASH_FILE_DOWNLOAD_URLS = "get_flash_file_download_urls"
    UPLOAD_FLASH_FILE = "upload_flash_file"
    RESHARE_FLASH_FILE = "reshare_flash_file"
    SET_GROUP_FILE_FOREVER = "set_group_file_forever"
    GET_PROFILE_LIKE_ME = "get_profile_like_me"
    GET_PROFILE_LIKE_COUNT = "get_profile_like_count"
    GET_QQ_AVATAR = "get_qq_avatar"
    SET_FRIEND_CATEGORY = "set_friend_category"
    GET_RECOMMEND_FACE = "get_recommend_face"
    UNSET_MSG_EMOJI_LIKE = "unset_msg_emoji_like"
    GET_CONFIG = "get_config"
    SET_CONFIG = "set_config"
    GET_EVENT = "get_event"
    LLONEBOT_DEBUG = "llonebot_debug"
    SCAN_QRCODE = "scan_qrcode"
    GET_GUILD_LIST = "get_guild_list"


# ============================================================================
# 常量定义
# ============================================================================

# NapCat 专属 API 集合（SnowLumia 不支持的 API）
# 重构后：SnowLuma 几乎实现了所有 NapCat 扩展 API，集合为空。
# 保留此字段以备未来 API 不兼容时使用；运行时通过 APIDef.snowluma_compat 单独标记。
NAPCAT_ONLY_APIS: set[str] = set()

# 扩展 API 集合（非标准 OneBot v11 API）
EXPAND_APIS: set[str] = {
    GoCqhttpCompatAction.SEND_GROUP_FORWARD_MSG,
    GoCqhttpCompatAction.SEND_PRIVATE_FORWARD_MSG,
    GoCqhttpCompatAction.GET_GROUP_MSG_HISTORY,
    GoCqhttpCompatAction.GET_FRIEND_MSG_HISTORY,
    GoCqhttpCompatAction.MARK_MSG_AS_READ,
    GoCqhttpCompatAction.SET_ESSENCE_MSG,
    GoCqhttpCompatAction.DELETE_ESSENCE_MSG,
    GoCqhttpCompatAction.GET_GROUP_AT_ALL_REMAIN,
    ExpandAction.FORWARD_FRIEND_SINGLE_MSG,
    ExpandAction.FORWARD_GROUP_SINGLE_MSG,
    ExpandAction.MARK_GROUP_MSG_AS_READ,
    ExpandAction.MARK_PRIVATE_MSG_AS_READ,
    ExpandAction.MARK_ALL_AS_READ,
    ExpandAction.FETCH_PTT_TEXT,
    OneBotAction.SET_FRIEND_ADD_REQUEST,
    OneBotAction.SET_GROUP_ADD_REQUEST,
    ExpandAction.GET_DOUBT_FRIENDS_ADD_REQUEST,
    ExpandAction.SET_DOUBT_FRIENDS_ADD_REQUEST,
    GoCqhttpCompatAction.GET_GROUP_FILE_URL,
    GoCqhttpCompatAction.GET_GROUP_ROOT_FILES,
    GoCqhttpCompatAction.GET_GROUP_FILES_BY_FOLDER,
    GoCqhttpCompatAction.DELETE_GROUP_FILE,
    GoCqhttpCompatAction.CREATE_GROUP_FILE_FOLDER,
    GoCqhttpCompatAction.DELETE_GROUP_FOLDER,
    GoCqhttpCompatAction.GET_GROUP_FILE_SYSTEM_INFO,
    ExpandAction.MOVE_GROUP_FILE,
    ExpandAction.RENAME_GROUP_FILE,
    ExpandAction.TRANS_GROUP_FILE,
    ExpandAction.GET_PRIVATE_FILE_URL,
    ExpandAction.SEND_GROUP_NOTICE,
    ExpandAction.GET_GROUP_NOTICE,
    ExpandAction.DEL_GROUP_NOTICE,
    ExpandAction.SET_GROUP_PORTRAIT,
    ExpandAction.SET_GROUP_REMARK,
    ExpandAction.SET_GROUP_ADD_OPTION,
    ExpandAction.SET_GROUP_SEARCH,
    ExpandAction.SET_GROUP_ROBOT_ADD_OPTION,
    ExpandAction.SET_GROUP_KICK_MEMBERS,
    ExpandAction.GET_GROUP_SHUT_LIST,
    ExpandAction.GET_GROUP_IGNORED_NOTIFIES,
    ExpandAction.GET_GROUP_IGNORE_ADD_REQUEST,
    ExpandAction.GET_GROUP_INFO_EX,
    ExpandAction.SET_GROUP_SIGN,
}

# 适配器签名常量
ADAPTER_SIGNATURE = "onebot_adapter:adapter:onebot_adapter"

# 默认超时时间（秒）
DEFAULT_TIMEOUT = 30.0


# ============================================================================
# 全部 158 个 API 定义
# ============================================================================

ALL_APIS: dict[str, APIDef] = {
    # ==================== 消息相关 API (18) ====================
    OneBotAction.SEND_GROUP_MSG: APIDef(
        action="send_group_msg",
        category=APICategory.MESSAGE,
        source=APISource.ONEBOT_V11,
        description="发送群聊消息",
        params={
            "group_id": "int",
            "message": "list[dict]",
            "auto_escape": "bool",
        },
    ),
    OneBotAction.SEND_PRIVATE_MSG: APIDef(
        action="send_private_msg",
        category=APICategory.MESSAGE,
        source=APISource.ONEBOT_V11,
        description="发送私聊消息",
        params={
            "user_id": "int",
            "message": "list[dict]",
            "auto_escape": "bool",
        },
    ),
    OneBotAction.SEND_MSG: APIDef(
        action="send_msg",
        category=APICategory.MESSAGE,
        source=APISource.ONEBOT_V11,
        description="发送消息（通用，按 message_type 或 user_id/group_id 自动路由）",
        params={
            "message_type": "str",
            "user_id": "int",
            "group_id": "int",
            "message": "list[dict]",
            "auto_escape": "bool",
        },
    ),
    OneBotAction.DELETE_MSG: APIDef(
        action="delete_msg",
        category=APICategory.MESSAGE,
        source=APISource.ONEBOT_V11,
        description="撤回消息",
        params={
            "message_id": "int | str",
        },
    ),
    OneBotAction.GET_MSG: APIDef(
        action="get_msg",
        category=APICategory.MESSAGE,
        source=APISource.ONEBOT_V11,
        description="获取消息详情",
        params={
            "message_id": "int | str",
        },
    ),
    OneBotAction.GET_FORWARD_MSG: APIDef(
        action="get_forward_msg",
        category=APICategory.MESSAGE,
        source=APISource.ONEBOT_V11,
        description="获取合并转发消息内容",
        params={
            "id": "str",
        },
    ),
    OneBotAction.SEND_LIKE: APIDef(
        action="send_like",
        category=APICategory.MESSAGE,
        source=APISource.ONEBOT_V11,
        description="发送名片点赞",
        params={
            "user_id": "int",
            "times": "int",
        },
    ),
    NapCatAction.SEND_POKE: APIDef(
        action="send_poke",
        category=APICategory.MESSAGE,
        source=APISource.NAPCAT_EXT,
        description="发送戳一戳（NapCat 扩展，自动路由版，等价于 friend_poke + group_poke）",
        params={
            "user_id": "int",
            "group_id": "int",
        },
    ),
    NapCatAction.SEND_FORWARD_MSG: APIDef(
        action="send_forward_msg",
        category=APICategory.MESSAGE,
        source=APISource.NAPCAT_EXT,
        description="发送合并转发消息（NapCat 扩展，自动路由）",
        params={
            "group_id": "int",
            "user_id": "int",
            "messages": "list[dict]",
            "news": "list[dict]",
            "prompt": "str",
            "summary": "str",
            "source_type": "str",
        },
    ),
    GoCqhttpCompatAction.SEND_GROUP_FORWARD_MSG: APIDef(
        action="send_group_forward_msg",
        category=APICategory.MESSAGE,
        source=APISource.GOCQHTTP_COMPAT,
        description="发送群合并转发消息（go-cqhttp兼容）",
        params={
            "group_id": "int",
            "messages": "list[dict]",
        },
    ),
    GoCqhttpCompatAction.SEND_PRIVATE_FORWARD_MSG: APIDef(
        action="send_private_forward_msg",
        category=APICategory.MESSAGE,
        source=APISource.GOCQHTTP_COMPAT,
        description="发送私聊合并转发消息（go-cqhttp兼容）",
        params={
            "user_id": "int",
            "messages": "list[dict]",
        },
    ),
    GoCqhttpCompatAction.GET_GROUP_MSG_HISTORY: APIDef(
        action="get_group_msg_history",
        category=APICategory.MESSAGE,
        source=APISource.GOCQHTTP_COMPAT,
        description="获取群消息历史（go-cqhttp兼容）",
        params={
            "group_id": "int",
            "message_seq": "int",
            "count": "int",
        },
    ),
    GoCqhttpCompatAction.GET_FRIEND_MSG_HISTORY: APIDef(
        action="get_friend_msg_history",
        category=APICategory.MESSAGE,
        source=APISource.GOCQHTTP_COMPAT,
        description="获取好友消息历史（go-cqhttp兼容）",
        params={
            "user_id": "int",
            "message_seq": "int",
            "count": "int",
        },
    ),
    ExpandAction.FORWARD_FRIEND_SINGLE_MSG: APIDef(
        action="forward_friend_single_msg",
        category=APICategory.MESSAGE,
        source=APISource.EXPAND,
        description="转发单条消息给好友（扩展）",
        params={
            "message_id": "int | str",
            "user_id": "int",
        },
    ),
    ExpandAction.FORWARD_GROUP_SINGLE_MSG: APIDef(
        action="forward_group_single_msg",
        category=APICategory.MESSAGE,
        source=APISource.EXPAND,
        description="转发单条消息到群（扩展）",
        params={
            "message_id": "int | str",
            "group_id": "int",
        },
    ),
    GoCqhttpCompatAction.MARK_MSG_AS_READ: APIDef(
        action="mark_msg_as_read",
        category=APICategory.MESSAGE,
        source=APISource.GOCQHTTP_COMPAT,
        description="标记消息已读（go-cqhttp兼容）",
        params={
            "message_id": "int | str",
            "target_id": "int",
        },
    ),
    ExpandAction.MARK_GROUP_MSG_AS_READ: APIDef(
        action="mark_group_msg_as_read",
        category=APICategory.MESSAGE,
        source=APISource.EXPAND,
        description="标记群消息已读（扩展）",
        params={
            "message_id": "int | str",
            "group_id": "int",
        },
    ),
    ExpandAction.MARK_PRIVATE_MSG_AS_READ: APIDef(
        action="mark_private_msg_as_read",
        category=APICategory.MESSAGE,
        source=APISource.EXPAND,
        description="标记私聊消息已读（扩展）",
        params={
            "message_id": "int | str",
            "user_id": "int",
        },
    ),
    ExpandAction.MARK_ALL_AS_READ: APIDef(
        action="_mark_all_as_read",
        category=APICategory.MESSAGE,
        source=APISource.EXPAND,
        description="标记全部已读（扩展）",
        params={},
    ),
    ExpandAction.UPLOAD_FORWARD_MSG: APIDef(
        action="upload_forward_msg",
        category=APICategory.MESSAGE,
        source=APISource.EXPAND,
        description="上传合并转发消息，返回 res_id（SnowLuma 扩展）",
        params={
            "messages": "list[dict]",
            "message": "list[dict]",
            "group_id": "int",
        },
        aliases=("upload_foward_msg",),
    ),
    OneBotAction.SET_GROUP_KICK: APIDef(
        action="set_group_kick",
        category=APICategory.GROUP,
        source=APISource.ONEBOT_V11,
        description="踢出群成员",
        params={
            "group_id": "int",
            "user_id": "int",
            "reject_add_request": "bool",
        },
    ),
    OneBotAction.SET_GROUP_BAN: APIDef(
        action="set_group_ban",
        category=APICategory.GROUP,
        source=APISource.ONEBOT_V11,
        description="禁言群成员",
        params={
            "group_id": "int",
            "user_id": "int",
            "duration": "int",
        },
    ),
    OneBotAction.SET_GROUP_ANONYMOUS_BAN: APIDef(
        action="set_group_anonymous_ban",
        category=APICategory.GROUP,
        source=APISource.ONEBOT_V11,
        description="禁言匿名群成员",
        params={
            "group_id": "int",
            "anonymous": "dict",
            "anonymous_flag": "str",
            "duration": "int",
        },
    ),
    OneBotAction.SET_GROUP_WHOLE_BAN: APIDef(
        action="set_group_whole_ban",
        category=APICategory.GROUP,
        source=APISource.ONEBOT_V11,
        description="全体禁言",
        params={
            "group_id": "int",
            "enable": "bool",
        },
    ),
    OneBotAction.SET_GROUP_ADMIN: APIDef(
        action="set_group_admin",
        category=APICategory.GROUP,
        source=APISource.ONEBOT_V11,
        description="设置/取消管理员",
        params={
            "group_id": "int",
            "user_id": "int",
            "enable": "bool",
        },
    ),
    OneBotAction.SET_GROUP_ANONYMOUS: APIDef(
        action="set_group_anonymous",
        category=APICategory.GROUP,
        source=APISource.ONEBOT_V11,
        description="开启/关闭匿名聊天",
        params={
            "group_id": "int",
            "enable": "bool",
        },
    ),
    OneBotAction.SET_GROUP_CARD: APIDef(
        action="set_group_card",
        category=APICategory.GROUP,
        source=APISource.ONEBOT_V11,
        description="设置群名片",
        params={
            "group_id": "int",
            "user_id": "int",
            "card": "str",
        },
    ),
    OneBotAction.SET_GROUP_NAME: APIDef(
        action="set_group_name",
        category=APICategory.GROUP,
        source=APISource.ONEBOT_V11,
        description="设置群名",
        params={
            "group_id": "int",
            "group_name": "str",
        },
    ),
    OneBotAction.SET_GROUP_LEAVE: APIDef(
        action="set_group_leave",
        category=APICategory.GROUP,
        source=APISource.ONEBOT_V11,
        description="退出群聊",
        params={
            "group_id": "int",
            "is_dismiss": "bool",
        },
    ),
    OneBotAction.SET_GROUP_SPECIAL_TITLE: APIDef(
        action="set_group_special_title",
        category=APICategory.GROUP,
        source=APISource.ONEBOT_V11,
        description="设置专属头衔",
        params={
            "group_id": "int",
            "user_id": "int",
            "special_title": "str",
            "duration": "int",
        },
    ),
    # ==================== 文件操作 API (7) ====================
    OneBotAction.UPLOAD_GROUP_FILE: APIDef(
        action="upload_group_file",
        category=APICategory.FILE,
        source=APISource.ONEBOT_V11,
        description="上传群文件",
        params={
            "group_id": "int",
            "file": "str",
            "name": "str",
        },
    ),
    OneBotAction.UPLOAD_PRIVATE_FILE: APIDef(
        action="upload_private_file",
        category=APICategory.FILE,
        source=APISource.ONEBOT_V11,
        description="上传私聊文件",
        params={
            "user_id": "int",
            "file": "str",
            "name": "str",
        },
    ),
    NapCatAction.GET_FILE: APIDef(
        action="get_file",
        category=APICategory.FILE,
        source=APISource.NAPCAT_EXT,
        description="获取文件信息（NapCat 扩展）",
        params={
            "file_id": "str",
            "url": "bool",
        },
    ),
    OneBotAction.GET_IMAGE: APIDef(
        action="get_image",
        category=APICategory.FILE,
        source=APISource.ONEBOT_V11,
        description="获取图片信息",
        params={
            "file": "str",
        },
    ),
    OneBotAction.GET_RECORD: APIDef(
        action="get_record",
        category=APICategory.FILE,
        source=APISource.ONEBOT_V11,
        description="获取语音文件信息",
        params={
            "file": "str",
            "out_format": "str",
        },
    ),
    NapCatAction.SEND_ONLINE_FILE: APIDef(
        action="send_online_file",
        category=APICategory.FILE,
        source=APISource.NAPCAT_EXT,
        description="发送在线文件（私聊，NapCat 扩展）",
        params={
            "user_id": "int",
            "file_path": "str",
            "file_name": "str",
        },
        napcat_only=True,
        snowluma_compat=False,
    ),
    NapCatAction.SEND_ONLINE_FOLDER: APIDef(
        action="send_online_folder",
        category=APICategory.FILE,
        source=APISource.NAPCAT_EXT,
        description="发送在线文件夹（私聊，NapCat 扩展）",
        params={
            "user_id": "int",
            "folder_path": "str",
            "folder_name": "str",
        },
        napcat_only=True,
        snowluma_compat=False,
    ),
    NapCatAction.GET_ONLINE_FILE_MSG: APIDef(
        action="get_online_file_msg",
        category=APICategory.FILE,
        source=APISource.NAPCAT_EXT,
        description="获取在线文件消息列表（NapCat 扩展）",
        params={
            "user_id": "int",
        },
        napcat_only=True,
        snowluma_compat=False,
    ),
    NapCatAction.RECEIVE_ONLINE_FILE: APIDef(
        action="receive_online_file",
        category=APICategory.FILE,
        source=APISource.NAPCAT_EXT,
        description="接收在线文件（NapCat 扩展）",
        params={
            "user_id": "int",
            "msg_id": "str",
            "element_id": "str",
        },
        napcat_only=True,
        snowluma_compat=False,
    ),
    NapCatAction.REFUSE_ONLINE_FILE: APIDef(
        action="refuse_online_file",
        category=APICategory.FILE,
        source=APISource.NAPCAT_EXT,
        description="拒绝在线文件（NapCat 扩展）",
        params={
            "user_id": "int",
            "msg_id": "str",
            "element_id": "str",
        },
        napcat_only=True,
        snowluma_compat=False,
    ),
    NapCatAction.CANCEL_ONLINE_FILE: APIDef(
        action="cancel_online_file",
        category=APICategory.FILE,
        source=APISource.NAPCAT_EXT,
        description="取消已发送的在线文件（NapCat 扩展）",
        params={
            "user_id": "int",
            "msg_id": "str",
        },
        napcat_only=True,
        snowluma_compat=False,
    ),
    ExpandAction.CLEAN_STREAM_TEMP_FILE: APIDef(
        action="clean_stream_temp_file",
        category=APICategory.FILE,
        source=APISource.EXPAND,
        description="清理流式传输临时文件（NapCat 与 SnowLuma 均支持）",
        params={},
    ),
    ExpandAction.UPLOAD_FILE_STREAM: APIDef(
        action="upload_file_stream",
        category=APICategory.FILE,
        source=APISource.EXPAND,
        description="流式上传文件（分块传输，NapCat 与 SnowLuma 均支持）",
        params={
            "stream_id": "str",
            "chunk_data": "str",
            "chunk_index": "int",
            "total_chunks": "int",
            "file_size": "int",
            "expected_sha256": "str",
            "is_complete": "bool",
            "filename": "str",
            "reset": "bool",
            "verify_only": "bool",
            "file_retention": "int",
        },
    ),
    ExpandAction.DOWNLOAD_FILE_STREAM: APIDef(
        action="download_file_stream",
        category=APICategory.FILE,
        source=APISource.EXPAND,
        description="流式下载文件（分块传输，NapCat 与 SnowLuma 均支持）",
        params={
            "file": "str",
            "file_id": "str",
            "chunk_size": "int",
        },
    ),
    ExpandAction.DOWNLOAD_FILE_RECORD_STREAM: APIDef(
        action="download_file_record_stream",
        category=APICategory.FILE,
        source=APISource.EXPAND,
        description="流式下载语音文件并转换格式（NapCat 与 SnowLuma 均支持）",
        params={
            "file": "str",
            "file_id": "str",
            "chunk_size": "int",
            "out_format": "str",
        },
    ),
    ExpandAction.DOWNLOAD_FILE_IMAGE_STREAM: APIDef(
        action="download_file_image_stream",
        category=APICategory.FILE,
        source=APISource.EXPAND,
        description="流式下载图片文件（NapCat 与 SnowLuma 均支持）",
        params={
            "file": "str",
            "file_id": "str",
            "chunk_size": "int",
        },
    ),
    # ==================== 账号信息查询 API (10) ====================
    OneBotAction.GET_LOGIN_INFO: APIDef(
        action="get_login_info",
        category=APICategory.ACCOUNT,
        source=APISource.ONEBOT_V11,
        description="获取 Bot 登录信息",
        params={},
    ),
    OneBotAction.GET_STRANGER_INFO: APIDef(
        action="get_stranger_info",
        category=APICategory.ACCOUNT,
        source=APISource.ONEBOT_V11,
        description="获取陌生人信息",
        params={
            "user_id": "int",
            "no_cache": "bool",
        },
    ),
    OneBotAction.GET_FRIEND_LIST: APIDef(
        action="get_friend_list",
        category=APICategory.ACCOUNT,
        source=APISource.ONEBOT_V11,
        description="获取好友列表",
        params={},
    ),
    OneBotAction.GET_GROUP_LIST: APIDef(
        action="get_group_list",
        category=APICategory.ACCOUNT,
        source=APISource.ONEBOT_V11,
        description="获取群列表",
        params={},
    ),
    OneBotAction.GET_GROUP_MEMBER_LIST: APIDef(
        action="get_group_member_list",
        category=APICategory.ACCOUNT,
        source=APISource.ONEBOT_V11,
        description="获取群成员列表",
        params={
            "group_id": "int",
            "no_cache": "bool",
        },
    ),
    OneBotAction.GET_GROUP_MEMBER_INFO: APIDef(
        action="get_group_member_info",
        category=APICategory.ACCOUNT,
        source=APISource.ONEBOT_V11,
        description="获取群成员详情",
        params={
            "group_id": "int",
            "user_id": "int",
            "no_cache": "bool",
        },
    ),
    OneBotAction.GET_GROUP_INFO: APIDef(
        action="get_group_info",
        category=APICategory.ACCOUNT,
        source=APISource.ONEBOT_V11,
        description="获取群信息",
        params={
            "group_id": "int",
            "no_cache": "bool",
        },
    ),
    NapCatAction.GET_GROUP_DETAIL_INFO: APIDef(
        action="get_group_detail_info",
        category=APICategory.ACCOUNT,
        source=APISource.NAPCAT_EXT,
        description="获取群详细信息（NapCat 扩展）",
        params={
            "group_id": "int",
        },
    ),
    OneBotAction.GET_GROUP_HONOR_INFO: APIDef(
        action="get_group_honor_info",
        category=APICategory.ACCOUNT,
        source=APISource.ONEBOT_V11,
        description="获取群荣誉信息",
        params={
            "group_id": "int",
            "type": "str",
        },
    ),
    # ==================== NapCat 扩展 API (15) ====================
    ExpandAction.GET_ROBOT_UIN_RANGE: APIDef(
        action="get_robot_uin_range",
        category=APICategory.ACCOUNT,
        source=APISource.EXPAND,
        description="获取机器人 UIN 范围（NapCat 扩展）",
        params={},
        napcat_only=True,
        snowluma_compat=False,
    ),
    NapCatAction.SET_MSG_EMOJI_LIKE: APIDef(
        action="set_msg_emoji_like",
        category=APICategory.NAPCAT_EXT,
        source=APISource.NAPCAT_EXT,
        description="对消息添加/取消表情回应",
        params={
            "message_id": "int | str",
            "emoji_id": "int",
            "set": "bool",
        },
    ),
    GoCqhttpCompatAction.GET_ESSENCE_MSG_LIST: APIDef(
        action="get_essence_msg_list",
        category=APICategory.NAPCAT_EXT,
        source=APISource.GOCQHTTP_COMPAT,
        description="获取群精华消息列表（go-cqhttp 兼容）",
        params={
            "group_id": "int",
        },
    ),

    NapCatAction.GET_ONLINE_CLIENTS: APIDef(
        action="get_online_clients",
        category=APICategory.NAPCAT_EXT,
        source=APISource.NAPCAT_EXT,
        description="获取在线客户端列表",
        params={},
    ),
    NapCatAction.GET_COOKIES: APIDef(
        action="get_cookies",
        category=APICategory.NAPCAT_EXT,
        source=APISource.NAPCAT_EXT,
        description="获取 Cookies",
        params={
            "domain": "str",
        },
    ),
    NapCatAction.GET_CSRF_TOKEN: APIDef(
        action="get_csrf_token",
        category=APICategory.NAPCAT_EXT,
        source=APISource.NAPCAT_EXT,
        description="获取 CSRF Token",
        params={},
    ),
    NapCatAction.GET_STATUS: APIDef(
        action="get_status",
        category=APICategory.NAPCAT_EXT,
        source=APISource.NAPCAT_EXT,
        description="获取协议端运行状态",
        params={},
        napcat_only=False,
        snowluma_compat=True,
    ),
    NapCatAction.SET_RESTART: APIDef(
        action="set_restart",
        category=APICategory.NAPCAT_EXT,
        source=APISource.NAPCAT_EXT,
        description="重启协议端",
        params={
            "delay": "int",
        },
    ),
    NapCatAction.CLEAN_CACHE: APIDef(
        action="clean_cache",
        category=APICategory.NAPCAT_EXT,
        source=APISource.NAPCAT_EXT,
        description="清理协议端缓存",
        params={},
    ),
    NapCatAction.CAN_SEND_IMAGE: APIDef(
        action="can_send_image",
        category=APICategory.NAPCAT_EXT,
        source=APISource.NAPCAT_EXT,
        description="检查是否支持发送图片",
        params={},
        napcat_only=False,
        snowluma_compat=True,
    ),
    NapCatAction.CAN_SEND_RECORD: APIDef(
        action="can_send_record",
        category=APICategory.NAPCAT_EXT,
        source=APISource.NAPCAT_EXT,
        description="检查是否支持发送语音",
        params={},
        napcat_only=False,
        snowluma_compat=True,
    ),
    NapCatAction.GET_VERSION_INFO: APIDef(
        action="get_version_info",
        category=APICategory.NAPCAT_EXT,
        source=APISource.NAPCAT_EXT,
        description="获取协议端版本信息",
        params={},
        napcat_only=False,
        snowluma_compat=True,
    ),
    GoCqhttpCompatAction.SET_ESSENCE_MSG: APIDef(
        action="set_essence_msg",
        category=APICategory.NAPCAT_EXT,
        source=APISource.GOCQHTTP_COMPAT,
        description="设置精华消息（go-cqhttp兼容）",
        params={
            "message_id": "int | str",
        },
    ),
    GoCqhttpCompatAction.DELETE_ESSENCE_MSG: APIDef(
        action="delete_essence_msg",
        category=APICategory.NAPCAT_EXT,
        source=APISource.GOCQHTTP_COMPAT,
        description="删除精华消息（go-cqhttp兼容）",
        params={
            "message_id": "int | str",
        },
    ),
    GoCqhttpCompatAction.GET_GROUP_AT_ALL_REMAIN: APIDef(
        action="get_group_at_all_remain",
        category=APICategory.NAPCAT_EXT,
        source=APISource.GOCQHTTP_COMPAT,
        description="获取@全体剩余次数（go-cqhttp兼容）",
        params={
            "group_id": "int",
        },
    ),
    ExpandAction.FETCH_PTT_TEXT: APIDef(
        action="fetch_ptt_text",
        category=APICategory.NAPCAT_EXT,
        source=APISource.EXPAND,
        description="获取语音转文字（扩展）",
        params={
            "message_id": "int | str",
        },
        aliases=("get_ptt_text", "get_record_text", "voice_msg_to_text"),
    ),
    # ==================== 群文件管理 API (11) ====================
    GoCqhttpCompatAction.GET_GROUP_FILE_URL: APIDef(
        action="get_group_file_url",
        category=APICategory.GROUP_FILE,
        source=APISource.GOCQHTTP_COMPAT,
        description="获取群文件下载链接（go-cqhttp 兼容）",
        params={
            "group_id": "int",
            "file_id": "str",
            "busid": "int",
        },
    ),
    GoCqhttpCompatAction.GET_GROUP_ROOT_FILES: APIDef(
        action="get_group_root_files",
        category=APICategory.GROUP_FILE,
        source=APISource.GOCQHTTP_COMPAT,
        description="获取群根目录文件（go-cqhttp 兼容）",
        params={
            "group_id": "int",
        },
    ),
    GoCqhttpCompatAction.GET_GROUP_FILES_BY_FOLDER: APIDef(
        action="get_group_files_by_folder",
        category=APICategory.GROUP_FILE,
        source=APISource.GOCQHTTP_COMPAT,
        description="获取群子目录文件（go-cqhttp 兼容）",
        params={
            "group_id": "int",
            "folder_id": "str",
        },
    ),
    GoCqhttpCompatAction.DELETE_GROUP_FILE: APIDef(
        action="delete_group_file",
        category=APICategory.GROUP_FILE,
        source=APISource.GOCQHTTP_COMPAT,
        description="删除群文件（go-cqhttp 兼容）",
        params={
            "group_id": "int",
            "file_id": "str",
            "busid": "int",
        },
    ),
    GoCqhttpCompatAction.CREATE_GROUP_FILE_FOLDER: APIDef(
        action="create_group_file_folder",
        category=APICategory.GROUP_FILE,
        source=APISource.GOCQHTTP_COMPAT,
        description="创建群文件夹（go-cqhttp 兼容）",
        params={
            "group_id": "int",
            "name": "str",
            "parent_id": "str",
        },
    ),
    GoCqhttpCompatAction.DELETE_GROUP_FOLDER: APIDef(
        action="delete_group_folder",
        category=APICategory.GROUP_FILE,
        source=APISource.GOCQHTTP_COMPAT,
        description="删除群文件夹（go-cqhttp 兼容）",
        params={
            "group_id": "int",
            "folder_id": "str",
        },
        aliases=("delete_group_file_folder",),
    ),
    GoCqhttpCompatAction.GET_GROUP_FILE_SYSTEM_INFO: APIDef(
        action="get_group_file_system_info",
        category=APICategory.GROUP_FILE,
        source=APISource.GOCQHTTP_COMPAT,
        description="获取群文件系统信息（go-cqhttp 兼容）",
        params={
            "group_id": "int",
        },
    ),
    ExpandAction.MOVE_GROUP_FILE: APIDef(
        action="move_group_file",
        category=APICategory.GROUP_FILE,
        source=APISource.EXPAND,
        description="移动群文件（扩展）",
        params={
            "group_id": "int",
            "file_id": "str",
            "current_parent_directory": "str",
            "target_directory": "str",
        },
    ),
    ExpandAction.RENAME_GROUP_FILE: APIDef(
        action="rename_group_file",
        category=APICategory.GROUP_FILE,
        source=APISource.EXPAND,
        description="重命名群文件（扩展）",
        params={
            "group_id": "int",
            "file_id": "str",
            "current_parent_directory": "str",
            "new_name": "str",
        },
    ),
    ExpandAction.RENAME_GROUP_FILE_FOLDER: APIDef(
        action="rename_group_file_folder",
        category=APICategory.GROUP_FILE,
        source=APISource.EXPAND,
        description="重命名群文件夹（SnowLuma 扩展）",
        params={
            "group_id": "int",
            "folder_id": "str",
            "new_folder_name": "str",
        },
        napcat_only=False,
        snowluma_compat=True,
    ),
    ExpandAction.TRANS_GROUP_FILE: APIDef(
        action="trans_group_file",
        category=APICategory.GROUP_FILE,
        source=APISource.EXPAND,
        description="转存群文件（扩展）",
        params={
            "group_id": "int",
            "file_id": "str",
        },
    ),
    ExpandAction.GET_PRIVATE_FILE_URL: APIDef(
        action="get_private_file_url",
        category=APICategory.GROUP_FILE,
        source=APISource.EXPAND,
        description="获取私聊文件下载链接（扩展）",
        params={
            "user_id": "int",
            "file_id": "str",
            "file_hash": "str",
        },
    ),
    # ==================== 群公告 API (3) ====================
    ExpandAction.SEND_GROUP_NOTICE: APIDef(
        action="_send_group_notice",
        category=APICategory.GROUP_NOTICE,
        source=APISource.EXPAND,
        description="发送群公告",
        params={
            "group_id": "int",
            "content": "str",
            "image": "str",
        },
    ),
    ExpandAction.GET_GROUP_NOTICE: APIDef(
        action="_get_group_notice",
        category=APICategory.GROUP_NOTICE,
        source=APISource.EXPAND,
        description="获取群公告",
        params={
            "group_id": "int",
        },
    ),
    ExpandAction.DEL_GROUP_NOTICE: APIDef(
        action="_del_group_notice",
        category=APICategory.GROUP_NOTICE,
        source=APISource.EXPAND,
        description="删除群公告",
        params={
            "group_id": "int",
            "notice_id": "str",
        },
        aliases=("_delete_group_notice",),
    ),
    # ==================== 群管理扩展 API (11) ====================
    ExpandAction.SET_GROUP_PORTRAIT: APIDef(
        action="set_group_portrait",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="设置群头像",
        params={
            "group_id": "int",
            "file": "str",
        },
    ),
    ExpandAction.SET_GROUP_REMARK: APIDef(
        action="set_group_remark",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="设置群备注",
        params={
            "group_id": "int",
            "remark": "str",
        },
    ),
    ExpandAction.SET_GROUP_ADD_OPTION: APIDef(
        action="set_group_add_option",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="设置加群选项",
        params={
            "group_id": "int",
            "add_type": "int",
        },
    ),
    ExpandAction.SET_GROUP_SEARCH: APIDef(
        action="set_group_search",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="允许群被搜索",
        params={
            "group_id": "int",
        },
    ),
    ExpandAction.SET_GROUP_ROBOT_ADD_OPTION: APIDef(
        action="set_group_robot_add_option",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="设置群机器人加群选项",
        params={
            "group_id": "int",
            "robot_member_switch": "bool",
        },
    ),
    ExpandAction.SET_GROUP_KICK_MEMBERS: APIDef(
        action="set_group_kick_members",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="批量踢出群成员",
        params={
            "group_id": "int",
            "user_id_list": "list[int]",
            "reject_add_request": "bool",
        },
    ),
    ExpandAction.GET_GROUP_SHUT_LIST: APIDef(
        action="get_group_shut_list",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="获取群禁言列表",
        params={
            "group_id": "int",
        },
    ),
    ExpandAction.GET_GROUP_IGNORED_NOTIFIES: APIDef(
        action="get_group_ignored_notifies",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="获取被过滤的入群请求",
        params={},
    ),
    ExpandAction.GET_GROUP_IGNORE_ADD_REQUEST: APIDef(
        action="get_group_ignore_add_request",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="获取被忽略的入群请求",
        params={},
    ),
    ExpandAction.GET_GROUP_INFO_EX: APIDef(
        action="get_group_info_ex",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="获取群信息扩展",
        params={
            "group_id": "int",
        },
    ),
    ExpandAction.SET_GROUP_SIGN: APIDef(
        action="set_group_sign",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="群签到",
        params={
            "group_id": "int",
        },
        aliases=("send_group_sign",),
    ),
    ExpandAction.GET_GROUP_SIGNED_LIST: APIDef(
        action="get_group_signed_list",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="获取群今日打卡列表",
        params={
            "group_id": "int",
        },
    ),
    # ==================== 请求处理 API (6) ====================
    OneBotAction.SET_FRIEND_ADD_REQUEST: APIDef(
        action="set_friend_add_request",
        category=APICategory.REQUEST,
        source=APISource.ONEBOT_V11,
        description="处理好友添加请求（OB11标准）",
        params={
            "flag": "str",
            "approve": "bool",
            "remark": "str",
        },
    ),
    OneBotAction.SET_GROUP_ADD_REQUEST: APIDef(
        action="set_group_add_request",
        category=APICategory.REQUEST,
        source=APISource.ONEBOT_V11,
        description="处理加群请求（OB11标准）",
        params={
            "flag": "str",
            "sub_type": "str",
            "approve": "bool",
            "reason": "str",
        },
    ),
    OneBotAction.GET_GROUP_SYSTEM_MSG: APIDef(
        action="get_group_system_msg",
        category=APICategory.REQUEST,
        source=APISource.ONEBOT_V11,
        description="获取群系统消息（OB11标准）",
        params={},
    ),
    ExpandAction.GET_DOUBT_FRIENDS_ADD_REQUEST: APIDef(
        action="get_doubt_friends_add_request",
        category=APICategory.REQUEST,
        source=APISource.EXPAND,
        description="获取可疑好友申请（扩展）",
        params={
            "count": "int",
        },
    ),
    ExpandAction.SET_DOUBT_FRIENDS_ADD_REQUEST: APIDef(
        action="set_doubt_friends_add_request",
        category=APICategory.REQUEST,
        source=APISource.EXPAND,
        description="处理可疑好友申请（扩展）",
        params={
            "flag": "str",
            "approve": "bool",
        },
    ),
    # ==================== 用户信息扩展 API (9) ====================
    ExpandAction.DELETE_FRIEND: APIDef(
        action="delete_friend",
        category=APICategory.USER_EXT,
        source=APISource.EXPAND,
        description="删除好友",
        params={
            "user_id": "int",
            "block": "bool",
        },
    ),
    ExpandAction.SET_FRIEND_REMARK: APIDef(
        action="set_friend_remark",
        category=APICategory.USER_EXT,
        source=APISource.EXPAND,
        description="设置好友备注",
        params={
            "user_id": "int",
            "remark": "str",
        },
    ),
    ExpandAction.GET_FRIENDS_WITH_CATEGORY: APIDef(
        action="get_friends_with_category",
        category=APICategory.USER_EXT,
        source=APISource.EXPAND,
        description="获取分组好友列表",
        params={},
    ),
    ExpandAction.GET_UNIDIRECTIONAL_FRIEND_LIST: APIDef(
        action="get_unidirectional_friend_list",
        category=APICategory.USER_EXT,
        source=APISource.EXPAND,
        description="获取单向好友列表",
        params={},
    ),
    GoCqhttpCompatAction.SET_QQ_PROFILE: APIDef(
        action="set_qq_profile",
        category=APICategory.USER_EXT,
        source=APISource.GOCQHTTP_COMPAT,
        description="设置QQ资料（go-cqhttp 兼容）",
        params={
            "nickname": "str",
            "personal_note": "str",
        },
    ),
    ExpandAction.SET_QQ_AVATAR: APIDef(
        action="set_qq_avatar",
        category=APICategory.USER_EXT,
        source=APISource.EXPAND,
        description="设置QQ头像",
        params={
            "file": "str",
        },
    ),
    ExpandAction.SET_SELF_LONGNICK: APIDef(
        action="set_self_longnick",
        category=APICategory.USER_EXT,
        source=APISource.EXPAND,
        description="设置个性签名",
        params={
            "long_nick": "str",
        },
    ),
    ExpandAction.GET_RECENT_CONTACT: APIDef(
        action="get_recent_contact",
        category=APICategory.USER_EXT,
        source=APISource.EXPAND,
        description="获取最近联系人",
        params={
            "count": "int",
        },
    ),
    ExpandAction.GET_PROFILE_LIKE: APIDef(
        action="get_profile_like",
        category=APICategory.USER_EXT,
        source=APISource.EXPAND,
        description="获取资料点赞",
        params={
            "user_id": "int",
            "start": "int",
            "count": "int",
        },
    ),
    # ==================== 在线状态 API (4) ====================
    ExpandAction.SET_ONLINE_STATUS: APIDef(
        action="set_online_status",
        category=APICategory.STATUS,
        source=APISource.EXPAND,
        description="设置在线状态",
        params={
            "status": "int",
            "ext_status": "int",
            "battery_status": "int",
        },
    ),
    ExpandAction.SET_DIY_ONLINE_STATUS: APIDef(
        action="set_diy_online_status",
        category=APICategory.STATUS,
        source=APISource.EXPAND,
        description="设置自定义在线状态",
        params={
            "face_id": "int",
            "face_type": "int",
            "wording": "str",
        },
    ),
    ExpandAction.SET_INPUT_STATUS: APIDef(
        action="set_input_status",
        category=APICategory.STATUS,
        source=APISource.EXPAND,
        description="设置输入状态",
        params={
            "user_id": "int",
            "event_type": "int",
        },
    ),
    ExpandAction.NC_GET_USER_STATUS: APIDef(
        action="nc_get_user_status",
        category=APICategory.STATUS,
        source=APISource.EXPAND,
        description="获取用户状态",
        params={
            "user_id": "int",
        },
    ),
    # ==================== 戳一拍 API (2) ====================
    ExpandAction.FRIEND_POKE: APIDef(
        action="friend_poke",
        category=APICategory.POKE,
        source=APISource.EXPAND,
        description="好友戳一拍（显式好友版，等价于 send_poke(user_id=...)）",
        params={
            "user_id": "int",
            "target_id": "int",
        },
    ),
    ExpandAction.GROUP_POKE: APIDef(
        action="group_poke",
        category=APICategory.POKE,
        source=APISource.EXPAND,
        description="群戳一拍（显式群版，等价于 send_poke(group_id=...)）",
        params={
            "group_id": "int",
            "user_id": "int",
        },
    ),
    # ==================== 表情/收藏扩展 API (5) ====================
    ExpandAction.FETCH_CUSTOM_FACE: APIDef(
        action="fetch_custom_face",
        category=APICategory.EMOJI_EXT,
        source=APISource.EXPAND,
        description="获取收藏表情",
        params={
            "count": "int",
        },
    ),
    ExpandAction.ADD_CUSTOM_FACE: APIDef(
        action="add_custom_face",
        category=APICategory.EMOJI_EXT,
        source=APISource.EXPAND,
        description="添加收藏表情",
        params={
            "file": "str",
        },
    ),
    ExpandAction.DELETE_CUSTOM_FACE: APIDef(
        action="delete_custom_face",
        category=APICategory.EMOJI_EXT,
        source=APISource.EXPAND,
        description="删除收藏表情",
        params={
            "emoji_id": "str",
        },
    ),
    ExpandAction.FETCH_CUSTOM_FACE_DETAIL: APIDef(
        action="fetch_custom_face_detail",
        category=APICategory.EMOJI_EXT,
        source=APISource.EXPAND,
        description="获取收藏表情详情列表（NapCat 扩展）",
        params={
            "count": "int",
        },
        napcat_only=True,
        snowluma_compat=False,
    ),
    ExpandAction.SET_CUSTOM_FACE_DESC: APIDef(
        action="set_custom_face_desc",
        category=APICategory.EMOJI_EXT,
        source=APISource.EXPAND,
        description="修改收藏表情描述（NapCat 扩展）",
        params={
            "emoji_id": "int",
            "res_id": "str",
            "md5": "str",
            "desc": "str",
        },
        napcat_only=True,
        snowluma_compat=False,
    ),
    ExpandAction.MODIFY_CUSTOM_FACE: APIDef(
        action="modify_custom_face",
        category=APICategory.EMOJI_EXT,
        source=APISource.EXPAND,
        description="修改收藏表情备注（SnowLuma 扩展）",
        params={
            "emoji_id": "str",
            "desc": "str",
        },
        napcat_only=False,
        snowluma_compat=True,
    ),
    ExpandAction.MOVE_CUSTOM_FACE_TO_FRONT: APIDef(
        action="move_custom_face_to_front",
        category=APICategory.EMOJI_EXT,
        source=APISource.EXPAND,
        description="收藏表情移到最前（SnowLuma 扩展）",
        params={
            "emoji_id": "str",
        },
        napcat_only=False,
        snowluma_compat=True,
    ),
    ExpandAction.FETCH_EMOJI_LIKE: APIDef(
        action="fetch_emoji_like",
        category=APICategory.EMOJI_EXT,
        source=APISource.EXPAND,
        description="获取表情回应分页",
        params={
            "message_id": "int | str",
            "emoji_id": "int",
            "count": "int",
        },
    ),
    ExpandAction.GET_EMOJI_LIKES: APIDef(
        action="get_emoji_likes",
        category=APICategory.EMOJI_EXT,
        source=APISource.EXPAND,
        description="获取表情回应用户",
        params={
            "message_id": "int | str",
            "emoji_id": "int",
        },
    ),
    ExpandAction.SET_GROUP_REACTION: APIDef(
        action="set_group_reaction",
        category=APICategory.EMOJI_EXT,
        source=APISource.EXPAND,
        description="群聊消息表情回应（SnowLuma 扩展）",
        params={
            "group_id": "int",
            "message_id": "int | str",
            "code": "str",
            "is_set": "bool",
        },
        napcat_only=False,
        snowluma_compat=True,
    ),
    # ==================== AI语音 API (3) ====================
    ExpandAction.GET_AI_CHARACTERS: APIDef(
        action="get_ai_characters",
        category=APICategory.AI_VOICE,
        source=APISource.EXPAND,
        description="获取AI语音角色",
        params={
            "group_id": "int",
            "chat_type": "int",
        },
    ),
    ExpandAction.GET_AI_RECORD: APIDef(
        action="get_ai_record",
        category=APICategory.AI_VOICE,
        source=APISource.EXPAND,
        description="生成AI语音",
        params={
            "group_id": "int",
            "character": "str",
            "text": "str",
        },
    ),
    ExpandAction.SEND_GROUP_AI_RECORD: APIDef(
        action="send_group_ai_record",
        category=APICategory.AI_VOICE,
        source=APISource.EXPAND,
        description="发送群AI语音",
        params={
            "group_id": "int",
            "character": "str",
            "text": "str",
        },
    ),
    # ==================== 凭证/安全/下载 API (6) ====================
    ExpandAction.GET_CLIENTKEY: APIDef(
        action="get_clientkey",
        category=APICategory.CRED,
        source=APISource.EXPAND,
        description="获取clientkey",
        params={},
    ),
    ExpandAction.GET_CREDENTIALS: APIDef(
        action="get_credentials",
        category=APICategory.CRED,
        source=APISource.EXPAND,
        description="获取凭证",
        params={
            "domain": "str",
        },
    ),
    ExpandAction.GET_RKEY: APIDef(
        action="get_rkey",
        category=APICategory.CRED,
        source=APISource.EXPAND,
        description="获取rkey",
        params={},
        aliases=("nc_get_rkey",),
    ),
    ExpandAction.GET_RKEY_SERVER: APIDef(
        action="get_rkey_server",
        category=APICategory.CRED,
        source=APISource.EXPAND,
        description="获取rkey服务器信息（含过期时间和服务器名）",
        params={},
    ),
    ExpandAction.CHECK_URL_SAFELY: APIDef(
        action="check_url_safely",
        category=APICategory.CRED,
        source=APISource.EXPAND,
        description="检查链接安全性",
        params={
            "url": "str",
        },
    ),
    GoCqhttpCompatAction.OCR_IMAGE: APIDef(
        action="ocr_image",
        category=APICategory.CRED,
        source=APISource.GOCQHTTP_COMPAT,
        description="OCR图片（go-cqhttp 兼容）",
        params={
            "image": "str",
        },
        aliases=(".ocr_image",),
    ),
    ExpandAction.DOWNLOAD_FILE: APIDef(
        action="download_file",
        category=APICategory.CRED,
        source=APISource.EXPAND,
        description="下载文件",
        params={
            "url": "str",
            "name": "str",
            "headers": "list[str]",
        },
    ),
    ExpandAction.REQUEST_DECRYPT_KEY: APIDef(
        action="request_decrypt_key",
        category=APICategory.CRED,
        source=APISource.EXPAND,
        description="请求数据库解密密钥（SnowLuma 扩展，传入 db_path）",
        params={
            "db_path": "str",
        },
        napcat_only=False,
        snowluma_compat=True,
    ),
    # ==================== 机型/其他 API (10) ====================
    ExpandAction.GET_MODEL_SHOW: APIDef(
        action="_get_model_show",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="获取机型展示",
        params={
            "model": "str",
        },
        aliases=("._get_model_show",),
    ),
    ExpandAction.SET_MODEL_SHOW: APIDef(
        action="_set_model_show",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="设置机型展示",
        params={
            "model": "str",
            "show": "str",
        },
        aliases=("._set_model_show",),
    ),
    ExpandAction.BOT_EXIT: APIDef(
        action="bot_exit",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="退出机器人",
        params={},
    ),
    ExpandAction.NC_GET_PACKET_STATUS: APIDef(
        action="nc_get_packet_status",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="获取packet状态",
        params={},
    ),
    ExpandAction.CLICK_INLINE_KEYBOARD_BUTTON: APIDef(
        action="click_inline_keyboard_button",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="点击内联键盘按钮",
        params={
            "group_id": "int",
            "bot_appid": "int",
            "msg_seq": "int",
            "button_id": "str",
        },
    ),
    ExpandAction.GET_MINI_APP_ARK: APIDef(
        action="get_mini_app_ark",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="获取小程序卡片",
        params={
            "type": "str",
            "title": "str",
            "desc": "str",
            "pic_url": "str",
            "jump_url": "str",
        },
    ),
    ExpandAction.TRANSLATE_EN2ZH: APIDef(
        action="translate_en2zh",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="英译中",
        params={
            "words": "list[str]",
        },
    ),
    ExpandAction.CREATE_COLLECTION: APIDef(
        action="create_collection",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="创建收藏",
        params={},
    ),
    ExpandAction.GET_COLLECTION_LIST: APIDef(
        action="get_collection_list",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="获取收藏列表",
        params={},
    ),
    ExpandAction.SEND_PACKET: APIDef(
        action="send_packet",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="发送原始SSO包",
        params={
            "cmd": "str",
            "data": "dict",
        },
        aliases=(".send_packet",),
    ),
    GoCqhttpCompatAction.HANDLE_QUICK_OPERATION: APIDef(
        action="handle_quick_operation",
        category=APICategory.MISC,
        source=APISource.GOCQHTTP_COMPAT,
        description="go-cqhttp 快速操作（NapCat 与 SnowLuma 均支持，传入 context 与 operation）",
        params={
            "context": "dict",
            "operation": "dict",
        },
        aliases=(".handle_quick_operation",),
    ),
    GoCqhttpCompatAction.GET_WORD_SLICES: APIDef(
        action="get_word_slices",
        category=APICategory.MISC,
        source=APISource.GOCQHTTP_COMPAT,
        description="go-cqhttp 分词（NapCat 支持，SnowLuma 未实现）",
        params={
            "content": "str",
        },
        napcat_only=True,
        snowluma_compat=False,
        aliases=(".get_word_slices",),
    ),
    # ==================== 闪传 API (8) ====================
    ExpandAction.CREATE_FLASH_TASK: APIDef(
        action="create_flash_task",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="创建闪传任务",
        params={
            "files": "list[dict]",
            "name": "str",
        },
    ),
    ExpandAction.SEND_FLASH_MSG: APIDef(
        action="send_flash_msg",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="发送闪传消息",
        params={
            "fileset_id": "str",
            "user_id": "int",
            "group_id": "int",
        },
    ),
    ExpandAction.GET_FLASH_FILE_LIST: APIDef(
        action="get_flash_file_list",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="获取闪传文件列表",
        params={
            "fileset_id": "str",
        },
    ),
    ExpandAction.GET_FLASH_FILE_URL: APIDef(
        action="get_flash_file_url",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="获取闪传文件URL",
        params={
            "fileset_id": "str",
            "file_name": "str",
        },
    ),
    ExpandAction.GET_SHARE_LINK: APIDef(
        action="get_share_link",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="获取文件分享链接",
        params={
            "fileset_id": "str",
        },
    ),
    ExpandAction.DOWNLOAD_FILESET: APIDef(
        action="download_fileset",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="下载文件集",
        params={
            "fileset_id": "str",
        },
        aliases=("download_flash_file",),
    ),
    ExpandAction.GET_FILESET_INFO: APIDef(
        action="get_fileset_info",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="获取文件集信息",
        params={
            "fileset_id": "str",
        },
        aliases=("get_flash_file_info",),
    ),
    ExpandAction.GET_FILESET_ID: APIDef(
        action="get_fileset_id",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="从分享码获取fileset_id",
        params={
            "share_code": "str",
        },
    ),
    ExpandAction.LIST_FILESETS: APIDef(
        action="list_filesets",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="列出当前账号所有闪传文件集（SnowLuma 扩展）",
        params={},
        napcat_only=False,
        snowluma_compat=True,
    ),
    ExpandAction.DELETE_FLASH_FILE: APIDef(
        action="delete_flash_file",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="删除闪传文件（SnowLuma 扩展）",
        params={
            "fileset_id": "str",
        },
        napcat_only=False,
        snowluma_compat=True,
    ),
    ExpandAction.RENAME_FLASH_FILE: APIDef(
        action="rename_flash_file",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="重命名闪传文件（SnowLuma 扩展）",
        params={
            "fileset_id": "str",
            "new_name": "str",
        },
        napcat_only=False,
        snowluma_compat=True,
    ),
    # ==================== 群相册 API (7) ====================
    ExpandAction.GET_QUN_ALBUM_LIST: APIDef(
        action="get_qun_album_list",
        category=APICategory.GROUP_ALBUM,
        source=APISource.EXPAND,
        description="获取群相册列表",
        params={
            "group_id": "int",
        },
        aliases=("get_group_album_list",),
    ),
    ExpandAction.UPLOAD_IMAGE_TO_QUN_ALBUM: APIDef(
        action="upload_image_to_qun_album",
        category=APICategory.GROUP_ALBUM,
        source=APISource.EXPAND,
        description="上传图片到群相册",
        params={
            "group_id": "int",
            "file": "str",
            "album_id": "str",
        },
        aliases=("upload_group_album",),
    ),
    ExpandAction.GET_GROUP_ALBUM_MEDIA_LIST: APIDef(
        action="get_group_album_media_list",
        category=APICategory.GROUP_ALBUM,
        source=APISource.EXPAND,
        description="获取群相册媒体列表",
        params={
            "group_id": "int",
            "album_id": "str",
        },
    ),
    ExpandAction.DO_GROUP_ALBUM_COMMENT: APIDef(
        action="do_group_album_comment",
        category=APICategory.GROUP_ALBUM,
        source=APISource.EXPAND,
        description="评论群相册",
        params={
            "group_id": "int",
            "album_id": "str",
            "lloc": "str",
            "content": "str",
        },
    ),
    ExpandAction.SET_GROUP_ALBUM_MEDIA_LIKE: APIDef(
        action="set_group_album_media_like",
        category=APICategory.GROUP_ALBUM,
        source=APISource.EXPAND,
        description="点赞群相册",
        params={
            "group_id": "int",
            "album_id": "str",
            "batch_id": "str",
        },
    ),
    ExpandAction.CANCEL_GROUP_ALBUM_MEDIA_LIKE: APIDef(
        action="cancel_group_album_media_like",
        category=APICategory.GROUP_ALBUM,
        source=APISource.EXPAND,
        description="取消点赞群相册",
        params={
            "group_id": "int",
            "album_id": "str",
            "batch_id": "str",
        },
    ),
    ExpandAction.DEL_GROUP_ALBUM_MEDIA: APIDef(
        action="del_group_album_media",
        category=APICategory.GROUP_ALBUM,
        source=APISource.EXPAND,
        description="删除群相册媒体",
        params={
            "group_id": "int",
            "album_id": "str",
            "lloc": "str",
        },
    ),
    # ==================== 群待办 API (3) ====================
    ExpandAction.SET_GROUP_TODO: APIDef(
        action="set_group_todo",
        category=APICategory.GROUP_TODO,
        source=APISource.EXPAND,
        description="设置群待办",
        params={
            "group_id": "int",
            "message_id": "int | str",
        },
    ),
    ExpandAction.COMPLETE_GROUP_TODO: APIDef(
        action="complete_group_todo",
        category=APICategory.GROUP_TODO,
        source=APISource.EXPAND,
        description="完成群待办",
        params={
            "group_id": "int",
            "message_id": "int | str",
        },
    ),
    ExpandAction.CANCEL_GROUP_TODO: APIDef(
        action="cancel_group_todo",
        category=APICategory.GROUP_TODO,
        source=APISource.EXPAND,
        description="取消群待办",
        params={
            "group_id": "int",
            "message_id": "int | str",
        },
    ),
    # ==================== QQ空间 API (7) ====================
    ExpandAction.GET_QZONE_MSG_LIST: APIDef(
        action="get_qzone_msg_list",
        category=APICategory.QZONE,
        source=APISource.EXPAND,
        description="获取QQ空间说说列表",
        params={
            "pos": "int",
            "num": "int",
        },
    ),
    ExpandAction.GET_QZONE_FEEDS: APIDef(
        action="get_qzone_feeds",
        category=APICategory.QZONE,
        source=APISource.EXPAND,
        description="获取QQ空间好友动态",
        params={
            "page_num": "int",
            "count": "int",
        },
    ),
    ExpandAction.SEND_QZONE_MSG: APIDef(
        action="send_qzone_msg",
        category=APICategory.QZONE,
        source=APISource.EXPAND,
        description="发表说说",
        params={
            "content": "str",
        },
    ),
    ExpandAction.DELETE_QZONE_MSG: APIDef(
        action="delete_qzone_msg",
        category=APICategory.QZONE,
        source=APISource.EXPAND,
        description="删除说说",
        params={
            "tid": "str",
        },
    ),
    ExpandAction.LIKE_QZONE: APIDef(
        action="like_qzone",
        category=APICategory.QZONE,
        source=APISource.EXPAND,
        description="给说说点赞",
        params={
            "tid": "str",
            "target_uin": "int",
        },
    ),
    ExpandAction.UNLIKE_QZONE: APIDef(
        action="unlike_qzone",
        category=APICategory.QZONE,
        source=APISource.EXPAND,
        description="取消点赞",
        params={
            "tid": "str",
            "target_uin": "int",
        },
    ),
    ExpandAction.COMMENT_QZONE: APIDef(
        action="comment_qzone",
        category=APICategory.QZONE,
        source=APISource.EXPAND,
        description="评论说说",
        params={
            "tid": "str",
            "content": "str",
            "target_uin": "int",
        },
    ),
    ExpandAction.SET_QZONE_BAN: APIDef(
        action="set_qzone_ban",
        category=APICategory.QZONE,
        source=APISource.EXPAND,
        description="拉黑或解除拉黑某人（机器人自身 QQ 空间黑名单；SnowLuma 扩展）",
        params={
            "user_id": "int",
            "enable": "bool",
        },
        napcat_only=False,
        snowluma_compat=True,
    ),
    ExpandAction.SET_QZONE_MSG_RIGHT: APIDef(
        action="set_qzone_msg_right",
        category=APICategory.QZONE,
        source=APISource.EXPAND,
        description="修改一条已发说说的查看权限（SnowLuma 扩展）",
        params={
            "tid": "str",
            "ugc_right": "int",
            "target_uins": "list[int]",
        },
        napcat_only=False,
        snowluma_compat=True,
    ),
    # ==================== Ark分享 API (4) ====================
    ExpandAction.SHARE_PEER: APIDef(
        action="share_peer",
        category=APICategory.ARK,
        source=APISource.EXPAND,
        description="分享用户/群Ark卡片（SnowLuma 主名，send_ark_share 是 NapCat 标准化别名）",
        params={
            "user_id": "int",
            "group_id": "int",
        },
    ),
    ExpandAction.SEND_ARK_SHARE: APIDef(
        action="send_ark_share",
        category=APICategory.ARK,
        source=APISource.EXPAND,
        description="分享Ark卡片（NapCat 名，功能等价于 share_peer）",
        params={
            "user_id": "int",
            "group_id": "int",
        },
    ),
    ExpandAction.SHARE_GROUP_EX: APIDef(
        action="share_group_ex",
        category=APICategory.ARK,
        source=APISource.EXPAND,
        description="分享群Ark卡片（SnowLuma 主名，send_group_ark_share 是 NapCat 标准化别名）",
        params={
            "group_id": "int",
        },
    ),
    ExpandAction.SEND_GROUP_ARK_SHARE: APIDef(
        action="send_group_ark_share",
        category=APICategory.ARK,
        source=APISource.EXPAND,
        description="发送群Ark分享（NapCat 名，功能等价于 share_group_ex）",
        params={
            "group_id": "int",
        },
    ),
    # ==================== LLBot 扩展 API (20) ====================
    ExpandAction.BATCH_DELETE_GROUP_MEMBER: APIDef(
        action="batch_delete_group_member",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="批量踢出群成员（LLBot 扩展）",
        params={
            "group_id": "int",
            "user_ids": "list[int]",
        },
    ),
    ExpandAction.SET_GROUP_MSG_MASK: APIDef(
        action="set_group_msg_mask",
        category=APICategory.GROUP_EXT,
        source=APISource.EXPAND,
        description="设置群消息屏蔽（LLBot 扩展）",
        params={
            "group_id": "int",
            "mask": "int",
        },
    ),
    ExpandAction.CREATE_GROUP_ALBUM: APIDef(
        action="create_group_album",
        category=APICategory.GROUP_ALBUM,
        source=APISource.EXPAND,
        description="创建群相册（LLBot 扩展）",
        params={
            "group_id": "int",
            "name": "str",
            "desc": "str",
        },
    ),
    ExpandAction.DELETE_GROUP_ALBUM: APIDef(
        action="delete_group_album",
        category=APICategory.GROUP_ALBUM,
        source=APISource.EXPAND,
        description="删除群相册（LLBot 扩展）",
        params={
            "group_id": "int",
            "album_id": "str",
        },
    ),
    ExpandAction.GET_FLASH_FILE_DOWNLOAD_URLS: APIDef(
        action="get_flash_file_download_urls",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="获取闪传文件集所有文件的下载URL（LLBot 扩展）",
        params={
            "fileset_id": "str",
            "share_link": "str",
        },
    ),
    ExpandAction.UPLOAD_FLASH_FILE: APIDef(
        action="upload_flash_file",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="上传闪传文件（LLBot 扩展）",
        params={
            "title": "str",
            "paths": "list[str]",
        },
    ),
    ExpandAction.RESHARE_FLASH_FILE: APIDef(
        action="reshare_flash_file",
        category=APICategory.FLASH,
        source=APISource.EXPAND,
        description="重新分享闪传文件，获取新的分享链接（LLBot 扩展）",
        params={
            "fileset_id": "str",
            "share_link": "str",
        },
    ),
    ExpandAction.SET_GROUP_FILE_FOREVER: APIDef(
        action="set_group_file_forever",
        category=APICategory.GROUP_FILE,
        source=APISource.EXPAND,
        description="设置群文件永久保存（LLBot 扩展）",
        params={
            "group_id": "int",
            "file_id": "str",
        },
    ),
    ExpandAction.GET_PROFILE_LIKE_ME: APIDef(
        action="get_profile_like_me",
        category=APICategory.USER_EXT,
        source=APISource.EXPAND,
        description="获取自身被点赞列表（LLBot 扩展）",
        params={
            "start": "int",
            "count": "int",
        },
    ),
    ExpandAction.GET_PROFILE_LIKE_COUNT: APIDef(
        action="get_profile_like_count",
        category=APICategory.USER_EXT,
        source=APISource.EXPAND,
        description="获取用户点赞总数（LLBot 扩展）",
        params={
            "user_id": "int",
        },
    ),
    ExpandAction.GET_QQ_AVATAR: APIDef(
        action="get_qq_avatar",
        category=APICategory.USER_EXT,
        source=APISource.EXPAND,
        description="获取QQ头像URL（LLBot 扩展）",
        params={
            "user_id": "int",
            "group_id": "int",
        },
    ),
    ExpandAction.SET_FRIEND_CATEGORY: APIDef(
        action="set_friend_category",
        category=APICategory.USER_EXT,
        source=APISource.EXPAND,
        description="设置好友分类（LLBot 扩展）",
        params={
            "user_id": "int",
            "category_id": "int",
        },
    ),
    ExpandAction.GET_RECOMMEND_FACE: APIDef(
        action="get_recommend_face",
        category=APICategory.EMOJI_EXT,
        source=APISource.EXPAND,
        description="获取推荐表情（LLBot 扩展）",
        params={
            "word": "str",
        },
    ),
    ExpandAction.UNSET_MSG_EMOJI_LIKE: APIDef(
        action="unset_msg_emoji_like",
        category=APICategory.EMOJI_EXT,
        source=APISource.EXPAND,
        description="取消消息表情回应（LLBot 扩展）",
        params={
            "message_id": "int | str",
            "emoji_id": "int",
        },
    ),
    ExpandAction.GET_CONFIG: APIDef(
        action="get_config",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="获取协议端配置（LLBot 扩展）",
        params={},
    ),
    ExpandAction.SET_CONFIG: APIDef(
        action="set_config",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="设置协议端配置（LLBot 扩展）",
        params={
            "config": "dict",
        },
    ),
    ExpandAction.GET_EVENT: APIDef(
        action="get_event",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="获取事件（LLBot 扩展）",
        params={},
    ),
    ExpandAction.LLONEBOT_DEBUG: APIDef(
        action="llonebot_debug",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="调试接口，调用内部API（LLBot 扩展）",
        params={
            "api_class": "str",
            "method": "str",
            "args": "list",
        },
    ),
    ExpandAction.SCAN_QRCODE: APIDef(
        action="scan_qrcode",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="扫码登录（LLBot 扩展）",
        params={
            "qrcode": "str",
        },
    ),
    ExpandAction.GET_GUILD_LIST: APIDef(
        action="get_guild_list",
        category=APICategory.MISC,
        source=APISource.EXPAND,
        description="获取频道列表（NapCat/LLBot 扩展）",
        params={},
    ),
}


# ============================================================================
# 按类别分组的 action 名称列表
# ============================================================================

MESSAGE_APIS: list[str] = [

    OneBotAction.SEND_GROUP_MSG,
    OneBotAction.SEND_PRIVATE_MSG,
    OneBotAction.SEND_MSG,
    OneBotAction.DELETE_MSG,
    OneBotAction.GET_MSG,
    OneBotAction.GET_FORWARD_MSG,
    OneBotAction.SEND_LIKE,
    NapCatAction.SEND_POKE,
    NapCatAction.SEND_FORWARD_MSG,
    GoCqhttpCompatAction.SEND_GROUP_FORWARD_MSG,
    GoCqhttpCompatAction.SEND_PRIVATE_FORWARD_MSG,
    GoCqhttpCompatAction.GET_GROUP_MSG_HISTORY,
    GoCqhttpCompatAction.GET_FRIEND_MSG_HISTORY,
    ExpandAction.FORWARD_FRIEND_SINGLE_MSG,
    ExpandAction.FORWARD_GROUP_SINGLE_MSG,
    GoCqhttpCompatAction.MARK_MSG_AS_READ,
    ExpandAction.MARK_GROUP_MSG_AS_READ,
    ExpandAction.MARK_PRIVATE_MSG_AS_READ,
    ExpandAction.MARK_ALL_AS_READ,
    ExpandAction.UPLOAD_FORWARD_MSG,
]

GROUP_APIS: list[str] = [
    OneBotAction.SET_GROUP_KICK,
    OneBotAction.SET_GROUP_BAN,
    OneBotAction.SET_GROUP_ANONYMOUS_BAN,
    OneBotAction.SET_GROUP_WHOLE_BAN,
    OneBotAction.SET_GROUP_ADMIN,
    OneBotAction.SET_GROUP_ANONYMOUS,
    OneBotAction.SET_GROUP_CARD,
    OneBotAction.SET_GROUP_NAME,
    OneBotAction.SET_GROUP_LEAVE,
    OneBotAction.SET_GROUP_SPECIAL_TITLE,
]

FILE_APIS: list[str] = [
    OneBotAction.UPLOAD_GROUP_FILE,
    OneBotAction.UPLOAD_PRIVATE_FILE,
    NapCatAction.GET_FILE,
    OneBotAction.GET_IMAGE,
    OneBotAction.GET_RECORD,
    NapCatAction.SEND_ONLINE_FILE,
    NapCatAction.SEND_ONLINE_FOLDER,
    NapCatAction.GET_ONLINE_FILE_MSG,
    NapCatAction.RECEIVE_ONLINE_FILE,
    NapCatAction.REFUSE_ONLINE_FILE,
    NapCatAction.CANCEL_ONLINE_FILE,
    ExpandAction.CLEAN_STREAM_TEMP_FILE,
    ExpandAction.UPLOAD_FILE_STREAM,
    ExpandAction.DOWNLOAD_FILE_STREAM,
    ExpandAction.DOWNLOAD_FILE_RECORD_STREAM,
    ExpandAction.DOWNLOAD_FILE_IMAGE_STREAM,
]

ACCOUNT_APIS: list[str] = [
    OneBotAction.GET_LOGIN_INFO,
    OneBotAction.GET_STRANGER_INFO,
    OneBotAction.GET_FRIEND_LIST,
    OneBotAction.GET_GROUP_LIST,
    OneBotAction.GET_GROUP_MEMBER_LIST,
    OneBotAction.GET_GROUP_MEMBER_INFO,
    OneBotAction.GET_GROUP_INFO,
    NapCatAction.GET_GROUP_DETAIL_INFO,
    OneBotAction.GET_GROUP_HONOR_INFO,
    ExpandAction.GET_ROBOT_UIN_RANGE,
]

NAPCAT_EXT_APIS: list[str] = [
    NapCatAction.SET_MSG_EMOJI_LIKE,
    GoCqhttpCompatAction.GET_ESSENCE_MSG_LIST,

    NapCatAction.GET_ONLINE_CLIENTS,
    NapCatAction.GET_COOKIES,
    NapCatAction.GET_CSRF_TOKEN,
    NapCatAction.GET_STATUS,
    NapCatAction.SET_RESTART,
    NapCatAction.CLEAN_CACHE,
    NapCatAction.CAN_SEND_IMAGE,
    NapCatAction.CAN_SEND_RECORD,
    NapCatAction.GET_VERSION_INFO,
    GoCqhttpCompatAction.SET_ESSENCE_MSG,
    GoCqhttpCompatAction.DELETE_ESSENCE_MSG,
    GoCqhttpCompatAction.GET_GROUP_AT_ALL_REMAIN,
    ExpandAction.FETCH_PTT_TEXT,
]

GROUP_FILE_APIS: list[str] = [
    GoCqhttpCompatAction.GET_GROUP_FILE_URL,
    GoCqhttpCompatAction.GET_GROUP_ROOT_FILES,
    GoCqhttpCompatAction.GET_GROUP_FILES_BY_FOLDER,
    GoCqhttpCompatAction.DELETE_GROUP_FILE,
    GoCqhttpCompatAction.CREATE_GROUP_FILE_FOLDER,
    GoCqhttpCompatAction.DELETE_GROUP_FOLDER,
    GoCqhttpCompatAction.GET_GROUP_FILE_SYSTEM_INFO,
    ExpandAction.MOVE_GROUP_FILE,
    ExpandAction.RENAME_GROUP_FILE,
    ExpandAction.RENAME_GROUP_FILE_FOLDER,
    ExpandAction.TRANS_GROUP_FILE,
    ExpandAction.GET_PRIVATE_FILE_URL,
    ExpandAction.SET_GROUP_FILE_FOREVER,
]

GROUP_NOTICE_APIS: list[str] = [
    ExpandAction.SEND_GROUP_NOTICE,
    ExpandAction.GET_GROUP_NOTICE,
    ExpandAction.DEL_GROUP_NOTICE,
]

GROUP_EXT_APIS: list[str] = [
    ExpandAction.SET_GROUP_PORTRAIT,
    ExpandAction.SET_GROUP_REMARK,
    ExpandAction.SET_GROUP_ADD_OPTION,
    ExpandAction.SET_GROUP_SEARCH,
    ExpandAction.SET_GROUP_ROBOT_ADD_OPTION,
    ExpandAction.SET_GROUP_KICK_MEMBERS,
    ExpandAction.GET_GROUP_SHUT_LIST,
    ExpandAction.GET_GROUP_IGNORED_NOTIFIES,
    ExpandAction.GET_GROUP_IGNORE_ADD_REQUEST,
    ExpandAction.GET_GROUP_INFO_EX,
    ExpandAction.SET_GROUP_SIGN,
    ExpandAction.GET_GROUP_SIGNED_LIST,
    ExpandAction.BATCH_DELETE_GROUP_MEMBER,
    ExpandAction.SET_GROUP_MSG_MASK,
]

REQUEST_APIS: list[str] = [
    OneBotAction.SET_FRIEND_ADD_REQUEST,
    OneBotAction.SET_GROUP_ADD_REQUEST,
    OneBotAction.GET_GROUP_SYSTEM_MSG,
    ExpandAction.GET_DOUBT_FRIENDS_ADD_REQUEST,
    ExpandAction.SET_DOUBT_FRIENDS_ADD_REQUEST,
]

USER_EXT_APIS: list[str] = [
    ExpandAction.DELETE_FRIEND,
    ExpandAction.SET_FRIEND_REMARK,
    ExpandAction.GET_FRIENDS_WITH_CATEGORY,
    ExpandAction.GET_UNIDIRECTIONAL_FRIEND_LIST,
    GoCqhttpCompatAction.SET_QQ_PROFILE,
    ExpandAction.SET_QQ_AVATAR,
    ExpandAction.SET_SELF_LONGNICK,
    ExpandAction.GET_RECENT_CONTACT,
    ExpandAction.GET_PROFILE_LIKE,
    ExpandAction.GET_PROFILE_LIKE_ME,
    ExpandAction.GET_PROFILE_LIKE_COUNT,
    ExpandAction.GET_QQ_AVATAR,
    ExpandAction.SET_FRIEND_CATEGORY,
]

STATUS_APIS: list[str] = [
    ExpandAction.SET_ONLINE_STATUS,
    ExpandAction.SET_DIY_ONLINE_STATUS,
    ExpandAction.SET_INPUT_STATUS,
    ExpandAction.NC_GET_USER_STATUS,
]

POKE_APIS: list[str] = [
    ExpandAction.FRIEND_POKE,
    ExpandAction.GROUP_POKE,
]

EMOJI_EXT_APIS: list[str] = [
    ExpandAction.FETCH_CUSTOM_FACE,
    ExpandAction.FETCH_CUSTOM_FACE_DETAIL,
    ExpandAction.ADD_CUSTOM_FACE,
    ExpandAction.DELETE_CUSTOM_FACE,
    ExpandAction.SET_CUSTOM_FACE_DESC,
    ExpandAction.MODIFY_CUSTOM_FACE,
    ExpandAction.MOVE_CUSTOM_FACE_TO_FRONT,
    ExpandAction.FETCH_EMOJI_LIKE,
    ExpandAction.GET_EMOJI_LIKES,
    ExpandAction.SET_GROUP_REACTION,
    ExpandAction.GET_RECOMMEND_FACE,
    ExpandAction.UNSET_MSG_EMOJI_LIKE,
]

AI_VOICE_APIS: list[str] = [
    ExpandAction.GET_AI_CHARACTERS,
    ExpandAction.GET_AI_RECORD,
    ExpandAction.SEND_GROUP_AI_RECORD,
]

CRED_APIS: list[str] = [
    ExpandAction.GET_CLIENTKEY,
    ExpandAction.GET_CREDENTIALS,
    ExpandAction.GET_RKEY,
    ExpandAction.GET_RKEY_SERVER,
    ExpandAction.CHECK_URL_SAFELY,
    GoCqhttpCompatAction.OCR_IMAGE,
    ExpandAction.DOWNLOAD_FILE,
    ExpandAction.REQUEST_DECRYPT_KEY,
]

MISC_APIS: list[str] = [
    ExpandAction.GET_MODEL_SHOW,
    ExpandAction.SET_MODEL_SHOW,
    ExpandAction.BOT_EXIT,
    ExpandAction.NC_GET_PACKET_STATUS,
    ExpandAction.CLICK_INLINE_KEYBOARD_BUTTON,
    ExpandAction.GET_MINI_APP_ARK,
    ExpandAction.TRANSLATE_EN2ZH,
    ExpandAction.CREATE_COLLECTION,
    ExpandAction.GET_COLLECTION_LIST,
    ExpandAction.SEND_PACKET,
    GoCqhttpCompatAction.HANDLE_QUICK_OPERATION,
    GoCqhttpCompatAction.GET_WORD_SLICES,
    ExpandAction.GET_CONFIG,
    ExpandAction.SET_CONFIG,
    ExpandAction.GET_EVENT,
    ExpandAction.LLONEBOT_DEBUG,
    ExpandAction.SCAN_QRCODE,
    ExpandAction.GET_GUILD_LIST,
]

FLASH_APIS: list[str] = [
    ExpandAction.CREATE_FLASH_TASK,
    ExpandAction.SEND_FLASH_MSG,
    ExpandAction.GET_FLASH_FILE_LIST,
    ExpandAction.GET_FLASH_FILE_URL,
    ExpandAction.GET_SHARE_LINK,
    ExpandAction.DOWNLOAD_FILESET,
    ExpandAction.GET_FILESET_INFO,
    ExpandAction.GET_FILESET_ID,
    ExpandAction.LIST_FILESETS,
    ExpandAction.DELETE_FLASH_FILE,
    ExpandAction.RENAME_FLASH_FILE,
    ExpandAction.GET_FLASH_FILE_DOWNLOAD_URLS,
    ExpandAction.UPLOAD_FLASH_FILE,
    ExpandAction.RESHARE_FLASH_FILE,
]

GROUP_ALBUM_APIS: list[str] = [
    ExpandAction.GET_QUN_ALBUM_LIST,
    ExpandAction.UPLOAD_IMAGE_TO_QUN_ALBUM,
    ExpandAction.GET_GROUP_ALBUM_MEDIA_LIST,
    ExpandAction.DO_GROUP_ALBUM_COMMENT,
    ExpandAction.SET_GROUP_ALBUM_MEDIA_LIKE,
    ExpandAction.CANCEL_GROUP_ALBUM_MEDIA_LIKE,
    ExpandAction.DEL_GROUP_ALBUM_MEDIA,
    ExpandAction.CREATE_GROUP_ALBUM,
    ExpandAction.DELETE_GROUP_ALBUM,
]

GROUP_TODO_APIS: list[str] = [
    ExpandAction.SET_GROUP_TODO,
    ExpandAction.COMPLETE_GROUP_TODO,
    ExpandAction.CANCEL_GROUP_TODO,
]

QZONE_APIS: list[str] = [
    ExpandAction.GET_QZONE_MSG_LIST,
    ExpandAction.GET_QZONE_FEEDS,
    ExpandAction.SEND_QZONE_MSG,
    ExpandAction.DELETE_QZONE_MSG,
    ExpandAction.LIKE_QZONE,
    ExpandAction.UNLIKE_QZONE,
    ExpandAction.COMMENT_QZONE,
    ExpandAction.SET_QZONE_BAN,
    ExpandAction.SET_QZONE_MSG_RIGHT,
]

ARK_APIS: list[str] = [
    ExpandAction.SHARE_PEER,
    ExpandAction.SEND_ARK_SHARE,
    ExpandAction.SHARE_GROUP_EX,
    ExpandAction.SEND_GROUP_ARK_SHARE,
]


# ============================================================================
# 查询函数
# ============================================================================


def get_api_def(action: str) -> APIDef | None:
    """根据 action 名称获取 API 定义。

    Args:
        action: API action 名称（如 "send_group_msg"）

    Returns:
        APIDef 实例，未找到时返回 None
    """
    return ALL_APIS.get(action)


def get_apis_by_category(category: APICategory) -> list[str]:
    """获取指定类别的所有 API action 名称列表。

    Args:
        category: API 类别

    Returns:
        该类别下所有 API action 名称列表
    """
    _category_map: dict[APICategory, list[str]] = {
        APICategory.MESSAGE: MESSAGE_APIS,
        APICategory.GROUP: GROUP_APIS,
        APICategory.FILE: FILE_APIS,
        APICategory.ACCOUNT: ACCOUNT_APIS,
        APICategory.NAPCAT_EXT: NAPCAT_EXT_APIS,
        APICategory.GROUP_FILE: GROUP_FILE_APIS,
        APICategory.GROUP_NOTICE: GROUP_NOTICE_APIS,
        APICategory.GROUP_EXT: GROUP_EXT_APIS,
        APICategory.REQUEST: REQUEST_APIS,
        APICategory.USER_EXT: USER_EXT_APIS,
        APICategory.STATUS: STATUS_APIS,
        APICategory.POKE: POKE_APIS,
        APICategory.EMOJI_EXT: EMOJI_EXT_APIS,
        APICategory.AI_VOICE: AI_VOICE_APIS,
        APICategory.CRED: CRED_APIS,
        APICategory.MISC: MISC_APIS,
        APICategory.FLASH: FLASH_APIS,
        APICategory.GROUP_ALBUM: GROUP_ALBUM_APIS,
        APICategory.GROUP_TODO: GROUP_TODO_APIS,
        APICategory.QZONE: QZONE_APIS,
        APICategory.ARK: ARK_APIS,
    }
    return _category_map.get(category, [])


def get_api_categories() -> list[APICategory]:
    """获取所有 API 类别列表。

    Returns:
        所有 API 类别枚举值列表
    """
    return [
        APICategory.MESSAGE,
        APICategory.GROUP,
        APICategory.FILE,
        APICategory.ACCOUNT,
        APICategory.NAPCAT_EXT,
        APICategory.GROUP_FILE,
        APICategory.GROUP_NOTICE,
        APICategory.GROUP_EXT,
        APICategory.REQUEST,
        APICategory.USER_EXT,
        APICategory.STATUS,
        APICategory.POKE,
        APICategory.EMOJI_EXT,
        APICategory.AI_VOICE,
        APICategory.CRED,
        APICategory.MISC,
        APICategory.FLASH,
        APICategory.GROUP_ALBUM,
        APICategory.GROUP_TODO,
        APICategory.QZONE,
        APICategory.ARK,
    ]


# ============================================================================
# 别名机制
# ============================================================================


# 别名到主名的反向映射（模块加载时构建）。
# 主名本身不在此 dict 中：调用 resolve_action 时先查 ALL_APIS，再查此 dict。
_ALIAS_TO_PRIMARY: dict[str, str] = {}
for _action, _def in ALL_APIS.items():
    for _alias in _def.aliases:
        _ALIAS_TO_PRIMARY[_alias] = _action
del _action, _def, _alias


def resolve_action(name: str) -> str | None:
    """输入 action 名，若是别名返回主名，若是主名直接返回，不存在返回 None。

    Args:
        name: action 名称（主名或别名）

    Returns:
        主名 action 字符串，不存在时返回 None

    Examples:
        >>> resolve_action("nc_get_rkey")
        'get_rkey'
        >>> resolve_action("get_rkey")
        'get_rkey'
        >>> resolve_action("._get_model_show")
        '_get_model_show'
        >>> resolve_action("unknown_action")
        None
    """
    if name in ALL_APIS:
        return name
    return _ALIAS_TO_PRIMARY.get(name)


def get_api_def_with_aliases(name: str) -> APIDef | None:
    """根据 action 名（主名或别名）获取 API 定义。

    与 ``get_api_def`` 不同，此函数接受别名作为输入，会先解析为主名再查找。

    Args:
        name: action 名称（主名或别名）

    Returns:
        APIDef 实例，未找到时返回 None
    """
    primary = resolve_action(name)
    if primary is None:
        return None
    return ALL_APIS[primary]


def get_all_action_names() -> list[str]:
    """获取全部 action 名列表（主名 + 别名）。

    Returns:
        全部 action 名列表，包含主名和别名
    """
    names: list[str] = list(ALL_APIS.keys())
    names.extend(_ALIAS_TO_PRIMARY.keys())
    return names


# ============================================================================
# 加载期校验
# ============================================================================


def _validate_api_definitions() -> list[str]:
    """校验 ALL_APIS 的完整性，返回所有问题列表（空列表表示无问题）。

    检查项：
        1. 跨常量类的 action 字符串重复
        2. 别名指向不存在的主名
        3. 别名同时作为 ALL_APIS 的键（应只作为主名的 aliases 字段）
        4. 别名被多个主名声明
        5. source 与常量类归属一致性
        6. 分类列表 (MESSAGE_APIS 等) 与 ALL_APIS 键集合一致

    Returns:
        问题描述列表，每条形如 "[WARN] action=xxx: ..."
    """
    issues: list[str] = []

    # 检查 1：跨常量类 action 字符串重复
    seen: dict[str, str] = {}
    for cls_name, cls in [
        ("OneBotAction", OneBotAction),
        ("NapCatAction", NapCatAction),
        ("GoCqhttpCompatAction", GoCqhttpCompatAction),
        ("ExpandAction", ExpandAction),
    ]:
        for attr in dir(cls):
            if attr.isupper():
                value = getattr(cls, attr)
                if isinstance(value, str):
                    if value in seen:
                        issues.append(
                            f"[WARN] action={value}: 重复定义于 "
                            f"{seen[value]} 和 {cls_name}.{attr}"
                        )
                    else:
                        seen[value] = f"{cls_name}.{attr}"

    # 检查 2 & 3 & 4：别名完整性
    alias_seen: dict[str, str] = {}  # alias -> primary
    for action, api_def in ALL_APIS.items():
        for alias in api_def.aliases:
            # 别名不应作为 ALL_APIS 的键
            if alias in ALL_APIS:
                issues.append(
                    f"[WARN] action={action}: 别名 '{alias}' 同时作为 ALL_APIS 键存在"
                )
            # 别名不应被多个主名声明
            if alias in alias_seen:
                issues.append(
                    f"[WARN] action={action}/{alias_seen[alias]}: "
                    f"别名 '{alias}' 被多个主名声明"
                )
            else:
                alias_seen[alias] = action

    # 检查 5：source 与常量类一致性
    expected_source_map = {
        "OneBotAction": APISource.ONEBOT_V11,
        "NapCatAction": APISource.NAPCAT_EXT,
        "GoCqhttpCompatAction": APISource.GOCQHTTP_COMPAT,
        "ExpandAction": APISource.EXPAND,
    }
    # 反向查找每个 action 字符串来自哪个常量类
    action_to_class: dict[str, str] = {}
    for cls_name, cls in [
        ("OneBotAction", OneBotAction),
        ("NapCatAction", NapCatAction),
        ("GoCqhttpCompatAction", GoCqhttpCompatAction),
        ("ExpandAction", ExpandAction),
    ]:
        for attr in dir(cls):
            if attr.isupper():
                value = getattr(cls, attr)
                if isinstance(value, str) and value not in action_to_class:
                    action_to_class[value] = cls_name
    for action, api_def in ALL_APIS.items():
        cls_name = action_to_class.get(action)
        if cls_name is None:
            # action 字符串未在常量类中定义，跳过 source 检查
            continue
        expected_source = expected_source_map.get(cls_name)
        if expected_source is not None and api_def.source != expected_source:
            issues.append(
                f"[WARN] action={action}: source={api_def.source.value} "
                f"与常量类 {cls_name} 应有 source={expected_source.value} 不一致"
            )

    # 检查 6：分类列表完整性
    all_in_lists: set[str] = set()
    category_lists = [
        MESSAGE_APIS, GROUP_APIS, FILE_APIS, ACCOUNT_APIS,
        NAPCAT_EXT_APIS, GROUP_FILE_APIS, GROUP_NOTICE_APIS,
        GROUP_EXT_APIS, REQUEST_APIS, USER_EXT_APIS, STATUS_APIS,
        POKE_APIS, EMOJI_EXT_APIS, AI_VOICE_APIS, CRED_APIS,
        MISC_APIS, FLASH_APIS, GROUP_ALBUM_APIS, GROUP_TODO_APIS,
        QZONE_APIS, ARK_APIS,
    ]
    for api_list in category_lists:
        for action in api_list:
            if action in all_in_lists:
                issues.append(
                    f"[WARN] action={action}: 在多个分类列表中重复"
                )
            all_in_lists.add(action)

    all_in_dict = set(ALL_APIS.keys())
    missing = all_in_dict - all_in_lists
    extra = all_in_lists - all_in_dict
    if missing:
        issues.append(
            f"[WARN] ALL_APIS 中有 action 未归入任何分类列表: {sorted(missing)}"
        )
    if extra:
        issues.append(
            f"[WARN] 分类列表中有 action 不在 ALL_APIS: {sorted(extra)}"
        )

    return issues


# 模块加载时运行校验，输出 warning（不抛异常，避免阻塞加载）
_validation_issues = _validate_api_definitions()
if _validation_issues:
    import warnings
    for _issue in _validation_issues:
        warnings.warn(_issue, RuntimeWarning, stacklevel=2)
    del _issue
del _validation_issues


__all__ = [
    "APICategory",
    "APISource",
    "APIDef",
    "OneBotAction",
    "NapCatAction",
    "GoCqhttpCompatAction",
    "ExpandAction",
    "NAPCAT_ONLY_APIS",
    "EXPAND_APIS",
    "ADAPTER_SIGNATURE",
    "DEFAULT_TIMEOUT",
    "ALL_APIS",
    "MESSAGE_APIS",
    "GROUP_APIS",
    "FILE_APIS",
    "ACCOUNT_APIS",
    "NAPCAT_EXT_APIS",
    "GROUP_FILE_APIS",
    "GROUP_NOTICE_APIS",
    "GROUP_EXT_APIS",
    "REQUEST_APIS",
    "USER_EXT_APIS",
    "STATUS_APIS",
    "POKE_APIS",
    "EMOJI_EXT_APIS",
    "AI_VOICE_APIS",
    "CRED_APIS",
    "MISC_APIS",
    "FLASH_APIS",
    "GROUP_ALBUM_APIS",
    "GROUP_TODO_APIS",
    "QZONE_APIS",
    "ARK_APIS",
    "get_api_def",
    "get_apis_by_category",
    "get_api_categories",
    "resolve_action",
    "get_api_def_with_aliases",
    "get_all_action_names",
]
