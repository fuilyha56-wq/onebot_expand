"""表情/收藏扩展 API 的 Tool 组件。

包含 11 个表情/收藏扩展 Tool，对应 NapCat/SnowLuma 表情/收藏扩展 API：
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

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
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
"GetRecommendFaceTool",
    "UnsetMsgEmojiLikeTool",
]


class FetchCustomFaceTool(BaseTool):
    """获取收藏表情的 Tool。

    对应 NapCat API: ``fetch_custom_face``。
    获取当前 Bot 的收藏表情列表。
    """

    tool_name = "fetch_custom_face"
    tool_description = "获取当前Bot的收藏表情列表"

    async def execute(
        self,
        count: Annotated[int, "获取数量"] = 48,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取收藏表情。"""
        params: dict[str, Any] = {"count": count}
        result = await _call_onebot_api("fetch_custom_face", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取收藏表情失败: {result.get('msg', '未知错误')}"


class FetchCustomFaceDetailTool(BaseTool):
    """获取收藏表情详情列表的 Tool（NapCat 扩展）。

    对应 NapCat API: ``fetch_custom_face_detail``。
    返回收藏表情的完整信息（resId/md5/emojiId 等），删除/改描述前置。
    """

    tool_name = "fetch_custom_face_detail"
    tool_description = "获取收藏表情详情列表（NapCat扩展）"

    async def execute(
        self,
        count: Annotated[int, "获取数量"] = 48,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取收藏表情详情。"""
        params: dict[str, Any] = {"count": count}
        result = await _call_onebot_api("fetch_custom_face_detail", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取收藏表情详情失败: {result.get('msg', '未知错误')}"


class AddCustomFaceTool(BaseTool):
    """添加收藏表情的 Tool。

    对应 NapCat API: ``add_custom_face``。
    添加表情到收藏列表。
    """

    tool_name = "add_custom_face"
    tool_description = "添加表情到收藏列表"

    async def execute(
        self,
        file: Annotated[str, "表情图片路径或URL"],
    ) -> tuple[bool, str]:
        """执行添加收藏表情。"""
        params: dict[str, Any] = {"file": file}
        result = await _call_onebot_api("add_custom_face", params)
        if result.get("status") == "ok":
            return True, "收藏表情添加成功"
        return False, f"添加收藏表情失败: {result.get('msg', '未知错误')}"


class DeleteCustomFaceTool(BaseTool):
    """删除收藏表情的 Tool。

    对应 NapCat API: ``delete_custom_face``。
    从收藏列表中删除指定表情。
    """

    tool_name = "delete_custom_face"
    tool_description = "从收藏列表中删除指定表情"

    async def execute(
        self,
        emoji_id: Annotated[str, "表情ID"],
    ) -> tuple[bool, str]:
        """执行删除收藏表情。"""
        params: dict[str, Any] = {"emoji_id": emoji_id}
        result = await _call_onebot_api("delete_custom_face", params)
        if result.get("status") == "ok":
            return True, f"已删除收藏表情 {emoji_id}"
        return False, f"删除收藏表情失败: {result.get('msg', '未知错误')}"


class SetCustomFaceDescTool(BaseTool):
    """修改收藏表情描述的 Tool（NapCat 扩展）。

    对应 NapCat API: ``set_custom_face_desc``。
    修改收藏表情的描述文字。
    """

    tool_name = "set_custom_face_desc"
    tool_description = "修改收藏表情描述（NapCat扩展）"

    async def execute(
        self,
        emoji_id: Annotated[int, "表情ID"],
        res_id: Annotated[str, "资源ID"],
        md5: Annotated[str, "表情MD5"],
        desc: Annotated[str, "新的描述"],
    ) -> tuple[bool, str]:
        """执行修改收藏表情描述。"""
        params: dict[str, Any] = {
            "emoji_id": emoji_id,
            "res_id": res_id,
            "md5": md5,
            "desc": desc,
        }
        result = await _call_onebot_api("set_custom_face_desc", params)
        if result.get("status") == "ok":
            return True, "收藏表情描述已更新"
        return False, f"修改收藏表情描述失败: {result.get('msg', '未知错误')}"


class ModifyCustomFaceTool(BaseTool):
    """修改收藏表情备注的 Tool（SnowLuma 扩展）。

    对应 SnowLuma API: ``modify_custom_face``。
    修改收藏表情的备注。
    """

    tool_name = "modify_custom_face"
    tool_description = "修改收藏表情备注（SnowLuma扩展）"

    async def execute(
        self,
        emoji_id: Annotated[str, "表情ID"],
        desc: Annotated[str, "新的备注"] = "",
    ) -> tuple[bool, str]:
        """执行修改收藏表情备注。"""
        params: dict[str, Any] = {
            "emoji_id": emoji_id,
            "desc": desc,
        }
        result = await _call_onebot_api("modify_custom_face", params)
        if result.get("status") == "ok":
            return True, "收藏表情备注已更新"
        return False, f"修改收藏表情备注失败: {result.get('msg', '未知错误')}"


class MoveCustomFaceToFrontTool(BaseTool):
    """收藏表情移到最前的 Tool（SnowLuma 扩展）。

    对应 SnowLuma API: ``move_custom_face_to_front``。
    将指定收藏表情移到列表最前。
    """

    tool_name = "move_custom_face_to_front"
    tool_description = "将指定收藏表情移到列表最前（SnowLuma扩展）"

    async def execute(
        self,
        emoji_id: Annotated[str, "表情ID"],
    ) -> tuple[bool, str]:
        """执行收藏表情移到最前。"""
        params: dict[str, Any] = {"emoji_id": emoji_id}
        result = await _call_onebot_api("move_custom_face_to_front", params)
        if result.get("status") == "ok":
            return True, "收藏表情已移到最前"
        return False, f"移动收藏表情失败: {result.get('msg', '未知错误')}"


class FetchEmojiLikeTool(BaseTool):
    """获取表情回应分页的 Tool。

    对应 NapCat API: ``fetch_emoji_like``。
    获取指定消息的表情回应分页数据。
    """

    tool_name = "fetch_emoji_like"
    tool_description = "获取指定消息的表情回应分页数据"

    async def execute(
        self,
        message_id: Annotated[int, "目标消息ID"],
        emoji_id: Annotated[int, "表情ID"] = 0,
        count: Annotated[int, "获取数量"] = 30,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取表情回应分页。"""
        params: dict[str, Any] = {
            "message_id": message_id,
            "emoji_id": emoji_id,
            "count": count,
        }
        result = await _call_onebot_api("fetch_emoji_like", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取表情回应分页失败: {result.get('msg', '未知错误')}"


class GetEmojiLikesTool(BaseTool):
    """获取表情回应用户的 Tool。

    对应 NapCat API: ``get_emoji_likes``。
    获取指定消息上某表情的回应用户列表。
    """

    tool_name = "get_emoji_likes"
    tool_description = "获取指定消息上某表情的回应用户列表"

    async def execute(
        self,
        message_id: Annotated[int, "目标消息ID"],
        emoji_id: Annotated[int, "表情ID"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取表情回应用户。"""
        params: dict[str, Any] = {
            "message_id": message_id,
            "emoji_id": emoji_id,
        }
        result = await _call_onebot_api("get_emoji_likes", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取表情回应用户失败: {result.get('msg', '未知错误')}"


class SetGroupReactionTool(BaseTool):
    """群聊消息表情回应的 Tool（SnowLuma 扩展）。

    对应 SnowLuma API: ``set_group_reaction``。
    对群消息进行表情回应（与 set_msg_emoji_like 不同，此为 SnowLuma 实现）。
    """

    tool_name = "set_group_reaction"
    tool_description = "对群消息进行表情回应（SnowLuma扩展）"

    async def execute(
        self,
        message_id: Annotated[int, "目标消息ID"],
        code: Annotated[str, "表情code"],
        group_id: Annotated[int, "群号（可选，不传则自动从消息派生）"] = 0,
        is_set: Annotated[bool, "True=设置，False=取消"] = True,
    ) -> tuple[bool, str]:
        """执行群聊消息表情回应。"""
        params: dict[str, Any] = {
            "message_id": message_id,
            "code": code,
            "is_set": is_set,
        }
        if group_id:
            params["group_id"] = group_id
        result = await _call_onebot_api("set_group_reaction", params)
        if result.get("status") == "ok":
            return True, "群消息表情回应已设置"
        return False, f"群消息表情回应失败: {result.get('msg', '未知错误')}"


class GetRecommendFaceTool(BaseTool):
    """获取推荐表情的 Tool。

    对应 API: ``get_recommend_face``。
    """

    tool_name = "get_recommend_face"
    tool_description = "获取推荐表情"

    async def execute(
        self,
        word: Annotated[str, "搜索关键词"],
    ) -> tuple[bool, str]:
        """执行获取推荐表情。"""
        params: dict[str, Any] = {
            "word": word,
        }
        result = await _call_onebot_api("get_recommend_face", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"获取推荐表情失败: {result.get('msg', '未知错误')}"



class UnsetMsgEmojiLikeTool(BaseTool):
    """取消消息表情回应的 Tool。

    对应 API: ``unset_msg_emoji_like``。
    """

    tool_name = "unset_msg_emoji_like"
    tool_description = "取消消息表情回应"

    async def execute(
        self,
        message_id: Annotated[int, "消息ID"],
        emoji_id: Annotated[int, "表情ID"],
    ) -> tuple[bool, str]:
        """执行取消消息表情回应。"""
        params: dict[str, Any] = {
            "message_id": message_id,
            "emoji_id": emoji_id,
        }
        result = await _call_onebot_api("unset_msg_emoji_like", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"取消消息表情回应失败: {result.get('msg', '未知错误')}"


