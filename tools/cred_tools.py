"""凭证/安全/下载 API 的 Tool 组件。

包含 7 个凭证/安全/下载 Tool，对应 NapCat 凭证/安全/下载 API：
    - get_clientkey: 获取clientkey
    - get_credentials: 获取凭证
    - get_rkey: 获取rkey
    - get_rkey_server: 获取rkey服务器信息
    - check_url_safely: 检查链接安全性
    - ocr_image: OCR图片
    - download_file: 下载文件

Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "GetClientkeyTool",
    "GetCredentialsTool",
    "GetRkeyTool",
    "GetRkeyServerTool",
    "CheckUrlSafelyTool",
    "OcrImageTool",
    "DownloadFileTool",
]


class GetClientkeyTool(BaseTool):
    """获取clientkey的 Tool。

    对应 NapCat API: ``get_clientkey``。
    获取当前 Bot 的 clientkey。
    """

    tool_name = "get_clientkey"
    tool_description = "获取当前Bot的clientkey"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取clientkey。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_clientkey", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取clientkey失败: {result.get('msg', '未知错误')}"


class GetCredentialsTool(BaseTool):
    """获取凭证的 Tool。

    对应 NapCat API: ``get_credentials``。
    获取指定域名的凭证信息。
    """

    tool_name = "get_credentials"
    tool_description = "获取指定域名的凭证信息"

    async def execute(
        self,
        domain: Annotated[str, "目标域名"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取凭证。"""
        params: dict[str, Any] = {"domain": domain}
        result = await _call_onebot_api("get_credentials", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取凭证失败: {result.get('msg', '未知错误')}"


class GetRkeyTool(BaseTool):
    """获取rkey的 Tool。

    对应 NapCat API: ``get_rkey``。
    获取当前 Bot 的 rkey。
    """

    tool_name = "get_rkey"
    tool_description = "获取当前Bot的rkey"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取rkey。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_rkey", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取rkey失败: {result.get('msg', '未知错误')}"


class GetRkeyServerTool(BaseTool):
    """获取rkey服务器信息的 Tool。

    对应 API: ``get_rkey_server``。
    返回 rkey 服务器信息（含过期时间和服务器名），比 get_rkey 多返回元数据。
    """

    tool_name = "get_rkey_server"
    tool_description = "获取rkey服务器信息（含过期时间和服务器名）"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取rkey服务器信息。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_rkey_server", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取rkey服务器信息失败: {result.get('msg', '未知错误')}"


class CheckUrlSafelyTool(BaseTool):
    """检查链接安全性的 Tool。

    对应 NapCat API: ``check_url_safely``。
    检查指定 URL 的安全性。
    """

    tool_name = "check_url_safely"
    tool_description = "检查指定URL的安全性"

    async def execute(
        self,
        url: Annotated[str, "目标URL"],
    ) -> tuple[bool, str]:
        """执行检查链接安全性。"""
        params: dict[str, Any] = {"url": url}
        result = await _call_onebot_api("check_url_safely", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            if isinstance(data, dict):
                safe = data.get("safe", False)
                return True, "链接安全" if safe else "链接不安全"
            return True, str(data)
        return False, f"检查链接安全性失败: {result.get('msg', '未知错误')}"


class OcrImageTool(BaseTool):
    """OCR图片的 Tool。

    对应 NapCat API: ``ocr_image``。
    对指定图片进行 OCR 识别。
    """

    tool_name = "ocr_image"
    tool_description = "对指定图片进行OCR文字识别"

    async def execute(
        self,
        image: Annotated[str, "图片路径或URL"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行OCR图片。"""
        params: dict[str, Any] = {"image": image}
        result = await _call_onebot_api("ocr_image", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"OCR识别失败: {result.get('msg', '未知错误')}"


class DownloadFileTool(BaseTool):
    """下载文件的 Tool。

    对应 NapCat API: ``download_file``。
    下载指定 URL 的文件。
    """

    tool_name = "download_file"
    tool_description = "下载指定URL的文件"

    async def execute(
        self,
        url: Annotated[str, "下载URL"],
        name: Annotated[str, "保存文件名（可选）"] = "",
        headers: Annotated[list[str] | None, "自定义请求头列表（可选）"] = None,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行下载文件。"""
        params: dict[str, Any] = {"url": url}
        if name:
            params["name"] = name
        if headers:
            params["headers"] = headers
        result = await _call_onebot_api("download_file", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"下载文件失败: {result.get('msg', '未知错误')}"