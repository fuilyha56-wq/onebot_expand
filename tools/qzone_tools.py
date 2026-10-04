"""QQ空间 API 的 Tool 组件。

包含 7 个 QQ 空间 Tool，对应 NapCat QQ 空间 API：
    - get_qzone_msg_list: 获取QQ空间说说列表
    - get_qzone_feeds: 获取QQ空间好友动态
    - send_qzone_msg: 发表说说
    - delete_qzone_msg: 删除说说
    - like_qzone: 给说说点赞
    - unlike_qzone: 取消点赞
    - comment_qzone: 评论说说

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "GetQzoneMsgListTool",
    "GetQzoneFeedsTool",
    "SendQzoneMsgTool",
    "DeleteQzoneMsgTool",
    "LikeQzoneTool",
    "UnlikeQzoneTool",
    "CommentQzoneTool",
    "SetQzoneBanTool",
    "SetQzoneMsgRightTool",
]


class GetQzoneMsgListTool(BaseTool):
    """获取QQ空间说说列表的 Tool。

    对应 NapCat API: ``get_qzone_msg_list``。
    获取当前 Bot 的 QQ 空间说说列表。
    """

    name = "get_qzone_msg_list"
    description = "获取当前Bot的QQ空间说说列表"

    async def execute(
        self,
        pos: Annotated[int, "起始位置"] = 0,
        num: Annotated[int, "获取数量"] = 10,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取QQ空间说说列表。"""
        params: dict[str, Any] = {
            "pos": pos,
            "num": num,
        }
        result = await _call_onebot_api("get_qzone_msg_list", params)
        return result.get("status") == "ok", result


