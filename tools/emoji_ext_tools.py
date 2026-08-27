"""表情/收藏扩展 API 的 Tool 组件。

包含 16 个表情/收藏扩展 Tool，对应 NapCat/SnowLuma 表情/收藏扩展 API：
    - fetch_custom_face: 获取收藏表情
    - fetch_custom_face_detail: 获取收藏表情详情列表（NapCat / SnowLuma 扩展）
    - add_custom_face: 添加收藏表情
    - delete_custom_face: 删除收藏表情
    - set_custom_face_desc: 修改收藏表情描述（NapCat 扩展）
    - modify_custom_face: 修改收藏表情备注（SnowLuma 扩展）
    - move_custom_face_to_front: 收藏表情移到最前（SnowLuma 扩展）
    - fetch_emoji_like: 获取表情回应分页
    - get_emoji_likes: 获取表情回应用户
    - set_group_reaction: 群聊消息表情回应（SnowLuma 扩展）
    - get_recommend_face: 获取推荐表情（LLOneBot 扩展）
    - unset_msg_emoji_like: 取消消息表情回应（LLOneBot 扩展）
    - fetch_sys_faces: 获取系统表情列表（SnowLuma 扩展）
    - fetch_face_entity: 获取系统表情实体（SnowLuma 扩展）
    - search_sys_faces: 搜索系统表情（SnowLuma 扩展）
    - fetch_super_face_id: 判断系统表情是否为超级表情（SnowLuma 扩展）

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from ..message_utils import MessageId
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
    "FetchSysFacesTool",
    "FetchFaceEntityTool",
    "SearchSysFacesTool",
    "FetchSuperFaceIdTool",
]


class FetchCustomFaceTool(BaseTool):
    """获取收藏表情的 Tool。

    对应 NapCat API: ``fetch_custom_face``。
    获取当前 Bot 的收藏表情列表。
    """

    name = "fetch_custom_face"
    description = "获取当前Bot的收藏表情列表"

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


class FetchSysFacesTool(BaseTool):
    """获取系统表情列表的 Tool（SnowLuma 扩展）。"""

    name = "fetch_sys_faces"
    description = "获取系统表情列表（SnowLuma扩展）"

    async def execute(
        self,
        refresh: Annotated[bool, "是否刷新缓存"] = False,
    ) -> tuple[bool, str | dict[str, Any]]:
        result = await _call_onebot_api("fetch_sys_faces", {"refresh": refresh})
        if result.get("status") == "ok":
            return True, result.get("data", {})
        return False, f"获取系统表情列表失败: {result.get('msg', '未知错误')}"


class FetchFaceEntityTool(BaseTool):
    """获取系统表情实体的 Tool（SnowLuma 扩展）。"""

    name = "fetch_face_entity"
    description = "获取指定系统表情实体（SnowLuma扩展）"

    async def execute(
        self,
        face_id: Annotated[int, "系统表情ID"],
        refresh: Annotated[bool, "是否刷新缓存"] = False,
    ) -> tuple[bool, str | dict[str, Any]]:
        result = await _call_onebot_api(
            "fetch_face_entity", {"face_id": face_id, "refresh": refresh}
        )
        if result.get("status") == "ok":
            return True, result.get("data", {})
        return False, f"获取系统表情实体失败: {result.get('msg', '未知错误')}"


class SearchSysFacesTool(BaseTool):
    """搜索系统表情的 Tool（SnowLuma 扩展）。"""

    name = "search_sys_faces"
    description = "按关键词搜索系统表情（SnowLuma扩展）"

    async def execute(
        self,
        query: Annotated[str, "搜索关键词"],
    ) -> tuple[bool, str | dict[str, Any]]:
        result = await _call_onebot_api("search_sys_faces", {"query": query})
        if result.get("status") == "ok":
            return True, result.get("data", {})
        return False, f"搜索系统表情失败: {result.get('msg', '未知错误')}"


class FetchSuperFaceIdTool(BaseTool):
    """判断系统表情是否为超级表情的 Tool（SnowLuma 扩展）。"""

    name = "fetch_super_face_id"
    description = "判断系统表情是否使用超级表情格式（SnowLuma扩展）"

    async def execute(
        self,
        face_id: Annotated[int, "系统表情ID"],
        refresh: Annotated[bool, "是否刷新缓存"] = False,
    ) -> tuple[bool, str | dict[str, Any]]:
        result = await _call_onebot_api(
            "fetch_super_face_id", {"face_id": face_id, "refresh": refresh}
        )
        if result.get("status") == "ok":
            return True, result.get("data", {})
        return False, f"判断超级表情格式失败: {result.get('msg', '未知错误')}"


class FetchCustomFaceDetailTool(BaseTool):
    """获取收藏表情详情列表的 Tool（NapCat / SnowLuma 扩展）。

    对应 NapCat / SnowLuma API: ``fetch_custom_face_detail``。
    返回收藏表情的完整信息（resId/md5/emojiId 等），删除/改描述前置。
    """

    name = "fetch_custom_face_detail"
    description = "获取收藏表情详情列表（NapCat/SnowLuma扩展）"

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

    name = "add_custom_face"
    description = "添加表情到收藏列表"

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

    name = "delete_custom_face"
    description = "从收藏列表中删除指定表情"

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

    name = "set_custom_face_desc"
    description = "修改收藏表情描述（NapCat扩展）"

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

    name = "modify_custom_face"
    description = "修改收藏表情备注（SnowLuma扩展）"

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

    name = "move_custom_face_to_front"
    description = "将指定收藏表情移到列表最前（SnowLuma扩展）"

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

    name = "fetch_emoji_like"
    description = "获取指定消息的表情回应分页数据"

    async def execute(
        self,
        message_id: Annotated[MessageId, "目标消息ID"],
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

    name = "get_emoji_likes"
    description = "获取指定消息上某表情的回应用户列表"

    async def execute(
        self,
        message_id: Annotated[MessageId, "目标消息ID"],
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

    name = "set_group_reaction"
    description = "对群消息进行表情回应（SnowLuma扩展）"

    async def execute(
        self,
        message_id: Annotated[MessageId, "目标消息ID"],
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

    name = "get_recommend_face"
    description = "获取推荐表情"

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



class GetMsgEmojiLikesTool(BaseTool):
    """获取一条消息全部表情回应的 Tool（SnowLuma 扩展）。

    对应 SnowLuma API: ``get_msg_emoji_likes``。
    返回该消息上每个表情回应的编号、数量与用户列表。
    """

    name = "get_msg_emoji_likes"
    description = "获取一条消息的全部表情回应（SnowLuma扩展）"

    async def execute(
        self,
        message_id: Annotated[MessageId, "目标消息ID"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取消息全部表情回应。"""
        params: dict[str, Any] = {
            "message_id": message_id,
        }
        result = await _call_onebot_api("get_msg_emoji_likes", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取消息全部表情回应失败: {result.get('msg', '未知错误')}"


class UnsetMsgEmojiLikeTool(BaseTool):
    """取消消息表情回应的 Tool。

    对应 API: ``unset_msg_emoji_like``。
    """

    name = "unset_msg_emoji_like"
    description = "取消消息表情回应"

    async def execute(
        self,
        message_id: Annotated[MessageId, "消息ID"],
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
