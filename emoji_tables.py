"""QQNT 表情双表模块。

内置完整的 QQNT 发送表情表（face 消息段）和表情回应表（set_msg_emoji_like），
提供双向查找能力：按 ID 查描述、按名称/关键词模糊查 ID。

数据来源: Koishi QQNT 表情数据。

表情双表设计说明:
    - 发送表情表 (SEND_EMOJI_TABLE): 通过消息段 ``face`` 发送的原生 QQ 表情集合，
      key 为 face_id。
    - 表情回应表 (REACTION_EMOJI_TABLE): 通过 ``set_msg_emoji_like`` API 对消息
      添加的表情回应集合。在 QQNT 上，回应使用的 ID 体系与发送 face 的 ID 体系相同，
      但设计为独立表，默认与发送表相同，可配置覆盖。
"""

from __future__ import annotations

from dataclasses import dataclass, field


__all__ = [
    "EmojiEntry",
    "SEND_EMOJI_TABLE",
    "REACTION_EMOJI_TABLE",
    "get_emoji_by_id",
    "get_emoji_by_name",
    "get_all_emoji_ids",
    "get_all_emoji_names",
]


# ---------------------------------------------------------------------------
# 数据模型
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class EmojiEntry:
    """表情表条目数据模型。

    Attributes:
        emoji_id: 表情 ID。发送表中为 face_id，回应表中为 emoji_id。
        describe: 表情描述，带 ``/`` 前缀（如 ``"/惊讶"``）。
        qzone_code: QQ 空间代码（如 ``"114"``），无对应代码时为空字符串。
        aliases: 别名元组，用于模糊匹配扩展（如 ``("点赞", "大拇指")``），
            无别名时为空元组。
    """

    emoji_id: int
    describe: str
    qzone_code: str = ""
    aliases: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# 发送表情表（face 消息段用 ID 表）
# ---------------------------------------------------------------------------

