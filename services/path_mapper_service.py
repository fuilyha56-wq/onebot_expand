"""文件路径映射服务。

封装 PathMapper 模块，提供统一的文件路径解析、base64 转换、
路径映射和传输模式查询功能。

支持三种传输模式（按优先级）：
    1. 路径映射: 将本地路径前缀替换为协议端可访问的路径前缀
    2. 共享卷: 直接使用原始路径发送
    3. base64: 读取文件内容编码为 base64 传输
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..path_mapper import PathMapper, TransferMode

__all__ = ["PathMapperService"]


class _PathMappingSubConfig:
    """路径映射配置子节适配器。

    PathMapper 通过 ``getattr(config, "enabled")`` 和
    ``getattr(config, "rules")`` 读取配置，因此需要提供属性而非字典。
    """

    def __init__(self, ft: Any) -> None:
        if ft is None:
            self.enabled: bool = False
            self.rules: list[str] = []
        else:
            self.enabled = getattr(ft, "enable_path_mapping", False)
            self.rules = getattr(ft, "path_mappings", [])


class _Base64SubConfig:
    """base64 传输配置子节适配器。"""

    def __init__(self, ft: Any) -> None:
        if ft is None:
            self.enabled: bool = True
            self.max_file_size_mb: int = 30
        else:
            self.enabled = getattr(ft, "enable_base64_transfer", True)
            self.max_file_size_mb = getattr(ft, "max_base64_size_mb", 30)


class _SharedVolumeSubConfig:
    """共享卷配置子节适配器。"""

    def __init__(self, ft: Any) -> None:
        if ft is None:
            self.enabled: bool = False
        else:
            self.enabled = getattr(ft, "enable_shared_volume", False)


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
        self.path_mapping: _PathMappingSubConfig = _PathMappingSubConfig(
            file_transfer_section
        )
        self.base64_transfer: _Base64SubConfig = _Base64SubConfig(file_transfer_section)
        self.shared_volume: _SharedVolumeSubConfig = _SharedVolumeSubConfig(
            file_transfer_section
        )


class PathMapperService(BaseService):
    """文件路径映射服务。

    封装 PathMapper 实例，提供统一的路径解析和传输模式查询接口。
    内部每次创建新的 PathMapper 实例（Service 不是单例）。
    """

    service_name: str = "path_mapper_service"
    service_description: str = "文件路径映射服务"
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
            return PathMapper(_FileTransferConfigAdapter(None))
        file_transfer = getattr(config, "file_transfer", None)
        if file_transfer is None:
            return PathMapper(_FileTransferConfigAdapter(None))
        return PathMapper(_FileTransferConfigAdapter(file_transfer))

    async def resolve_path(self, file_path: str) -> str:
        """解析文件路径，根据配置的模式返回适配后的路径。

        按优先级尝试：路径映射 > 共享卷 > base64。
        如果所有模式均未命中且无法传输，抛出 RuntimeError。

        Args:
            file_path: 本地文件路径。

        Returns:
            适配后的路径字符串（可能是映射路径、原始路径或 base64:// 前缀）。

        Raises:
            FileNotFoundError: base64 模式下文件不存在。
            PermissionError: base64 模式下无读取权限。
            RuntimeError: 所有模式均未命中且无法传输。
        """
        mapper = self._get_path_mapper()
        return await mapper.resolve_path(file_path)

    async def to_base64(self, file_path: str) -> str:
        """将文件转为 base64 编码字符串。

        读取文件内容并编码为 base64，返回 "base64://" 前缀的字符串。

        Args:
            file_path: 本地文件路径。

        Returns:
            "base64://" + base64 编码内容。

        Raises:
            FileNotFoundError: 文件不存在。
            PermissionError: 无读取权限。
            ValueError: 文件大小超过限制。
        """
        mapper = self._get_path_mapper()
        return await mapper.to_base64(file_path)

    async def map_path(self, host_path: str) -> str | None:
        """根据路径映射表转换路径。

        遍历映射规则，将本地路径前缀替换为协议端可访问的路径前缀。

        Args:
            host_path: 本地文件路径。

        Returns:
            映射后的路径字符串，未命中映射规则则返回 None。
        """
        mapper = self._get_path_mapper()
        return await mapper.map_path(host_path)

    async def get_transfer_mode(self) -> str:
        """获取当前传输模式。

        根据配置自动检测最佳传输模式。

        Returns:
            当前传输模式字符串，可选值:
            - "path_mapping": 路径映射模式
            - "base64": base64 模式
            - "shared_volume": 共享卷模式
        """
        mapper = self._get_path_mapper()
        mode = await mapper.auto_detect_best_mode()
        return mode.value

    async def get_available_modes(self) -> list[str]:
        """获取可用模式列表。

        检查配置中启用了哪些传输模式。

        Returns:
            已启用的传输模式字符串列表，按优先级排序。
        """
        available: list[str] = []

        config = self.plugin.config
        if config is None:
            # 无配置时仅 base64 可用（默认模式）
            return [TransferMode.BASE64.value]

        file_transfer = getattr(config, "file_transfer", None)
        if file_transfer is None:
            return [TransferMode.BASE64.value]

        # 按优先级检查每种模式是否启用
        if getattr(file_transfer, "enable_path_mapping", False) and getattr(
            file_transfer, "path_mappings", None
        ):
            available.append(TransferMode.PATH_MAPPING.value)

        if getattr(file_transfer, "enable_shared_volume", False):
            available.append(TransferMode.SHARED_VOLUME.value)

        if getattr(file_transfer, "enable_base64_transfer", True):
            available.append(TransferMode.BASE64.value)

        return available
