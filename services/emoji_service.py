"""QQNT 表情表查询服务。

提供表情表查询功能，支持按 ID 查找、按名称模糊查找、获取全部表情列表等。
直接调用 emoji_tables 模块的函数，并检查配置中的表情开关。

表情双表说明:
    - send 表: 通过消息段 ``face`` 发送的原生 QQ 表情集合
    - reaction 表: 通过 ``set_msg_emoji_like`` API 添加的表情回应集合
"""

from __future__ import annotations

from typing import Any

from src.app.plugin_system.base import BaseService

from ..emoji_tables import (
    EmojiEntry,
    get_all_emoji_ids,
    get_emoji_by_id,
    get_emoji_by_name,
)

__all__ = ["EmojiService"]


class EmojiService(BaseService):
    """QQNT 表情表查询服务。

    封装 emoji_tables 模块的查询功能，提供配置开关检查。
    支持按 ID 查找、按名称模糊查找、获取全部表情列表、检查表情是否启用等。
    Service 不是单例，每次 get_service() 都创建新实例，不应依赖实例级缓存。
    """

    service_name: str = "emoji_service"
    service_description: str = "QQNT 表情表查询服务"
    version: str = "1.0.0"

    def _is_emoji_function_enabled(self, table_type: str) -> bool:
        """检查表情功能是否启用。

        根据 table_type 检查对应的配置开关：
        - "send" 表: 检查 emoji.enable_send_emoji
        - "reaction" 表: 检查 emoji.enable_reaction_emoji

        Args:
            table_type: 表类型，"send" 或 "reaction"。

        Returns:
            True 表示功能启用，False 表示禁用。无配置时默认启用。
        """
        config = self.plugin.config
        if config is None:
            return True
        emoji_cfg = getattr(config, "emoji", None)
        if emoji_cfg is None:
            return True
        if table_type == "send":
            return getattr(emoji_cfg, "enable_send_emoji", True)
        elif table_type == "reaction":
            return getattr(emoji_cfg, "enable_reaction_emoji", True)
        return True

    def _get_enabled_ids(self, table_type: str) -> list[int]:
        """获取启用的表情 ID 白名单。

        根据 table_type 获取对应的配置白名单：
        - "send" 表: emoji.send_emoji_enabled_ids
        - "reaction" 表: emoji.reaction_emoji_enabled_ids

        空列表表示全部启用。

        Args:
            table_type: 表类型，"send" 或 "reaction"。

        Returns:
            启用的表情 ID 列表，空列表表示全部启用。
        """
        config = self.plugin.config
        if config is None:
            return []
        emoji_cfg = getattr(config, "emoji", None)
        if emoji_cfg is None:
            return []
        if table_type == "send":
            return list(getattr(emoji_cfg, "send_emoji_enabled_ids", []))
        elif table_type == "reaction":
            return list(getattr(emoji_cfg, "reaction_emoji_enabled_ids", []))
        return []

    def _is_emoji_id_enabled(self, emoji_id: int, table_type: str) -> bool:
        """检查指定表情 ID 是否在白名单中。

        需同时满足：
        1. 对应的表情功能已启用
        2. 表情 ID 在白名单中（空列表表示全部启用）

        Args:
            emoji_id: 表情 ID。
            table_type: 表类型，"send" 或 "reaction"。

        Returns:
            True 表示启用，False 表示禁用。
        """
        if not self._is_emoji_function_enabled(table_type):
            return False
        enabled_ids = self._get_enabled_ids(table_type)
        if not enabled_ids:
            return True
        return emoji_id in enabled_ids

    @staticmethod
    def _entry_to_dict(entry: EmojiEntry) -> dict[str, Any]:
        """将 EmojiEntry 转换为字典。

        Args:
            entry: EmojiEntry 实例。

        Returns:
            包含 emoji_id、describe、qzone_code、aliases 的字典。
        """
        return {
            "emoji_id": entry.emoji_id,
            "describe": entry.describe,
            "qzone_code": entry.qzone_code,
            "aliases": list(entry.aliases),
        }

    async def get_emoji_by_id(
        self,
        emoji_id: int,
        table_type: str = "send",
    ) -> dict[str, Any] | None:
        """按 emoji_id 查找表情条目。

        Args:
            emoji_id: 表情 ID。发送表中为 face_id，回应表中为 emoji_id。
            table_type: 表类型，"send"（发送表情表）或 "reaction"（回应表情表），
                默认为 "send"。

        Returns:
            匹配的表情信息字典，包含 emoji_id、describe、qzone_code、aliases。
            未找到时返回 None。

        Raises:
            ValueError: 当 table_type 不是合法值时。
        """
        entry = get_emoji_by_id(emoji_id, table_type=table_type)
        if entry is None:
            return None
        return self._entry_to_dict(entry)

    async def get_emoji_by_name(
        self,
        name: str,
        table_type: str = "send",
    ) -> dict[str, Any] | None:
        """按名称/关键词模糊查找表情条目。

        查找策略（按优先级）:
            1. 精确匹配: 去掉 ``/`` 前缀后与 describe 和 aliases 精确匹配
               （大小写不敏感）。
            2. 包含匹配: describe（去掉 ``/`` 前缀）包含关键词的条目。

        Args:
            name: 搜索关键词（如 "赞"、"点赞"、"/赞"、"狗头"）。
                会自动去掉 ``/`` 前缀。
            table_type: 表类型，"send" 或 "reaction"，默认为 "send"。

        Returns:
            匹配的表情信息字典。未找到时返回 None。

        Raises:
            ValueError: 当 table_type 不是合法值时。
        """
        entry = get_emoji_by_name(name, table_type=table_type)
        if entry is None:
            return None
        return self._entry_to_dict(entry)

    async def get_all_emojis(self, table_type: str = "send") -> list[dict[str, Any]]:
        """获取指定表的全部表情列表。

        Args:
            table_type: 表类型，"send" 或 "reaction"，默认为 "send"。

        Returns:
            全部表情信息字典列表，按表中的插入顺序排列。

        Raises:
            ValueError: 当 table_type 不是合法值时。
        """
        all_ids = get_all_emoji_ids(table_type=table_type)
        result: list[dict[str, Any]] = []
        for eid in all_ids:
            entry = get_emoji_by_id(eid, table_type=table_type)
            if entry is not None:
                result.append(self._entry_to_dict(entry))
        return result

    async def get_all_emoji_ids(self, table_type: str = "send") -> list[int]:
        """获取指定表的全部表情 ID 列表。

        Args:
            table_type: 表类型，"send" 或 "reaction"，默认为 "send"。

        Returns:
            表情 ID 列表，按表中的 key 顺序排列。

        Raises:
            ValueError: 当 table_type 不是合法值时。
        """
        return get_all_emoji_ids(table_type=table_type)

    async def is_emoji_enabled(
        self,
        emoji_id: int,
        table_type: str = "send",
    ) -> bool:
        """检查指定表情 ID 是否启用。

        需同时满足：
        1. 表情功能在配置中已启用
        2. 表情 ID 在白名单中（空列表表示全部启用）
        3. 表情 ID 在表情表中存在

        Args:
            emoji_id: 表情 ID。
            table_type: 表类型，"send" 或 "reaction"，默认为 "send"。

        Returns:
            True 表示表情已启用且存在，False 表示禁用或不存在。
        """
        # 先检查表情是否在表中存在
        entry = get_emoji_by_id(emoji_id, table_type=table_type)
        if entry is None:
            return False
        # 再检查配置开关
        return self._is_emoji_id_enabled(emoji_id, table_type)

    async def get_enabled_emojis(
        self, table_type: str = "send"
    ) -> list[dict[str, Any]]:
        """获取已启用的表情列表。

        根据配置开关和白名单过滤表情列表。

        Args:
            table_type: 表类型，"send" 或 "reaction"，默认为 "send"。

        Returns:
            已启用的表情信息字典列表。

        Raises:
            ValueError: 当 table_type 不是合法值时。
        """
        # 如果整体功能未启用，返回空列表
        if not self._is_emoji_function_enabled(table_type):
            return []

        all_ids = get_all_emoji_ids(table_type=table_type)
        enabled_ids = self._get_enabled_ids(table_type)

        # 空白名单表示全部启用
        if not enabled_ids:
            target_ids = all_ids
        else:
            # 取白名单与实际存在的 ID 的交集，保持表中顺序
            enabled_set = set(enabled_ids)
            target_ids = [eid for eid in all_ids if eid in enabled_set]

        result: list[dict[str, Any]] = []
        for eid in target_ids:
            entry = get_emoji_by_id(eid, table_type=table_type)
            if entry is not None:
                result.append(self._entry_to_dict(entry))
        return result