# 完整 QQNT 发送表情表，共 130+ 条。
# 数据格式: emoji_id: describe(qzone_code)
# describe 带 "/" 前缀；qzone_code 为空表示无对应 QQ 空间代码。
SEND_EMOJI_TABLE: dict[int, EmojiEntry] = {
    0: EmojiEntry(0, "/惊讶", "114"),
    1: EmojiEntry(1, "/撇嘴", "101"),
    2: EmojiEntry(2, "/色", "102"),
    3: EmojiEntry(3, "/发呆", "103"),
    4: EmojiEntry(4, "/得意", "104"),
    5: EmojiEntry(5, "/流泪", "105"),
    6: EmojiEntry(6, "/害羞", "106"),
    7: EmojiEntry(7, "/闭嘴", "107"),
    8: EmojiEntry(8, "/睡", "108"),
    9: EmojiEntry(9, "/大哭", "109"),
    10: EmojiEntry(10, "/尴尬", "110"),
    11: EmojiEntry(11, "/发怒", "111", ("生气",)),
    12: EmojiEntry(12, "/调皮", "112"),
    13: EmojiEntry(13, "/呲牙", "113"),
    14: EmojiEntry(14, "/微笑", "100"),
    15: EmojiEntry(15, "/难过", "115"),
    16: EmojiEntry(16, "/酷", "116"),
    18: EmojiEntry(18, "/抓狂", "118"),
    19: EmojiEntry(19, "/吐", "119"),
    20: EmojiEntry(20, "/偷笑", "120"),
    21: EmojiEntry(21, "/可爱", "121"),
    22: EmojiEntry(22, "/白眼", "122"),
    23: EmojiEntry(23, "/傲慢", "123"),
    24: EmojiEntry(24, "/饥饿", "124"),
    25: EmojiEntry(25, "/困", "125"),
    26: EmojiEntry(26, "/惊恐", "126"),
    27: EmojiEntry(27, "/流汗", "127"),
    28: EmojiEntry(28, "/憨笑", "128"),
    29: EmojiEntry(29, "/悠闲", "129"),
    30: EmojiEntry(30, "/奋斗", "130"),
    31: EmojiEntry(31, "/咒骂", "131"),
    32: EmojiEntry(32, "/疑问", "132"),
    33: EmojiEntry(33, "/嘘", "133"),
    34: EmojiEntry(34, "/晕", "134"),
    35: EmojiEntry(35, "/折磨", "135"),
    36: EmojiEntry(36, "/衰", "136"),
    37: EmojiEntry(37, "/骷髅", "137"),
    38: EmojiEntry(38, "/敲打", "138"),
    39: EmojiEntry(39, "/再见", "139"),
    41: EmojiEntry(41, "/发抖", "193"),
    42: EmojiEntry(42, "/爱情", "190"),
    43: EmojiEntry(43, "/跳跳", "192"),
    46: EmojiEntry(46, "/猪头", "162"),
    49: EmojiEntry(49, "/拥抱", "178"),
    53: EmojiEntry(53, "/蛋糕", "168"),
    55: EmojiEntry(55, "/炸弹", "170"),
    56: EmojiEntry(56, "/刀", "171"),
    59: EmojiEntry(59, "/便便", "174"),
    60: EmojiEntry(60, "/咖啡", "160"),
    63: EmojiEntry(63, "/玫瑰", "163"),
    64: EmojiEntry(64, "/凋谢", "164"),
    66: EmojiEntry(66, "/爱心", "166"),
    67: EmojiEntry(67, "/心碎", "167"),
    74: EmojiEntry(74, "/太阳", "176"),
    75: EmojiEntry(75, "/月亮", "175"),
    76: EmojiEntry(76, "/赞", "179", ("点赞", "大拇指")),
    77: EmojiEntry(77, "/踩", "180"),
    78: EmojiEntry(78, "/握手", "181"),
    79: EmojiEntry(79, "/胜利", "182"),
    85: EmojiEntry(85, "/飞吻", "191"),
    86: EmojiEntry(86, "/怄火", "194"),
    89: EmojiEntry(89, "/西瓜", "156"),
    96: EmojiEntry(96, "/冷汗", "117"),
    97: EmojiEntry(97, "/擦汗", "140"),
    98: EmojiEntry(98, "/抠鼻", "141"),
    99: EmojiEntry(99, "/鼓掌", "142"),
    100: EmojiEntry(100, "/糗大了", "143"),
    101: EmojiEntry(101, "/坏笑", "144"),
    102: EmojiEntry(102, "/左哼哼", "145"),
    103: EmojiEntry(103, "/右哼哼", "146"),
    104: EmojiEntry(104, "/哈欠", "147"),
    105: EmojiEntry(105, "/鄙视", "148"),
    106: EmojiEntry(106, "/委屈", "149"),
    107: EmojiEntry(107, "/快哭了", "150"),
    108: EmojiEntry(108, "/阴险", "151"),
    109: EmojiEntry(109, "/左亲亲", "152"),
    110: EmojiEntry(110, "/吓", "153"),
    111: EmojiEntry(111, "/可怜", "154"),
    112: EmojiEntry(112, "/菜刀", "155"),
    114: EmojiEntry(114, "/篮球", "157"),
    116: EmojiEntry(116, "/示爱", "158"),
    118: EmojiEntry(118, "/抱拳", "159"),
    119: EmojiEntry(119, "/勾引", "165"),
    120: EmojiEntry(120, "/拳头", "169"),
    121: EmojiEntry(121, "/差劲", "172"),
    123: EmojiEntry(123, "/NO", "173", ("不",)),
    124: EmojiEntry(124, "/OK", "177", ("好的",)),
    125: EmojiEntry(125, "/转圈", "184"),
    129: EmojiEntry(129, "/挥手", "185"),
    137: EmojiEntry(137, "/鞭炮", "186"),
    144: EmojiEntry(144, "/喝彩", "187"),
    146: EmojiEntry(146, "/爆筋", "188"),
    147: EmojiEntry(147, "/棒棒糖", "189"),
    169: EmojiEntry(169, "/手枪", "197"),
    171: EmojiEntry(171, "/茶", "198"),
    172: EmojiEntry(172, "/眨眼睛", "199"),
    173: EmojiEntry(173, "/泪奔", "200"),
    174: EmojiEntry(174, "/无奈", "201"),
    175: EmojiEntry(175, "/卖萌", "202"),
    176: EmojiEntry(176, "/小纠结", "203"),
    177: EmojiEntry(177, "/喷血", "204"),
    178: EmojiEntry(178, "/斜眼笑", "205"),
    179: EmojiEntry(179, "/doge", "206", ("狗头",)),
    181: EmojiEntry(181, "/戳一戳", "207"),
    182: EmojiEntry(182, "/笑哭", "208"),
    183: EmojiEntry(183, "/我最美", "209"),
    185: EmojiEntry(185, "/羊驼", "210"),
    187: EmojiEntry(187, "/幽灵", "211"),
    201: EmojiEntry(201, "/点赞", "212", ("赞",)),
    212: EmojiEntry(212, "/托腮", "213"),
    262: EmojiEntry(262, "/脑阔疼", "214"),
    263: EmojiEntry(263, "/沧桑", "215"),
    264: EmojiEntry(264, "/捂脸", "216"),
    265: EmojiEntry(265, "/辣眼睛", "217"),
    266: EmojiEntry(266, "/哦哟", "218"),
    267: EmojiEntry(267, "/头秃", "219"),
    268: EmojiEntry(268, "/问号脸", "220"),
    269: EmojiEntry(269, "/暗中观察", "221"),
    270: EmojiEntry(270, "/emm", "222"),
    271: EmojiEntry(271, "/吃瓜", "223"),
    272: EmojiEntry(272, "/呵呵哒", "224"),
    273: EmojiEntry(273, "/我酸了", "225"),
    277: EmojiEntry(277, "/滑稽狗头", "226"),
    281: EmojiEntry(281, "/翻白眼", "227"),
    282: EmojiEntry(282, "/敬礼", "228"),
    283: EmojiEntry(283, "/狂笑", "229"),
    284: EmojiEntry(284, "/面无表情", "230"),
    285: EmojiEntry(285, "/摸鱼", "231"),
    286: EmojiEntry(286, "/魔鬼笑", "232"),
    287: EmojiEntry(287, "/哦", "233"),
    289: EmojiEntry(289, "/睁眼", "234"),
    293: EmojiEntry(293, "/摸锦鲤", "235"),
    294: EmojiEntry(294, "/期待", "236"),
    295: EmojiEntry(295, "/拿到红包", "237"),
    297: EmojiEntry(297, "/拜谢", "238"),
    298: EmojiEntry(298, "/元宝", "239"),
    299: EmojiEntry(299, "/牛啊", "240"),
    300: EmojiEntry(300, "/胖三斤", "241"),
    302: EmojiEntry(302, "/左拜年", "242"),
    303: EmojiEntry(303, "/右拜年", "243"),
    305: EmojiEntry(305, "/右亲亲", "244"),
    306: EmojiEntry(306, "/牛气冲天", "245"),
    307: EmojiEntry(307, "/喵喵", "246"),
    311: EmojiEntry(311, "/打call", "247"),
    312: EmojiEntry(312, "/变形", "248"),
    314: EmojiEntry(314, "/仔细分析", "249"),
    317: EmojiEntry(317, "/菜汪", "250"),
    318: EmojiEntry(318, "/崇拜", "251"),
    319: EmojiEntry(319, "/比心", "252"),
    320: EmojiEntry(320, "/庆祝", "253"),
    323: EmojiEntry(323, "/嫌弃", "254"),
    324: EmojiEntry(324, "/吃糖", "255"),
    325: EmojiEntry(325, "/惊吓", "256"),
    326: EmojiEntry(326, "/生气", "257", ("发怒",)),
    332: EmojiEntry(332, "/举牌牌", "258"),
    333: EmojiEntry(333, "/烟花", "259"),
    334: EmojiEntry(334, "/虎虎生威", "260"),
    336: EmojiEntry(336, "/豹富", "261"),
    337: EmojiEntry(337, "/花朵脸", "262"),
    338: EmojiEntry(338, "/我想开了", "263"),
    339: EmojiEntry(339, "/舔屏", "264"),
    341: EmojiEntry(341, "/打招呼", "265"),
    342: EmojiEntry(342, "/酸Q", "266"),
    343: EmojiEntry(343, "/我方了", "267"),
    344: EmojiEntry(344, "/大怨种", "268"),
    345: EmojiEntry(345, "/红包多多", "269"),
    346: EmojiEntry(346, "/你真棒棒", "270"),
    347: EmojiEntry(347, "/大展宏兔", "271"),
    349: EmojiEntry(349, "/坚强", "272"),
    350: EmojiEntry(350, "/贴贴", "273"),
    351: EmojiEntry(351, "/敲敲", "274"),
    352: EmojiEntry(352, "/咦", "275"),
    353: EmojiEntry(353, "/拜托", "276"),
    354: EmojiEntry(354, "/尊嘟假嘟", "277"),
    355: EmojiEntry(355, "/耶", "278"),
    356: EmojiEntry(356, "/666", "279", ("牛牛牛",)),
    357: EmojiEntry(357, "/裂开", "280"),
    392: EmojiEntry(392, "/龙年快乐", "281"),
    393: EmojiEntry(393, "/新年中龙", "282"),
    394: EmojiEntry(394, "/新年大龙", "283"),
    395: EmojiEntry(395, "/略略略", "284"),
    396: EmojiEntry(396, "/龙年快乐", "285"),
    424: EmojiEntry(424, "/按钮", "286"),
}