class GetQzoneFeedsTool(BaseTool):
    """获取QQ空间好友动态的 Tool。

    对应 NapCat API: ``get_qzone_feeds``。
    获取 QQ 空间好友动态列表。
    """

    name = "get_qzone_feeds"
    description = "获取QQ空间好友动态列表"

    async def execute(
        self,
        page_num: Annotated[int, "页码"] = 0,
        count: Annotated[int, "每页数量"] = 10,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取QQ空间好友动态。"""
        params: dict[str, Any] = {
            "page_num": page_num,
            "count": count,
        }
        result = await _call_onebot_api("get_qzone_feeds", params)
        return result.get("status") == "ok", result


class SendQzoneMsgTool(BaseTool):
    """发表说说的 Tool。

    对应 NapCat API: ``send_qzone_msg``。
    在 QQ 空间发表说说，支持纯文字或带图，可设置查看权限。
    """

    name = "send_qzone_msg"
    description = "在QQ空间发表说说（支持纯文字或带图，可设置查看权限）"

    async def execute(
        self,
        content: Annotated[str, "说说内容"],
        images: Annotated[list[str] | None, "图片数组（可选），支持 file:// http(s):// base://"] = None,
        ugc_right: Annotated[int, "查看权限：1=所有人可见，4=好友可见，16=部分好友可见，64=仅自己可见，128=部分好友不可见"] = 1,
        target_uins: Annotated[list[int] | None, "权限作用QQ号数组（ugc_right=16/128 时必填）"] = None,
    ) -> tuple[bool, dict[str, Any]]:
        """执行发表说说。"""
        params: dict[str, Any] = {"content": content, "ugc_right": ugc_right}
        if images:
            params["images"] = images
        if target_uins:
            params["target_uins"] = target_uins
        result = await _call_onebot_api("send_qzone_msg", params)
        return result.get("status") == "ok", result


class DeleteQzoneMsgTool(BaseTool):
    """删除说说的 Tool。

    对应 NapCat API: ``delete_qzone_msg``。
    删除 QQ 空间中指定的说说。
    """

    name = "delete_qzone_msg"
    description = "删除QQ空间中指定的说说"

    async def execute(
        self,
        tid: Annotated[str, "说说ID"],
    ) -> tuple[bool, dict[str, Any]]:
        """执行删除说说。"""
        params: dict[str, Any] = {"tid": tid}
        result = await _call_onebot_api("delete_qzone_msg", params)
        return result.get("status") == "ok", result


class LikeQzoneTool(BaseTool):
    """给说说点赞的 Tool。

    对应 NapCat API: ``like_qzone``。
    对 QQ 空间说说点赞。
    """

    name = "like_qzone"
    description = "对QQ空间说说点赞"

    async def execute(
        self,
        tid: Annotated[str, "说说ID"],
        target_uin: Annotated[int, "说说发布者QQ号（可选）"] = 0,
    ) -> tuple[bool, dict[str, Any]]:
        """执行给说说点赞。"""
        params: dict[str, Any] = {"tid": tid}
        if target_uin:
            params["target_uin"] = target_uin
        result = await _call_onebot_api("like_qzone", params)
        return result.get("status") == "ok", result


class UnlikeQzoneTool(BaseTool):
    """取消点赞的 Tool。

    对应 NapCat API: ``unlike_qzone``。
    取消对 QQ 空间说说的点赞。
    """

    name = "unlike_qzone"
    description = "取消对QQ空间说说的点赞"

    async def execute(
        self,
        tid: Annotated[str, "说说ID"],
        target_uin: Annotated[int, "说说发布者QQ号（可选）"] = 0,
    ) -> tuple[bool, dict[str, Any]]:
        """执行取消点赞。"""
        params: dict[str, Any] = {"tid": tid}
        if target_uin:
            params["target_uin"] = target_uin
        result = await _call_onebot_api("unlike_qzone", params)
        return result.get("status") == "ok", result


class CommentQzoneTool(BaseTool):
    """评论说说的 Tool。

    对应 NapCat API: ``comment_qzone``。
    对 QQ 空间说说发表评论，支持纯文字或带图。
    """

    name = "comment_qzone"
    description = "对QQ空间说说发表评论（支持纯文字或带图）"

    async def execute(
        self,
        tid: Annotated[str, "说说ID"],
        content: Annotated[str, "评论内容"],
        target_uin: Annotated[int, "说说发布者QQ号（可选）"] = 0,
        images: Annotated[list[str] | None, "图片数组（可选），支持 file:// http(s):// base://"] = None,
    ) -> tuple[bool, dict[str, Any]]:
        """执行评论说说。"""
        params: dict[str, Any] = {
            "tid": tid,
            "content": content,
        }
        if target_uin:
            params["target_uin"] = target_uin
        if images:
            params["images"] = images
        result = await _call_onebot_api("comment_qzone", params)
        return result.get("status") == "ok", result

class SetQzoneBanTool(BaseTool):
    """QQ 空间拉黑/解除拉黑的 Tool（SnowLuma 扩展）。

    对应扩展 API: ``set_qzone_ban``。
    """

    name = "set_qzone_ban"
    description = "QQ空间拉黑或解除拉黑某人（SnowLuma 扩展）"

    async def execute(
        self,
        user_id: Annotated[int, "目标QQ号"],
        enable: Annotated[bool, "true 拉黑，false 解除拉黑"] = True,
    ) -> tuple[bool, dict[str, Any]]:
        """执行 QQ 空间拉黑。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "enable": enable,
        }
        result = await _call_onebot_api("set_qzone_ban", params)
        return result.get("status") == "ok", result


class SetQzoneMsgRightTool(BaseTool):
    """修改说说查看权限的 Tool（SnowLuma 扩展）。

    对应扩展 API: ``set_qzone_msg_right``。
    """

    name = "set_qzone_msg_right"
    description = "修改一条已发说说的查看权限（SnowLuma 扩展）"

    async def execute(
        self,
        tid: Annotated[str, "说说ID"],
        ugc_right: Annotated[int, "查看权限：1=所有人可见，4=好友可见，16=部分好友可见，64=仅自己可见，128=部分好友不可见"],
        target_uins: Annotated[list[int] | None, "权限作用QQ号数组（ugc_right=16/128 时必填）"] = None,
    ) -> tuple[bool, dict[str, Any]]:
        """执行修改说说权限。"""
        params: dict[str, Any] = {
            "tid": tid,
            "ugc_right": ugc_right,
        }
        if target_uins:
            params["target_uins"] = target_uins
        result = await _call_onebot_api("set_qzone_msg_right", params)
        return result.get("status") == "ok", result
