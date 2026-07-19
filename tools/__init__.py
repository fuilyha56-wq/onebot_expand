"""onebot_expand 插件 Tool 组件包。

导出全部 205 个 Tool 类，按功能域分组：
    - 消息相关 (20): message_tools
    - 群操作 (10): group_tools
    - 文件操作 (16): file_tools
    - 账号信息 (10): account_tools
    - NapCat 扩展 (15): napcat_tools
    - 群文件管理 (13): group_file_tools
    - 群公告 (3): group_notice_tools
    - 群管理扩展 (14): group_ext_tools
    - 请求处理 (5): request_tools
    - 用户信息扩展 (13): user_ext_tools
    - 在线状态 (4): status_tools
    - 戳一拍 (2): poke_tools
    - 表情/收藏扩展 (12): emoji_ext_tools
    - AI语音 (3): ai_voice_tools
    - 凭证/安全/下载 (8): cred_tools
    - 机型/其他 (18): misc_tools
    - 闪传 (14): flash_tools
    - 群相册 (9): group_album_tools
    - 群待办 (3): group_todo_tools
    - QQ空间 (9): qzone_tools
    - Ark分享 (4): ark_tools

同时导出模块级共享函数 ``_call_onebot_api``，供各 Tool 模块统一调用。
"""

from __future__ import annotations

import functools
from typing import Any

from src.app.plugin_system.api.adapter_api import send_adapter_command

from ..api_defs import (
    ADAPTER_SIGNATURE,
    DEFAULT_TIMEOUT,
    resolve_action,
)
from ..message_utils import normalize_message_ids

