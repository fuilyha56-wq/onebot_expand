"""群文件管理服务。

封装群文件管理相关 API，提供统一的群文件操作接口。
所有方法在执行前会检查对应的配置开关，禁用时返回错误提示。

API 列表 (11):
    - get_group_file_url: 获取群文件下载链接 (go-cqhttp兼容)
    - get_group_root_files: 获取群根目录文件 (go-cqhttp兼容)
    - get_group_files_by_folder: 获取群子目录文件 (go-cqhttp兼容)
    - delete_group_file: 删除群文件 (go-cqhttp兼容)
    - create_group_file_folder: 创建群文件夹 (go-cqhttp兼容)
    - delete_group_folder: 删除群文件夹 (go-cqhttp兼容)
    - get_group_file_system_info: 获取群文件系统信息 (go-cqhttp兼容)
    - move_group_file: 移动群文件 (扩展)
    - rename_group_file: 重命名群文件 (扩展)
    - trans_group_file: 转存群文件 (扩展)
    - get_private_file_url: 获取私聊文件下载链接 (扩展)
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["GroupFileService"]


class GroupFileService(BaseService):
    """群文件管理服务。

    封装全部群文件管理 API 调用，提供配置开关检查和统一调用入口。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "group_file_service"
    service_description: str = "群文件管理服务"
    version: str = "1.0.0"

    def _is_api_enabled(self, api_name: str) -> bool:
        """检查 API 是否在配置中启用。

        1.3.0 起支持别名：传入别名时会先解析为主名再查询配置开关，
        保证主名与别名共用同一开关。

        Args:
            api_name: API 名称（主名或别名，对应配置中 ``enable_<api_name>`` 字段）。

        Returns:
            True 表示启用，False 表示禁用。无配置时默认启用。
        """
        from ..api_defs import resolve_action

        config = self.plugin.config
        if config is None:
            return True
        switches = getattr(config, "api_switches", None)
        if switches is None:
            return True
        primary = resolve_action(api_name) or api_name
        return getattr(switches, f"enable_{primary}", True)

    @staticmethod
    def _disabled_response(api_name: str) -> dict[str, Any]:
        """构造 API 禁用时的标准响应。

        Args:
            api_name: 被禁用的 API 名称。

        Returns:
            包含错误状态和提示信息的字典。
        """
        return {"status": "error", "retcode": -1, "msg": f"API {api_name} 已禁用"}

    async def get_group_file_url(
        self,
        group_id: int,
        file_id: str,
        busid: int,
    ) -> dict[str, Any]:
        """获取群文件下载链接。

        对应 go-cqhttp 兼容 API: ``get_group_file_url``。

        Args:
            group_id: 群号。
            file_id: 群文件 ID。
            busid: 文件类型 ID（busid）。

        Returns:
            适配器返回的响应字典，包含文件下载链接。
        """
        if not self._is_api_enabled("get_group_file_url"):
            return self._disabled_response("get_group_file_url")
        params: dict[str, Any] = {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid,
        }
        return await _call_onebot_api("get_group_file_url", params)

    async def get_group_root_files(
        self,
        group_id: int,
    ) -> dict[str, Any]:
        """获取群根目录文件。

        对应 go-cqhttp 兼容 API: ``get_group_root_files``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典，包含根目录文件和文件夹列表。
        """
        if not self._is_api_enabled("get_group_root_files"):
            return self._disabled_response("get_group_root_files")
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        return await _call_onebot_api("get_group_root_files", params)

    async def get_group_files_by_folder(
        self,
        group_id: int,
        folder_id: str,
    ) -> dict[str, Any]:
        """获取群子目录文件。

        对应 go-cqhttp 兼容 API: ``get_group_files_by_folder``。

        Args:
            group_id: 群号。
            folder_id: 文件夹 ID。

        Returns:
            适配器返回的响应字典，包含子目录文件列表。
        """
        if not self._is_api_enabled("get_group_files_by_folder"):
            return self._disabled_response("get_group_files_by_folder")
        params: dict[str, Any] = {
            "group_id": group_id,
            "folder_id": folder_id,
        }
        return await _call_onebot_api("get_group_files_by_folder", params)

    async def delete_group_file(
        self,
        group_id: int,
        file_id: str,
        busid: int,
    ) -> dict[str, Any]:
        """删除群文件。

        对应 go-cqhttp 兼容 API: ``delete_group_file``。

        Args:
            group_id: 群号。
            file_id: 群文件 ID。
            busid: 文件类型 ID（busid）。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("delete_group_file"):
            return self._disabled_response("delete_group_file")
        params: dict[str, Any] = {
            "group_id": group_id,
            "file_id": file_id,
            "busid": busid,
        }
        return await _call_onebot_api("delete_group_file", params)

    async def create_group_file_folder(
        self,
        group_id: int,
        name: str,
        parent_id: str = "",
    ) -> dict[str, Any]:
        """创建群文件夹。

        对应 go-cqhttp 兼容 API: ``create_group_file_folder``。

        Args:
            group_id: 群号。
            name: 文件夹名称。
            parent_id: 父文件夹 ID，空字符串表示根目录，默认为空。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("create_group_file_folder"):
            return self._disabled_response("create_group_file_folder")
        params: dict[str, Any] = {
            "group_id": group_id,
            "name": name,
        }
        if parent_id:
            params["parent_id"] = parent_id
        return await _call_onebot_api("create_group_file_folder", params)

    async def delete_group_folder(
        self,
        group_id: int,
        folder_id: str,
    ) -> dict[str, Any]:
        """删除群文件夹。

        对应 go-cqhttp 兼容 API: ``delete_group_folder``。

        Args:
            group_id: 群号。
            folder_id: 文件夹 ID。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("delete_group_folder"):
            return self._disabled_response("delete_group_folder")
        params: dict[str, Any] = {
            "group_id": group_id,
            "folder_id": folder_id,
        }
        return await _call_onebot_api("delete_group_folder", params)

    async def get_group_file_system_info(
        self,
        group_id: int,
    ) -> dict[str, Any]:
        """获取群文件系统信息。

        对应 go-cqhttp 兼容 API: ``get_group_file_system_info``。

        Args:
            group_id: 群号。

        Returns:
            适配器返回的响应字典，包含文件系统容量信息。
        """
        if not self._is_api_enabled("get_group_file_system_info"):
            return self._disabled_response("get_group_file_system_info")
        params: dict[str, Any] = {
            "group_id": group_id,
        }
        return await _call_onebot_api("get_group_file_system_info", params)

    async def move_group_file(
        self,
        group_id: int,
        file_id: str,
        current_parent_directory: str,
        target_directory: str,
    ) -> dict[str, Any]:
        """移动群文件。

        对应扩展 API: ``move_group_file``。

        Args:
            group_id: 群号。
            file_id: 群文件 ID。
            current_parent_directory: 当前所在目录 ID。
            target_directory: 目标目录 ID。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("move_group_file"):
            return self._disabled_response("move_group_file")
        params: dict[str, Any] = {
            "group_id": group_id,
            "file_id": file_id,
            "current_parent_directory": current_parent_directory,
            "target_directory": target_directory,
        }
        return await _call_onebot_api("move_group_file", params)

    async def rename_group_file(
        self,
        group_id: int,
        file_id: str,
        current_parent_directory: str,
        new_name: str,
    ) -> dict[str, Any]:
        """重命名群文件。

        对应扩展 API: ``rename_group_file``。

        Args:
            group_id: 群号。
            file_id: 群文件 ID。
            current_parent_directory: 当前所在目录 ID。
            new_name: 新文件名。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("rename_group_file"):
            return self._disabled_response("rename_group_file")
        params: dict[str, Any] = {
            "group_id": group_id,
            "file_id": file_id,
            "current_parent_directory": current_parent_directory,
            "new_name": new_name,
        }
        return await _call_onebot_api("rename_group_file", params)

    async def trans_group_file(
        self,
        group_id: int,
        file_id: str,
    ) -> dict[str, Any]:
        """转存群文件。

        对应扩展 API: ``trans_group_file``。

        Args:
            group_id: 群号。
            file_id: 群文件 ID。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("trans_group_file"):
            return self._disabled_response("trans_group_file")
        params: dict[str, Any] = {
            "group_id": group_id,
            "file_id": file_id,
        }
        return await _call_onebot_api("trans_group_file", params)

    async def get_private_file_url(
        self,
        user_id: int,
        file_id: str,
        file_hash: str,
    ) -> dict[str, Any]:
        """获取私聊文件下载链接。

        对应扩展 API: ``get_private_file_url``。

        Args:
            user_id: 目标用户 QQ 号。
            file_id: 文件 ID。
            file_hash: 文件哈希。

        Returns:
            适配器返回的响应字典，包含私聊文件下载链接。
        """
        if not self._is_api_enabled("get_private_file_url"):
            return self._disabled_response("get_private_file_url")
        params: dict[str, Any] = {
            "user_id": user_id,
            "file_id": file_id,
            "file_hash": file_hash,
        }
        return await _call_onebot_api("get_private_file_url", params)