"""文件操作 API 的 Tool 组件。

包含 7 个文件操作 Tool，对应 OneBot v11 文件 API 和 NapCat 文件扩展 API：
    - upload_file: 上传文件
    - upload_group_file: 上传群文件
    - upload_private_file: 上传私聊文件
    - get_file: 获取文件信息（NapCat 扩展）
    - get_image: 获取图片信息
    - get_record: 获取语音文件信息
    - get_file_url: 获取文件下载 URL（NapCat 扩展）

文件上传类 Tool 使用 PathMapper 处理路径映射，将本地路径适配为协议端可访问的路径。
Tool 不检查配置开关，配置开关由 Service 层统一检查。

文件操作超时时间为 120 秒（较消息操作更长）。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.api.log_api import get_logger
from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

logger = get_logger("onebot_expand")

# 文件操作超时时间（秒）
_FILE_TIMEOUT: float = 120.0

__all__ = [
    "UploadFileTool",
    "UploadGroupFileTool",
    "UploadPrivateFileTool",
    "GetFileTool",
    "GetImageTool",
    "GetRecordTool",
    "GetFileUrlTool",
]


def _extract_file_name(file_path: str, file_name: str = "") -> str:
    """从文件路径或参数中提取文件名。

    Args:
        file_path: 文件路径。
        file_name: 显式指定的文件名，优先使用。

    Returns:
        文件名字符串。
    """
    if file_name:
        return file_name
    # 兼容 / 和 \\ 路径分隔符
    return file_path.replace("\\", "/").rstrip("/").split("/")[-1]


async def _resolve_file_path(file_path: str) -> str:
    """通过 PathMapper 解析文件路径。

    延迟导入 PathMapper 和配置，避免循环依赖。
    如果 PathMapper 不可用或解析失败，回退到原始路径。

    Args:
        file_path: 本地文件路径。

    Returns:
        适配后的路径字符串（可能是映射路径、base64 编码或原始路径）。
    """
    try:
        from ..path_mapper import PathMapper

        # 尝试从配置管理器获取配置实例
        config = _try_get_config()
        if config is None:
            # 无法获取配置，直接返回原始路径
            logger.debug("无法获取配置实例，使用原始路径上传文件")
            return file_path

        # 从 file_transfer 配置节构建 PathMapper 配置对象
        mapper_config = _build_mapper_config(config)
        mapper = PathMapper(mapper_config)
        return await mapper.resolve_path(file_path)
    except Exception as e:
        logger.warning(f"路径映射失败，使用原始路径: {e}")
        return file_path


def _try_get_config() -> Any:
    """尝试从配置管理器获取配置实例。

    通过 config_api.get_config 获取已加载的 onebot_expand 配置实例。

    Returns:
        配置实例，获取失败时返回 None。
    """
    try:
        from src.app.plugin_system.api.config_api import get_config

        return get_config("onebot_expand")
    except Exception:
        return None


def _build_mapper_config(config: Any) -> Any:
    """从 OnebotExpandConfig 构建 PathMapper 所需的配置对象。

    PathMapper 期望配置对象包含 path_mapping、base64_transfer、shared_volume
    三个子属性。这里从 OnebotExpandConfig.file_transfer 中提取并构建。

    Args:
        config: OnebotExpandConfig 配置实例。

    Returns:
        包含路径映射配置的适配对象。
    """

    class _PathMappingConfig:
        """路径映射配置适配器。"""

        def __init__(self, ft: Any) -> None:
            self.enabled: bool = getattr(ft, "enable_path_mapping", False)
            self.rules: list[str] = getattr(ft, "path_mappings", [])

    class _Base64Config:
        """base64 传输配置适配器。"""

        def __init__(self, ft: Any) -> None:
            self.enabled: bool = getattr(ft, "enable_base64_transfer", True)
            self.max_file_size_mb: int = getattr(ft, "max_base64_size_mb", 10)

    class _SharedVolumeConfig:
        """共享卷配置适配器。"""

        def __init__(self, ft: Any) -> None:
            self.enabled: bool = getattr(ft, "enable_shared_volume", False)

    class _MapperConfig:
        """PathMapper 配置适配器。"""

        def __init__(self, ft: Any) -> None:
            self.path_mapping = _PathMappingConfig(ft)
            self.base64_transfer = _Base64Config(ft)
            self.shared_volume = _SharedVolumeConfig(ft)

    file_transfer = getattr(config, "file_transfer", None)
    if file_transfer is None:
        # 回退：创建默认配置
        from ..config import OnebotExpandConfig

        default_config = OnebotExpandConfig()
        file_transfer = default_config.file_transfer

    return _MapperConfig(file_transfer)


class UploadFileTool(BaseTool):
    """上传文件的 Tool。

    对应 OneBot API: ``upload_file``。
    上传文件到协议端，需指定文件路径和显示名称。
    使用 PathMapper 进行路径映射适配。
    """

    tool_name = "upload_file"
    tool_description = "上传文件到协议端"

    async def execute(
        self,
        file_path: Annotated[str, "本地文件路径"],
        file_name: Annotated[str, "显示的文件名（空则自动从路径提取）"] = "",
    ) -> tuple[bool, str]:
        """执行上传文件。"""
        resolved_path = await _resolve_file_path(file_path)
        name = _extract_file_name(file_path, file_name)

        params: dict[str, Any] = {
            "file": resolved_path,
            "name": name,
        }
        result = await _call_onebot_api("upload_file", params, timeout=_FILE_TIMEOUT)
        if result.get("status") == "ok":
            return True, f"文件上传成功: {name}"
        return False, f"文件上传失败: {result.get('msg', '未知错误')}"


class UploadGroupFileTool(BaseTool):
    """上传群文件的 Tool。

    对应 OneBot API: ``upload_group_file``。
    上传文件到指定群的群文件存储。
    使用 PathMapper 进行路径映射适配。
    """

    tool_name = "upload_group_file"
    tool_description = "上传文件到指定群的群文件"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        file_path: Annotated[str, "本地文件路径"],
        file_name: Annotated[str, "显示的文件名（空则自动从路径提取）"] = "",
    ) -> tuple[bool, str]:
        """执行上传群文件。"""
        resolved_path = await _resolve_file_path(file_path)
        name = _extract_file_name(file_path, file_name)

        params: dict[str, Any] = {
            "group_id": group_id,
            "file": resolved_path,
            "name": name,
        }
        result = await _call_onebot_api(
            "upload_group_file", params, timeout=_FILE_TIMEOUT
        )
        if result.get("status") == "ok":
            return True, f"群文件上传成功: {name}"
        return False, f"群文件上传失败: {result.get('msg', '未知错误')}"


class UploadPrivateFileTool(BaseTool):
    """上传私聊文件的 Tool。

    对应 OneBot API: ``upload_private_file``。
    上传文件到指定用户的私聊会话。
    使用 PathMapper 进行路径映射适配。
    """

    tool_name = "upload_private_file"
    tool_description = "上传文件到指定用户的私聊会话"

    async def execute(
        self,
        user_id: Annotated[int, "目标用户QQ号"],
        file_path: Annotated[str, "本地文件路径"],
        file_name: Annotated[str, "显示的文件名（空则自动从路径提取）"] = "",
    ) -> tuple[bool, str]:
        """执行上传私聊文件。"""
        resolved_path = await _resolve_file_path(file_path)
        name = _extract_file_name(file_path, file_name)

        params: dict[str, Any] = {
            "user_id": user_id,
            "file": resolved_path,
            "name": name,
        }
        result = await _call_onebot_api(
            "upload_private_file", params, timeout=_FILE_TIMEOUT
        )
        if result.get("status") == "ok":
            return True, f"私聊文件上传成功: {name}"
        return False, f"私聊文件上传失败: {result.get('msg', '未知错误')}"


class GetFileTool(BaseTool):
    """获取文件信息的 Tool（NapCat 扩展）。

    对应 NapCat API: ``get_file``。
    根据文件 ID 获取文件信息，可选返回下载 URL。
    """

    tool_name = "get_file"
    tool_description = "根据文件ID获取文件信息（NapCat扩展）"

    async def execute(
        self,
        file_id: Annotated[str, "文件ID"],
        url: Annotated[bool, "是否返回下载URL"] = False,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取文件信息。"""
        params: dict[str, Any] = {
            "file_id": file_id,
            "url": url,
        }
        result = await _call_onebot_api("get_file", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取文件信息失败: {result.get('msg', '未知错误')}"


class GetImageTool(BaseTool):
    """获取图片信息的 Tool。

    对应 OneBot API: ``get_image``。
    根据图片文件名或 ID 获取图片信息（包括下载 URL）。
    """

    tool_name = "get_image"
    tool_description = "获取图片信息（包括下载URL）"

    async def execute(
        self,
        file: Annotated[str, "图片文件名或ID（收到的图片消息中的 file 字段）"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取图片信息。"""
        params: dict[str, Any] = {"file": file}
        result = await _call_onebot_api("get_image", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取图片信息失败: {result.get('msg', '未知错误')}"


class GetRecordTool(BaseTool):
    """获取语音文件信息的 Tool。

    对应 OneBot API: ``get_record``。
    根据语音文件名获取语音文件信息，可指定输出格式。
    """

    tool_name = "get_record"
    tool_description = "获取语音文件信息，可指定转换格式"

    async def execute(
        self,
        file: Annotated[str, "语音文件名或ID（收到的语音消息中的 file 字段）"],
        out_format: Annotated[
            str, "输出格式（如 mp3, amr, wma, m4a, spx, ogg, wav）"
        ] = "mp3",
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取语音文件信息。"""
        params: dict[str, Any] = {
            "file": file,
            "out_format": out_format,
        }
        result = await _call_onebot_api("get_record", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取语音文件信息失败: {result.get('msg', '未知错误')}"


class GetFileUrlTool(BaseTool):
    """获取文件下载 URL 的 Tool（NapCat 扩展）。

    对应 NapCat API: ``get_file_url``。
    根据文件 ID 获取文件的下载 URL。
    """

    tool_name = "get_file_url"
    tool_description = "根据文件ID获取文件下载URL（NapCat扩展）"

    async def execute(
        self,
        file_id: Annotated[str, "文件ID"],
    ) -> tuple[bool, str]:
        """执行获取文件下载 URL。"""
        params: dict[str, Any] = {"file_id": file_id}
        result = await _call_onebot_api("get_file_url", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            url_value = ""
            if isinstance(data, dict):
                url_value = str(data.get("url", ""))
            elif isinstance(data, str):
                url_value = data
            return True, url_value
        return False, f"获取文件URL失败: {result.get('msg', '未知错误')}"