__all__ = [
    # 消息相关 Tool (18)
    "SendGroupMsgTool",
    "SendPrivateMsgTool",
    "SendMsgTool",
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
    "UploadForwardMsgTool",
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
    # 文件操作 Tool (11)
    "UploadGroupFileTool",
    "UploadPrivateFileTool",
    "GetFileTool",
    "GetImageTool",
    "GetRecordTool",
    "SendOnlineFileTool",
    "SendOnlineFolderTool",
    "GetOnlineFileMsgTool",
    "ReceiveOnlineFileTool",
    "RefuseOnlineFileTool",
    "CancelOnlineFileTool",
    "CleanStreamTempFileTool",
    "UploadFileStreamTool",
    "DownloadFileStreamTool",
    "DownloadFileRecordStreamTool",
    "DownloadFileImageStreamTool",
    # 账号信息 Tool (10)
    "GetLoginInfoTool",
    "GetStrangerInfoTool",
    "GetFriendListTool",
    "GetGroupListTool",
    "GetGroupMemberListTool",
    "GetGroupMemberInfoTool",
    "GetGroupInfoTool",
    "GetGroupDetailInfoTool",
    "GetGroupHonorInfoTool",
    "GetRobotUinRangeTool",
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
    "RenameGroupFileFolderTool",
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
    "GetGroupSignedListTool",
    # 请求处理 Tool (5)
    "SetFriendAddRequestTool",
    "SetGroupAddRequestTool",
    "GetGroupSystemMsgTool",
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
    # 表情/收藏扩展 Tool (10)
    "FetchCustomFaceTool",
    "FetchCustomFaceDetailTool",
    "AddCustomFaceTool",
    "DeleteCustomFaceTool",
    "SetCustomFaceDescTool",
    "ModifyCustomFaceTool",
    "MoveCustomFaceToFrontTool",
    "FetchEmojiLikeTool",
    "GetEmojiLikesTool",
    "SetGroupReactionTool",
    # AI语音 Tool (3)
    "GetAiCharactersTool",
    "GetAiRecordTool",
    "SendGroupAiRecordTool",
    # 凭证/安全/下载 Tool (6)
    "GetClientkeyTool",
    "GetCredentialsTool",
    "GetRkeyTool",
    "GetRkeyServerTool",
    "CheckUrlSafelyTool",
    "OcrImageTool",
    "DownloadFileTool",
    "RequestDecryptKeyTool",
    # 机型/其他 Tool (12)
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
    "HandleQuickOperationTool",
    "GetWordSlicesTool",
    # 闪传 Tool (8)
    "CreateFlashTaskTool",
    "SendFlashMsgTool",
    "GetFlashFileListTool",
    "GetFlashFileUrlTool",
    "GetShareLinkTool",
    "DownloadFilesetTool",
    "GetFilesetInfoTool",
    "GetFilesetIdTool",
    "ListFilesetsTool",
    "DeleteFlashFileTool",
    "RenameFlashFileTool",
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
    "SetQzoneBanTool",
    "SetQzoneMsgRightTool",
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
    调用前会先通过 :func:`resolve_action` 将别名解析为主名，
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
        command_data=normalize_message_ids(params),
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
    SendMsgTool,
    SendPrivateForwardMsgTool,
    SendPokeTool,
    SendPrivateMsgTool,
    UploadForwardMsgTool,
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
    GetImageTool,
    GetRecordTool,
    UploadGroupFileTool,
    UploadPrivateFileTool,
    SendOnlineFileTool,
    SendOnlineFolderTool,
    GetOnlineFileMsgTool,
    ReceiveOnlineFileTool,
    RefuseOnlineFileTool,
    CancelOnlineFileTool,
    CleanStreamTempFileTool,
    UploadFileStreamTool,
    DownloadFileStreamTool,
    DownloadFileRecordStreamTool,
    DownloadFileImageStreamTool,
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
    GetRobotUinRangeTool,
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
    RenameGroupFileFolderTool,
    SetGroupFileForeverTool,
    TransGroupFileTool,
)
from .group_notice_tools import (  # noqa: E402
    DelGroupNoticeTool,
    GetGroupNoticeTool,
    SendGroupNoticeTool,
)
from .group_ext_tools import (  # noqa: E402
    BatchDeleteGroupMemberTool,
    GetGroupIgnoredNotifiesTool,
    GetGroupIgnoreAddRequestTool,
    GetGroupInfoExTool,
    GetGroupShutListTool,
    GetGroupSignedListTool,
    SetGroupAddOptionTool,
    SetGroupKickMembersTool,
    SetGroupMsgMaskTool,
    SetGroupPortraitTool,
    SetGroupRemarkTool,
    SetGroupRobotAddOptionTool,
    SetGroupSearchTool,
    SetGroupSignTool,
)
from .request_tools import (  # noqa: E402
    GetDoubtFriendsAddRequestTool,
    GetGroupSystemMsgTool,
    SetDoubtFriendsAddRequestTool,
    SetFriendAddRequestTool,
    SetGroupAddRequestTool,
)
from .user_ext_tools import (  # noqa: E402
    DeleteFriendTool,
    GetFriendsWithCategoryTool,
    GetProfileLikeMeTool,
    GetProfileLikeCountTool,
    GetProfileLikeTool,
    GetQQAvatarTool,
    GetRecentContactTool,
    GetUnidirectionalFriendListTool,
    SetFriendCategoryTool,
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
    FetchCustomFaceDetailTool,
    FetchCustomFaceTool,
    FetchEmojiLikeTool,
    GetEmojiLikesTool,
    GetRecommendFaceTool,
    ModifyCustomFaceTool,
    MoveCustomFaceToFrontTool,
    SetCustomFaceDescTool,
    SetGroupReactionTool,
    UnsetMsgEmojiLikeTool,
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
    GetRkeyServerTool,
    GetRkeyTool,
    OcrImageTool,
    RequestDecryptKeyTool,
)
from .misc_tools import (  # noqa: E402
    BotExitTool,
    ClickInlineKeyboardButtonTool,
    CreateCollectionTool,
    GetCollectionListTool,
    GetConfigTool,
    GetEventTool,
    GetGuildListTool,
    GetMiniAppArkTool,
    GetModelShowTool,
    GetWordSlicesTool,
    HandleQuickOperationTool,
    LlonebotDebugTool,
    NcGetPacketStatusTool,
    ScanQRCodeTool,
    SendPacketTool,
    SetConfigTool,
    SetModelShowTool,
    TranslateEn2zhTool,
)
from .flash_tools import (  # noqa: E402
    CreateFlashTaskTool,
    DeleteFlashFileTool,
    DownloadFilesetTool,
    GetFilesetIdTool,
    GetFilesetInfoTool,
    GetFlashFileDownloadUrlsTool,
    GetFlashFileListTool,
    GetFlashFileUrlTool,
    GetShareLinkTool,
    ListFilesetsTool,
    RenameFlashFileTool,
    ReshareFlashFileTool,
    SendFlashMsgTool,
    UploadFlashFileTool,
)
from .group_album_tools import (  # noqa: E402
    CancelGroupAlbumMediaLikeTool,
    CreateGroupAlbumTool,
    DelGroupAlbumMediaTool,
    DeleteGroupAlbumTool,
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
    SetQzoneBanTool,
    SetQzoneMsgRightTool,
    UnlikeQzoneTool,
)
from .ark_tools import (  # noqa: E402
    SendArkShareTool,
    SendGroupArkShareTool,
    ShareGroupExTool,
    SharePeerTool,
)

