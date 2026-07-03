"""机型/其他扩展服务。

封装 NapCat 机型/其他扩展 API，提供机型展示、Bot 退出、
packet 状态、内联键盘、小程序卡片、翻译、收藏、SSO 包等功能。

API 列表 (10):
    - _get_model_show: 获取机型展示
    - _set_model_show: 设置机型展示
    - bot_exit: 退出机器人
    - nc_get_packet_status: 获取packet状态
    - click_inline_keyboard_button: 点击内联键盘按钮
    - get_mini_app_ark: 获取小程序卡片
    - translate_en2zh: 英译中
    - create_collection: 创建收藏
    - get_collection_list: 获取收藏列表
    - send_packet: 发送原始SSO包
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["MiscService"]


class MiscService(BaseService):
    """机型/其他扩展服务。

    封装全部机型/其他扩展 API 调用，提供配置开关检查和统一调用入口。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "misc_service"
    service_description: str = "机型/其他扩展服务"
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

    async def get_model_show(self, model: str) -> dict[str, Any]:
        """获取机型展示。

        对应 NapCat 扩展 API: ``._get_model_show``。

        Args:
            model: 机型型号。

        Returns:
            适配器返回的响应字典，包含机型展示信息。
        """
        if not self._is_api_enabled("get_model_show"):
            return self._disabled_response("get_model_show")
        params: dict[str, Any] = {"model": model}
        return await _call_onebot_api("._get_model_show", params)

    async def set_model_show(self, model: str, show: str) -> dict[str, Any]:
        """设置机型展示。

        对应 NapCat 扩展 API: ``._set_model_show``。

        Args:
            model: 机型型号。
            show: 展示内容。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("set_model_show"):
            return self._disabled_response("set_model_show")
        params: dict[str, Any] = {
            "model": model,
            "show": show,
        }
        return await _call_onebot_api("._set_model_show", params)

    async def bot_exit(self) -> dict[str, Any]:
        """退出机器人。

        对应 NapCat 扩展 API: ``bot_exit``。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("bot_exit"):
            return self._disabled_response("bot_exit")
        return await _call_onebot_api("bot_exit", {})

    async def nc_get_packet_status(self) -> dict[str, Any]:
        """获取packet状态。

        对应 NapCat 扩展 API: ``nc_get_packet_status``。

        Returns:
            适配器返回的响应字典，包含 packet 处理状态。
        """
        if not self._is_api_enabled("nc_get_packet_status"):
            return self._disabled_response("nc_get_packet_status")
        return await _call_onebot_api("nc_get_packet_status", {})

    async def click_inline_keyboard_button(
        self,
        group_id: int,
        bot_appid: int,
        msg_seq: int,
        button_id: str,
    ) -> dict[str, Any]:
        """点击内联键盘按钮。

        对应 NapCat 扩展 API: ``click_inline_keyboard_button``。

        Args:
            group_id: 群号。
            bot_appid: 机器人 AppID。
            msg_seq: 消息序号。
            button_id: 按钮 ID。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("click_inline_keyboard_button"):
            return self._disabled_response("click_inline_keyboard_button")
        params: dict[str, Any] = {
            "group_id": group_id,
            "bot_appid": bot_appid,
            "msg_seq": msg_seq,
            "button_id": button_id,
        }
        return await _call_onebot_api("click_inline_keyboard_button", params)

    async def get_mini_app_ark(
        self,
        type: str,
        title: str,
        desc: str,
        pic_url: str,
        jump_url: str,
    ) -> dict[str, Any]:
        """获取小程序卡片。

        对应 NapCat 扩展 API: ``get_mini_app_ark``。

        Args:
            type: 卡片类型。
            title: 卡片标题。
            desc: 卡片描述。
            pic_url: 卡片图片 URL。
            jump_url: 跳转 URL。

        Returns:
            适配器返回的响应字典，包含 Ark 卡片数据。
        """
        if not self._is_api_enabled("get_mini_app_ark"):
            return self._disabled_response("get_mini_app_ark")
        params: dict[str, Any] = {
            "type": type,
            "title": title,
            "desc": desc,
            "pic_url": pic_url,
            "jump_url": jump_url,
        }
        return await _call_onebot_api("get_mini_app_ark", params)

    async def translate_en2zh(self, words: list[str]) -> dict[str, Any]:
        """英译中。

        对应 NapCat 扩展 API: ``translate_en2zh``。

        Args:
            words: 待翻译的英文单词列表。

        Returns:
            适配器返回的响应字典，包含翻译结果。
        """
        if not self._is_api_enabled("translate_en2zh"):
            return self._disabled_response("translate_en2zh")
        params: dict[str, Any] = {"words": words}
        return await _call_onebot_api("translate_en2zh", params)

    async def create_collection(self) -> dict[str, Any]:
        """创建收藏。

        对应 NapCat 扩展 API: ``create_collection``。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("create_collection"):
            return self._disabled_response("create_collection")
        return await _call_onebot_api("create_collection", {})

    async def get_collection_list(self) -> dict[str, Any]:
        """获取收藏列表。

        对应 NapCat 扩展 API: ``get_collection_list``。

        Returns:
            适配器返回的响应字典，包含收藏列表。
        """
        if not self._is_api_enabled("get_collection_list"):
            return self._disabled_response("get_collection_list")
        return await _call_onebot_api("get_collection_list", {})

    async def send_packet(
        self,
        cmd: str,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """发送原始SSO包。

        对应 NapCat 扩展 API: ``send_packet``。

        Args:
            cmd: SSO 命令名。
            data: SSO 数据，默认为 None。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("send_packet"):
            return self._disabled_response("send_packet")
        params: dict[str, Any] = {"cmd": cmd}
        if data:
            params["data"] = data
        return await _call_onebot_api("send_packet", params)