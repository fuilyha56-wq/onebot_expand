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
]


class GetQzoneMsgListTool(BaseTool):
    """获取QQ空间说说列表的 Tool。

    对应 NapCat API: ``get_qzone_msg_list``。
    获取当前 Bot 的 QQ 空间说说列表。
    """

    tool_name = "get_qzone_msg_list"
    tool_description = "获取当前Bot的QQ空间说说列表"

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
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取QQ空间说说列表失败: {result.get('msg', '未知错误')}"


class GetQzoneFeedsTool(BaseTool):
    """获取QQ空间好友动态的 Tool。

    对应 NapCat API: ``get_qzone_feeds``。
    获取 QQ 空间好友动态列表。
    """

    tool_name = "get_qzone_feeds"
    tool_description = "获取QQ空间好友动态列表"

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
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取QQ空间好友动态失败: {result.get('msg', '未知错误')}"


class SendQzoneMsgTool(BaseTool):
    """发表说说的 Tool。

    对应 NapCat API: ``send_qzone_msg``。
    在 QQ 空间发表说说。
    """

    tool_name = "send_qzone_msg"
    tool_description = "在QQ空间发表说说"

    async def execute(
        self,
        content: Annotated[str, "说说内容"],
    ) -> tuple[bool, str]:
        """执行发表说说。"""
        params: dict[str, Any] = {"content": content}
        result = await _call_onebot_api("send_qzone_msg", params)
        if result.get("status") == "ok":
            return True, "说说发表成功"
        return False, f"发表说说失败: {result.get('msg', '未知错误')}"


class DeleteQzoneMsgTool(BaseTool):
    """删除说说的 Tool。

    对应 NapCat API: ``delete_qzone_msg``。
    删除 QQ 空间中指定的说说。
    """

    tool_name = "delete_qzone_msg"
    tool_description = "删除QQ空间中指定的说说"

    async def execute(
        self,
        tid: Annotated[str, "说说ID"],
    ) -> tuple[bool, str]:
        """执行删除说说。"""
        params: dict[str, Any] = {"tid": tid}
        result = await _call_onebot_api("delete_qzone_msg", params)
        if result.get("status") == "ok":
            return True, f"说说 {tid} 已删除"
        return False, f"删除说说失败: {result.get('msg', '未知错误')}"


class LikeQzoneTool(BaseTool):
    """给说说点赞的 Tool。

    对应 NapCat API: ``like_qzone``。
    对 QQ 空间说说点赞。
    """

    tool_name = "like_qzone"
    tool_description = "对QQ空间说说点赞"

    async def execute(
        self,
        tid: Annotated[str, "说说ID"],
        target_uin: Annotated[int, "说说发布者QQ号（可选）"] = 0,
    ) -> tuple[bool, str]:
        """执行给说说点赞。"""
        params: dict[str, Any] = {"tid": tid}
        if target_uin:
            params["target_uin"] = target_uin
        result = await _call_onebot_api("like_qzone", params)
        if result.get("status") == "ok":
            return True, "点赞成功"
        return False, f"点赞说说失败: {result.get('msg', '未知错误')}"


class UnlikeQzoneTool(BaseTool):
    """取消点赞的 Tool。

    对应 NapCat API: ``unlike_qzone``。
    取消对 QQ 空间说说的点赞。
    """

    tool_name = "unlike_qzone"
    tool_description = "取消对QQ空间说说的点赞"

    async def execute(
        self,
        tid: Annotated[str, "说说ID"],
        target_uin: Annotated[int, "说说发布者QQ号（可选）"] = 0,
    ) -> tuple[bool, str]:
        """执行取消点赞。"""
        params: dict[str, Any] = {"tid": tid}
        if target_uin:
            params["target_uin"] = target_uin
        result = await _call_onebot_api("unlike_qzone", params)
        if result.get("status") == "ok":
            return True, "已取消点赞"
        return False, f"取消点赞失败: {result.get('msg', '未知错误')}"


class CommentQzoneTool(BaseTool):
    """评论说说的 Tool。

    对应 NapCat API: ``comment_qzone``。
    对 QQ 空间说说发表评论。
    """

    tool_name = "comment_qzone"
    tool_description = "对QQ空间说说发表评论"

    async def execute(
        self,
        tid: Annotated[str, "说说ID"],
        content: Annotated[str, "评论内容"],
        target_uin: Annotated[int, "说说发布者QQ号（可选）"] = 0,
    ) -> tuple[bool, str]:
        """执行评论说说。"""
        params: dict[str, Any] = {
            "tid": tid,
            "content": content,
        }
        if target_uin:
            params["target_uin"] = target_uin
        result = await _call_onebot_api("comment_qzone", params)
        if result.get("status") == "ok":
            return True, "评论发送成功"
        return False, f"评论说说失败: {result.get('msg', '未知错误')}"