# 全部 205 个 Tool 类列表
ALL_TOOLS: list[type] = [
    # 消息相关 (18)
    SendGroupMsgTool,
    SendPrivateMsgTool,
    SendMsgTool,
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
    UploadForwardMsgTool,
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
    # 文件操作 (11)
    UploadGroupFileTool,
    UploadPrivateFileTool,
    GetFileTool,
    GetImageTool,
    GetRecordTool,
    SendOnlineFileTool,
    SendOnlineFolderTool,
    GetOnlineFileMsgTool,
    ReceiveOnlineFileTool,
    RefuseOnlineFileTool,
    CancelOnlineFileTool,
    CleanStreamTempFileTool,
    UploadFileStreamTool,
    DownloadFileStreamTool,
    DownloadFileRecordStreamTool,
    DownloadFileImageStreamTool,
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
    GetRobotUinRangeTool,
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
    RenameGroupFileFolderTool,
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
    GetGroupSignedListTool,
    # 请求处理 (5)
    SetFriendAddRequestTool,
    SetGroupAddRequestTool,
    GetGroupSystemMsgTool,
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
    # 表情/收藏扩展 (10)
    FetchCustomFaceTool,
    FetchCustomFaceDetailTool,
    AddCustomFaceTool,
    DeleteCustomFaceTool,
    SetCustomFaceDescTool,
    ModifyCustomFaceTool,
    MoveCustomFaceToFrontTool,
    FetchEmojiLikeTool,
    GetEmojiLikesTool,
    SetGroupReactionTool,
    # AI语音 (3)
    GetAiCharactersTool,
    GetAiRecordTool,
    SendGroupAiRecordTool,
    # 凭证/安全/下载 (6)
    GetClientkeyTool,
    GetCredentialsTool,
    GetRkeyTool,
    GetRkeyServerTool,
    CheckUrlSafelyTool,
    OcrImageTool,
    DownloadFileTool,
    RequestDecryptKeyTool,
    # 机型/其他 (12)
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
    HandleQuickOperationTool,
    GetWordSlicesTool,
    # 闪传 (8)
    CreateFlashTaskTool,
    SendFlashMsgTool,
    GetFlashFileListTool,
    GetFlashFileUrlTool,
    GetShareLinkTool,
    DownloadFilesetTool,
    GetFilesetInfoTool,
    GetFilesetIdTool,
    ListFilesetsTool,
    DeleteFlashFileTool,
    RenameFlashFileTool,
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
    SetQzoneBanTool,
    SetQzoneMsgRightTool,
    # Ark分享 (4)
    SharePeerTool,
    SendArkShareTool,
    ShareGroupExTool,
    SendGroupArkShareTool,
    # group_ext_tools 新增
    BatchDeleteGroupMemberTool,
    SetGroupMsgMaskTool,
    # group_album_tools 新增
    CreateGroupAlbumTool,
    DeleteGroupAlbumTool,
    # flash_tools 新增
    GetFlashFileDownloadUrlsTool,
    UploadFlashFileTool,
    ReshareFlashFileTool,
    # group_file_tools 新增
    SetGroupFileForeverTool,
    # user_ext_tools 新增
    GetProfileLikeMeTool,
    GetProfileLikeCountTool,
    GetQQAvatarTool,
    SetFriendCategoryTool,
    # emoji_ext_tools 新增
    GetRecommendFaceTool,
    UnsetMsgEmojiLikeTool,
    # misc_tools 新增
    GetConfigTool,
    SetConfigTool,
    GetEventTool,
    LlonebotDebugTool,
    ScanQRCodeTool,
    GetGuildListTool,
]


