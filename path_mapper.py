"""文件路径映射器模块。

支持三种文件传输模式：路径映射、base64 编码、共享卷。
用于在 Neo-MoFox 与 NapCat/SnowLumia 协议端之间适配文件路径。

优先级：路径映射 > 共享卷 > base64。
"""

from __future__ import annotations

import asyncio

from enum import Enum
from pathlib import Path
from typing import Any

from src.app.plugin_system.api.log_api import get_logger
from src.core.utils.base64_helper import base64_encode_bytes

logger = get_logger("onebot_expand")


# ============================================================================
# 枚举定义
# ============================================================================


class TransferMode(Enum):
    """文件传输模式枚举。"""

    PATH_MAPPING = "path_mapping"
    """路径映射模式：将本地路径前缀替换为协议端可访问的路径前缀"""

    BASE64 = "base64"
    """base64 模式：读取文件内容并编码为 base64 传输"""

    SHARED_VOLUME = "shared_volume"
    """共享卷模式：直接使用原始路径发送"""

    AUTO = "auto"
    """自动检测模式：根据配置和文件可用性自动选择最佳模式"""


# ============================================================================
# 常量定义
# ============================================================================

# 禁止映射的系统敏感目录
_SENSITIVE_DIRS: set[str] = {
    "/",
    "/etc",
    "/sys",
    "/proc",
    "/boot",
    "/dev",
    "/root",
    "c:\\windows",
    "c:\\system32",
    "c:\\program files",
}

# base64 传输最大文件大小（字节），默认 30MB
_DEFAULT_MAX_FILE_SIZE = 30 * 1024 * 1024

# base64 传输前缀
_BASE64_PREFIX = "base64://"


# ============================================================================
# 路径映射器
# ============================================================================


