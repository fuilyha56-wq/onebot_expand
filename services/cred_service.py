"""凭证/安全/下载服务。

封装 NapCat 凭证/安全/下载 API，提供 clientkey、凭证、
rkey、URL 安全检查、OCR、文件下载等功能。

API 列表 (6):
    - get_clientkey: 获取clientkey
    - get_credentials: 获取凭证
    - get_rkey: 获取rkey
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

    封装全部凭证/安全/下载 API 调用，提供配置开关检查和统一调用入口。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "cred_service"
    service_description: str = "凭证/安全/下载服务"
    version: str = "1.0.0"

    def _is_api_enabled(self, api_name: str) -> bool:
        """检查 API 是否在配置中启用。

        1.3.0 起支持别名：传入别名时会先解析为主名再查询配置开关。
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
        """构造 API 禁用时的标准响应。"""
        return {"status": "error", "retcode": -1, "msg": f"API {api_name} 已禁用"}

    async def get_clientkey(self) -> dict[str, Any]:
        """获取clientkey。

        对应 NapCat 扩展 API: ``get_clientkey``。

        Returns:
            适配器返回的响应字典，包含 clientkey。
        """
        if not self._is_api_enabled("get_clientkey"):
            return self._disabled_response("get_clientkey")
        return await _call_onebot_api("get_clientkey", {})

    async def get_credentials(self, domain: str) -> dict[str, Any]:
        """获取凭证。

        对应 NapCat 扩展 API: ``get_credentials``。

        Args:
            domain: 目标域名。

        Returns:
            适配器返回的响应字典，包含凭证信息。
        """
        if not self._is_api_enabled("get_credentials"):
            return self._disabled_response("get_credentials")
        params: dict[str, Any] = {"domain": domain}
        return await _call_onebot_api("get_credentials", params)

    async def get_rkey(self) -> dict[str, Any]:
        """获取rkey。

        对应 NapCat 扩展 API: ``get_rkey``。

        Returns:
            适配器返回的响应字典，包含 rkey。
        """
        if not self._is_api_enabled("get_rkey"):
            return self._disabled_response("get_rkey")
        return await _call_onebot_api("get_rkey", {})

    async def check_url_safely(self, url: str) -> dict[str, Any]:
        """检查链接安全性。

        对应 NapCat 扩展 API: ``check_url_safely``。

        Args:
            url: 目标 URL。

        Returns:
            适配器返回的响应字典，包含安全性检查结果。
        """
        if not self._is_api_enabled("check_url_safely"):
            return self._disabled_response("check_url_safely")
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
        if not self._is_api_enabled("ocr_image"):
            return self._disabled_response("ocr_image")
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
        if not self._is_api_enabled("download_file"):
            return self._disabled_response("download_file")
        params: dict[str, Any] = {"url": url}
        if name:
            params["name"] = name
        if headers:
            params["headers"] = headers
        return await _call_onebot_api("download_file", params)