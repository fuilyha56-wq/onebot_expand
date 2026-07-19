"""群相册服务。

封装 NapCat 群相册 API，提供群相册列表查询、图片上传、
媒体列表查询、评论、点赞、取消点赞、删除等功能。

API 列表 (7):
    - get_qun_album_list: 获取群相册列表
    - upload_image_to_qun_album: 上传图片到群相册
    - get_group_album_media_list: 获取群相册媒体列表
    - do_group_album_comment: 评论群相册
    - set_group_album_media_like: 点赞群相册
    - cancel_group_album_media_like: 取消点赞群相册
    - del_group_album_media: 删除群相册媒体
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["GroupAlbumService"]


class GroupAlbumService(BaseService):
    """群相册服务。

    封装全部群相册 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    name: str = "group_album_service"
    description: str = "群相册服务"
    version: str = "1.0.0"

    async def get_qun_album_list(self, group_id: int) -> dict[str, Any]:
        """获取群相册列表。

        对应 NapCat 扩展 API: ``get_qun_album_list``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典，包含相册列表。
        """
        params: dict[str, Any] = {"group_id": group_id}
        return await _call_onebot_api("get_qun_album_list", params)

    async def upload_image_to_qun_album(
        self,
        group_id: int,
        file: str,
        album_id: str = "",
    ) -> dict[str, Any]:
        """上传图片到群相册。

        对应 NapCat 扩展 API: ``upload_image_to_qun_album``。

        Args:
            group_id: 群号。
            file: 图片路径或 URL。
            album_id: 相册 ID，默认为空字符串。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "file": file,
        }
        if album_id:
            params["album_id"] = album_id
        return await _call_onebot_api("upload_image_to_qun_album", params)

    async def get_group_album_media_list(
        self,
        group_id: int,
        album_id: str,
    ) -> dict[str, Any]:
        """获取群相册媒体列表。

        对应 NapCat 扩展 API: ``get_group_album_media_list``。

        Args:
            group_id: 群号。
            album_id: 相册 ID。

        Returns:
            适配器返回的响应字典，包含媒体文件列表。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
        }
        return await _call_onebot_api("get_group_album_media_list", params)

    async def do_group_album_comment(
        self,
        group_id: int,
        album_id: str,
        lloc: str,
        content: str,
    ) -> dict[str, Any]:
        """评论群相册。

        对应 NapCat 扩展 API: ``do_group_album_comment``。

        Args:
            group_id: 群号。
            album_id: 相册 ID。
            lloc: 图片位置标识。
            content: 评论内容。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
            "lloc": lloc,
            "content": content,
        }
        return await _call_onebot_api("do_group_album_comment", params)

    async def set_group_album_media_like(
        self,
        group_id: int,
        album_id: str,
        batch_id: str,
    ) -> dict[str, Any]:
        """点赞群相册。

        对应 NapCat 扩展 API: ``set_group_album_media_like``。

        Args:
            group_id: 群号。
            album_id: 相册 ID。
            batch_id: 批次 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
            "batch_id": batch_id,
        }
        return await _call_onebot_api("set_group_album_media_like", params)

    async def cancel_group_album_media_like(
        self,
        group_id: int,
        album_id: str,
        batch_id: str,
    ) -> dict[str, Any]:
        """取消点赞群相册。

        对应 NapCat 扩展 API: ``cancel_group_album_media_like``。

        Args:
            group_id: 群号。
            album_id: 相册 ID。
            batch_id: 批次 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
            "batch_id": batch_id,
        }
        return await _call_onebot_api("cancel_group_album_media_like", params)

    async def del_group_album_media(
        self,
        group_id: int,
        album_id: str,
        lloc: str,
    ) -> dict[str, Any]:
        """删除群相册媒体。

        对应 NapCat 扩展 API: ``del_group_album_media``。

        Args:
            group_id: 群号。
            album_id: 相册 ID。
            lloc: 图片位置标识。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
            "lloc": lloc,
        }
        return await _call_onebot_api("del_group_album_media", params)

    async def CreateGroupAlbum(
        self,
        group_id: int,
        name: str,
        desc: str,
    ) -> dict[str, Any]:
        """创建群相册。

        对应 OneBot API: ``create_group_album``。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "name": name,
            "desc": desc,
        }
        return await _call_onebot_api("create_group_album", params)

    async def DeleteGroupAlbum(
        self,
        group_id: int,
        album_id: str,
    ) -> dict[str, Any]:
        """删除群相册。

        对应 OneBot API: ``delete_group_album``。
        """
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
        }
        return await _call_onebot_api("delete_group_album", params)

