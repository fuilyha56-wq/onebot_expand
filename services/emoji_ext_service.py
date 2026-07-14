"""表情/收藏扩展服务。

封装 NapCat 表情/收藏扩展 API，提供收藏表情管理、
表情回应查询等功能。

API 列表 (10):
    - fetch_custom_face: 获取收藏表情
    - fetch_custom_face_detail: 获取收藏表情详情列表（NapCat 扩展）
    - add_custom_face: 添加收藏表情
    - delete_custom_face: 删除收藏表情
    - set_custom_face_desc: 修改收藏表情描述（NapCat 扩展）
    - modify_custom_face: 修改收藏表情备注（SnowLuma 扩展）
    - move_custom_face_to_front: 收藏表情移到最前（SnowLuma 扩展）
    - fetch_emoji_like: 获取表情回应分页
    - get_emoji_likes: 获取表情回应用户
    - set_group_reaction: 群聊消息表情回应（SnowLuma 扩展）
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["EmojiExtService"]


class EmojiExtService(BaseService):
    """表情/收藏扩展服务。

    封装全部表情/收藏扩展 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "emoji_ext_service"
    service_description: str = "表情/收藏扩展服务"
    version: str = "1.0.0"

    async def fetch_custom_face(self, count: int = 48) -> dict[str, Any]:
        """获取收藏表情。

        对应 NapCat 扩展 API: ``fetch_custom_face``。

        Args:
            count: 获取数量，默认为 48。

        Returns:
            适配器返回的响应字典，包含收藏表情列表。
        """
        params: dict[str, Any] = {"count": count}
        return await _call_onebot_api("fetch_custom_face", params)

    async def fetch_custom_face_detail(self, count: int = 48) -> dict[str, Any]:
        """获取收藏表情详情列表（NapCat 扩展）。

        对应 NapCat 扩展 API: ``fetch_custom_face_detail``。
        返回 resId/md5/emojiId 等完整字段，删除/改描述前置。

        Args:
            count: 获取数量，默认为 48。

        Returns:
            适配器返回的响应字典，包含收藏表情详情列表。
        """
        params: dict[str, Any] = {"count": count}
        return await _call_onebot_api("fetch_custom_face_detail", params)

    async def add_custom_face(self, file: str) -> dict[str, Any]:
        """添加收藏表情。

        对应 NapCat 扩展 API: ``add_custom_face``。

        Args:
            file: 表情图片路径或 URL。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"file": file}
        return await _call_onebot_api("add_custom_face", params)

    async def delete_custom_face(self, emoji_id: str) -> dict[str, Any]:
        """删除收藏表情。

        对应 NapCat 扩展 API: ``delete_custom_face``。

        Args:
            emoji_id: 表情 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"emoji_id": emoji_id}
        return await _call_onebot_api("delete_custom_face", params)

    async def set_custom_face_desc(
        self,
        emoji_id: int,
        res_id: str,
        md5: str,
        desc: str,
    ) -> dict[str, Any]:
        """修改收藏表情描述（NapCat 扩展）。

        对应 NapCat 扩展 API: ``set_custom_face_desc``。

        Args:
            emoji_id: 表情 ID。
            res_id: 资源 ID。
            md5: 表情 MD5。
            desc: 新的描述。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "emoji_id": emoji_id,
            "res_id": res_id,
            "md5": md5,
            "desc": desc,
        }
        return await _call_onebot_api("set_custom_face_desc", params)

    async def modify_custom_face(
        self,
        emoji_id: str,
        desc: str = "",
    ) -> dict[str, Any]:
        """修改收藏表情备注（SnowLuma 扩展）。

        对应 SnowLuma 扩展 API: ``modify_custom_face``。

        Args:
            emoji_id: 表情 ID。
            desc: 新的备注，默认为空。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "emoji_id": emoji_id,
            "desc": desc,
        }
        return await _call_onebot_api("modify_custom_face", params)

    async def move_custom_face_to_front(self, emoji_id: str) -> dict[str, Any]:
        """收藏表情移到最前（SnowLuma 扩展）。

        对应 SnowLuma 扩展 API: ``move_custom_face_to_front``。

        Args:
            emoji_id: 表情 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"emoji_id": emoji_id}
        return await _call_onebot_api("move_custom_face_to_front", params)

    async def fetch_emoji_like(
        self,
        message_id: int,
        emoji_id: int = 0,
        count: int = 30,
    ) -> dict[str, Any]:
        """获取表情回应分页。

        对应 NapCat 扩展 API: ``fetch_emoji_like``。

        Args:
            message_id: 消息 ID。
            emoji_id: 表情 ID，默认为 0。
            count: 获取数量，默认为 30。

        Returns:
            适配器返回的响应字典，包含表情回应分页数据。
        """
        params: dict[str, Any] = {
            "message_id": message_id,
            "emoji_id": emoji_id,
            "count": count,
        }
        return await _call_onebot_api("fetch_emoji_like", params)

    async def get_emoji_likes(
        self,
        message_id: int,
        emoji_id: int,
    ) -> dict[str, Any]:
        """获取表情回应用户。

        对应 NapCat 扩展 API: ``get_emoji_likes``。

        Args:
            message_id: 消息 ID。
            emoji_id: 表情 ID。

        Returns:
            适配器返回的响应字典，包含表情回应用户列表。
        """
        params: dict[str, Any] = {
            "message_id": message_id,
            "emoji_id": emoji_id,
        }
        return await _call_onebot_api("get_emoji_likes", params)

    async def set_group_reaction(
        self,
        message_id: int,
        code: str,
        group_id: int | None = None,
        is_set: bool = True,
    ) -> dict[str, Any]:
        """群聊消息表情回应（SnowLuma 扩展）。

        对应 SnowLuma 扩展 API: ``set_group_reaction``。
        与 set_msg_emoji_like 不同，此为 SnowLuma 实现。

        Args:
            message_id: 消息 ID。
            code: 表情 code。
            group_id: 群号，可选（不传则由协议端从消息派生）。
            is_set: True=设置，False=取消，默认为 True。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "message_id": message_id,
            "code": code,
            "is_set": is_set,
        }
        if group_id is not None:
            params["group_id"] = group_id
        return await _call_onebot_api("set_group_reaction", params)

    async def GetRecommendFace(
        self,
        word: str,
    ) -> dict[str, Any]:
        """获取推荐表情。

        对应 OneBot API: ``get_recommend_face``。
        """
        params: dict[str, Any] = {
            "word": word,
        }
        return await _call_onebot_api("get_recommend_face", params)

    async def UnSetMsgEmojiLike(
        self,
        message_id: int,
        emoji_id: int,
    ) -> dict[str, Any]:
        """取消消息表情回应。

        对应 OneBot API: ``unset_msg_emoji_like``。
        """
        params: dict[str, Any] = {
            "message_id": message_id,
            "emoji_id": emoji_id,
        }
        return await _call_onebot_api("unset_msg_emoji_like", params)

