"""闪传服务。

封装 NapCat 闪传 API，提供闪传任务创建、消息发送、
文件列表查询、文件下载、分享链接等功能。

API 列表 (11):
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
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["FlashService"]


class FlashService(BaseService):
    """闪传服务。

    封装全部闪传 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    name: str = "flash_service"
    description: str = "闪传服务"
    version: str = "1.0.0"

    async def create_flash_task(
        self,
        files: list[dict[str, Any]],
        name: str = "",
    ) -> dict[str, Any]:
        """创建闪传任务。

        对应 NapCat 扩展 API: ``create_flash_task``。

        Args:
            files: 文件列表（每项含 path 和 name）。
            name: 任务名称，默认为空字符串。

        Returns:
            适配器返回的响应字典，包含任务信息。
        """
        params: dict[str, Any] = {"files": files}
        if name:
            params["name"] = name
        return await _call_onebot_api("create_flash_task", params)

    async def send_flash_msg(
        self,
        fileset_id: str,
        user_id: int | None = None,
        group_id: int | None = None,
    ) -> dict[str, Any]:
        """发送闪传消息。

        对应 NapCat 扩展 API: ``send_flash_msg``。

        Args:
            fileset_id: 文件集 ID。
            user_id: 目标用户 QQ 号，默认为 None。
            group_id: 目标群号，默认为 None。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"fileset_id": fileset_id}
        if user_id is not None:
            params["user_id"] = user_id
        if group_id is not None:
            params["group_id"] = group_id
        return await _call_onebot_api("send_flash_msg", params)

    async def get_flash_file_list(self, fileset_id: str) -> dict[str, Any]:
        """获取闪传文件列表。

        对应 NapCat 扩展 API: ``get_flash_file_list``。

        Args:
            fileset_id: 文件集 ID。

        Returns:
            适配器返回的响应字典，包含文件列表。
        """
        params: dict[str, Any] = {"fileset_id": fileset_id}
        return await _call_onebot_api("get_flash_file_list", params)

    async def get_flash_file_url(
        self,
        fileset_id: str,
        file_name: str = "",
    ) -> dict[str, Any]:
        """获取闪传文件URL。

        对应 NapCat 扩展 API: ``get_flash_file_url``。

        Args:
            fileset_id: 文件集 ID。
            file_name: 文件名，默认为空字符串。

        Returns:
            适配器返回的响应字典，包含文件下载 URL。
        """
        params: dict[str, Any] = {"fileset_id": fileset_id}
        if file_name:
            params["file_name"] = file_name
        return await _call_onebot_api("get_flash_file_url", params)

    async def get_share_link(self, fileset_id: str) -> dict[str, Any]:
        """获取文件分享链接。

        对应 NapCat 扩展 API: ``get_share_link``。

        Args:
            fileset_id: 文件集 ID。

        Returns:
            适配器返回的响应字典，包含分享链接。
        """
        params: dict[str, Any] = {"fileset_id": fileset_id}
        return await _call_onebot_api("get_share_link", params)

    async def download_fileset(self, fileset_id: str) -> dict[str, Any]:
        """下载文件集。

        对应 NapCat 扩展 API: ``download_fileset``。

        Args:
            fileset_id: 文件集 ID。

        Returns:
            适配器返回的响应字典，包含下载结果。
        """
        params: dict[str, Any] = {"fileset_id": fileset_id}
        return await _call_onebot_api("download_fileset", params)

    async def get_fileset_info(self, fileset_id: str) -> dict[str, Any]:
        """获取文件集信息。

        对应 NapCat 扩展 API: ``get_fileset_info``。

        Args:
            fileset_id: 文件集 ID。

        Returns:
            适配器返回的响应字典，包含文件集详细信息。
        """
        params: dict[str, Any] = {"fileset_id": fileset_id}
        return await _call_onebot_api("get_fileset_info", params)

    async def get_fileset_id(self, share_code: str) -> dict[str, Any]:
        """从分享码获取fileset_id。

        对应 NapCat 扩展 API: ``get_fileset_id``。

        Args:
            share_code: 分享码。

        Returns:
            适配器返回的响应字典，包含文件集 ID。
        """
        params: dict[str, Any] = {"share_code": share_code}
        return await _call_onebot_api("get_fileset_id", params)

    async def list_filesets(self) -> dict[str, Any]:
        """列出所有闪传文件集（SnowLuma 扩展）。

        对应 SnowLuma 扩展 API: ``list_filesets``。

        Returns:
            适配器返回的响应字典，包含当前账号所有闪传文件集列表。
        """
        return await _call_onebot_api("list_filesets", {})

    async def delete_flash_file(self, fileset_id: str) -> dict[str, Any]:
        """删除闪传文件（SnowLuma 扩展）。

        对应 SnowLuma 扩展 API: ``delete_flash_file``。

        Args:
            fileset_id: 文件集 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"fileset_id": fileset_id}
        return await _call_onebot_api("delete_flash_file", params)

    async def rename_flash_file(
        self,
        fileset_id: str,
        new_name: str,
    ) -> dict[str, Any]:
        """重命名闪传文件（SnowLuma 扩展）。

        对应 SnowLuma 扩展 API: ``rename_flash_file``。

        Args:
            fileset_id: 文件集 ID。
            new_name: 新文件名。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "fileset_id": fileset_id,
            "new_name": new_name,
        }
        return await _call_onebot_api("rename_flash_file", params)

    async def GetFlashFileDownloadUrls(
        self,
        fileset_id: str,
        share_link: str,
    ) -> dict[str, Any]:
        """获取闪传文件集下载URL。

        对应 OneBot API: ``get_flash_file_download_urls``。
        """
        params: dict[str, Any] = {
            "fileset_id": fileset_id,
            "share_link": share_link,
        }
        return await _call_onebot_api("get_flash_file_download_urls", params)

    async def UploadFlashFile(
        self,
        title: str,
        paths: list[str],
    ) -> dict[str, Any]:
        """上传闪传文件。

        对应 OneBot API: ``upload_flash_file``。
        """
        params: dict[str, Any] = {
            "title": title,
            "paths": paths,
        }
        return await _call_onebot_api("upload_flash_file", params)

    async def ReshareFlashFile(
        self,
        fileset_id: str,
        share_link: str,
    ) -> dict[str, Any]:
        """重新分享闪传文件。

        对应 OneBot API: ``reshare_flash_file``。
        """
        params: dict[str, Any] = {
            "fileset_id": fileset_id,
            "share_link": share_link,
        }
        return await _call_onebot_api("reshare_flash_file", params)

