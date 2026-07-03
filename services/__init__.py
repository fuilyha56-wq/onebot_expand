"""onebot_expand 插件 Service 组件包。

导出全部 23 个 Service 类，按功能域分组：
    - 消息发送与管理: MessageService
    - 群管理操作: GroupService
    - 文件上传与管理: FileService
    - 账号与群组信息查询: AccountService
    - NapCat 扩展功能: NapcatExtService
    - QQNT 表情表查询: EmojiService
    - 文件路径映射: PathMapperService
    - 群文件管理: GroupFileService
    - 群公告管理: GroupNoticeService
    - 群管理扩展: GroupExtService
    - 请求处理: RequestService
    - 用户信息扩展: UserExtService
    - 在线状态: StatusService
    - 戳一拍: PokeService
    - 表情/收藏扩展: EmojiExtService
    - AI语音: AiVoiceService
    - 凭证/安全/下载: CredService
    - 机型/其他: MiscService
    - 闪传: FlashService
    - 群相册: GroupAlbumService
    - 群待办: GroupTodoService
    - QQ空间: QzoneService
    - Ark分享: ArkService

所有 Service 继承 BaseService，通过 ``__init__(plugin)`` 构造，
通过 ``self.plugin.config`` 访问配置。
"""

from __future__ import annotations

from .account_service import AccountService
from .ai_voice_service import AiVoiceService
from .ark_service import ArkService
from .cred_service import CredService
from .emoji_ext_service import EmojiExtService
from .emoji_service import EmojiService
from .file_service import FileService
from .flash_service import FlashService
from .group_album_service import GroupAlbumService
from .group_ext_service import GroupExtService
from .group_file_service import GroupFileService
from .group_notice_service import GroupNoticeService
from .group_service import GroupService
from .group_todo_service import GroupTodoService
from .message_service import MessageService
from .misc_service import MiscService
from .napcat_service import NapcatExtService
from .path_mapper_service import PathMapperService
from .poke_service import PokeService
from .qzone_service import QzoneService
from .request_service import RequestService
from .status_service import StatusService
from .user_ext_service import UserExtService

__all__ = [
    "MessageService",
    "GroupService",
    "FileService",
    "AccountService",
    "NapcatExtService",
    "EmojiService",
    "PathMapperService",
    "GroupFileService",
    "GroupNoticeService",
    "GroupExtService",
    "RequestService",
    "UserExtService",
    "StatusService",
    "PokeService",
    "EmojiExtService",
    "AiVoiceService",
    "CredService",
    "MiscService",
    "FlashService",
    "GroupAlbumService",
    "GroupTodoService",
    "QzoneService",
    "ArkService",
    "ALL_SERVICES",
]


# 全部 23 个 Service 类列表，按功能域排序
ALL_SERVICES: list[type] = [
    MessageService,
    GroupService,
    FileService,
    AccountService,
    NapcatExtService,
    EmojiService,
    PathMapperService,
    GroupFileService,
    GroupNoticeService,
    GroupExtService,
    RequestService,
    UserExtService,
    StatusService,
    PokeService,
    EmojiExtService,
    AiVoiceService,
    CredService,
    MiscService,
    FlashService,
    GroupAlbumService,
    GroupTodoService,
    QzoneService,
    ArkService,
]
