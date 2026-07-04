"""文件上传与管理服务。

封装 OneBot v11 文件操作 API 和 NapCat 文件扩展 API，提供统一的文件操作接口。
文件上传方法通过 PathMapper 解析路径，支持路径映射、base64 编码和共享卷三种传输模式。

API 列表 (11):
    - upload_group_file: 上传群文件
    - upload_private_file: 上传私聊文件
    - get_file: 获取文件信息（NapCat 扩展）
    - get_image: 获取图片信息
    - get_record: 获取语音文件信息
    - send_online_file: 发送在线文件（NapCat 扩展）
    - send_online_folder: 发送在线文件夹（NapCat 扩展）
    - get_online_file_msg: 获取在线文件消息列表（NapCat 扩展）
    - receive_online_file: 接收在线文件（NapCat 扩展）
    - refuse_online_file: 拒绝在线文件（NapCat 扩展）
    - cancel_online_file: 取消已发送的在线文件（NapCat 扩展）
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..path_mapper import PathMapper
from ..tools import _call_onebot_api

__all__ = ["FileService"]


class _PathMappingSubConfig:
    """路径映射配置子节适配器。

    PathMapper 通过 ``getattr(config, "enabled")`` 和
    ``getattr(config, "rules")`` 读取配置，因此需要提供属性而非字典。
    """

    def __init__(self, ft: Any) -> None:
        self.enabled: bool = getattr(ft, "enable_path_mapping", False)
        self.rules: list[str] = getattr(ft, "path_mappings", [])


class _Base64SubConfig:
    """base64 传输配置子节适配器。"""

    def __init__(self, ft: Any) -> None:
        self.enabled: bool = getattr(ft, "enable_base64_transfer", True)
        self.max_file_size_mb: int = getattr(ft, "max_base64_size_mb", 30)


class _SharedVolumeSubConfig:
    """共享卷配置子节适配器。"""

    def __init__(self, ft: Any) -> None:
        self.enabled: bool = getattr(ft, "enable_shared_volume", False)


class _FileTransferConfigAdapter:
    """文件传输配置适配器。

    OnebotExpandConfig 的 file_transfer 节使用 ``enable_*`` 命名风格，
    而 PathMapper 期望 ``path_mapping``/``base64_transfer``/``shared_volume``
    三个子配置节（通过属性访问）。本适配器在两者之间转换，
    返回具有 ``enabled``/``rules`` 等属性的对象，使 PathMapper 能正确读取配置。
    """

    def __init__(self, file_transfer_section: Any) -> None:
        """初始化适配器。

        Args:
            file_transfer_section: OnebotExpandConfig.file_transfer 配置节实例。
                为 None 时使用默认值。
        """
        ft = file_transfer_section
        self.path_mapping: _PathMappingSubConfig = _PathMappingSubConfig(ft)
        self.base64_transfer: _Base64SubConfig = _Base64SubConfig(ft)
        self.shared_volume: _SharedVolumeSubConfig = _SharedVolumeSubConfig(ft)


class FileService(BaseService):
    """文件上传与管理服务。

    封装全部文件操作 OneBot API 调用，文件上传方法通过 PathMapper
    解析本地路径为协议端可访问的路径。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "file_service"
    service_description: str = "文件上传与管理服务"
    version: str = "1.0.0"

    def _get_path_mapper(self) -> PathMapper:
        """获取 PathMapper 实例。

        从插件配置中提取 file_transfer 节，通过适配器转换后传入 PathMapper。
        每次调用创建新实例，因为 Service 不是单例。

        Returns:
            PathMapper 实例。
        """
        config = self.plugin.config
        if config is None:
            # 无配置时传入空适配器，PathMapper 会使用默认值
            return PathMapper(_FileTransferConfigAdapter(None))
        file_transfer = getattr(config, "file_transfer", None)
        if file_transfer is None:
            return PathMapper(_FileTransferConfigAdapter(None))
        return PathMapper(_FileTransferConfigAdapter(file_transfer))

    async def _resolve_file_path(self, file_path: str) -> str:
        """通过 PathMapper 解析文件路径。

        按优先级尝试路径映射、共享卷、base64 三种模式。

        Args:
            file_path: 本地文件路径。

        Returns:
            解析后的路径字符串（可能是映射路径、原始路径或 base64:// 前缀）。

        Raises:
            RuntimeError: 所有模式均未命中且无法传输。
            FileNotFoundError: base64 模式下文件不存在。
        """
        mapper = self._get_path_mapper()
        return await mapper.resolve_path(file_path)

    async def upload_group_file(
        self,
        group_id: int,
        file_path: str,
        name: str,
    ) -> dict[str, Any]:
        """上传群文件。

        对应 OneBot API: ``upload_group_file``。
        通过 PathMapper 解析本地文件路径。

        Args:
            group_id: 群号。
            file_path: 本地文件路径。
            name: 文件名称。

        Returns:
            适配器返回的响应字典。
        """
        resolved_path = await self._resolve_file_path(file_path)
        params: dict[str, Any] = {
            "group_id": group_id,
            "file": resolved_path,
            "name": name,
        }
        return await _call_onebot_api("upload_group_file", params)

    async def upload_private_file(
        self,
        user_id: int,
        file_path: str,
        name: str,
    ) -> dict[str, Any]:
        """上传私聊文件。

        对应 OneBot API: ``upload_private_file``。
        通过 PathMapper 解析本地文件路径。

        Args:
            user_id: 目标用户 QQ 号。
            file_path: 本地文件路径。
            name: 文件名称。

        Returns:
            适配器返回的响应字典。
        """
        resolved_path = await self._resolve_file_path(file_path)
        params: dict[str, Any] = {
            "user_id": user_id,
            "file": resolved_path,
            "name": name,
        }
        return await _call_onebot_api("upload_private_file", params)

    async def get_file(
        self,
        file_id: str,
        url: bool = False,
    ) -> dict[str, Any]:
        """获取文件信息（NapCat 扩展）。

        对应 NapCat 扩展 API: ``get_file``。

        Args:
            file_id: 文件 ID。
            url: 是否返回下载 URL，默认为 False。

        Returns:
            适配器返回的响应字典，包含文件信息。
        """
        params: dict[str, Any] = {
            "file_id": file_id,
            "url": url,
        }
        return await _call_onebot_api("get_file", params)

    async def get_image(self, file: str) -> dict[str, Any]:
        """获取图片信息。

        对应 OneBot API: ``get_image``。

        Args:
            file: 图片文件标识（收到的图片 file 或本地路径）。

        Returns:
            适配器返回的响应字典，包含图片信息。
        """
        params: dict[str, Any] = {"file": file}
        return await _call_onebot_api("get_image", params)

    async def get_record(self, file: str, out_format: str = "mp3") -> dict[str, Any]:
        """获取语音文件信息。

        对应 OneBot API: ``get_record``。

        Args:
            file: 语音文件标识（收到的语音 file 或本地路径）。
            out_format: 输出格式（如 "mp3"、"amr"、"wma"），默认为 "mp3"。

        Returns:
            适配器返回的响应字典，包含语音文件信息。
        """
        params: dict[str, Any] = {
            "file": file,
            "out_format": out_format,
        }
        return await _call_onebot_api("get_record", params)

    async def send_online_file(
        self,
        user_id: int,
        file_path: str,
        file_name: str = "",
    ) -> dict[str, Any]:
        """发送在线文件（NapCat 扩展）。

        对应 NapCat 扩展 API: ``send_online_file``。
        通过 PathMapper 解析本地文件路径。

        Args:
            user_id: 目标用户 QQ 号。
            file_path: 本地文件路径。
            file_name: 文件名，默认从路径提取。

        Returns:
            适配器返回的响应字典。
        """
        resolved_path = await self._resolve_file_path(file_path)
        params: dict[str, Any] = {
            "user_id": user_id,
            "file_path": resolved_path,
            "file_name": file_name,
        }
        return await _call_onebot_api("send_online_file", params)

    async def send_online_folder(
        self,
        user_id: int,
        folder_path: str,
        folder_name: str = "",
    ) -> dict[str, Any]:
        """发送在线文件夹（NapCat 扩展）。

        对应 NapCat 扩展 API: ``send_online_folder``。

        Args:
            user_id: 目标用户 QQ 号。
            folder_path: 本地文件夹路径。
            folder_name: 文件夹名，默认从路径提取。

        Returns:
            适配器返回的响应字典。
        """
        resolved_path = await self._resolve_file_path(folder_path)
        params: dict[str, Any] = {
            "user_id": user_id,
            "folder_path": resolved_path,
            "folder_name": folder_name,
        }
        return await _call_onebot_api("send_online_folder", params)

    async def get_online_file_msg(self, user_id: int) -> dict[str, Any]:
        """获取在线文件消息列表（NapCat 扩展）。

        对应 NapCat 扩展 API: ``get_online_file_msg``。

        Args:
            user_id: 目标用户 QQ 号。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {"user_id": user_id}
        return await _call_onebot_api("get_online_file_msg", params)

    async def receive_online_file(
        self,
        user_id: int,
        msg_id: str,
        element_id: str,
    ) -> dict[str, Any]:
        """接收在线文件（NapCat 扩展）。

        对应 NapCat 扩展 API: ``receive_online_file``。

        Args:
            user_id: 发送方 QQ 号。
            msg_id: 消息 ID。
            element_id: 元素 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "msg_id": msg_id,
            "element_id": element_id,
        }
        return await _call_onebot_api("receive_online_file", params)

    async def refuse_online_file(
        self,
        user_id: int,
        msg_id: str,
        element_id: str,
    ) -> dict[str, Any]:
        """拒绝在线文件（NapCat 扩展）。

        对应 NapCat 扩展 API: ``refuse_online_file``。

        Args:
            user_id: 发送方 QQ 号。
            msg_id: 消息 ID。
            element_id: 元素 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "msg_id": msg_id,
            "element_id": element_id,
        }
        return await _call_onebot_api("refuse_online_file", params)

    async def cancel_online_file(
        self,
        user_id: int,
        msg_id: str,
    ) -> dict[str, Any]:
        """取消已发送的在线文件（NapCat 扩展）。

        对应 NapCat 扩展 API: ``cancel_online_file``。

        Args:
            user_id: 接收方 QQ 号。
            msg_id: 消息 ID。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "user_id": user_id,
            "msg_id": msg_id,
        }
        return await _call_onebot_api("cancel_online_file", params)
