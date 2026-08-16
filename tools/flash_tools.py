"""闪传 API 的 Tool 组件。

包含 11 个闪传 Tool，对应 NapCat/SnowLuma 闪传 API：
    - create_flash_task: 创建闪传任务
    - send_flash_msg: 发送闪传消息
    - get_flash_file_list: 获取闪传文件列表
    - get_flash_file_url: 获取闪传文件URL
    - get_share_link: 获取文件分享链接
    - download_fileset: 下载文件集
    - get_fileset_info: 获取文件集信息
    - get_fileset_id: 从分享码获取fileset_id
    - list_filesets: 列出所有闪传文件集（SnowLuma 扩展）
    - delete_flash_file: 删除闪传文件（SnowLuma 扩展）
    - rename_flash_file: 重命名闪传文件（SnowLuma 扩展）

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "CreateFlashTaskTool",
    "SendFlashMsgTool",
    "GetFlashFileListTool",
    "GetFlashFileUrlTool",
    "GetShareLinkTool",
    "DownloadFilesetTool",
    "GetFilesetInfoTool",
    "GetFilesetIdTool",
    "ListFilesetsTool",
    "DeleteFlashFileTool",
    "RenameFlashFileTool",
"GetFlashFileDownloadUrlsTool",
    "UploadFlashFileTool",
    "ReshareFlashFileTool",
]


class CreateFlashTaskTool(BaseTool):
    """创建闪传任务的 Tool。

    对应 NapCat API: ``create_flash_task``。
    创建一个闪传文件传输任务。
    """

    name = "create_flash_task"
    description = "创建一个闪传文件传输任务"

    async def execute(
        self,
        files: Annotated[list[dict[str, Any]], "文件列表（每项含path和name）"],
        name: Annotated[str, "任务名称（可选）"] = "",
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行创建闪传任务。"""
        params: dict[str, Any] = {"files": files}
        if name:
            params["name"] = name
        result = await _call_onebot_api("create_flash_task", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"创建闪传任务失败: {result.get('msg', '未知错误')}"


class SendFlashMsgTool(BaseTool):
    """发送闪传消息的 Tool。

    对应 NapCat API: ``send_flash_msg``。
    发送闪传文件消息到指定用户或群。
    """

    name = "send_flash_msg"
    description = "发送闪传文件消息到指定用户或群"

    async def execute(
        self,
        fileset_id: Annotated[str, "文件集ID"],
        user_id: Annotated[int, "目标用户QQ号（可选）"] = 0,
        group_id: Annotated[int, "目标群号（可选）"] = 0,
    ) -> tuple[bool, str]:
        """执行发送闪传消息。"""
        params: dict[str, Any] = {"fileset_id": fileset_id}
        if user_id:
            params["user_id"] = user_id
        if group_id:
            params["group_id"] = group_id
        result = await _call_onebot_api("send_flash_msg", params)
        if result.get("status") == "ok":
            return True, "闪传消息已发送"
        return False, f"发送闪传消息失败: {result.get('msg', '未知错误')}"


class GetFlashFileListTool(BaseTool):
    """获取闪传文件列表的 Tool。

    对应 NapCat API: ``get_flash_file_list``。
    获取指定文件集的文件列表。
    """

    name = "get_flash_file_list"
    description = "获取指定文件集的文件列表"

    async def execute(
        self,
        fileset_id: Annotated[str, "文件集ID"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取闪传文件列表。"""
        params: dict[str, Any] = {"fileset_id": fileset_id}
        result = await _call_onebot_api("get_flash_file_list", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取闪传文件列表失败: {result.get('msg', '未知错误')}"


class GetFlashFileUrlTool(BaseTool):
    """获取闪传文件URL的 Tool。

    对应 NapCat API: ``get_flash_file_url``。
    获取指定文件集中文件的下载 URL。
    """

    name = "get_flash_file_url"
    description = "获取指定文件集中文件的下载URL"

    async def execute(
        self,
        fileset_id: Annotated[str, "文件集ID"],
        file_name: Annotated[str, "文件名（可选）"] = "",
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取闪传文件URL。"""
        params: dict[str, Any] = {"fileset_id": fileset_id}
        if file_name:
            params["file_name"] = file_name
        result = await _call_onebot_api("get_flash_file_url", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取闪传文件URL失败: {result.get('msg', '未知错误')}"


class GetShareLinkTool(BaseTool):
    """获取文件分享链接的 Tool。

    对应 NapCat API: ``get_share_link``。
    获取指定文件集的分享链接。
    """

    name = "get_share_link"
    description = "获取指定文件集的分享链接"

    async def execute(
        self,
        fileset_id: Annotated[str, "文件集ID"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取文件分享链接。"""
        params: dict[str, Any] = {"fileset_id": fileset_id}
        result = await _call_onebot_api("get_share_link", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取分享链接失败: {result.get('msg', '未知错误')}"


class DownloadFilesetTool(BaseTool):
    """下载文件集的 Tool。

    对应 NapCat API: ``download_fileset``。
    下载指定文件集的全部文件。
    """

    name = "download_fileset"
    description = "下载指定文件集的全部文件"

    async def execute(
        self,
        fileset_id: Annotated[str, "文件集ID"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行下载文件集。"""
        params: dict[str, Any] = {"fileset_id": fileset_id}
        result = await _call_onebot_api("download_fileset", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"下载文件集失败: {result.get('msg', '未知错误')}"


class GetFilesetInfoTool(BaseTool):
    """获取文件集信息的 Tool。

    对应 NapCat API: ``get_fileset_info``。
    获取指定文件集的详细信息。
    """

    name = "get_fileset_info"
    description = "获取指定文件集的详细信息"

    async def execute(
        self,
        fileset_id: Annotated[str, "文件集ID"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取文件集信息。"""
        params: dict[str, Any] = {"fileset_id": fileset_id}
        result = await _call_onebot_api("get_fileset_info", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取文件集信息失败: {result.get('msg', '未知错误')}"


class GetFilesetIdTool(BaseTool):
    """从分享码获取fileset_id的 Tool。

    对应 NapCat API: ``get_fileset_id``。
    根据分享码解析出文件集 ID。
    """

    name = "get_fileset_id"
    description = "根据分享码解析出文件集ID"

    async def execute(
        self,
        share_code: Annotated[str, "分享码"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行从分享码获取fileset_id。"""
        params: dict[str, Any] = {"share_code": share_code}
        result = await _call_onebot_api("get_fileset_id", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取fileset_id失败: {result.get('msg', '未知错误')}"


class ListFilesetsTool(BaseTool):
    """列出所有闪传文件集的 Tool（SnowLuma 扩展）。

    对应 SnowLuma API: ``list_filesets``。
    列出当前账号的所有闪传文件集。
    """

    name = "list_filesets"
    description = "列出当前账号所有闪传文件集（SnowLuma扩展）"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行列出所有闪传文件集。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("list_filesets", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"列出闪传文件集失败: {result.get('msg', '未知错误')}"


class DeleteFlashFileTool(BaseTool):
    """删除闪传文件的 Tool（SnowLuma 扩展）。

    对应 SnowLuma API: ``delete_flash_file``。
    根据文件集 ID 删除闪传文件。
    """

    name = "delete_flash_file"
    description = "根据文件集ID删除闪传文件（SnowLuma扩展）"

    async def execute(
        self,
        fileset_id: Annotated[str, "文件集ID"],
    ) -> tuple[bool, str]:
        """执行删除闪传文件。"""
        params: dict[str, Any] = {"fileset_id": fileset_id}
        result = await _call_onebot_api("delete_flash_file", params)
        if result.get("status") == "ok":
            return True, f"已删除闪传文件 {fileset_id}"
        return False, f"删除闪传文件失败: {result.get('msg', '未知错误')}"


class RenameFlashFileTool(BaseTool):
    """重命名闪传文件的 Tool（SnowLuma 扩展）。

    对应 SnowLuma API: ``rename_flash_file``。
    根据文件集 ID 重命名闪传文件。
    """

    name = "rename_flash_file"
    description = "根据文件集ID重命名闪传文件（SnowLuma扩展）"

    async def execute(
        self,
        fileset_id: Annotated[str, "文件集ID"],
        new_name: Annotated[str, "新文件名"],
    ) -> tuple[bool, str]:
        """执行重命名闪传文件。"""
        params: dict[str, Any] = {
            "fileset_id": fileset_id,
            "new_name": new_name,
        }
        result = await _call_onebot_api("rename_flash_file", params)
        if result.get("status") == "ok":
            return True, f"已重命名闪传文件 {fileset_id}"
        return False, f"重命名闪传文件失败: {result.get('msg', '未知错误')}"


class GetFlashFileDownloadUrlsTool(BaseTool):
    """获取闪传文件集下载URL的 Tool。

    对应 API: ``get_flash_file_download_urls``。
    """

    name = "get_flash_file_download_urls"
    description = "获取闪传文件集下载URL"

    async def execute(
        self,
        fileset_id: Annotated[str, "文件集ID"],
        share_link: Annotated[str, "分享链接"],
    ) -> tuple[bool, str]:
        """执行获取闪传文件集下载URL。"""
        params: dict[str, Any] = {
            "fileset_id": fileset_id,
            "share_link": share_link,
        }
        result = await _call_onebot_api("get_flash_file_download_urls", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"获取闪传文件集下载URL失败: {result.get('msg', '未知错误')}"



class UploadFlashFileTool(BaseTool):
    """上传闪传文件的 Tool。

    对应 API: ``upload_flash_file``。
    """

    name = "upload_flash_file"
    description = "上传闪传文件"

    async def execute(
        self,
        title: Annotated[str, "文件集标题"],
        paths: Annotated[list[str], "本地文件路径列表"],
    ) -> tuple[bool, str]:
        """执行上传闪传文件。"""
        params: dict[str, Any] = {
            "title": title,
            "paths": paths,
        }
        result = await _call_onebot_api("upload_flash_file", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"上传闪传文件失败: {result.get('msg', '未知错误')}"



class ReshareFlashFileTool(BaseTool):
    """重新分享闪传文件的 Tool。

    对应 API: ``reshare_flash_file``。
    """

    name = "reshare_flash_file"
    description = "重新分享闪传文件"

    async def execute(
        self,
        fileset_id: Annotated[str, "文件集ID"],
        share_link: Annotated[str, "分享链接"],
    ) -> tuple[bool, str]:
        """执行重新分享闪传文件。"""
        params: dict[str, Any] = {
            "fileset_id": fileset_id,
            "share_link": share_link,
        }
        result = await _call_onebot_api("reshare_flash_file", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"重新分享闪传文件失败: {result.get('msg', '未知错误')}"