# ============================================================================
# Tool 执行阶段开关保护
# ============================================================================
#
# 插件入口会在注册阶段按 ``enable_all_tools`` 和独立开关过滤工具。
# 本包装器作为第二层保护，避免旧实例或配置异常绕过注册过滤。
#
# Service 不走 Tool.execute，故不受影响，始终可用——其他插件通过 Service
# 调用的路径不会被总开关拦截。Tool 直接调 ``_call_onebot_api`` 也不经过
# Service 层的 ``_is_api_enabled``，所以 Tool 路径的独立开关拦截由本包装器
# 顺带处理。


from ..api_defs import resolve_action as _resolve_action


def _is_tool_master_switch_on(plugin: Any) -> bool:
    """读取工具总开关状态。配置缺失时默认关闭。"""
    try:
        switches = getattr(getattr(plugin, "config", None), "api_switches", None)
        if switches is None:
            return False
        return bool(getattr(switches, "enable_all_tools", False))
    except (AttributeError, TypeError):
        return False


def _is_tool_independently_enabled(plugin: Any, tool_name: str) -> bool:
    """读取单个 Tool 的独立开关状态。

    tool_name 应等于 action 主名。若 Tool 类的 name 与主名不一致
    （历史遗留），通过 resolve_action 解析到主名后查 ``enable_<primary>``。
    """
    try:
        switches = getattr(getattr(plugin, "config", None), "api_switches", None)
        if switches is None:
            return False
        primary = _resolve_action(tool_name) or tool_name
        return bool(getattr(switches, f"enable_{primary}", False))
    except (AttributeError, ImportError, TypeError):
        return False


def _wrap_tool_execute(tool_cls: type) -> None:
    """给 Tool.execute 加总开关 + 独立开关前置检查。原地修改，幂等。"""
    original = tool_cls.execute
    if getattr(original, "_onebot_expand_wrapped", False):
        return

    @functools.wraps(original)
    async def wrapped(self: Any, *args: Any, **kwargs: Any) -> tuple[bool, Any]:
        plugin = getattr(self, "plugin", None)
        if not _is_tool_master_switch_on(plugin):
            return False, "工具已被总开关禁用（enable_all_tools=False）"
        tool_name = getattr(tool_cls, "name", "")
        if tool_name and not _is_tool_independently_enabled(plugin, tool_name):
            return False, f"工具 {tool_name} 已被独立开关禁用"
        return await original(self, *args, **kwargs)

    wrapped._onebot_expand_wrapped = True  # type: ignore[attr-defined]
    tool_cls.execute = wrapped  # type: ignore[assignment]


for _tool_cls in ALL_TOOLS:
    _wrap_tool_execute(_tool_cls)
del _tool_cls