class PathMapper:
    """文件路径映射器。

    支持三种传输模式，按优先级处理：路径映射 > 共享卷 > base64。
    所有文件 IO 操作通过 asyncio.to_thread 包装，避免阻塞事件循环。

    配置对象需包含以下结构（与 OnebotExpandConfig.file_transfer 对应）：
        - config.path_mapping.enabled: bool
        - config.path_mapping.rules: list[dict] (含 source_path, target_path, enabled)
        - config.base64_transfer.enabled: bool
        - config.base64_transfer.max_file_size_mb: int
        - config.shared_volume.enabled: bool
    """

    def __init__(self, config: Any) -> None:
        """初始化路径映射器。

        Args:
            config: 文件传输配置对象，需包含 path_mapping、base64_transfer、
                    shared_volume 三个子配置节。
        """
        self._config = config
        self._mappings: dict[str, str] = self._parse_mappings(
            self._get_path_mapping_rules()
        )

    # ==================== 公开方法 ====================

    async def resolve_path(self, file_path: str) -> str:
        """解析文件路径，根据配置的模式返回适配后的路径。

        按优先级尝试：路径映射 > 共享卷 > base64。
        如果所有模式均未命中且无法传输，抛出 RuntimeError。

        Args:
            file_path: 本地文件路径

        Returns:
            适配后的路径字符串（可能是映射路径、原始路径或 base64:// 前缀）

        Raises:
            FileNotFoundError: base64 模式下文件不存在
            PermissionError: base64 模式下无读取权限
            RuntimeError: 所有模式均未命中且无法传输
        """
        # 1. 尝试路径映射模式
        mapped = await self.map_path(file_path)
        if mapped is not None:
            logger.debug(f"路径映射成功: {file_path} -> {mapped}")
            return mapped

        # 2. 尝试共享卷模式
        if self._is_shared_volume_enabled():
            logger.debug(f"使用共享卷模式: {file_path}")
            return file_path

        # 3. 尝试 base64 模式
        if self._is_base64_enabled():
            logger.debug(f"使用 base64 模式: {file_path}")
            return await self.to_base64(file_path)

        # 所有模式均未命中
        raise RuntimeError(f"无法发送文件：路径未映射且无备选模式可用: {file_path}")

    async def to_base64(self, file_path: str) -> str:
        """将文件转为 base64 编码字符串。

        读取文件内容并编码为 base64，返回 "base64://" 前缀的字符串。

        Args:
            file_path: 本地文件路径

        Returns:
            "base64://" + base64 编码内容

        Raises:
            FileNotFoundError: 文件不存在
            PermissionError: 无读取权限
            ValueError: 文件大小超过限制
        """
        path = Path(file_path)

        # 检查文件是否存在（在线程中执行避免阻塞）
        exists = await asyncio.to_thread(path.is_file)
        if not exists:
            raise FileNotFoundError(f"文件不存在: {file_path}")

        # 检查文件大小
        max_size = self._get_max_file_size()
        file_size = await asyncio.to_thread(path.stat)
        if file_size.st_size > max_size:
            raise ValueError(
                f"文件大小 {file_size.st_size} 字节超过限制 "
                f"{max_size} 字节 ({max_size // (1024 * 1024)}MB)"
            )

        # 在线程中读取文件内容
        file_bytes = await asyncio.to_thread(lambda: path.read_bytes())

        encoded = base64_encode_bytes(file_bytes)
        return f"{_BASE64_PREFIX}{encoded}"

    async def map_path(self, host_path: str) -> str | None:
        """根据路径映射表转换路径。

        遍历映射规则，将本地路径前缀替换为协议端可访问的路径前缀。
        支持跨平台路径分隔符（/ 和 \\）。

        Args:
            host_path: 本地文件路径

        Returns:
            映射后的路径字符串，未命中映射规则则返回 None
        """
        if not self._mappings:
            return None

        # 统一路径分隔符为 / 进行匹配
        normalized_host = host_path.replace("\\", "/")

        for source, target in self._mappings.items():
            normalized_source = source.replace("\\", "/")
            normalized_target = target.replace("\\", "/")

            # 安全检查：禁止映射到系统敏感目录
            if self._is_sensitive_dir(normalized_target):
                logger.warning(f"路径映射目标路径指向敏感目录，跳过: {target}")
                continue

            # 前缀匹配
            if normalized_host.startswith(normalized_source):
                # 替换前缀，保留剩余路径
                remaining = normalized_host[len(normalized_source) :]
                mapped = normalized_target.rstrip("/") + remaining

                # 使用目标路径的分隔符风格
                if "\\" in target:
                    mapped = mapped.replace("/", "\\")
                else:
                    mapped = mapped.replace("\\", "/")

                return mapped

        return None

    def _parse_mappings(self, mappings: list[str]) -> dict[str, str]:
        """解析 "host|container" 格式的映射规则。

        也支持配置中的 rules 列表格式（dict 含 source_path 和 target_path）。

        Args:
            mappings: 映射规则字符串列表，格式为 "host_path|container_path"

        Returns:
            源路径到目标路径的映射字典
        """
        result: dict[str, str] = {}

        for item in mappings:
            if isinstance(item, str):
                # 字符串格式: "host|container"
                parts = item.split("|", 1)
                if len(parts) != 2:
                    logger.warning(f"路径映射规则格式无效，跳过: {item}")
                    continue
                source = parts[0].strip()
                target = parts[1].strip()
                if source and target:
                    result[source] = target
            elif isinstance(item, dict):
                # 字典格式: {"source_path": "...", "target_path": "...", "enabled": True}
                if not item.get("enabled", True):
                    continue
                source = str(item.get("source_path", "")).strip()
                target = str(item.get("target_path", "")).strip()
                if source and target:
                    result[source] = target

        return result

    async def auto_detect_best_mode(self) -> TransferMode:
        """自动检测最佳传输模式。

        根据配置和文件系统可用性自动选择：
        1. 如果路径映射已配置且有规则，选择 PATH_MAPPING
        2. 如果共享卷模式启用，选择 SHARED_VOLUME
        3. 如果 base64 模式启用，选择 BASE64
        4. 默认回退到 BASE64

        Returns:
            检测到的最佳传输模式
        """
        if self._is_path_mapping_enabled() and self._mappings:
            return TransferMode.PATH_MAPPING

        if self._is_shared_volume_enabled():
            return TransferMode.SHARED_VOLUME

        if self._is_base64_enabled():
            return TransferMode.BASE64

        # 默认回退
        return TransferMode.BASE64

    def get_mode_description(self, mode: TransferMode) -> str:
        """获取传输模式的描述文本。

        Args:
            mode: 传输模式枚举值

        Returns:
            模式的中文描述
        """
        _descriptions: dict[TransferMode, str] = {
            TransferMode.PATH_MAPPING: (
                "路径映射模式：将本地路径前缀替换为协议端可访问的路径前缀。"
                "适用于 Neo-MoFox 和 NapCat 在不同机器/容器但有共享路径的场景。"
            ),
            TransferMode.BASE64: (
                "base64 模式：读取文件内容并编码为 base64 传输。"
                "适用于无共享路径，通过内容传输的场景。"
            ),
            TransferMode.SHARED_VOLUME: (
                "共享卷模式：直接使用原始路径发送。"
                "适用于 Neo-MoFox 和 NapCat 在同一文件系统的场景。"
            ),
            TransferMode.AUTO: (
                "自动检测模式：根据配置和文件可用性自动选择最佳模式。"
                "优先级为 路径映射 > 共享卷 > base64。"
            ),
        }
        return _descriptions.get(mode, "未知模式")

    # ==================== 私有方法 ====================

    def _get_path_mapping_rules(self) -> list[str]:
        """从配置中获取路径映射规则列表。

        Returns:
            映射规则列表（字符串或字典混合）
        """
        try:
            path_mapping = getattr(self._config, "path_mapping", None)
            if path_mapping is None:
                return []
            rules = getattr(path_mapping, "rules", [])
            # rules 可能是 list[dict] 或 list[str]
            return list(rules) if rules else []
        except Exception:
            return []

    def _is_path_mapping_enabled(self) -> bool:
        """检查路径映射模式是否启用。"""
        try:
            path_mapping = getattr(self._config, "path_mapping", None)
            if path_mapping is None:
                return False
            return getattr(path_mapping, "enabled", False)
        except Exception:
            return False

    def _is_base64_enabled(self) -> bool:
        """检查 base64 传输模式是否启用。"""
        try:
            base64_config = getattr(self._config, "base64_transfer", None)
            if base64_config is None:
                return True  # 默认启用
            return getattr(base64_config, "enabled", True)
        except Exception:
            return True

    def _is_shared_volume_enabled(self) -> bool:
        """检查共享卷模式是否启用。"""
        try:
            shared = getattr(self._config, "shared_volume", None)
            if shared is None:
                return False
            return getattr(shared, "enabled", False)
        except Exception:
            return False

    def _get_max_file_size(self) -> int:
        """获取 base64 传输最大文件大小（字节）。"""
        try:
            base64_config = getattr(self._config, "base64_transfer", None)
            if base64_config is None:
                return _DEFAULT_MAX_FILE_SIZE
            max_mb = getattr(base64_config, "max_file_size_mb", 30)
            return int(max_mb) * 1024 * 1024
        except Exception:
            return _DEFAULT_MAX_FILE_SIZE

    @staticmethod
    def _is_sensitive_dir(path: str) -> bool:
        """检查路径是否指向系统敏感目录。

        Args:
            path: 待检查的路径字符串

        Returns:
            True 如果路径指向敏感目录，False 否则
        """
        normalized = path.lower().replace("\\", "/")
        normalized = normalized.rstrip("/")

        for sensitive in _SENSITIVE_DIRS:
            sensitive_normalized = sensitive.lower().replace("\\", "/")
            if normalized == sensitive_normalized:
                return True
            if normalized.startswith(sensitive_normalized + "/"):
                return True

        return False


__all__ = [
    "TransferMode",
    "PathMapper",
]
