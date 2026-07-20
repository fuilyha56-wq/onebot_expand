"""机型/其他扩展 API 的 Tool 组件。

包含 12 个机型/其他扩展 Tool，对应 NapCat 机型/其他扩展 API：
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
    "HandleQuickOperationTool",
    "GetWordSlicesTool",
"GetConfigTool",
    "SetConfigTool",
    "GetEventTool",
    "LlonebotDebugTool",
    "ScanQRCodeTool",
    "GetGuildListTool",
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

class HandleQuickOperationTool(BaseTool):
    """go-cqhttp 快速操作的 Tool。

    对应 go-cqhttp 兼容 API: ``handle_quick_operation``（别名 ``.handle_quick_operation``）。
    """

    tool_name = "handle_quick_operation"
    tool_description = "go-cqhttp 快速操作（NapCat 与 SnowLuma 均支持）"

    async def execute(
        self,
        context: Annotated[dict[str, Any], "事件上下文"],
        operation: Annotated[dict[str, Any], "快速操作内容"],
    ) -> tuple[bool, str]:
        """执行快速操作。"""
        params: dict[str, Any] = {
            "context": context,
            "operation": operation,
        }
        result = await _call_onebot_api("handle_quick_operation", params)
        if result.get("status") == "ok":
            return True, "快速操作已执行"
        return False, f"快速操作失败: {result.get('msg', '未知错误')}"


class GetWordSlicesTool(BaseTool):
    """go-cqhttp 分词的 Tool。

    对应 go-cqhttp 兼容 API: ``get_word_slices``（别名 ``.get_word_slices``）。
    对文本内容进行分词，返回切分后的词组列表。仅 NapCat 支持，SnowLuma 未实现。
    """

    tool_name = "get_word_slices"
    tool_description = "对文本内容进行分词（go-cqhttp 兼容，仅 NapCat 支持）"

    async def execute(
        self,
        content: Annotated[str, "待分词的文本内容"],
    ) -> tuple[bool, str | dict[str, Any]]:
        """执行文本分词。"""
        params: dict[str, Any] = {"content": content}
        result = await _call_onebot_api("get_word_slices", params)
        if result.get("status") == "ok":
            data = result.get("data", {})
            return True, data
        return False, f"分词失败: {result.get('msg', '未知错误')}"


class GetConfigTool(BaseTool):
    """获取协议端配置的 Tool。

    对应 API: ``get_config``。
    """

    tool_name = "get_config"
    tool_description = "获取协议端配置"

    async def execute(
        self,
    ) -> tuple[bool, str]:
        """执行获取协议端配置。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_config", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"获取协议端配置失败: {result.get('msg', '未知错误')}"



class SetConfigTool(BaseTool):
    """设置协议端配置的 Tool。

    对应 API: ``set_config``。
    """

    tool_name = "set_config"
    tool_description = "设置协议端配置"

    async def execute(
        self,
        config: Annotated[dict, "配置字典"],
    ) -> tuple[bool, str]:
        """执行设置协议端配置。"""
        params: dict[str, Any] = {
            "config": config,
        }
        result = await _call_onebot_api("set_config", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"设置协议端配置失败: {result.get('msg', '未知错误')}"



class GetEventTool(BaseTool):
    """获取事件的 Tool。

    对应 API: ``get_event``。
    """

    tool_name = "get_event"
    tool_description = "获取事件"

    async def execute(
        self,
    ) -> tuple[bool, str]:
        """执行获取事件。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_event", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"获取事件失败: {result.get('msg', '未知错误')}"



class LlonebotDebugTool(BaseTool):
    """调试接口的 Tool。

    对应 API: ``llonebot_debug``。
    """

    tool_name = "llonebot_debug"
    tool_description = "调试接口"

    async def execute(
        self,
        api_class: Annotated[str, "API类名"],
        method: Annotated[str, "方法名"],
        args: Annotated[list, "参数列表"],
    ) -> tuple[bool, str]:
        """执行调试接口。"""
        params: dict[str, Any] = {
            "api_class": api_class,
            "method": method,
            "args": args,
        }
        result = await _call_onebot_api("llonebot_debug", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"调试接口失败: {result.get('msg', '未知错误')}"



class ScanQRCodeTool(BaseTool):
    """扫码登录的 Tool。

    对应 API: ``scan_qrcode``。
    """

    tool_name = "scan_qrcode"
    tool_description = "扫码登录"

    async def execute(
        self,
        qrcode: Annotated[str, "二维码内容"],
    ) -> tuple[bool, str]:
        """执行扫码登录。"""
        params: dict[str, Any] = {
            "qrcode": qrcode,
        }
        result = await _call_onebot_api("scan_qrcode", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"扫码登录失败: {result.get('msg', '未知错误')}"



class GetGuildListTool(BaseTool):
    """获取频道列表的 Tool。

    对应 API: ``get_guild_list``。
    """

    tool_name = "get_guild_list"
    tool_description = "获取频道列表"

    async def execute(
        self,
    ) -> tuple[bool, str]:
        """执行获取频道列表。"""
        params: dict[str, Any] = {}
        result = await _call_onebot_api("get_guild_list", params)
        if result.get("status") == "ok":
            return True, str(result.get("data", ""))
        return False, f"获取频道列表失败: {result.get('msg', '未知错误')}"


