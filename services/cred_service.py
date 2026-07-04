"""凭证/安全/下载服务。

封装 NapCat 凭证/安全/下载 API，提供 clientkey、凭证、
rkey、URL 安全检查、OCR、文件下载等功能。

API 列表 (7):
    - get_clientkey: 获取clientkey
    - get_credentials: 获取凭证
    - get_rkey: 获取rkey
    - get_rkey_server: 获取rkey服务器信息
    - check_url_safely: 检查链接安全性
    - ocr_image: OCR图片
    - download_file: 下载文件
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["CredService"]


class CredService(BaseService):
    """凭证/安全/下载服务。

    封装全部凭证/安全/下载 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "cred_service"
    service_description: str = "凭证/安全/下载服务"
    version: str = "1.0.0"

    async def get_clientkey(self) -> dict[str, Any]:
        """获取clientkey。

        对应 NapCat 扩展 API: ``get_clientkey``。

        Returns:
            适配器返回的响应字典，包含 clientkey。
        """
        return await _call_onebot_api("get_clientkey", {})

    async def get_credentials(self, domain: str) -> dict[str, Any]:
        """获取凭证。

        对应 NapCat 扩展 API: ``get_credentials``。

        Args:
            domain: 目标域名。

        Returns:
            适配器返回的响应字典，包含凭证信息。
        """
        params: dict[str, Any] = {"domain": domain}
        return await _call_onebot_api("get_credentials", params)

    async def get_rkey(self) -> dict[str, Any]:
        """获取rkey。

        对应 NapCat 扩展 API: ``get_rkey``。

        Returns:
            适配器返回的响应字典，包含 rkey。
        """
        return await _call_onebot_api("get_rkey", {})

    async def get_rkey_server(self) -> dict[str, Any]:
        """获取rkey服务器信息。

        对应扩展 API: ``get_rkey_server``。
        比 get_rkey 多返回 expired_time / name 等元数据。

        Returns:
            适配器返回的响应字典，包含 rkey 服务器信息。
        """
        return await _call_onebot_api("get_rkey_server", {})

    async def check_url_safely(self, url: str) -> dict[str, Any]:
        """检查链接安全性。

        对应 NapCat 扩展 API: ``check_url_safely``。

        Args:
            url: 目标 URL。

        Returns:
            适配器返回的响应字典，包含安全性检查结果。
        """
        params: dict[str, Any] = {"url": url}
        return await _call_onebot_api("check_url_safely", params)

    async def ocr_image(self, image: str) -> dict[str, Any]:
        """OCR图片。

        对应 NapCat 扩展 API: ``ocr_image``。

        Args:
            image: 图片路径或 URL。

        Returns:
            适配器返回的响应字典，包含 OCR 识别结果。
        """
        params: dict[str, Any] = {"image": image}
        return await _call_onebot_api("ocr_image", params)

    async def download_file(
        self,
        url: str,
        name: str = "",
        headers: list[str] | None = None,
    ) -> dict[str, Any]:
        """下载文件。

        对应 NapCat 扩展 API: ``download_file``。

        Args:
            url: 下载 URL。
            name: 保存文件名，默认为空字符串。
            headers: 自定义请求头列表，默认为 None。

        Returns:
            适配器返回的响应字典，包含下载结果。
        """
        params: dict[str, Any] = {"url": url}
        if name:
            params["name"] = name
        if headers:
            params["headers"] = headers
        return await _call_onebot_api("download_file", params)