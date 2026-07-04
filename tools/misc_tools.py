"""机型/其他扩展 API 的 Tool 组件。

包含 10 个机型/其他扩展 Tool，对应 NapCat 机型/其他扩展 API：
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

注意：tool_name 中的下划线与 action 名一致（如 _get_model_show），
Tool 不检查配置开关，配置开关由 Service 层统一检查。
"""

from __future__ import annotations

from typing import Annotated, Any

from src.app.plugin_system.base import BaseTool

from . import _call_onebot_api

__all__ = [
    "GetModelShowTool",
    "SetModelShowTool",
    "BotExitTool",
    "NcGetPacketStatusTool",
    "ClickInlineKeyboardButtonTool",
    "GetMiniAppArkTool",
    "TranslateEn2zhTool",
    "CreateCollectionTool",
    "GetCollectionListTool",
    "SendPacketTool",
]


class GetModelShowTool(BaseTool):
    """获取机型展示的 Tool。

    对应 NapCat API: ``_get_model_show``。
    获取指定机型型号的展示信息。
    """

    tool_name = "_get_model_show"
    tool_description = "获取指定机型型号的展示信息"

    async def execute(
        self,
        model: Annotated[str, "机型型号"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取机型展示。"""
        params: dict[str, Any] = {"model": model}
        result = await _call_onebot_api("_get_model_show", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取机型展示失败: {result.get('msg', '未知错误')}"


class SetModelShowTool(BaseTool):
    """设置机型展示的 Tool。

    对应 NapCat API: ``_set_model_show``。
    设置当前 Bot 的机型展示信息。
    """

    tool_name = "_set_model_show"
    tool_description = "设置当前Bot的机型展示信息"

    async def execute(
        self,
        model: Annotated[str, "机型型号"],
        show: Annotated[str, "展示内容"],
    ) -> tuple[bool, str]:
        """执行设置机型展示。"""
        params: dict[str, Any] = {
            "model": model,
            "show": show,
        }
        result = await _call_onebot_api("_set_model_show", params)
        if result.get("status") == "ok":
            return True, f"机型展示已设置为 {model}: {show}"
        return False, f"设置机型展示失败: {result.get('msg', '未知错误')}"


class BotExitTool(BaseTool):
    """退出机器人的 Tool。

    对应 NapCat API: ``bot_exit``。
    退出当前 Bot 实例。请谨慎使用。
    """

    tool_name = "bot_exit"
    tool_description = "退出当前Bot实例（请谨慎使用）"

    async def execute(
        self,
    ) -> tuple[bool, str]:
        """执行退出机器人。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("bot_exit", params)
        if result.get("status") == "ok":
            return True, "Bot 已退出"
        return False, f"Bot退出失败: {result.get('msg', '未知错误')}"


class NcGetPacketStatusTool(BaseTool):
    """获取packet状态的 Tool。

    对应 NapCat API: ``nc_get_packet_status``。
    获取协议端的 packet 处理状态。
    """

    tool_name = "nc_get_packet_status"
    tool_description = "获取协议端的packet处理状态"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取packet状态。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("nc_get_packet_status", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取packet状态失败: {result.get('msg', '未知错误')}"


class ClickInlineKeyboardButtonTool(BaseTool):
    """点击内联键盘按钮的 Tool。

    对应 NapCat API: ``click_inline_keyboard_button``。
    点击指定群中的内联键盘按钮。
    """

    tool_name = "click_inline_keyboard_button"
    tool_description = "点击指定群中的内联键盘按钮"

    async def execute(
        self,
        group_id: Annotated[int, "目标群号"],
        bot_appid: Annotated[int, "机器人AppID"],
        msg_seq: Annotated[int, "消息序号"],
        button_id: Annotated[str, "按钮ID"],
    ) -> tuple[bool, str]:
        """执行点击内联键盘按钮。"""
        params: dict[str, Any] = {
            "group_id": group_id,
            "bot_appid": bot_appid,
            "msg_seq": msg_seq,
            "button_id": button_id,
        }
        result = await _call_onebot_api("click_inline_keyboard_button", params)
        if result.get("status") == "ok":
            return True, f"已点击按钮 {button_id}"
        return False, f"点击内联键盘按钮失败: {result.get('msg', '未知错误')}"


class GetMiniAppArkTool(BaseTool):
    """获取小程序卡片的 Tool。

    对应 NapCat API: ``get_mini_app_ark``。
    生成小程序 Ark 卡片数据。
    """

    tool_name = "get_mini_app_ark"
    tool_description = "生成小程序Ark卡片数据"

    async def execute(
        self,
        type: Annotated[str, "卡片类型"],
        title: Annotated[str, "卡片标题"],
        desc: Annotated[str, "卡片描述"],
        pic_url: Annotated[str, "卡片图片URL"],
        jump_url: Annotated[str, "跳转URL"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取小程序卡片。"""
        params: dict[str, Any] = {
            "type": type,
            "title": title,
            "desc": desc,
            "pic_url": pic_url,
            "jump_url": jump_url,
        }
        result = await _call_onebot_api("get_mini_app_ark", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"获取小程序卡片失败: {result.get('msg', '未知错误')}"


class TranslateEn2zhTool(BaseTool):
    """英译中的 Tool。

    对应 NapCat API: ``translate_en2zh``。
    将英文单词列表翻译为中文。
    """

    tool_name = "translate_en2zh"
    tool_description = "将英文单词列表翻译为中文"

    async def execute(
        self,
        words: Annotated[list[str], "待翻译的英文单词列表"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行英译中。"""
        params: dict[str, Any] = {"words": words}
        result = await _call_onebot_api("translate_en2zh", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"英译中失败: {result.get('msg', '未知错误')}"


class CreateCollectionTool(BaseTool):
    """创建收藏的 Tool。

    对应 NapCat API: ``create_collection``。
    创建一条收藏内容。
    """

    tool_name = "create_collection"
    tool_description = "创建一条收藏内容"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行创建收藏。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("create_collection", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"创建收藏失败: {result.get('msg', '未知错误')}"


class GetCollectionListTool(BaseTool):
    """获取收藏列表的 Tool。

    对应 NapCat API: ``get_collection_list``。
    获取当前 Bot 的收藏列表。
    """

    tool_name = "get_collection_list"
    tool_description = "获取当前Bot的收藏列表"

    async def execute(
        self,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行获取收藏列表。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_collection_list", params)
        if result.get("status") == "ok":
            data = result.get("data", [])
            return True, data
        return False, f"获取收藏列表失败: {result.get('msg', '未知错误')}"


class SendPacketTool(BaseTool):
    """发送原始SSO包的 Tool。

    对应 NapCat API: ``send_packet``。
    发送原始 SSO 数据包。高级功能，请谨慎使用。
    """

    tool_name = "send_packet"
    tool_description = "发送原始SSO数据包（高级功能，请谨慎使用）"

    async def execute(
        self,
        cmd: Annotated[str, "SSO命令名"],
        data: Annotated[dict[str, Any] | None, "SSO数据（可选）"] = None,
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行发送原始SSO包。"""
        params: dict[str, Any] = {"cmd": cmd}
        if data:
            params["data"] = data
        result = await _call_onebot_api("send_packet", params)
        if result.get("status") == "ok":
            data_resp = result.get("data", {})
            return True, data_resp
        return False, f"发送SSO包失败: {result.get('msg', '未知错误')}"