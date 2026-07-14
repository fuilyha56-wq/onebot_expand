"""机型/其他扩展服务。

封装 NapCat 机型/其他扩展 API，提供机型展示、Bot 退出、
packet 状态、内联键盘、小程序卡片、翻译、收藏、SSO 包、快速操作、分词等功能。

API 列表 (12):
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
    - handle_quick_operation: go-cqhttp 快速操作
    - get_word_slices: go-cqhttp 分词
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["MiscService"]


class MiscService(BaseService):
    """机型/其他扩展服务。

    封装全部机型/其他扩展 API 调用，提供统一调用入口，始终可用（不受 Tool 开关影响）。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "misc_service"
    service_description: str = "机型/其他扩展服务"
    version: str = "1.0.0"

    async def get_model_show(self, model: str) -> dict[str, Any]:
        """获取机型展示。

        对应 NapCat 扩展 API: ``_get_model_show``。

        Args:
            model: 机型型号。

        Returns:
            适配器返回的响应字典，包含机型展示信息。
        """
        params: dict[str, Any] = {"model": model}
        return await _call_onebot_api("_get_model_show", params)

    async def set_model_show(self, model: str, show: str) -> dict[str, Any]:
        """设置机型展示。

        对应 NapCat 扩展 API: ``_set_model_show``。

        Args:
            model: 机型型号。
            show: 展示内容。

        Returns:
            适配器返回的响应字典。
        """
        params: dict[str, Any] = {
            "model": model,
            "show": show,
        }
        return await _call_onebot_api("_set_model_show", params)

    async def bot_exit(self) -> dict[str, Any]:
        """退出机器人。

        对应 NapCat 扩展 API: ``bot_exit``。

        Returns:
            适配器返回的响应字典。
        """
        return await _call_onebot_api("bot_exit", {})

    async def nc_get_packet_status(self) -> dict[str, Any]:
        """获取packet状态。

        对应 NapCat 扩展 API: ``nc_get_packet_status``。

        Returns:
            适配器返回的响应字典，包含 packet 处理状态。
        """
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
        params: dict[str, Any] = {"words": words}
        return await _call_onebot_api("translate_en2zh", params)

    async def create_collection(self) -> dict[str, Any]:
        """创建收藏。

        对应 NapCat 扩展 API: ``create_collection``。

        Returns:
            适配器返回的响应字典。
        """
        return await _call_onebot_api("create_collection", {})

    async def get_collection_list(self) -> dict[str, Any]:
        """获取收藏列表。

        对应 NapCat 扩展 API: ``get_collection_list``。

        Returns:
            适配器返回的响应字典，包含收藏列表。
        """
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
        params: dict[str, Any] = {"cmd": cmd}
        if data:
            params["data"] = data
        return await _call_onebot_api("send_packet", params)
    async def handle_quick_operation(
        self,
        context: dict[str, Any],
        operation: dict[str, Any],
    ) -> dict[str, Any]:
        """go-cqhttp 快速操作（NapCat 与 SnowLuma 均支持）。

        对应 go-cqhttp 兼容 API: ``handle_quick_operation``（别名 ``.handle_quick_operation``）。

        Args:
            context: 事件上下文。
            operation: 快速操作内容。

        Returns:
            适配器返回的响应字典。
        """
        return await _call_onebot_api(
            "handle_quick_operation",
            {"context": context, "operation": operation},
        )

    async def get_word_slices(self, content: str) -> dict[str, Any]:
        """go-cqhttp 分词（仅 NapCat 支持，SnowLuma 未实现）。

        对应 go-cqhttp 兼容 API: ``get_word_slices``（别名 ``.get_word_slices``）。

        Args:
            content: 待分词的文本内容。

        Returns:
            适配器返回的响应字典，包含切分后的词组列表。
        """
        return await _call_onebot_api("get_word_slices", {"content": content})

    async def GetConfig(
        self,
    ) -> dict[str, Any]:
        """获取协议端配置。

        对应 OneBot API: ``get_config``。
        """
        params: dict[str, Any] = {
        }
        return await _call_onebot_api("get_config", params)

    async def SetConfig(
        self,
        config: dict,
    ) -> dict[str, Any]:
        """设置协议端配置。

        对应 OneBot API: ``set_config``。
        """
        params: dict[str, Any] = {
            "config": config,
        }
        return await _call_onebot_api("set_config", params)

    async def GetEvent(
        self,
    ) -> dict[str, Any]:
        """获取事件。

        对应 OneBot API: ``get_event``。
        """
        params: dict[str, Any] = {
        }
        return await _call_onebot_api("get_event", params)

    async def LlonebotDebug(
        self,
        api_class: str,
        method: str,
        args: list,
    ) -> dict[str, Any]:
        """调试接口。

        对应 OneBot API: ``llonebot_debug``。
        """
        params: dict[str, Any] = {
            "api_class": api_class,
            "method": method,
            "args": args,
        }
        return await _call_onebot_api("llonebot_debug", params)

    async def ScanQRCode(
        self,
        qrcode: str,
    ) -> dict[str, Any]:
        """扫码登录。

        对应 OneBot API: ``scan_qrcode``。
        """
        params: dict[str, Any] = {
            "qrcode": qrcode,
        }
        return await _call_onebot_api("scan_qrcode", params)

    async def GetGuildList(
        self,
    ) -> dict[str, Any]:
        """获取频道列表。

        对应 OneBot API: ``get_guild_list``。
        """
        params: dict[str, Any] = {
        }
        return await _call_onebot_api("get_guild_list", params)

