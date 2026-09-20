"""OneBot 消息 ID 类型别名。

原样透传铁律（SKILL.md §11.1）：消息 ID 等参数值不做任何清洗、
类型转换或规范化，调用方给什么就透传什么。历史上本模块的
``normalize_message_id`` / ``normalize_message_ids`` / ``build_text_message``
参数改写辅助函数已按透传铁律移除，仅保留类型别名供签名标注使用。
"""

from __future__ import annotations

from typing import TypeAlias

MessageId: TypeAlias = int | str