# ---------------------------------------------------------------------------
# 表情回应表（set_msg_emoji_like 用的 ID 表）
# ---------------------------------------------------------------------------

# 在 QQNT 上，表情回应使用的 ID 体系与发送 face 消息段的 ID 体系相同。
# 默认与发送表相同，保持独立表以便配置覆盖。
REACTION_EMOJI_TABLE: dict[int, EmojiEntry] = dict(SEND_EMOJI_TABLE)


# ---------------------------------------------------------------------------
# 预构建的名称→ID 反向索引
# ---------------------------------------------------------------------------

# 模块加载时构建反向索引，将 describe（去掉 / 前缀）和 aliases 映射到 emoji_id，
# 用于快速按名称查找。同一名称可能映射到多个 ID（如 "龙年快乐" 对应 392 和 396）。
_send_name_index: dict[str, list[int]] = {}
_reaction_name_index: dict[str, list[int]] = {}


def _build_name_index(table: dict[int, EmojiEntry]) -> dict[str, list[int]]:
    """构建名称→ID 反向索引。

    将每个条目的 describe（去掉 ``/`` 前缀）和所有 aliases 作为 key，
    映射到 emoji_id 列表。key 统一转为小写以支持大小写不敏感匹配。

    Args:
        table: 表情表（emoji_id -> EmojiEntry）

    Returns:
        名称到 emoji_id 列表的映射字典
    """
    index: dict[str, list[int]] = {}
    for emoji_id, entry in table.items():
        # describe 去掉 / 前缀作为主名称
        names = [entry.describe.lstrip("/")]
        names.extend(entry.aliases)
        for name in names:
            key = name.lower()
            index.setdefault(key, []).append(emoji_id)
    return index


