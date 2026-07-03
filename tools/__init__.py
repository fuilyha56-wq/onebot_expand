"""onebot_expand 插件 Tool 组件包。

导出全部 158 个 Tool 类，按功能域分组：
    - 消息相关 (18): message_tools
    - 群操作 (10): group_tools
    - 文件操作 (7): file_tools
    - 账号信息 (9): account_tools
    - NapCat 扩展 (15): napcat_tools
    - 群文件管理 (11): group_file_tools
    - 群公告 (3): group_notice_tools
    - 群管理扩展 (11): group_ext_tools
    - 请求处理 (6): request_tools
    - 用户信息扩展 (9): user_ext_tools
    - 在线状态 (4): status_tools
    - 戳一拍 (2): poke_tools
    - 表情/收藏扩展 (5): emoji_ext_tools
    - AI语音 (3): ai_voice_tools
    - 凭证/安全/下载 (6): cred_tools
    - 机型/其他 (10): misc_tools
    - 闪传 (8): flash_tools
    - 群相册 (7): group_album_tools
    - 群待办 (3): group_todo_tools
    - QQ空间 (7): qzone_tools
    - Ark分享 (4): ark_tools

同时导出模块级共享函数 ``_call_onebot_api``，供各 Tool 模块统一调用。
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.api.adapter_api import send_adapter_command

from ..api_defs import (
    ADAPTER_SIGNATURE,
    DEFAULT_TIMEOUT,
    resolve_action,
)

__all__ = [
    # 消息相关 Tool (18)
    "SendGroupMsgTool",
    "SendPrivateMsgTool",
    "DeleteMsgTool",
    "GetMsgTool",
    "GetForwardMsgTool",
    "SendLikeTool",
    "SendPokeTool",
    "SendForwardMsgTool",
    "SendGroupForwardMsgTool",
    "SendPrivateForwardMsgTool",
    "GetGroupMsgHistoryTool",
    "GetFriendMsgHistoryTool",
    "ForwardFriendSingleMsgTool",
    "ForwardGroupSingleMsgTool",
    "MarkMsgAsReadTool",
    "MarkGroupMsgAsReadTool",
    "MarkPrivateMsgAsReadTool",
    "MarkAllAsReadTool",
    # 群操作 Tool (10)
    "SetGroupKickTool",
    "SetGroupBanTool",
    "SetGroupAnonymousBanTool",
    "SetGroupWholeBanTool",
    "SetGroupAdminTool",
    "SetGroupAnonymousTool",
    "SetGroupCardTool",
    "SetGroupNameTool",
    "SetGroupLeaveTool",
    "SetGroupSpecialTitleTool",
    # 文件操作 Tool (7)
    "UploadFileTool",
    "UploadGroupFileTool",
    "UploadPrivateFileTool",
    "GetFileTool",
    "GetImageTool",
    "GetRecordTool",
    "GetFileUrlTool",
    # 账号信息 Tool (9)
    "GetLoginInfoTool",
    "GetStrangerInfoTool",
    "GetFriendListTool",
    "GetGroupListTool",
    "GetGroupMemberListTool",
    "GetGroupMemberInfoTool",
    "GetGroupInfoTool",
    "GetGroupDetailInfoTool",
    "GetGroupHonorInfoTool",
    # NapCat 扩展 Tool (15)
    "SetMsgEmojiLikeTool",
    "GetEssenceMsgListTool",
    "GetOnlineClientsTool",
    "GetCookiesTool",
    "GetCsrfTokenTool",
    "GetStatusTool",
    "SetRestartTool",
    "CleanCacheTool",
    "CanSendImageTool",
    "CanSendRecordTool",
    "GetVersionInfoTool",
    "SetEssenceMsgTool",
    "DeleteEssenceMsgTool",
    "GetGroupAtAllRemainTool",
    "FetchPttTextTool",
    # 群文件管理 Tool (11)
    "GetGroupFileUrlTool",
    "GetGroupRootFilesTool",
    "GetGroupFilesByFolderTool",
    "DeleteGroupFileTool",
    "CreateGroupFileFolderTool",
    "DeleteGroupFolderTool",
    "GetGroupFileSystemInfoTool",
    "MoveGroupFileTool",
    "RenameGroupFileTool",
    "TransGroupFileTool",
    "GetPrivateFileUrlTool",
    # 群公告 Tool (3)
    "SendGroupNoticeTool",
    "GetGroupNoticeTool",
    "DelGroupNoticeTool",
    # 群管理扩展 Tool (11)
    "SetGroupPortraitTool",
    "SetGroupRemarkTool",
    "SetGroupAddOptionTool",
    "SetGroupSearchTool",
    "SetGroupRobotAddOptionTool",
    "SetGroupKickMembersTool",
    "GetGroupShutListTool",
    "GetGroupIgnoredNotifiesTool",
    "GetGroupIgnoreAddRequestTool",
    "GetGroupInfoExTool",
    "SetGroupSignTool",
    # 请求处理 Tool (6)
    "SetFriendAddRequestTool",
    "SetGroupAddRequestTool",
    "GetGroupSystemMsgTool",
    "GetGroupAddRequestTool",
    "GetDoubtFriendsAddRequestTool",
    "SetDoubtFriendsAddRequestTool",
    # 用户信息扩展 Tool (9)
    "DeleteFriendTool",
    "SetFriendRemarkTool",
    "GetFriendsWithCategoryTool",
    "GetUnidirectionalFriendListTool",
    "SetQQProfileTool",
    "SetQQAvatarTool",
    "SetSelfLongnickTool",
    "GetRecentContactTool",
    "GetProfileLikeTool",
    # 在线状态 Tool (4)
    "SetOnlineStatusTool",
    "SetDiyOnlineStatusTool",
    "SetInputStatusTool",
    "NcGetUserStatusTool",
    # 戳一拍 Tool (2)
    "FriendPokeTool",
    "GroupPokeTool",
    # 表情/收藏扩展 Tool (5)
    "FetchCustomFaceTool",
    "AddCustomFaceTool",
    "DeleteCustomFaceTool",
    "FetchEmojiLikeTool",
    "GetEmojiLikesTool",
    # AI语音 Tool (3)
    "GetAiCharactersTool",
    "GetAiRecordTool",
    "SendGroupAiRecordTool",
    # 凭证/安全/下载 Tool (6)
    "GetClientkeyTool",
    "GetCredentialsTool",
    "GetRkeyTool",
    "CheckUrlSafelyTool",
    "OcrImageTool",
    "DownloadFileTool",
    # 机型/其他 Tool (10)
    "GetModelShowTool",
    "SetModelShowTool",
    "BotExitTool",
    "NcGetPacketStatusTool",
    "ClickInlineKeyboardButtonTool",
    "GetMiniAppArkTool",
    "TranslateEn2zhTool",
    "CreateCollectionTool",
    "GetCollectionListTool",
    "SendPacketTool",
    # 闪传 Tool (8)
    "CreateFlashTaskTool",
    "SendFlashMsgTool",
    "GetFlashFileListTool",
    "GetFlashFileUrlTool",
    "GetShareLinkTool",
    "DownloadFilesetTool",
    "GetFilesetInfoTool",
    "GetFilesetIdTool",
    # 群相册 Tool (7)
    "GetQunAlbumListTool",
    "UploadImageToQunAlbumTool",
    "GetGroupAlbumMediaListTool",
    "DoGroupAlbumCommentTool",
    "SetGroupAlbumMediaLikeTool",
    "CancelGroupAlbumMediaLikeTool",
    "DelGroupAlbumMediaTool",
    # 群待办 Tool (3)
    "SetGroupTodoTool",
    "CompleteGroupTodoTool",
    "CancelGroupTodoTool",
    # QQ空间 Tool (7)
    "GetQzoneMsgListTool",
    "GetQzoneFeedsTool",
    "SendQzoneMsgTool",
    "DeleteQzoneMsgTool",
    "LikeQzoneTool",
    "UnlikeQzoneTool",
    "CommentQzoneTool",
    # Ark分享 Tool (4)
    "SharePeerTool",
    "SendArkShareTool",
    "ShareGroupExTool",
    "SendGroupArkShareTool",
    # 全部 Tool 类列表
    "ALL_TOOLS",
]


async def _call_onebot_api(
    action: str,
    params: dict[str, Any],
    timeout: float = DEFAULT_TIMEOUT,
) -> dict[str, Any]:
    """调用 OneBot API 的统一入口。

    通过 adapter_api 向 onebot_adapter 适配器发送命令，并等待响应。
    1.3.0 起在调用前会先通过 :func:`resolve_action` 将别名解析为主名，
    保证配置开关、协议端兼容性检查、文档引用的一致性。

    Args:
        action: OneBot API action 名称（主名或别名，如 ``"send_group_msg"`` 或 ``"nc_get_rkey"``）。
        params: API 参数字典。
        timeout: 超时时间（秒），默认为 :data:`DEFAULT_TIMEOUT`。

    Returns:
        适配器返回的响应字典，通常包含 ``status``、``retcode``、``data`` 等字段。
        若 action 名（含别名）无法识别，返回 ``{"status": "error", "retcode": -1, "msg": ...}``。
    """
    primary = resolve_action(action)
    if primary is None:
        return {
            "status": "error",
            "retcode": -1,
            "msg": f"未知 action: {action}",
        }
    return await send_adapter_command(
        adapter_sign=ADAPTER_SIGNATURE,
        command_name=primary,
        command_data=params,
        timeout=timeout,
    )


# ============================================================================
# 延迟导入各 Tool 模块，避免循环依赖
# ============================================================================

from .message_tools import (  # noqa: E402
    DeleteMsgTool,
    ForwardFriendSingleMsgTool,
    ForwardGroupSingleMsgTool,
    GetForwardMsgTool,
    GetFriendMsgHistoryTool,
    GetGroupMsgHistoryTool,
    GetMsgTool,
    MarkAllAsReadTool,
    MarkGroupMsgAsReadTool,
    MarkMsgAsReadTool,
    MarkPrivateMsgAsReadTool,
    SendForwardMsgTool,
    SendGroupForwardMsgTool,
    SendGroupMsgTool,
    SendLikeTool,
    SendPrivateForwardMsgTool,
    SendPokeTool,
    SendPrivateMsgTool,
)
from .group_tools import (  # noqa: E402
    SetGroupAdminTool,
    SetGroupAnonymousBanTool,
    SetGroupAnonymousTool,
    SetGroupBanTool,
    SetGroupCardTool,
    SetGroupKickTool,
    SetGroupLeaveTool,
    SetGroupNameTool,
    SetGroupSpecialTitleTool,
    SetGroupWholeBanTool,
)
from .file_tools import (  # noqa: E402
    GetFileTool,
    GetFileUrlTool,
    GetImageTool,
    GetRecordTool,
    UploadFileTool,
    UploadGroupFileTool,
    UploadPrivateFileTool,
)
from .account_tools import (  # noqa: E402
    GetFriendListTool,
    GetGroupDetailInfoTool,
    GetGroupHonorInfoTool,
    GetGroupInfoTool,
    GetGroupListTool,
    GetGroupMemberInfoTool,
    GetGroupMemberListTool,
    GetLoginInfoTool,
    GetStrangerInfoTool,
)
from .napcat_tools import (  # noqa: E402

    CanSendImageTool,
    CanSendRecordTool,
    CleanCacheTool,
    DeleteEssenceMsgTool,
    FetchPttTextTool,
    GetCookiesTool,
    GetCsrfTokenTool,
    GetEssenceMsgListTool,
    GetGroupAtAllRemainTool,
    GetOnlineClientsTool,
    GetStatusTool,
    GetVersionInfoTool,
    SetEssenceMsgTool,
    SetMsgEmojiLikeTool,
    SetRestartTool,
)
from .group_file_tools import (  # noqa: E402
    CreateGroupFileFolderTool,
    DeleteGroupFileTool,
    DeleteGroupFolderTool,
    GetGroupFileUrlTool,
    GetGroupFilesByFolderTool,
    GetGroupFileSystemInfoTool,
    GetGroupRootFilesTool,
    GetPrivateFileUrlTool,
    MoveGroupFileTool,
    RenameGroupFileTool,
    TransGroupFileTool,
)
from .group_notice_tools import (  # noqa: E402
    DelGroupNoticeTool,
    GetGroupNoticeTool,
    SendGroupNoticeTool,
)
from .group_ext_tools import (  # noqa: E402
    GetGroupIgnoredNotifiesTool,
    GetGroupIgnoreAddRequestTool,
    GetGroupInfoExTool,
    GetGroupShutListTool,
    SetGroupAddOptionTool,
    SetGroupKickMembersTool,
    SetGroupPortraitTool,
    SetGroupRemarkTool,
    SetGroupRobotAddOptionTool,
    SetGroupSearchTool,
    SetGroupSignTool,
)
from .request_tools import (  # noqa: E402
    GetDoubtFriendsAddRequestTool,
    GetGroupAddRequestTool,
    GetGroupSystemMsgTool,
    SetDoubtFriendsAddRequestTool,
    SetFriendAddRequestTool,
    SetGroupAddRequestTool,
)
from .user_ext_tools import (  # noqa: E402
    DeleteFriendTool,
    GetFriendsWithCategoryTool,
    GetProfileLikeTool,
    GetRecentContactTool,
    GetUnidirectionalFriendListTool,
    SetFriendRemarkTool,
    SetQQAvatarTool,
    SetQQProfileTool,
    SetSelfLongnickTool,
)
from .status_tools import (  # noqa: E402
    NcGetUserStatusTool,
    SetDiyOnlineStatusTool,
    SetInputStatusTool,
    SetOnlineStatusTool,
)
from .poke_tools import (  # noqa: E402
    FriendPokeTool,
    GroupPokeTool,
)
from .emoji_ext_tools import (  # noqa: E402
    AddCustomFaceTool,
    DeleteCustomFaceTool,
    FetchCustomFaceTool,
    FetchEmojiLikeTool,
    GetEmojiLikesTool,
)
from .ai_voice_tools import (  # noqa: E402
    GetAiCharactersTool,
    GetAiRecordTool,
    SendGroupAiRecordTool,
)
from .cred_tools import (  # noqa: E402
    CheckUrlSafelyTool,
    DownloadFileTool,
    GetClientkeyTool,
    GetCredentialsTool,
    GetRkeyTool,
    OcrImageTool,
)
from .misc_tools import (  # noqa: E402
    BotExitTool,
    ClickInlineKeyboardButtonTool,
    CreateCollectionTool,
    GetCollectionListTool,
    GetMiniAppArkTool,
    GetModelShowTool,
    NcGetPacketStatusTool,
    SendPacketTool,
    SetModelShowTool,
    TranslateEn2zhTool,
)
from .flash_tools import (  # noqa: E402
    CreateFlashTaskTool,
    DownloadFilesetTool,
    GetFilesetIdTool,
    GetFilesetInfoTool,
    GetFlashFileListTool,
    GetFlashFileUrlTool,
    GetShareLinkTool,
    SendFlashMsgTool,
)
from .group_album_tools import (  # noqa: E402
    CancelGroupAlbumMediaLikeTool,
    DelGroupAlbumMediaTool,
    DoGroupAlbumCommentTool,
    GetGroupAlbumMediaListTool,
    GetQunAlbumListTool,
    SetGroupAlbumMediaLikeTool,
    UploadImageToQunAlbumTool,
)
from .group_todo_tools import (  # noqa: E402
    CancelGroupTodoTool,
    CompleteGroupTodoTool,
    SetGroupTodoTool,
)
from .qzone_tools import (  # noqa: E402
    CommentQzoneTool,
    DeleteQzoneMsgTool,
    GetQzoneFeedsTool,
    GetQzoneMsgListTool,
    LikeQzoneTool,
    SendQzoneMsgTool,
    UnlikeQzoneTool,
)
from .ark_tools import (  # noqa: E402
    SendArkShareTool,
    SendGroupArkShareTool,
    ShareGroupExTool,
    SharePeerTool,
)

# 全部 158 个 Tool 类列表
ALL_TOOLS: list[type] = [
    # 消息相关 (18)
    SendGroupMsgTool,
    SendPrivateMsgTool,
    DeleteMsgTool,
    GetMsgTool,
    GetForwardMsgTool,
    SendLikeTool,
    SendPokeTool,
    SendForwardMsgTool,
    SendGroupForwardMsgTool,
    SendPrivateForwardMsgTool,
    GetGroupMsgHistoryTool,
    GetFriendMsgHistoryTool,
    ForwardFriendSingleMsgTool,
    ForwardGroupSingleMsgTool,
    MarkMsgAsReadTool,
    MarkGroupMsgAsReadTool,
    MarkPrivateMsgAsReadTool,
    MarkAllAsReadTool,
    # 群操作 (10)
    SetGroupKickTool,
    SetGroupBanTool,
    SetGroupAnonymousBanTool,
    SetGroupWholeBanTool,
    SetGroupAdminTool,
    SetGroupAnonymousTool,
    SetGroupCardTool,
    SetGroupNameTool,
    SetGroupLeaveTool,
    SetGroupSpecialTitleTool,
    # 文件操作 (7)
    UploadFileTool,
    UploadGroupFileTool,
    UploadPrivateFileTool,
    GetFileTool,
    GetImageTool,
    GetRecordTool,
    GetFileUrlTool,
    # 账号信息 (9)
    GetLoginInfoTool,
    GetStrangerInfoTool,
    GetFriendListTool,
    GetGroupListTool,
    GetGroupMemberListTool,
    GetGroupMemberInfoTool,
    GetGroupInfoTool,
    GetGroupDetailInfoTool,
    GetGroupHonorInfoTool,
    # NapCat 扩展 (15)
    SetMsgEmojiLikeTool,
    GetEssenceMsgListTool,
    GetOnlineClientsTool,
    GetCookiesTool,
    GetCsrfTokenTool,
    GetStatusTool,
    SetRestartTool,
    CleanCacheTool,
    CanSendImageTool,
    CanSendRecordTool,
    GetVersionInfoTool,
    SetEssenceMsgTool,
    DeleteEssenceMsgTool,
    GetGroupAtAllRemainTool,
    FetchPttTextTool,
    # 群文件管理 (11)
    GetGroupFileUrlTool,
    GetGroupRootFilesTool,
    GetGroupFilesByFolderTool,
    DeleteGroupFileTool,
    CreateGroupFileFolderTool,
    DeleteGroupFolderTool,
    GetGroupFileSystemInfoTool,
    MoveGroupFileTool,
    RenameGroupFileTool,
    TransGroupFileTool,
    GetPrivateFileUrlTool,
    # 群公告 (3)
    SendGroupNoticeTool,
    GetGroupNoticeTool,
    DelGroupNoticeTool,
    # 群管理扩展 (11)
    SetGroupPortraitTool,
    SetGroupRemarkTool,
    SetGroupAddOptionTool,
    SetGroupSearchTool,
    SetGroupRobotAddOptionTool,
    SetGroupKickMembersTool,
    GetGroupShutListTool,
    GetGroupIgnoredNotifiesTool,
    GetGroupIgnoreAddRequestTool,
    GetGroupInfoExTool,
    SetGroupSignTool,
    # 请求处理 (6)
    SetFriendAddRequestTool,
    SetGroupAddRequestTool,
    GetGroupSystemMsgTool,
    GetGroupAddRequestTool,
    GetDoubtFriendsAddRequestTool,
    SetDoubtFriendsAddRequestTool,
    # 用户信息扩展 (9)
    DeleteFriendTool,
    SetFriendRemarkTool,
    GetFriendsWithCategoryTool,
    GetUnidirectionalFriendListTool,
    SetQQProfileTool,
    SetQQAvatarTool,
    SetSelfLongnickTool,
    GetRecentContactTool,
    GetProfileLikeTool,
    # 在线状态 (4)
    SetOnlineStatusTool,
    SetDiyOnlineStatusTool,
    SetInputStatusTool,
    NcGetUserStatusTool,
    # 戳一拍 (2)
    FriendPokeTool,
    GroupPokeTool,
    # 表情/收藏扩展 (5)
    FetchCustomFaceTool,
    AddCustomFaceTool,
    DeleteCustomFaceTool,
    FetchEmojiLikeTool,
    GetEmojiLikesTool,
    # AI语音 (3)
    GetAiCharactersTool,
    GetAiRecordTool,
    SendGroupAiRecordTool,
    # 凭证/安全/下载 (6)
    GetClientkeyTool,
    GetCredentialsTool,
    GetRkeyTool,
    CheckUrlSafelyTool,
    OcrImageTool,
    DownloadFileTool,
    # 机型/其他 (10)
    GetModelShowTool,
    SetModelShowTool,
    BotExitTool,
    NcGetPacketStatusTool,
    ClickInlineKeyboardButtonTool,
    GetMiniAppArkTool,
    TranslateEn2zhTool,
    CreateCollectionTool,
    GetCollectionListTool,
    SendPacketTool,
    # 闪传 (8)
    CreateFlashTaskTool,
    SendFlashMsgTool,
    GetFlashFileListTool,
    GetFlashFileUrlTool,
    GetShareLinkTool,
    DownloadFilesetTool,
    GetFilesetInfoTool,
    GetFilesetIdTool,
    # 群相册 (7)
    GetQunAlbumListTool,
    UploadImageToQunAlbumTool,
    GetGroupAlbumMediaListTool,
    DoGroupAlbumCommentTool,
    SetGroupAlbumMediaLikeTool,
    CancelGroupAlbumMediaLikeTool,
    DelGroupAlbumMediaTool,
    # 群待办 (3)
    SetGroupTodoTool,
    CompleteGroupTodoTool,
    CancelGroupTodoTool,
    # QQ空间 (7)
    GetQzoneMsgListTool,
    GetQzoneFeedsTool,
    SendQzoneMsgTool,
    DeleteQzoneMsgTool,
    LikeQzoneTool,
    UnlikeQzoneTool,
    CommentQzoneTool,
    # Ark分享 (4)
    SharePeerTool,
    SendArkShareTool,
    ShareGroupExTool,
    SendGroupArkShareTool,
]
