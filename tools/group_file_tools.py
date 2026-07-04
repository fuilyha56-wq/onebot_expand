"""群文件管理 API 的 Tool 组件。

包含 12 个群文件管理 Tool，对应 go-cqhttp 兼容 API 和扩展 API：
    - get_group_file_url: 获取群文件下载链接 (go-cqhttp兼容)
    - get_group_root_files: 获取群根目录文件 (go-cqhttp兼容)
    - get_group_files_by_folder: 获取群子目录文件 (go-cqhttp兼容)
    - delete_group_file: 删除群文件 (go-cqhttp兼容)
    - create_group_file_folder: 创建群文件夹 (go-cqhttp兼容)
    - delete_group_folder: 删除群文件夹 (go-cqhttp兼容)
    - get_group_file_system_info: 获取群文件系统信息 (go-cqhttp兼容)
    - move_group_file: 移动群文件 (扩展)
    - rename_group_file: 重命名群文件 (扩展)
    - rename_group_file_folder: 重命名群文件夹 (SnowLuma 扩展)
    - trans_group_file: 转存群文件 (扩展)
    - get_private_file_url: 获取私聊文件下载链接 (扩展)

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
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
]


class GetGroupFileUrlTool(BaseTool):
    """获取群文件下载链接的 Tool。

    对应 go-cqhttp 兼容 API: ``get_group_file_url``。
    根据群号、文件 ID 和 busid 获取群文件的下载链接。
    """

    tool_name = "get_group_file_url"
    tool_description = "获取群文件下载链接"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        file_id: Annotated[str, "群文件ID"],
        busid: Annotated[int, "文件类型ID（busid）"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群文件下载链接。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid,
        }
        result = await _call_onebot_api("get_group_file_url", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群文件下载链接失败: {result.get('msg', '未知错误')}"


class GetGroupRootFilesTool(BaseTool):
    """获取群根目录文件的 Tool。

    对应 go-cqhttp 兼容 API: ``get_group_root_files``。
    获取指定群根目录下的文件和文件夹列表。
    """

    tool_name = "get_group_root_files"
    tool_description = "获取群根目录文件列表"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群根目录文件。"""
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        result = await _call_onebot_api("get_group_root_files", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群根目录文件失败: {result.get('msg', '未知错误')}"


class GetGroupFilesByFolderTool(BaseTool):
    """获取群子目录文件的 Tool。

    对应 go-cqhttp 兼容 API: ``get_group_files_by_folder``。
    根据文件夹 ID 获取群子目录下的文件列表。
    """

    tool_name = "get_group_files_by_folder"
    tool_description = "获取群子目录文件列表"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        folder_id: Annotated[str, "群文件夹ID"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群子目录文件。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "folder_id": folder_id,
        }
        result = await _call_onebot_api("get_group_files_by_folder", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群子目录文件失败: {result.get('msg', '未知错误')}"


class DeleteGroupFileTool(BaseTool):
    """删除群文件的 Tool。

    对应 go-cqhttp 兼容 API: ``delete_group_file``。
    删除指定群中的群文件。
    """

    tool_name = "delete_group_file"
    tool_description = "删除群文件"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        file_id: Annotated[str, "群文件ID"],
        busid: Annotated[int, "文件类型ID（busid）"],
    ) -> tuple[bool, str]:
        """执行删除群文件。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid,
        }
        result = await _call_onebot_api("delete_group_file", params)
        if result.get("status") == "ok":
            return True, f"已删除群 {group_id} 中的文件 {file_id}"
        return False, f"删除群文件失败: {result.get('msg', '未知错误')}"


class CreateGroupFileFolderTool(BaseTool):
    """创建群文件夹的 Tool。

    对应 go-cqhttp 兼容 API: ``create_group_file_folder``。
    在指定群中创建文件夹，可指定父文件夹。
    """

    tool_name = "create_group_file_folder"
    tool_description = "创建群文件夹"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        name: Annotated[str, "文件夹名称"],
        parent_id: Annotated[str, "父文件夹ID（可选，空字符串表示根目录）"] = "",
    ) -> tuple[bool, str]:
        """执行创建群文件夹。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "name": name,
        }
        if parent_id:
            params["parent_id"] = parent_id
        result = await _call_onebot_api("create_group_file_folder", params)
        if result.get("status") == "ok":
            return True, f"已在群 {group_id} 中创建文件夹 \"{name}\""
        return False, f"创建群文件夹失败: {result.get('msg', '未知错误')}"


