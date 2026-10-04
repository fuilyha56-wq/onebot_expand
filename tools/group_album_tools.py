"""群相册 API 的 Tool 组件。

包含 7 个群相册 Tool，对应 NapCat 群相册 API：
    - get_qun_album_list: 获取群相册列表
    - upload_image_to_qun_album: 上传图片到群相册
    - get_group_album_media_list: 获取群相册媒体列表
    - do_group_album_comment: 评论群相册
    - set_group_album_media_like: 点赞群相册
    - cancel_group_album_media_like: 取消点赞群相册
    - del_group_album_media: 删除群相册媒体

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "GetQunAlbumListTool",
    "UploadImageToQunAlbumTool",
    "GetGroupAlbumMediaListTool",
    "DoGroupAlbumCommentTool",
    "SetGroupAlbumMediaLikeTool",
    "CancelGroupAlbumMediaLikeTool",
    "DelGroupAlbumMediaTool",
"CreateGroupAlbumTool",
    "DeleteGroupAlbumTool",
]


class GetQunAlbumListTool(BaseTool):
    """获取群相册列表的 Tool。

    对应 NapCat API: ``get_qun_album_list``。
    获取指定群的相册列表。
    """

    name = "get_qun_album_list"
    description = "获取指定群的相册列表"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群相册列表。"""
        params: dict[str, Any] = {"group_id": group_id}
        result = await _call_onebot_api("get_qun_album_list", params)
        return result.get("status") == "ok", result


class UploadImageToQunAlbumTool(BaseTool):
    """上传图片到群相册的 Tool。

    对应 NapCat API: ``upload_image_to_qun_album``。
    上传图片到指定群的相册中。
    """

    name = "upload_image_to_qun_album"
    description = "上传图片到指定群的相册中"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        file: Annotated[str, "图片路径或URL"],
        album_id: Annotated[str, "相册ID（可选）"] = "",
    ) -> tuple[bool, dict[str, Any]]:
        """执行上传图片到群相册。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "file": file,
        }
        if album_id:
            params["album_id"] = album_id
        result = await _call_onebot_api("upload_image_to_qun_album", params)
        return result.get("status") == "ok", result


class GetGroupAlbumMediaListTool(BaseTool):
    """获取群相册媒体列表的 Tool。

    对应 NapCat API: ``get_group_album_media_list``。
    获取指定群相册中的媒体文件列表。
    """

    name = "get_group_album_media_list"
    description = "获取指定群相册中的媒体文件列表"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        album_id: Annotated[str, "相册ID"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群相册媒体列表。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
        }
        result = await _call_onebot_api("get_group_album_media_list", params)
        return result.get("status") == "ok", result


class DoGroupAlbumCommentTool(BaseTool):
    """评论群相册的 Tool。

    对应 NapCat API: ``do_group_album_comment``。
    对群相册中的图片发表评论。
    """

    name = "do_group_album_comment"
    description = "对群相册中的图片发表评论"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        album_id: Annotated[str, "相册ID"],
        lloc: Annotated[str, "图片位置标识"],
        content: Annotated[str, "评论内容"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行评论群相册。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
            "lloc": lloc,
            "content": content,
        }
        result = await _call_onebot_api("do_group_album_comment", params)
        return result.get("status") == "ok", result


class SetGroupAlbumMediaLikeTool(BaseTool):
    """点赞群相册的 Tool。

    对应 NapCat API: ``set_group_album_media_like``。
    对群相册中的图片点赞。
    """

    name = "set_group_album_media_like"
    description = "对群相册中的图片点赞"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        album_id: Annotated[str, "相册ID"],
        batch_id: Annotated[str, "批次ID"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行点赞群相册。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
            "batch_id": batch_id,
        }
        result = await _call_onebot_api("set_group_album_media_like", params)
        return result.get("status") == "ok", result


class CancelGroupAlbumMediaLikeTool(BaseTool):
    """取消点赞群相册的 Tool。

    对应 NapCat API: ``cancel_group_album_media_like``。
    取消对群相册中图片的点赞。
    """

    name = "cancel_group_album_media_like"
    description = "取消对群相册中图片的点赞"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        album_id: Annotated[str, "相册ID"],
        batch_id: Annotated[str, "批次ID"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行取消点赞群相册。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
            "batch_id": batch_id,
        }
        result = await _call_onebot_api("cancel_group_album_media_like", params)
        return result.get("status") == "ok", result


class DelGroupAlbumMediaTool(BaseTool):
    """删除群相册媒体的 Tool。

    对应 NapCat API: ``del_group_album_media``。
    删除群相册中的指定图片。
    """

    name = "del_group_album_media"
    description = "删除群相册中的指定图片"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        album_id: Annotated[str, "相册ID"],
        lloc: Annotated[str, "图片位置标识"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行删除群相册媒体。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
            "lloc": lloc,
        }
        result = await _call_onebot_api("del_group_album_media", params)
        return result.get("status") == "ok", result


class CreateGroupAlbumTool(BaseTool):
    """创建群相册的 Tool。

    对应 API: ``create_group_album``。
    """

    name = "create_group_album"
    description = "创建群相册"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        name: Annotated[str, "相册名称"],
        desc: Annotated[str, "相册描述"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行创建群相册。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "name": name,
            "desc": desc,
        }
        result = await _call_onebot_api("create_group_album", params)
        return result.get("status") == "ok", result



class DeleteGroupAlbumTool(BaseTool):
    """删除群相册的 Tool。

    对应 API: ``delete_group_album``。
    """

    name = "delete_group_album"
    description = "删除群相册"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        album_id: Annotated[str, "相册ID"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行删除群相册。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
        }
        result = await _call_onebot_api("delete_group_album", params)
        return result.get("status") == "ok", result


