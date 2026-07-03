"""QQ空间服务。

封装 NapCat QQ 空间 API，提供说说列表查询、好友动态、
发表说说、删除说说、点赞、取消点赞、评论等功能。

API 列表 (7):
    - get_qzone_msg_list: 获取QQ空间说说列表
    - get_qzone_feeds: 获取QQ空间好友动态
    - send_qzone_msg: 发表说说
    - delete_qzone_msg: 删除说说
    - like_qzone: 给说说点赞
    - unlike_qzone: 取消点赞
    - comment_qzone: 评论说说
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..tools import _call_onebot_api

__all__ = ["QzoneService"]


class QzoneService(BaseService):
    """QQ空间服务。

    封装全部 QQ 空间 API 调用，提供配置开关检查和统一调用入口。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "qzone_service"
    service_description: str = "QQ空间服务"
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

    async def get_qzone_msg_list(
        self,
        pos: int = 0,
        num: int = 10,
    ) -> dict[str, Any]:
        """获取QQ空间说说列表。

        对应 NapCat 扩展 API: ``get_qzone_msg_list``。

        Args:
            pos: 起始位置，默认为 0。
            num: 获取数量，默认为 10。

        Returns:
            适配器返回的响应字典，包含说说列表。
        """
        if not self._is_api_enabled("get_qzone_msg_list"):
            return self._disabled_response("get_qzone_msg_list")
        params: dict[str, Any] = {
            "pos": pos,
            "num": num,
        }
        return await _call_onebot_api("get_qzone_msg_list", params)

    async def get_qzone_feeds(
        self,
        page_num: int = 0,
        count: int = 10,
    ) -> dict[str, Any]:
        """获取QQ空间好友动态。

        对应 NapCat 扩展 API: ``get_qzone_feeds``。

        Args:
            page_num: 页码，默认为 0。
            count: 每页数量，默认为 10。

        Returns:
            适配器返回的响应字典，包含好友动态列表。
        """
        if not self._is_api_enabled("get_qzone_feeds"):
            return self._disabled_response("get_qzone_feeds")
        params: dict[str, Any] = {
            "page_num": page_num,
            "count": count,
        }
        return await _call_onebot_api("get_qzone_feeds", params)

    async def send_qzone_msg(self, content: str) -> dict[str, Any]:
        """发表说说。

        对应 NapCat 扩展 API: ``send_qzone_msg``。

        Args:
            content: 说说内容。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("send_qzone_msg"):
            return self._disabled_response("send_qzone_msg")
        params: dict[str, Any] = {"content": content}
        return await _call_onebot_api("send_qzone_msg", params)

    async def delete_qzone_msg(self, tid: str) -> dict[str, Any]:
        """删除说说。

        对应 NapCat 扩展 API: ``delete_qzone_msg``。

        Args:
            tid: 说说 ID。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("delete_qzone_msg"):
            return self._disabled_response("delete_qzone_msg")
        params: dict[str, Any] = {"tid": tid}
        return await _call_onebot_api("delete_qzone_msg", params)

    async def like_qzone(
        self,
        tid: str,
        target_uin: int | None = None,
    ) -> dict[str, Any]:
        """给说说点赞。

        对应 NapCat 扩展 API: ``like_qzone``。

        Args:
            tid: 说说 ID。
            target_uin: 说说发布者 QQ 号，默认为 None。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("like_qzone"):
            return self._disabled_response("like_qzone")
        params: dict[str, Any] = {"tid": tid}
        if target_uin is not None:
            params["target_uin"] = target_uin
        return await _call_onebot_api("like_qzone", params)

    async def unlike_qzone(
        self,
        tid: str,
        target_uin: int | None = None,
    ) -> dict[str, Any]:
        """取消点赞。

        对应 NapCat 扩展 API: ``unlike_qzone``。

        Args:
            tid: 说说 ID。
            target_uin: 说说发布者 QQ 号，默认为 None。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("unlike_qzone"):
            return self._disabled_response("unlike_qzone")
        params: dict[str, Any] = {"tid": tid}
        if target_uin is not None:
            params["target_uin"] = target_uin
        return await _call_onebot_api("unlike_qzone", params)

    async def comment_qzone(
        self,
        tid: str,
        content: str,
        target_uin: int | None = None,
    ) -> dict[str, Any]:
        """评论说说。

        对应 NapCat 扩展 API: ``comment_qzone``。

        Args:
            tid: 说说 ID。
            content: 评论内容。
            target_uin: 说说发布者 QQ 号，默认为 None。

        Returns:
            适配器返回的响应字典。
        """
        if not self._is_api_enabled("comment_qzone"):
            return self._disabled_response("comment_qzone")
        params: dict[str, Any] = {
            "tid": tid,
            "content": content,
        }
        if target_uin is not None:
            params["target_uin"] = target_uin
        return await _call_onebot_api("comment_qzone", params)