class DeleteGroupFolderTool(BaseTool):
    """删除群文件夹的 Tool。

    对应 go-cqhttp 兼容 API: ``delete_group_folder``。
    删除指定群中的群文件夹。
    """

    tool_name = "delete_group_folder"
    tool_description = "删除群文件夹"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        folder_id: Annotated[str, "群文件夹ID"],
    ) -> tuple[bool, str]:
        """执行删除群文件夹。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "folder_id": folder_id,
        }
        result = await _call_onebot_api("delete_group_folder", params)
        if result.get("status") == "ok":
            return True, f"已删除群 {group_id} 中的文件夹 {folder_id}"
        return False, f"删除群文件夹失败: {result.get('msg', '未知错误')}"


class GetGroupFileSystemInfoTool(BaseTool):
    """获取群文件系统信息的 Tool。

    对应 go-cqhttp 兼容 API: ``get_group_file_system_info``。
    获取指定群的文件系统信息（总容量、已用容量等）。
    """

    tool_name = "get_group_file_system_info"
    tool_description = "获取群文件系统信息"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取群文件系统信息。"""
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        result = await _call_onebot_api("get_group_file_system_info", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取群文件系统信息失败: {result.get('msg', '未知错误')}"


class MoveGroupFileTool(BaseTool):
    """移动群文件的 Tool（扩展）。

    对应扩展 API: ``move_group_file``。
    将群文件从当前目录移动到目标目录。
    """

    tool_name = "move_group_file"
    tool_description = "移动群文件到目标目录"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        file_id: Annotated[str, "群文件ID"],
        current_parent_directory: Annotated[str, "当前所在目录ID"],
        target_directory: Annotated[str, "目标目录ID"],
    ) -> tuple[bool, str]:
        """执行移动群文件。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "file_id": file_id,
            "current_parent_directory": current_parent_directory,
            "target_directory": target_directory,
        }
        result = await _call_onebot_api("move_group_file", params)
        if result.get("status") == "ok":
            return True, f"已移动群 {group_id} 中的文件 {file_id}"
        return False, f"移动群文件失败: {result.get('msg', '未知错误')}"


class RenameGroupFileTool(BaseTool):
    """重命名群文件的 Tool（扩展）。

    对应扩展 API: ``rename_group_file``。
    重命名指定群文件的文件名。
    """

    tool_name = "rename_group_file"
    tool_description = "重命名群文件"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        file_id: Annotated[str, "群文件ID"],
        current_parent_directory: Annotated[str, "当前所在目录ID"],
        new_name: Annotated[str, "新文件名"],
    ) -> tuple[bool, str]:
        """执行重命名群文件。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "file_id": file_id,
            "current_parent_directory": current_parent_directory,
            "new_name": new_name,
        }
        result = await _call_onebot_api("rename_group_file", params)
        if result.get("status") == "ok":
            return True, f"已重命名群 {group_id} 中的文件为 \"{new_name}\""
        return False, f"重命名群文件失败: {result.get('msg', '未知错误')}"


class RenameGroupFileFolderTool(BaseTool):
    """重命名群文件夹的 Tool（SnowLuma 扩展）。

    对应 SnowLuma API: ``rename_group_file_folder``。
    重命名指定群文件夹的名称。
    """

    tool_name = "rename_group_file_folder"
    tool_description = "重命名群文件夹（SnowLuma扩展）"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        folder_id: Annotated[str, "群文件夹ID"],
        new_folder_name: Annotated[str, "新文件夹名"],
    ) -> tuple[bool, str]:
        """执行重命名群文件夹。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "folder_id": folder_id,
            "new_folder_name": new_folder_name,
        }
        result = await _call_onebot_api("rename_group_file_folder", params)
        if result.get("status") == "ok":
            return True, f"已重命名群 {group_id} 中的文件夹为 \"{new_folder_name}\""
        return False, f"重命名群文件夹失败: {result.get('msg', '未知错误')}"


class TransGroupFileTool(BaseTool):
    """转存群文件的 Tool（扩展）。

    对应扩展 API: ``trans_group_file``。
    将群文件转存到自己的文件存储中。
    """

    tool_name = "trans_group_file"
    tool_description = "转存群文件"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        file_id: Annotated[str, "群文件ID"],
    ) -> tuple[bool, str]:
        """执行转存群文件。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "file_id": file_id,
        }
        result = await _call_onebot_api("trans_group_file", params)
        if result.get("status") == "ok":
            return True, f"已转存群 {group_id} 中的文件 {file_id}"
        return False, f"转存群文件失败: {result.get('msg', '未知错误')}"


class GetPrivateFileUrlTool(BaseTool):
    """获取私聊文件下载链接的 Tool（扩展）。

    对应扩展 API: ``get_private_file_url``。
    根据用户 ID、文件 ID 和文件哈希获取私聊文件的下载链接。
    """

    tool_name = "get_private_file_url"
    tool_description = "获取私聊文件下载链接"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        file_id: Annotated[str, "文件ID"],
        file_hash: Annotated[str, "文件哈希"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取私聊文件下载链接。"""
        params: dict[str, Any] = {
            "user_id": user_id,
            "file_id": file_id,
            "file_hash": file_hash,
        }
        result = await _call_onebot_api("get_private_file_url", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取私聊文件下载链接失败: {result.get('msg', '未知错误')}"