_send_name_index = _build_name_index(SEND_EMOJI_TABLE)
_reaction_name_index = _build_name_index(REACTION_EMOJI_TABLE)


# ---------------------------------------------------------------------------
# 表查找表
# ---------------------------------------------------------------------------

# 表类型名称到实际表的映射，避免在函数中反复 if-else。
_TABLES: dict[str, dict[int, EmojiEntry]] = {
    "send": SEND_EMOJI_TABLE,
    "reaction": REACTION_EMOJI_TABLE,
}

# 表类型名称到反向索引的映射。
_NAME_INDEXES: dict[str, dict[str, list[int]]] = {
    "send": _send_name_index,
    "reaction": _reaction_name_index,
}

# 合法的表类型集合，用于参数校验。
_VALID_TABLE_TYPES: frozenset[str] = frozenset(_TABLES.keys())


# ---------------------------------------------------------------------------
# 公开查询接口
# ---------------------------------------------------------------------------


def _get_table(table_type: str) -> dict[int, EmojiEntry]:
    """根据 table_type 获取对应的表情表。

    Args:
        table_type: 表类型，``"send"`` 或 ``"reaction"``

    Returns:
        对应的表情表字典

    Raises:
        ValueError: 当 table_type 不是合法值时
    """
    table = _TABLES.get(table_type)
    if table is None:
        raise ValueError(
            f"无效的 table_type: {table_type!r}，合法值为: {sorted(_VALID_TABLE_TYPES)}"
        )
    return table


