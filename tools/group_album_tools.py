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

    tool_name = "get_qun_album_list"
    tool_description = "获取指定群的相册列表"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群相册列表。"""
        params: dict[str, Any] = {"group_id": group_id}
        result = await _call_onebot_api("get_qun_album_list", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取群相册列表失败: {result.get('msg', '未知错误')}"


class UploadImageToQunAlbumTool(BaseTool):
    """上传图片到群相册的 Tool。

    对应 NapCat API: ``upload_image_to_qun_album``。
    上传图片到指定群的相册中。
    """

    tool_name = "upload_image_to_qun_album"
    tool_description = "上传图片到指定群的相册中"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        file: Annotated[str, "图片路径或URL"],
        album_id: Annotated[str, "相册ID（可选）"] = "",
    ) -> tuple[bool, str]:
        """执行上传图片到群相册。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "file": file,
        }
        if album_id:
            params["album_id"] = album_id
        result = await _call_onebot_api("upload_image_to_qun_album", params)
        if result.get("status") == "ok":
            return True, f"图片已上传到群 {group_id} 的相册"
        return False, f"上传图片到群相册失败: {result.get('msg', '未知错误')}"


class GetGroupAlbumMediaListTool(BaseTool):
    """获取群相册媒体列表的 Tool。

    对应 NapCat API: ``get_group_album_media_list``。
    获取指定群相册中的媒体文件列表。
    """

    tool_name = "get_group_album_media_list"
    tool_description = "获取指定群相册中的媒体文件列表"

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
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取群相册媒体列表失败: {result.get('msg', '未知错误')}"


class DoGroupAlbumCommentTool(BaseTool):
    """评论群相册的 Tool。

    对应 NapCat API: ``do_group_album_comment``。
    对群相册中的图片发表评论。
    """

    tool_name = "do_group_album_comment"
    tool_description = "对群相册中的图片发表评论"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        album_id: Annotated[str, "相册ID"],
        lloc: Annotated[str, "图片位置标识"],
        content: Annotated[str, "评论内容"],
    ) -> tuple[bool, str]:
        """执行评论群相册。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
            "lloc": lloc,
            "content": content,
        }
        result = await _call_onebot_api("do_group_album_comment", params)
        if result.get("status") == "ok":
            return True, "评论发送成功"
        return False, f"评论群相册失败: {result.get('msg', '未知错误')}"


class SetGroupAlbumMediaLikeTool(BaseTool):
    """点赞群相册的 Tool。

    对应 NapCat API: ``set_group_album_media_like``。
    对群相册中的图片点赞。
    """

    tool_name = "set_group_album_media_like"
    tool_description = "对群相册中的图片点赞"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        album_id: Annotated[str, "相册ID"],
        batch_id: Annotated[str, "批次ID"],
    ) -> tuple[bool, str]:
        """执行点赞群相册。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
            "batch_id": batch_id,
        }
        result = await _call_onebot_api("set_group_album_media_like", params)
        if result.get("status") == "ok":
            return True, "点赞成功"
        return False, f"点赞群相册失败: {result.get('msg', '未知错误')}"


class CancelGroupAlbumMediaLikeTool(BaseTool):
    """取消点赞群相册的 Tool。

    对应 NapCat API: ``cancel_group_album_media_like``。
    取消对群相册中图片的点赞。
    """

    tool_name = "cancel_group_album_media_like"
    tool_description = "取消对群相册中图片的点赞"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        album_id: Annotated[str, "相册ID"],
        batch_id: Annotated[str, "批次ID"],
    ) -> tuple[bool, str]:
        """执行取消点赞群相册。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
            "batch_id": batch_id,
        }
        result = await _call_onebot_api("cancel_group_album_media_like", params)
        if result.get("status") == "ok":
            return True, "已取消点赞"
        return False, f"取消点赞群相册失败: {result.get('msg', '未知错误')}"


class DelGroupAlbumMediaTool(BaseTool):
    """删除群相册媒体的 Tool。

    对应 NapCat API: ``del_group_album_media``。
    删除群相册中的指定图片。
    """

    tool_name = "del_group_album_media"
    tool_description = "删除群相册中的指定图片"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        album_id: Annotated[str, "相册ID"],
        lloc: Annotated[str, "图片位置标识"],
    ) -> tuple[bool, str]:
        """执行删除群相册媒体。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
            "lloc": lloc,
        }
        result = await _call_onebot_api("del_group_album_media", params)
        if result.get("status") == "ok":
            return True, "图片删除成功"
        return False, f"删除群相册媒体失败: {result.get('msg', '未知错误')}"


class CreateGroupAlbumTool(BaseTool):
    """创建群相册的 Tool。

    对应 API: ``create_group_album``。
    """

    tool_name = "create_group_album"
    tool_description = "创建群相册"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        name: Annotated[str, "相册名称"],
        desc: Annotated[str, "相册描述"],
    ) -> tuple[bool, str]:
        """执行创建群相册。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "name": name,
            "desc": desc,
        }
        result = await _call_onebot_api("create_group_album", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"创建群相册失败: {result.get('msg', '未知错误')}"



class DeleteGroupAlbumTool(BaseTool):
    """删除群相册的 Tool。

    对应 API: ``delete_group_album``。
    """

    tool_name = "delete_group_album"
    tool_description = "删除群相册"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        album_id: Annotated[str, "相册ID"],
    ) -> tuple[bool, str]:
        """执行删除群相册。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "album_id": album_id,
        }
        result = await _call_onebot_api("delete_group_album", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"删除群相册失败: {result.get('msg', '未知错误')}"