def get_emoji_by_id(emoji_id: int, table_type: str = "send") -> EmojiEntry | None:
    """按 emoji_id 查找表情条目。

    Args:
        emoji_id: 表情 ID。发送表中为 face_id，回应表中为 emoji_id。
        table_type: 表类型，``"send"``（发送表情表）或 ``"reaction"``（回应表情表），
            默认为 ``"send"``。

    Returns:
        匹配的 :class:`EmojiEntry`，未找到时返回 ``None``。

    Raises:
        ValueError: 当 table_type 不是合法值时。

    Examples:
        >>> entry = get_emoji_by_id(76)
        >>> entry.describe
        '/赞'
        >>> entry = get_emoji_by_id(99999)
        >>> entry is None
        True
    """
    table = _get_table(table_type)
    return table.get(emoji_id)


def get_emoji_by_name(name: str, table_type: str = "send") -> EmojiEntry | None:
    """按名称/关键词模糊查找表情条目。

    查找策略（按优先级）:
        1. 精确匹配: 去掉 ``/`` 前缀后与 describe 和 aliases 精确匹配
           （大小写不敏感）。
        2. 包含匹配: describe（去掉 ``/`` 前缀）包含关键词的条目。

    若精确匹配命中多个 ID，返回第一个（按表中的插入顺序）。
    若精确匹配未命中，返回包含匹配的第一个结果。
    若均未命中，返回 ``None``。

    Args:
        name: 搜索关键词（如 ``"赞"``、``"点赞"``、``"/赞"``、``"狗头"``）。
            会自动去掉 ``/`` 前缀。
        table_type: 表类型，``"send"`` 或 ``"reaction"``，默认为 ``"send"``。

    Returns:
        匹配的 :class:`EmojiEntry`，未找到时返回 ``None``。

    Raises:
        ValueError: 当 table_type 不是合法值时。

    Examples:
        >>> entry = get_emoji_by_name("赞")
        >>> entry.emoji_id
        76
        >>> entry = get_emoji_by_name("/点赞")
        >>> entry.emoji_id
        201
        >>> entry = get_emoji_by_name("狗头")
        >>> entry.describe
        '/doge'
    """
    table = _get_table(table_type)
    name_index = _NAME_INDEXES[table_type]

    # 标准化关键词：去掉 / 前缀，去掉首尾空白，转小写
    keyword = name.strip().lstrip("/").lower()
    if not keyword:
        return None

    # 1. 精确匹配
    matched_ids = name_index.get(keyword)
    if matched_ids:
        return table[matched_ids[0]]

    # 2. 包含匹配：遍历所有条目，describe（去 / 前缀）包含关键词
    for entry in table.values():
        describe_text = entry.describe.lstrip("/").lower()
        if keyword in describe_text:
            return entry

    # 3. 在 aliases 中做包含匹配
    for entry in table.values():
        for alias in entry.aliases:
            if keyword in alias.lower():
                return entry

    return None


def get_all_emoji_ids(table_type: str = "send") -> list[int]:
    """获取指定表的所有表情 ID 列表。

    Args:
        table_type: 表类型，``"send"`` 或 ``"reaction"``，默认为 ``"send"``。

    Returns:
        表情 ID 列表，按表中的 key 顺序排列。

    Raises:
        ValueError: 当 table_type 不是合法值时。

    Examples:
        >>> ids = get_all_emoji_ids()
        >>> 76 in ids
        True
        >>> len(ids) > 130
        True
    """
    table = _get_table(table_type)
    return list(table.keys())


def get_all_emoji_names(table_type: str = "send") -> list[str]:
    """获取指定表的所有表情描述名称列表。

    返回的名称为 describe 原始值（带 ``/`` 前缀）。

    Args:
        table_type: 表类型，``"send"`` 或 ``"reaction"``，默认为 ``"send"``。

    Returns:
        表情描述名称列表，按表中的插入顺序排列。

    Raises:
        ValueError: 当 table_type 不是合法值时。

    Examples:
        >>> names = get_all_emoji_names()
        >>> "/赞" in names
        True
    """
    table = _get_table(table_type)
    return [entry.describe for entry in table.values()]
