# api_defs.py 重构设计文档

> 文件位置：`E:\codearts\1`\Neo-MoFox\plugins\onebot_expand\api_defs.py`
> 当前规模：2375 行，158 个 API，21 个功能域，4 个常量类
> 重构目标：解决语义重复、来源标注矛盾、标志位不一致问题，引入别名机制
> 重构版本：1.2.0 → 1.3.0

---

## 目录

1. [当前状态分析](#1-当前状态分析)
2. [问题清单](#2-问题清单)
3. [别名机制设计](#3-别名机制设计)
4. [主名选取规则](#4-主名选取规则)
5. [别名组完整清单](#5-别名组完整清单)
6. [source 标注修正清单](#6-source-标注修正清单)
7. [napcat_only 标志修正清单](#7-napcat_only-标志修正清单)
8. [加载期校验设计](#8-加载期校验设计)
9. [Service 层集成设计](#9-service-层集成设计)
10. [配置开关设计](#10-配置开关设计)
11. [迁移步骤](#11-迁移步骤)
12. [风险评估](#12-风险评估)
13. [三方 API 完整对照表](#13-三方-api-完整对照表)
14. [附录](#14-附录)

---

## 1. 当前状态分析

### 1.1 文件结构

```
api_defs.py (2375 行)
├── APICategory 枚举 (line 18-82)        # 21 个功能域
├── APISource 枚举 (line 85-98)          # 4 种来源
├── APIDef dataclass (line 106-126)      # API 元数据
├── OneBotAction 常量类 (line 134-173)   # OneBot v11 标准
├── NapCatAction 常量类 (line 176-202)   # NapCat 扩展
├── GoCqhttpCompatAction 常量类 (line 205-226)  # go-cqhttp 兼容
├── ExpandAction 常量类 (line 229-361)   # 其他扩展
├── NAPCAT_ONLY_APIS 集合 (line 369-383)
├── EXPAND_APIS 集合 (line 386-432)
├── ALL_APIS dict (line 445-2023)        # 158 个 API 定义
├── 21 个分类列表 (line 2030-2251)
└── 3 个查询函数 (line 2259-2334)
```

### 1.2 现有去重机制

| 机制 | 位置 | 作用 |
|---|---|---|
| `ALL_APIS: dict[str, APIDef]` | line 445 | dict 键唯一，保证字面去重 |
| `napcat_only: bool` | line 125 | 标记 NapCat 专属，SnowLuma 不支持 |
| `snowluma_compat: bool` | line 126 | 标记 SnowLuma 兼容性 |
| `NAPCAT_ONLY_APIS: set[str]` | line 369 | NapCat 专属 API 集合 |
| `enable_<api_name>` 配置开关 | config.py | 每个 API 独立开关 |

### 1.3 已识别问题统计

| 问题类型 | 数量 | 严重程度 |
|---|---|---|
| A. 常量类归属与 source 矛盾 | 5 | 中 |
| B. napcat_only 标志错误（SnowLuma 实际支持）| 12 | 高 |
| C. 同组 API napcat_only 不一致 | 1 组（3 个 API）| 中 |
| D. 纯别名未声明 | 5 组（11 个 action）| 中 |
| E. 语义重复未标记 | 3 组（6 个 API）| 低 |
| F. 未覆盖 API（附录，不在本次范围）| ~30 | - |

---

## 2. 问题清单

### 2.1 问题类型 A：常量类归属与 source 矛盾

| 行号 | 常量类 | action 名 | 当前 source | 应改为 | 应搬到 | 原因 |
|---|---|---|---|---|---|---|
| 241 | ExpandAction.SET_FRIEND_ADD_REQUEST | set_friend_add_request | ONEBOT_V11 | ONEBOT_V11 ✓ | OneBotAction | OneBot v11 标准定义 |
| 242 | ExpandAction.SET_GROUP_ADD_REQUEST | set_group_add_request | ONEBOT_V11 | ONEBOT_V11 ✓ | OneBotAction | OneBot v11 标准定义 |
| 217 | GoCqhttpCompatAction.GET_GROUP_SYSTEM_MSG | get_group_system_msg | GOCQHTTP_COMPAT | ONEBOT_V11 | OneBotAction | OneBot v11 标准定义 |
| 276 | ExpandAction.SET_QQ_PROFILE | set_qq_profile | EXPAND | GOCQHTTP_COMPAT | GoCqhttpCompatAction | NapCat 在 go-cqhttp 目录实现 |
| 1622 | ExpandAction.OCR_IMAGE | ocr_image | EXPAND | GOCQHTTP_COMPAT | GoCqhttpCompatAction | go-cqhttp 兼容 API |
| 919 | NapCatAction.GET_ESSENCE_MSG_LIST | get_essence_msg_list | NAPCAT_EXT | GOCQHTTP_COMPAT | GoCqhttpCompatAction | go-cqhttp 兼容（NapCat 也实现）|

### 2.2 问题类型 B：napcat_only 标志错误

SnowLuma 实际支持但当前标 `napcat_only=True` 的 API：

| 行号 | action 名 | 当前 napcat_only | 应改为 | SnowLuma 实现状态 |
|---|---|---|---|---|
| 515 | send_poke | True | False | 已实现（自动路由）|
| 533 | send_forward_msg | True | False | 已实现（自动路由）|
| 784 | get_file | True | False | 已实现（图片/语音缓存）|
| 815 | get_file_url | True | False | 已实现 |
| 889 | get_group_detail_info | True | False | 已实现 |
| 913 | set_msg_emoji_like | True | False | 已实现 |
| 924 | get_essence_msg_list | True | False | 已实现 |
| 934 | get_online_clients | True | False | 已实现（占位）|
| 945 | get_cookies | True | False | 已实现（指定域名）|
| 954 | get_csrf_token | True | False | 已实现 |
| 974 | set_restart | True | False | 已实现（不支持，但有响应）|
| 983 | clean_cache | True | False | 已实现（no-op）|

### 2.3 问题类型 C：同组 API napcat_only 不一致

精华消息三个 API（同组）标志位不一致：

| 行号 | action 名 | 当前 napcat_only | 应改为 |
|---|---|---|---|
| 924 | get_essence_msg_list | True | False |
| 1013 | set_essence_msg | False | False ✓ |
| 1022 | delete_essence_msg | False | False ✓ |

### 2.4 问题类型 D：纯别名未声明

同 handler 多 actionName 注册，当前未在 `aliases` 字段声明：

| 主名 | 别名 | 来源 | 备注 |
|---|---|---|---|
| get_rkey | nc_get_rkey | NapCat | NapCat 旧格式名 |
| set_group_sign | send_group_sign | NapCat | NapCat 数组别名 |
| send_packet | .send_packet | NapCat | 旧名带点前缀 |
| ocr_image | .ocr_image | go-cqhttp | 旧名带点前缀 |
| fetch_ptt_text | get_ptt_text, get_record_text | NapCat | 三联别名 |

### 2.5 问题类型 E：语义重复未标记

功能等价但实现独立的 API（不合并为别名，但需标记关系）：

| 主名 | 等价 API | 区别 | 处理 |
|---|---|---|---|
| send_poke | friend_poke, group_poke | 路由版 vs 显式版 | 各自保留，description 交叉引用 |
| share_peer | send_ark_share | NapCat 新旧名 | 各自保留，description 标注 |
| share_group_ex | send_group_ark_share | NapCat 新旧名 | 各自保留，description 标注 |

### 2.6 问题类型 F：未覆盖 API（附录）

NapCatQQ/SnowLuma 有但 onebot_expand 未包装的 API，不在本次重构范围，详见 [附录 A](#附录-a未覆盖-api-清单)。

---

## 3. 别名机制设计

### 3.1 APIDef schema 修改

在 `APIDef` dataclass 新增 `aliases` 字段：

```python
@dataclass(frozen=True, slots=True)
class APIDef:
    """单个 API 的定义元数据。

    Attributes:
        action: API action 名称（如 "send_group_msg"）
        category: API 所属类别
        source: API 来源（OneBot v11 或 NapCat 扩展）
        description: API 中文描述
        params: 参数名到类型描述的映射（如 {"group_id": "int"}）
        napcat_only: 是否为 NapCat 专属 API（SnowLumia 不支持）
        snowluma_compat: 是否兼容 SnowLumia 协议端
        aliases: 同 handler 的别名 action 名元组（不含主名本身）
    """
    action: str
    category: APICategory
    source: APISource
    description: str
    params: dict[str, str] = field(default_factory=dict)
    napcat_only: bool = False
    snowluma_compat: bool = True
    aliases: tuple[str, ...] = ()  # 新增字段
```

### 3.2 设计要点

1. **类型选择**：用 `tuple` 而非 `list`，保证 `frozen=True` 兼容
2. **默认值**：空 tuple `()` 表示无别名，不破坏现有 158 个 APIDef 构造
3. **语义**：`aliases` 严格表示"同 handler 注册的别名"，不包含功能等价但实现独立的 API
4. **唯一性**：别名不作为 `ALL_APIS` 的键，只作为主名的 `aliases` 字段值

### 3.3 向后兼容

- 新增字段有默认值，现有 APIDef 构造无需改动
- 只有 5 组纯别名需要填充 `aliases` 数据
- 不影响现有 Tool / Service 层代码

---

## 4. 主名选取规则

别名组中选一个作为主名，其余作为别名。优先级（从高到低）：

1. **OneBot v11 标准 action 名优先**（如 `send_group_msg`）
2. **go-cqhttp 兼容 action 名优先**（如 `set_essence_msg`）
3. **NapCat 扩展 action 名优先**（如 `get_rkey`）
4. **不带点前缀的名优先**（如 `ocr_image` 主，`.ocr_image` 别名）
5. **不带 `nc_` 前缀的名优先**（如 `get_rkey` 主，`nc_get_rkey` 别名）
6. **自动路由版优先**（如 `send_poke` 主，`friend_poke`/`group_poke` 别名）—— 仅在同 handler 数组别名时适用

### 4.1 决策原则

- 主名应是"最通用、最标准、最不带前缀"的形式
- 别名通常是历史遗留、旧版兼容、或显式细分版本
- 主名用于配置开关、文档引用、默认调用
- 别名仅用于向后兼容的调用入口

### 4.2 边界情况

- **同 handler 数组别名**（NapCat `defineAction(['set_group_sign', 'send_group_sign'])`）：纳入 `aliases` 字段
- **独立 defineAction 但功能等价**（SnowLuma 的 `share_peer` 和 `send_ark_share`）：**不**纳入 `aliases`，各自保留为独立 APIDef，仅在 description 里交叉引用
- **同 handler 但参数 schema 不同**（如某些 API 在 NapCat 和 SnowLuma 间参数不同）：不视为别名，按主名调用，Service 层根据后端构造不同 params

---

## 5. 别名组完整清单

### 5.1 纯别名（纳入 `aliases` 字段）

| 主名 | aliases | source | category | 修正说明 |
|---|---|---|---|---|
| `get_rkey` | `("nc_get_rkey",)` | EXPAND | CRED | NapCat 旧格式名 `nc_get_rkey` |
| `set_group_sign` | `("send_group_sign",)` | EXPAND | GROUP_EXT | NapCat 数组别名 |
| `send_packet` | `(".send_packet",)` | EXPAND | MISC | 旧名带点前缀 |
| `ocr_image` | `(".ocr_image",)` | GOCQHTTP_COMPAT | CRED | 旧名带点前缀（source 需从 EXPAND 改为 GOCQHTTP_COMPAT）|
| `fetch_ptt_text` | `("get_ptt_text", "get_record_text")` | EXPAND | NAPCAT_EXT | 三联别名 |

### 5.2 语义等价（不纳入 `aliases`，标记关系）

| 主名 | 等价 API | 标记方式 |
|---|---|---|
| `send_poke` | `friend_poke`, `group_poke` | description 标注"自动路由版，等价于 friend_poke + group_poke" |
| `friend_poke` | `send_poke`, `group_poke` | description 标注"显式好友版，等价于 send_poke(user_id=...)" |
| `group_poke` | `send_poke`, `friend_poke` | description 标注"显式群版，等价于 send_poke(group_id=...)" |
| `share_peer` | `send_ark_share` | description 标注"send_ark_share 是 NapCat 标准化别名" |
| `send_ark_share` | `share_peer` | description 标注"等价于 share_peer" |
| `share_group_ex` | `send_group_ark_share` | description 标注"send_group_ark_share 是 NapCat 标准化别名" |
| `send_group_ark_share` | `share_group_ex` | description 标注"等价于 share_group_ex" |

---

## 6. source 标注修正清单

### 6.1 完整修正表

| 行号 | action | 当前 source | 应改为 | 当前常量类 | 应搬到 | 修正原因 |
|---|---|---|---|---|---|---|
| 1303 | set_friend_add_request | ONEBOT_V11 | ONEBOT_V11 ✓ | ExpandAction | OneBotAction | OneBot v11 标准 |
| 1314 | set_group_add_request | ONEBOT_V11 | ONEBOT_V11 ✓ | ExpandAction | OneBotAction | OneBot v11 标准 |
| 1326 | get_group_system_msg | GOCQHTTP_COMPAT | ONEBOT_V11 | GoCqhttpCompatAction | OneBotAction | OneBot v11 标准 |
| 1396 | set_qq_profile | EXPAND | GOCQHTTP_COMPAT | ExpandAction | GoCqhttpCompatAction | go-cqhttp 兼容 |
| 1618 | ocr_image | EXPAND | GOCQHTTP_COMPAT | ExpandAction | GoCqhttpCompatAction | go-cqhttp 兼容 |
| 919 | get_essence_msg_list | NAPCAT_EXT | GOCQHTTP_COMPAT | NapCatAction | GoCqhttpCompatAction | go-cqhttp 兼容（NapCat 也实现）|

### 6.2 常量类搬迁影响

搬迁后需要更新所有引用旧常量类的位置：

- `ExpandAction.SET_FRIEND_ADD_REQUEST` → `OneBotAction.SET_FRIEND_ADD_REQUEST`
- `ExpandAction.SET_GROUP_ADD_REQUEST` → `OneBotAction.SET_GROUP_ADD_REQUEST`
- `GoCqhttpCompatAction.GET_GROUP_SYSTEM_MSG` → `OneBotAction.GET_GROUP_SYSTEM_MSG`
- `ExpandAction.SET_QQ_PROFILE` → `GoCqhttpCompatAction.SET_QQ_PROFILE`
- `ExpandAction.OCR_IMAGE` → `GoCqhttpCompatAction.OCR_IMAGE`
- `NapCatAction.GET_ESSENCE_MSG_LIST` → `GoCqhttpCompatAction.GET_ESSENCE_MSG_LIST`

引用位置包括：
- `ALL_APIS` dict 的键（line 445-2023）
- 21 个分类列表（line 2030-2251）
- `NAPCAT_ONLY_APIS` 集合（line 369-383）
- `EXPAND_APIS` 集合（line 386-432）
- Service 层、Tool 层的 import

### 6.3 兼容性处理

为避免破坏旧 import，可在原常量类保留 alias 引用：

```python
class ExpandAction:
    # 已搬迁到 OneBotAction，保留旧引用以兼容
    SET_FRIEND_ADD_REQUEST = OneBotAction.SET_FRIEND_ADD_REQUEST
    SET_GROUP_ADD_REQUEST = OneBotAction.SET_GROUP_ADD_REQUEST
    # 已搬迁到 GoCqhttpCompatAction
    SET_QQ_PROFILE = GoCqhttpCompatAction.SET_QQ_PROFILE
    OCR_IMAGE = GoCqhttpCompatAction.OCR_IMAGE
    # ...
```

---

## 7. napcat_only 标志修正清单

### 7.1 完整修正表

| 行号 | action | 当前 napcat_only | 应改为 | 当前 snowluma_compat | 应改为 | 加入 NAPCAT_ONLY_APIS? |
|---|---|---|---|---|---|---|
| 515 | send_poke | True | False | False | True | 移除 |
| 533 | send_forward_msg | True | False | False | True | 移除 |
| 784 | get_file | True | False | False | True | 移除 |
| 815 | get_file_url | True | False | False | True | 移除 |
| 889 | get_group_detail_info | True | False | False | True | 移除 |
| 913 | set_msg_emoji_like | True | False | False | True | 移除 |
| 924 | get_essence_msg_list | True | False | False | True | 移除 |
| 934 | get_online_clients | True | False | False | True | 移除 |
| 945 | get_cookies | True | False | False | True | 移除 |
| 954 | get_csrf_token | True | False | False | True | 移除 |
| 974 | set_restart | True | False | False | True | 移除 |
| 983 | clean_cache | True | False | False | True | 移除 |

### 7.2 NAPCAT_ONLY_APIS 集合修正

当前 `NAPCAT_ONLY_APIS`（line 369-383）包含 12 个 API，修正后应清空或大幅缩减。

**修正后的 NAPCAT_ONLY_APIS**：

```python
# NapCat 专属 API 集合（SnowLumia 不支持的 API）
# 修正后：SnowLuma 几乎实现了所有 NapCat 扩展 API，集合为空
# 保留此字段以备未来 API 不兼容时使用
NAPCAT_ONLY_APIS: set[str] = set()
```

### 7.3 真正的 NapCat 专属 API（候选）

根据调研，以下 API 在 SnowLuma 中确实未实现或为占位：

| action | SnowLuma 实现状态 | 是否纳入 NAPCAT_ONLY_APIS |
|---|---|---|
| get_rkey_server | 已实现 | 否 |
| nc_get_rkey | 已实现（别名）| 否 |
| get_robot_uin_range | 未实现 | 是（候选）|
| ArkSharePeer / ArkShareGroup | 未实现（NapCat 已废弃旧名）| 是（候选）|
| .handle_quick_operation | 已实现（legacy）| 否 |
| .get_word_slices | 未注册 handler | 不纳入（不可调用）|

**建议**：`NAPCAT_ONLY_APIS` 清空，真正不兼容的 API 通过 `snowluma_compat=False` 单独标记。

---

## 8. 加载期校验设计

### 8.1 函数签名

```python
def _validate_api_definitions() -> list[str]:
    """校验 ALL_APIS 的完整性，返回所有问题列表（空列表表示无问题）。
    
    检查项：
    1. 跨常量类的 action 字符串重复
    2. 别名指向不存在的主名
    3. 别名同时作为 ALL_APIS 的键（应只作为主名的 aliases 字段）
    4. 同组 API 的 napcat_only 标志不一致
    5. source 与常量类归属一致性
    6. 分类列表 (MESSAGE_APIS 等) 与 ALL_APIS 键集合一致
    
    Returns:
        问题描述列表，每条形如 "[WARN] action=xxx: ..."
    """
```

### 8.2 检查项详细伪代码

#### 检查 1：跨常量类 action 字符串重复

```python
def _check_duplicate_constants() -> list[str]:
    """扫描四个常量类的所有字符串常量，找重复值。"""
    issues = []
    seen: dict[str, str] = {}  # action_str -> 类名
    for cls_name, cls in [
        ("OneBotAction", OneBotAction),
        ("NapCatAction", NapCatAction),
        ("GoCqhttpCompatAction", GoCqhttpCompatAction),
        ("ExpandAction", ExpandAction),
    ]:
        for attr in dir(cls):
            if attr.isupper():
                value = getattr(cls, attr)
                if isinstance(value, str):
                    if value in seen:
                        issues.append(
                            f"[WARN] action={value}: 重复定义于 {seen[value]} 和 {cls_name}.{attr}"
                        )
                    else:
                        seen[value] = f"{cls_name}.{attr}"
    return issues
```

#### 检查 2 & 3：别名完整性

```python
def _check_aliases() -> list[str]:
    """检查别名指向有效主名，且不作为 ALL_APIS 键。"""
    issues = []
    for action, api_def in ALL_APIS.items():
        for alias in api_def.aliases:
            # 别名不应作为 ALL_APIS 的键
            if alias in ALL_APIS:
                issues.append(
                    f"[WARN] action={action}: 别名 '{alias}' 同时作为 ALL_APIS 键存在"
                )
            # 别名不应与其他 API 的别名重复
            for other_action, other_def in ALL_APIS.items():
                if other_action != action and alias in other_def.aliases:
                    issues.append(
                        f"[WARN] action={action}/{other_action}: 别名 '{alias}' 被多个主名声明"
                    )
    return issues
```

#### 检查 4：同组 API napcat_only 不一致

```python
def _check_group_flag_consistency() -> list[str]:
    """检查同分类列表内 napcat_only 标志一致性。"""
    issues = []
    for category, api_list in [
        (APICategory.NAPCAT_EXT, NAPCAT_EXT_APIS),
        # 其他分类...
    ]:
        flags = {action: ALL_APIS[action].napcat_only for action in api_list}
        unique_flags = set(flags.values())
        if len(unique_flags) > 1:
            issues.append(
                f"[WARN] category={category.value}: napcat_only 标志不一致 {flags}"
            )
    return issues
```

#### 检查 5：source 与常量类一致性

```python
def _check_source_class_consistency() -> list[str]:
    """检查 source 字段与常量类归属一致性。"""
    issues = []
    expected_mapping = {
        OneBotAction: APISource.ONEBOT_V11,
        NapCatAction: APISource.NAPCAT_EXT,
        GoCqhttpCompatAction: APISource.GOCQHTTP_COMPAT,
        ExpandAction: APISource.EXPAND,
    }
    # 反向查找每个 action 来自哪个常量类
    # ... 实现略
    return issues
```

#### 检查 6：分类列表完整性

```python
def _check_category_lists() -> list[str]:
    """检查分类列表并集等于 ALL_APIS 键集合。"""
    issues = []
    all_in_lists = set()
    for api_list in [
        MESSAGE_APIS, GROUP_APIS, FILE_APIS, ACCOUNT_APIS,
        NAPCAT_EXT_APIS, GROUP_FILE_APIS, GROUP_NOTICE_APIS,
        GROUP_EXT_APIS, REQUEST_APIS, USER_EXT_APIS, STATUS_APIS,
        POKE_APIS, EMOJI_EXT_APIS, AI_VOICE_APIS, CRED_APIS,
        MISC_APIS, FLASH_APIS, GROUP_ALBUM_APIS, GROUP_TODO_APIS,
        QZONE_APIS, ARK_APIS,
    ]:
        for action in api_list:
            if action in all_in_lists:
                issues.append(f"[WARN] action={action}: 在多个分类列表中重复")
            all_in_lists.add(action)
    
    all_in_dict = set(ALL_APIS.keys())
    missing = all_in_dict - all_in_lists
    extra = all_in_lists - all_in_dict
    if missing:
        issues.append(f"[WARN] ALL_APIS 中有 action 未归入任何分类列表: {missing}")
    if extra:
        issues.append(f"[WARN] 分类列表中有 action 不在 ALL_APIS: {extra}")
    return issues
```

### 8.3 调用时机

模块末尾调用，输出 warning（不抛异常，避免阻塞加载）：

```python
# api_defs.py 模块末尾

_validation_issues = _validate_api_definitions()
if _validation_issues:
    import warnings
    for issue in _validation_issues:
        warnings.warn(issue, RuntimeWarning, stacklevel=2)
```

### 8.4 校验失败示例输出

```
api_defs.py:1: RuntimeWarning: [WARN] action=set_friend_add_request: 常量类 ExpandAction 与 source ONEBOT_V11 不一致
api_defs.py:1: RuntimeWarning: [WARN] action=get_essence_msg_list: 同组 napcat_only 不一致 (get_essence_msg_list=True, set_essence_msg=False, delete_essence_msg=False)
api_defs.py:1: RuntimeWarning: [WARN] action=get_rkey: 别名 'nc_get_rkey' 同时作为 ALL_APIS 键存在
```

---

## 9. Service 层集成设计

### 9.1 主名解析函数

在 `api_defs.py` 新增 `resolve_action` 函数：

```python
# 别名到主名的反向映射（模块加载时构建）
_ALIAS_TO_PRIMARY: dict[str, str] = {}
for _action, _def in ALL_APIS.items():
    for _alias in _def.aliases:
        _ALIAS_TO_PRIMARY[_alias] = _action
del _action, _def, _alias


def resolve_action(name: str) -> str | None:
    """输入 action 名，若是别名返回主名，若是主名直接返回，不存在返回 None。
    
    Args:
        name: action 名称（主名或别名）
    
    Returns:
        主名 action 字符串，不存在时返回 None
    
    Examples:
        >>> resolve_action("nc_get_rkey")
        'get_rkey'
        >>> resolve_action("get_rkey")
        'get_rkey'
        >>> resolve_action("unknown_action")
        None
    """
    if name in ALL_APIS:
        return name
    return _ALIAS_TO_PRIMARY.get(name)
```

### 9.2 Service 层调用流程伪代码

```python
# services/base.py 或类似位置

from ..api_defs import ALL_APIS, resolve_action, APIDef

class OnebotExpandServiceBase:
    async def call_api(
        self,
        action: str,
        params: dict,
        timeout: float = 30.0,
    ) -> tuple[bool, str]:
        """统一 API 调用入口，处理别名解析、开关检查、协议端兼容。"""
        # 步骤 1: 解析主名
        primary = resolve_action(action)
        if primary is None:
            return False, f"未知 action: {action}"
        
        api_def = ALL_APIS[primary]
        
        # 步骤 2: 检查配置开关（按主名）
        if not self._is_api_enabled(primary):
            return False, f"API {primary} 已禁用"
        
        # 步骤 3: 检查协议端兼容性
        backend = self.config.protocol.backend
        if backend == "snowluma" and not api_def.snowluma_compat:
            return False, f"SnowLuma 不支持 {primary}"
        if backend == "napcat" and api_def.napcat_only is False:
            pass  # NapCat 支持所有非 napcat_only 的 API
            # 实际上 napcat_only=False 意味着两端都支持
        
        # 步骤 4: 选择实际调用的 action 名
        actual_action = self._select_action_name(primary, api_def, backend)
        
        # 步骤 5: 调用适配器
        return await self._call_onebot_api(actual_action, params, timeout)
    
    def _select_action_name(
        self,
        primary: str,
        api_def: APIDef,
        backend: str,
    ) -> str:
        """根据后端选择实际 action 名。
        
        默认返回主名。某些后端可能只识别别名（如旧版 NapCat 只认 nc_get_rkey）。
        可通过 config.protocol.backend_action_map 配置覆盖。
        """
        # 检查后端特定映射
        backend_overrides = getattr(
            self.config.protocol, "backend_action_map", {}
        ).get(backend, {})
        if primary in backend_overrides:
            return backend_overrides[primary]
        
        # 默认返回主名
        return primary
    
    def _is_api_enabled(self, primary: str) -> bool:
        """检查 API 是否在配置中启用（按主名）。"""
        switch_key = f"enable_{primary}"
        return getattr(self.config.api_switches, switch_key, True)
```

### 9.3 别名调用支持

调用方主动传入别名时的处理：

```python
# Service 层接收别名调用示例
async def get_rkey(self, use_legacy_name: bool = False) -> tuple[bool, str]:
    """获取 rkey。
    
    Args:
        use_legacy_name: 是否使用旧版 action 名 nc_get_rkey（用于兼容旧客户端）
    """
    action = "nc_get_rkey" if use_legacy_name else "get_rkey"
    # call_api 内部会 resolve_action 到主名 get_rkey
    return await self.call_api(action, params={})
```

### 9.4 Tool 层无需改动

Tool 层只接收参数并调用 Service，不直接处理 action 名。因此 Tool 层无需改动。

---

## 10. 配置开关设计

### 10.1 开关生成规则

- `enable_<api_name>` 只对主名生成
- 别名不生成独立开关
- 别名的启用/禁用跟随主名

### 10.2 config.py 修改

在 `OnebotExpandConfig.api_switches` 中：

```python
@dataclass
class ApiSwitches:
    """API 开关配置。
    
    每个 API 对应一个 enable_<action> 字段，按主名生成。
    别名不生成独立字段，跟随主名开关。
    """
    # 消息相关
    enable_send_group_msg: bool = True
    enable_send_private_msg: bool = True
    # ... 其他 156 个主名
    
    # 已废弃字段（保留以兼容旧配置，加载时映射到主名）
    # enable_nc_get_rkey: bool = True  # 映射到 enable_get_rkey
    # enable_send_group_sign: bool = True  # 映射到 enable_set_group_sign
```

### 10.3 旧配置兼容

在 config 加载逻辑里加一层别名映射：

```python
# config.py 加载逻辑

from .api_defs import resolve_action

def _normalize_config_key(key: str) -> str:
    """将别名配置键映射到主名。
    
    旧配置文件可能用 enable_nc_get_rkey，需映射到 enable_get_rkey。
    """
    if key.startswith("enable_"):
        action = key[7:]
        primary = resolve_action(action)
        if primary and primary != action:
            return f"enable_{primary}"
    return key


def load_config(config_dict: dict) -> OnebotExpandConfig:
    """加载配置，处理别名映射。"""
    normalized = {}
    for key, value in config_dict.items():
        normalized_key = _normalize_config_key(key)
        if normalized_key in normalized and normalized_key != key:
            # 别名与主名同时存在，warning
            import warnings
            warnings.warn(
                f"配置键 '{key}' 是 '{normalized_key}' 的别名，"
                f"两者同时存在，使用主名 '{normalized_key}'",
                UserWarning,
                stacklevel=2,
            )
        normalized[normalized_key] = value
    return OnebotExpandConfig(**normalized)
```

### 10.4 配置文件示例

```toml
# config/plugins/onebot_expand/config.toml

[api_switches]
# 主名开关（推荐）
enable_get_rkey = true
enable_set_group_sign = true
enable_send_packet = true
enable_ocr_image = true
enable_fetch_ptt_text = true

# 旧别名开关（兼容，加载时映射到主名）
# enable_nc_get_rkey = true       # 映射到 enable_get_rkey
# enable_send_group_sign = true    # 映射到 enable_set_group_sign
# enable_.send_packet = true       # 映射到 enable_send_packet
# enable_.ocr_image = true         # 映射到 enable_ocr_image
# enable_get_ptt_text = true       # 映射到 enable_fetch_ptt_text
# enable_get_record_text = true    # 映射到 enable_fetch_ptt_text
```

---

## 11. 迁移步骤

按以下顺序执行，每步可独立验证：

### 阶段 1：基础结构（不破坏现有功能）

1. **步骤 1**：在 `APIDef` dataclass 添加 `aliases: tuple[str, ...] = ()` 字段
2. **步骤 2**：在 `api_defs.py` 末尾添加 `_ALIAS_TO_PRIMARY` 反向映射构建
3. **步骤 3**：在 `api_defs.py` 末尾添加 `resolve_action` 函数
4. **步骤 4**：在 `api_defs.py` 末尾添加 `_validate_api_definitions` 函数及调用

### 阶段 2：数据修正（可能影响行为）

5. **步骤 5**：为 5 组纯别名填充 `aliases` 数据（5 个 APIDef 改动）
6. **步骤 6**：修正 12 个 API 的 `napcat_only` 标志（False）和 `snowluma_compat` 标志（True）
7. **步骤 7**：清空 `NAPCAT_ONLY_APIS` 集合
8. **步骤 8**：修正 6 个 API 的 `source` 标注
9. **步骤 9**：修正 6 个常量的常量类归属（搬迁 + 保留旧引用兼容）

### 阶段 3：集成与验证

10. **步骤 10**：运行加载期校验，确认无 warning
11. **步骤 11**：更新 Service 层，集成 `resolve_action` 调用
12. **步骤 12**：更新 `config.py`，添加别名配置键映射
13. **步骤 13**：更新 `plugin.py` 版本号（1.2.0 → 1.3.0）
14. **步骤 14**：更新文档和 `plugin_description`

### 阶段 4：测试

15. **步骤 15**：单元测试 `resolve_action` 函数
16. **步骤 16**：单元测试 `_validate_api_definitions` 函数
17. **步骤 17**：集成测试 Service 层别名调用
18. **步骤 18**：集成测试 SnowLuma 后端兼容性
19. **步骤 19**：回归测试 158 个 API 调用

---

## 12. 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|---|---|---|---|
| 别名改动导致旧配置文件失效 | 中 | 中 | config.py 加别名映射，旧键自动转换为主名 |
| 常量类搬迁导致旧 import 失败 | 高 | 高 | 在原常量类保留 alias 引用（如 `ExpandAction.SET_FRIEND_ADD_REQUEST = OneBotAction.SET_FRIEND_ADD_REQUEST`）|
| napcat_only 改动导致 SnowLuma 调用失败 | 低 | 高 | 实测验证；保留 `snowluma_compat` 字段作为兜底 |
| 加载期校验输出过多 warning | 中 | 低 | 分批修正，每批修正后运行校验 |
| Service 层 `resolve_action` 性能开销 | 低 | 低 | 模块加载时构建 `_ALIAS_TO_PRIMARY` dict，O(1) 查询 |
| 别名 `aliases` 字段类型变更（tuple vs list）| 低 | 低 | 用 tuple 保证 frozen=True 兼容 |
| 配置开关合并导致部分 API 无法单独控制 | 低 | 中 | 主名+别名视为一个整体控制，符合预期 |

---

## 13. 三方 API 完整对照表

### 13.1 总览

| 来源 | 独立 action | 含别名 | 备注 |
|---|---|---|---|
| **OneBot v11 标准** | 39 | 39 | 38 公开 + 1 隐藏（`.handle_quick_operation`）|
| **NapCatQQ** | 176 | 176 | 每个 action 自动派生 `_async` / `_rate_limited` 两个变体（共 528 个注册键）；3 个占位枚举（test_auto_register_01/02、unknown）不计；`.get_word_slices` 枚举有定义但无 handler |
| **SnowLuma** | 172 | 178 | 6 个别名（fetch_ptt_text↔get_ptt_text/get_record_text、get_rkey↔nc_get_rkey、ocr_image↔.ocr_image、set_group_sign↔send_group_sign、send_packet↔.send_packet）|
| **onebot_expand（当前）** | 158 | 158 | 无别名机制 |
| **onebot_expand（重构后）** | 158 | 163 | 5 组纯别名（5 主名 + 6 别名 action 串）|

### 13.2 按来源分布

#### NapCatQQ 176 个 action 分布
- OneBot v11 标准：25 个
- go-cqhttp 兼容：27 个
- NapCat 扩展：124 个

#### SnowLuma 172 个 action 分布
- OneBot v11 标准：38 个
- go-cqhttp 兼容：10 个
- NapCat 兼容：约 53 个
- SnowLuma 扩展：约 71 个

### 13.3 三方完整 API 对照表（按 action 名字典序）

下表列出三方所有 action 名，标注每个项目是否实现。

**列说明**：
- `Action` — action 字符串名
- `功能` — 简短功能说明
- `标准` — OneBot v11 标准是否定义（✓ 标准 / ○ 隐藏 / ✗ 非标准）
- `NC` — NapCatQQ 是否实现（✓ 实现 / ✗ 未实现 / ○ 占位空实现）
- `SL` — SnowLuma 是否实现（✓ 实现 / ✗ 未实现 / ○ 占位空实现）
- `OE` — onebot_expand 是否包装（✓ 包装 / ✗ 未包装）
- `OE 分类` — onebot_expand 中的功能域分类
- `OE source` — onebot_expand 标注的来源（OB11=OneBot v11 / NC=NapCat 扩展 / GOCQ=go-cqhttp 兼容 / EXP=扩展）
- `OE napcat_only` — onebot_expand 标注的 napcat_only（重构前）
- `备注` — 别名、修正建议等

#### A. 消息相关

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `send_msg` | 发送消息（自动路由）| ✓ | ✓ | ✓ | ✗ | - | - | - | OE 未单独包装，由 send_group/private_msg 替代 |
| `send_private_msg` | 发送私聊消息 | ✓ | ✓ | ✓ | ✓ | MESSAGE | OB11 | False | |
| `send_group_msg` | 发送群消息 | ✓ | ✓ | ✓ | ✓ | MESSAGE | OB11 | False | |
| `delete_msg` | 撤回消息 | ✓ | ✓ | ✓ | ✓ | MESSAGE | OB11 | False | |
| `get_msg` | 获取消息 | ✓ | ✓ | ✓ | ✓ | MESSAGE | OB11 | False | |
| `get_forward_msg` | 获取合并转发消息 | ✓ | ✓ | ✓ | ✓ | MESSAGE | OB11 | False | |
| `send_forward_msg` | 发送合并转发（自动路由）| ✗ | ✓ | ✓ | ✓ | MESSAGE | NC | **True** | napcat_only 应改为 False（SnowLuma 实现）|
| `send_group_forward_msg` | 发送群合并转发 | ✗ | ✓ | ✓ | ✓ | MESSAGE | GOCQ | False | |
| `send_private_forward_msg` | 发送私聊合并转发 | ✗ | ✓ | ✓ | ✓ | MESSAGE | GOCQ | False | |
| `upload_forward_msg` | 上传转发消息（返回 res_id）| ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 独有 |
| `upload_foward_msg` | 上传转发消息（拼写别名）| ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 独有（拼写错误别名）|
| `get_group_msg_history` | 获取群消息历史 | ✗ | ✓ | ✓ | ✓ | MESSAGE | GOCQ | False | |
| `get_friend_msg_history` | 获取好友消息历史 | ✗ | ✓ | ✓ | ✓ | MESSAGE | GOCQ | False | |
| `mark_msg_as_read` | 标记消息已读（自动路由）| ✗ | ✓ | ✓ | ✓ | MESSAGE | GOCQ | False | |
| `mark_group_msg_as_read` | 标记群消息已读 | ✗ | ✓ | ✓ | ✓ | MESSAGE | EXP | False | |
| `mark_private_msg_as_read` | 标记私聊消息已读 | ✗ | ✓ | ✓ | ✓ | MESSAGE | EXP | False | |
| `_mark_all_as_read` | 标记全部已读 | ✗ | ✓ | ○ | ✓ | MESSAGE | EXP | False | SnowLuma 占位 no-op |
| `forward_friend_single_msg` | 转发单条消息给好友 | ✗ | ✓ | ✓ | ✓ | MESSAGE | EXP | False | |
| `forward_group_single_msg` | 转发单条消息到群 | ✗ | ✓ | ✓ | ✓ | MESSAGE | EXP | False | |
| `set_msg_emoji_like` | 设置消息表情回应 | ✗ | ✓ | ✓ | ✓ | NAPCAT_EXT | NC | **True** | napcat_only 应改为 False |
| `get_emoji_likes` | 获取表情回应用户 | ✗ | ✓ | ✓ | ✓ | EMOJI_EXT | EXP | False | |
| `fetch_emoji_like` | 获取表情回应分页 | ✗ | ✓ | ✓ | ✓ | EMOJI_EXT | EXP | False | |
| `set_group_reaction` | 群聊表情回应 | ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 独有 |
| `fetch_ptt_text` | 语音转文字 | ✗ | ✓ | ✓ | ✓ | NAPCAT_EXT | EXP | False | 别名：get_ptt_text, get_record_text |
| `get_ptt_text` | 语音转文字（别名）| ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 别名，OE 应纳入 aliases |
| `get_record_text` | 语音转文字（别名）| ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 别名，OE 应纳入 aliases |
| `send_like` | 发送好友赞 | ✓ | ✓ | ✓ | ✓ | MESSAGE | OB11 | False | |
| `send_poke` | 戳一戳（自动路由）| ✗ | ✓ | ✓ | ✓ | MESSAGE | NC | **True** | napcat_only 应改为 False；路由版，等价 friend_poke+group_poke |
| `friend_poke` | 好友戳一拍 | ✗ | ✓ | ✓ | ✓ | POKE | EXP | False | NapCat 同 handler 数组别名 |
| `group_poke` | 群戳一拍 | ✗ | ✓ | ✓ | ✓ | POKE | EXP | False | NapCat 同 handler 数组别名 |
| `click_inline_keyboard_button` | 点击内联键盘按钮 | ✗ | ✓ | ✓ | ✓ | MISC | EXP | False | |
| `get_mini_app_ark` | 获取小程序卡片 ark | ✗ | ✓ | ✓ | ✓ | MISC | EXP | False | |

#### B. 群操作 / 群管理

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `get_group_list` | 获取群列表 | ✓ | ✓ | ✓ | ✓ | ACCOUNT | OB11 | False | |
| `get_group_info` | 获取群信息 | ✓ | ✓ | ✓ | ✓ | ACCOUNT | OB11 | False | |
| `get_group_info_ex` | 获取群扩展信息 | ✗ | ✓ | ✓ | ✓ | GROUP_EXT | EXP | False | |
| `get_group_detail_info` | 获取群详细信息 | ✗ | ✓ | ✓ | ✓ | ACCOUNT | NC | **True** | napcat_only 应改为 False |
| `get_group_member_list` | 获取群成员列表 | ✓ | ✓ | ✓ | ✓ | ACCOUNT | OB11 | False | |
| `get_group_member_info` | 获取群成员信息 | ✓ | ✓ | ✓ | ✓ | ACCOUNT | OB11 | False | |
| `get_group_honor_info` | 获取群荣誉信息 | ✓ | ✓ | ✓ | ✓ | ACCOUNT | OB11 | False | |
| `get_group_system_msg` | 获取群系统消息 | ✓ | ✓ | ✓ | ✓ | REQUEST | GOCQ | False | source 应改为 OB11 |
| `get_group_at_all_remain` | 获取群 @全体 剩余次数 | ✗ | ✓ | ✓ | ✓ | NAPCAT_EXT | GOCQ | False | |
| `get_group_shut_list` | 获取群禁言列表 | ✗ | ✓ | ✓ | ✓ | GROUP_EXT | EXP | False | |
| `get_group_signed_list` | 获取群今日打卡列表 | ✗ | ✓ | ✓ | ✗ | - | - | - | OE 未包装 |
| `get_group_ignored_notifies` | 获取被过滤入群请求 | ✗ | ✓ | ✓ | ✓ | GROUP_EXT | EXP | False | |
| `get_group_ignore_add_request` | 获取被忽略入群请求 | ✗ | ✓ | ✓ | ✓ | GROUP_EXT | EXP | False | |
| `get_group_add_request` | 获取群添加请求 | ✗ | ✓ | ✗ | ✓ | REQUEST | NC | True | SnowLuma 未实现 |
| `set_group_kick` | 群组踢人 | ✓ | ✓ | ✓ | ✓ | GROUP | OB11 | False | |
| `set_group_kick_members` | 批量踢出群成员 | ✗ | ✓ | ✓ | ✓ | GROUP_EXT | EXP | False | |
| `set_group_ban` | 群组单人禁言 | ✓ | ✓ | ✓ | ✓ | GROUP | OB11 | False | |
| `set_group_whole_ban` | 群组全员禁言 | ✓ | ✓ | ✓ | ✓ | GROUP | OB11 | False | |
| `set_group_admin` | 设置/取消管理员 | ✓ | ✓ | ✓ | ✓ | GROUP | OB11 | False | |
| `set_group_card` | 设置群名片 | ✓ | ✓ | ✓ | ✓ | GROUP | OB11 | False | |
| `set_group_name` | 设置群名 | ✓ | ✓ | ✓ | ✓ | GROUP | OB11 | False | |
| `set_group_leave` | 退出群组 | ✓ | ✓ | ✓ | ✓ | GROUP | OB11 | False | |
| `set_group_special_title` | 设置群专属头衔 | ✓ | ✓ | ✓ | ✓ | GROUP | OB11 | False | |
| `set_group_anonymous` | 群组匿名开关 | ✓ | ○ | ○ | ✓ | GROUP | OB11 | False | 两端均为 no-op |
| `set_group_anonymous_ban` | 群组匿名禁言 | ✓ | ○ | ○ | ✓ | GROUP | OB11 | False | 两端均为 no-op |
| `set_group_portrait` | 设置群头像 | ✗ | ✓ | ✓ | ✓ | GROUP_EXT | EXP | False | |
| `set_group_remark` | 设置群备注 | ✗ | ✓ | ✓ | ✓ | GROUP_EXT | EXP | False | |
| `set_group_add_option` | 设置加群选项 | ✗ | ✓ | ✓ | ✓ | GROUP_EXT | EXP | False | |
| `set_group_search` | 允许群被搜索 | ✗ | ✓ | ✓ | ✓ | GROUP_EXT | EXP | False | |
| `set_group_robot_add_option` | 设置群机器人加群选项 | ✗ | ✓ | ✓ | ✓ | GROUP_EXT | EXP | False | |
| `set_group_sign` | 群签到（主名）| ✗ | ✓ | ✓ | ✓ | GROUP_EXT | EXP | False | 别名：send_group_sign |
| `send_group_sign` | 群签到（别名）| ✗ | ✓ | ✓ | ✗ | - | - | - | NapCat 同 handler 数组别名，OE 应纳入 aliases |
| `set_group_todo` | 设置群待办 | ✗ | ✓ | ✓ | ✓ | GROUP_TODO | EXP | False | |
| `complete_group_todo` | 完成群待办 | ✗ | ✓ | ✓ | ✓ | GROUP_TODO | EXP | False | |
| `cancel_group_todo` | 取消群待办 | ✗ | ✓ | ✓ | ✓ | GROUP_TODO | EXP | False | |

#### C. 群文件 / 文件操作

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `upload_file` | 上传文件 | ✗ | ✗ | ✗ | ✓ | FILE | OB11 | False | OE 自定义，标准无此 action |
| `upload_group_file` | 上传群文件 | ✗ | ✓ | ✓ | ✓ | FILE | OB11 | False | source 应为 GOCQ |
| `upload_private_file` | 上传私聊文件 | ✗ | ✓ | ✓ | ✓ | FILE | OB11 | False | source 应为 GOCQ |
| `get_file` | 获取文件信息 | ✗ | ✓ | ✓ | ✓ | FILE | NC | **True** | napcat_only 应改为 False |
| `get_file_url` | 获取文件下载 URL | ✗ | ✓ | ✓ | ✓ | FILE | NC | **True** | napcat_only 应改为 False |
| `get_image` | 获取图片信息 | ✓ | ✓ | ✓ | ✓ | FILE | OB11 | False | |
| `get_record` | 获取语音信息 | ✓ | ✓ | ✓ | ✓ | FILE | OB11 | False | |
| `get_group_file_url` | 获取群文件下载链接 | ✗ | ✓ | ✓ | ✓ | GROUP_FILE | GOCQ | False | |
| `get_private_file_url` | 获取私聊文件下载链接 | ✗ | ✓ | ✓ | ✓ | GROUP_FILE | EXP | False | |
| `get_group_root_files` | 获取群根目录文件列表 | ✗ | ✓ | ✓ | ✓ | GROUP_FILE | GOCQ | False | |
| `get_group_files_by_folder` | 获取群子目录文件列表 | ✗ | ✓ | ✓ | ✓ | GROUP_FILE | GOCQ | False | |
| `delete_group_file` | 删除群文件 | ✗ | ✓ | ✓ | ✓ | GROUP_FILE | GOCQ | False | |
| `create_group_file_folder` | 创建群文件夹 | ✗ | ✓ | ✓ | ✓ | GROUP_FILE | GOCQ | False | |
| `delete_group_folder` | 删除群文件夹 | ✗ | ✓ | ✓ | ✓ | GROUP_FILE | GOCQ | False | |
| `delete_group_file_folder` | 删除群文件夹（SL 主名）| ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 独有 |
| `rename_group_file` | 重命名群文件 | ✗ | ✓ | ✓ | ✓ | GROUP_FILE | EXP | False | |
| `rename_group_file_folder` | 重命名群文件夹 | ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 独有 |
| `move_group_file` | 移动群文件 | ✗ | ✓ | ✓ | ✓ | GROUP_FILE | EXP | False | |
| `trans_group_file` | 转存群文件 | ✗ | ✓ | ○ | ✓ | GROUP_FILE | EXP | False | SnowLuma 未实现 |
| `get_group_file_system_info` | 获取群文件系统信息 | ✗ | ✓ | ✓ | ✓ | GROUP_FILE | GOCQ | False | |
| `download_file` | 下载文件到本地 | ✗ | ✓ | ✓ | ✓ | CRED | EXP | False | |
| `check_url_safely` | 检查 URL 安全性 | ✗ | ✓ | ○ | ✓ | CRED | EXP | False | SnowLuma 占位 |
| `ocr_image` | OCR 图片（主名）| ✗ | ✓ | ✓ | ✓ | CRED | EXP | False | 别名：.ocr_image；source 应为 GOCQ |
| `.ocr_image` | OCR 图片（别名）| ✗ | ✓ | ✓ | ✗ | - | - | - | NapCat 同 handler 数组别名，OE 应纳入 aliases |
| `get_rkey` | 获取下载 rkey（主名）| ✗ | ✓ | ✓ | ✓ | CRED | EXP | False | 别名：nc_get_rkey |
| `nc_get_rkey` | 获取 rkey（旧名）| ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 旧名，OE 应纳入 aliases |
| `get_rkey_server` | 获取 rkey 服务器信息 | ✗ | ✓ | ✓ | ✗ | - | - | - | OE 未包装 |

#### D. 闪传 / 文件集

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `create_flash_task` | 创建闪传任务 | ✗ | ✓ | ✓ | ✓ | FLASH | EXP | False | |
| `send_flash_msg` | 发送闪传消息 | ✗ | ✓ | ✓ | ✓ | FLASH | EXP | False | |
| `get_flash_file_list` | 获取闪传文件列表 | ✗ | ✓ | ✓ | ✓ | FLASH | EXP | False | |
| `get_flash_file_url` | 获取闪传文件链接 | ✗ | ✓ | ✓ | ✓ | FLASH | EXP | False | |
| `get_share_link` | 获取文件分享链接 | ✗ | ✓ | ✓ | ✓ | FLASH | EXP | False | |
| `download_fileset` | 下载文件集 | ✗ | ✓ | ✓ | ✓ | FLASH | EXP | False | |
| `get_fileset_info` | 获取文件集信息 | ✗ | ✓ | ✓ | ✓ | FLASH | EXP | False | |
| `get_fileset_id` | 从分享码获取 fileset_id | ✗ | ✓ | ✓ | ✓ | FLASH | EXP | False | |
| `list_filesets` | 列出所有闪传文件集 | ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 独有 |
| `delete_flash_file` | 删除闪传文件 | ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 独有 |
| `rename_flash_file` | 重命名闪传文件 | ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 独有 |

#### E. 在线文件（NapCat 独有）

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `send_online_file` | 发送在线文件 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |
| `send_online_folder` | 发送在线文件夹 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |
| `get_online_file_msg` | 获取在线文件消息列表 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |
| `receive_online_file` | 接收在线文件 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |
| `refuse_online_file` | 拒绝在线文件 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |
| `cancel_online_file` | 取消在线文件 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |

#### F. 流式传输（NapCat 独有）

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `clean_stream_temp_file` | 清理流式传输临时文件 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |
| `upload_file_stream` | 上传文件流（分块）| ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |
| `download_file_stream` | 下载文件流（分块）| ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |
| `download_file_record_stream` | 下载语音文件流 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |
| `download_file_image_stream` | 下载图片文件流 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |
| `test_download_stream` | 测试下载流 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |

#### G. 群公告

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `_send_group_notice` | 发送群公告 | ✗ | ✓ | ✓ | ✓ | GROUP_NOTICE | EXP | False | |
| `_get_group_notice` | 获取群公告 | ✗ | ✓ | ✓ | ✓ | GROUP_NOTICE | EXP | False | |
| `_del_group_notice` | 删除群公告 | ✗ | ✓ | ✓ | ✓ | GROUP_NOTICE | EXP | False | |

#### H. 群精华消息

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `get_essence_msg_list` | 获取群精华消息列表 | ✗ | ✓ | ✓ | ✓ | NAPCAT_EXT | NC | **True** | napcat_only 应改为 False；source 应为 GOCQ |
| `set_essence_msg` | 设置精华消息 | ✗ | ✓ | ✓ | ✓ | NAPCAT_EXT | GOCQ | False | |
| `delete_essence_msg` | 移除精华消息 | ✗ | ✓ | ✓ | ✓ | NAPCAT_EXT | GOCQ | False | |

#### I. 请求处理

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `set_friend_add_request` | 处理好友添加请求 | ✓ | ✓ | ✓ | ✓ | REQUEST | OB11 | False | 常量类应搬至 OneBotAction |
| `set_group_add_request` | 处理加群请求/邀请 | ✓ | ✓ | ✓ | ✓ | REQUEST | OB11 | False | 常量类应搬至 OneBotAction |
| `get_doubt_friends_add_request` | 获取可疑好友申请 | ✗ | ✓ | ✓ | ✓ | REQUEST | EXP | False | |
| `set_doubt_friends_add_request` | 处理可疑好友申请 | ✗ | ✓ | ✓ | ✓ | REQUEST | EXP | False | |

#### J. 好友 / 用户

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `get_login_info` | 获取登录号信息 | ✓ | ✓ | ✓ | ✓ | ACCOUNT | OB11 | False | |
| `get_stranger_info` | 获取陌生人信息 | ✓ | ✓ | ✓ | ✓ | ACCOUNT | OB11 | False | |
| `get_friend_list` | 获取好友列表 | ✓ | ✓ | ✓ | ✓ | ACCOUNT | OB11 | False | |
| `get_friends_with_category` | 获取分组好友列表 | ✗ | ✓ | ✓ | ✓ | USER_EXT | EXP | False | |
| `get_unidirectional_friend_list` | 获取单向好友列表 | ✗ | ✓ | ✓ | ✓ | USER_EXT | EXP | False | |
| `get_recent_contact` | 获取最近会话 | ✗ | ✓ | ○ | ✓ | USER_EXT | EXP | False | SnowLuma 占位 |
| `delete_friend` | 删除好友 | ✗ | ✓ | ✓ | ✓ | USER_EXT | EXP | False | |
| `set_friend_remark` | 设置好友备注 | ✗ | ✓ | ✓ | ✓ | USER_EXT | EXP | False | |
| `get_profile_like` | 获取资料点赞 | ✗ | ✓ | ✓ | ✓ | USER_EXT | EXP | False | |
| `set_qq_profile` | 设置 QQ 资料 | ✗ | ✓ | ✓ | ✓ | USER_EXT | EXP | False | source 应为 GOCQ |
| `set_qq_avatar` | 设置 QQ 头像 | ✗ | ✓ | ✓ | ✓ | USER_EXT | EXP | False | |
| `set_self_longnick` | 设置个性签名 | ✗ | ✓ | ✓ | ✓ | USER_EXT | EXP | False | |
| `get_robot_uin_range` | 获取机器人 UIN 范围 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |

#### K. 在线状态

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `set_online_status` | 设置在线状态 | ✗ | ✓ | ✓ | ✓ | STATUS | EXP | False | |
| `set_diy_online_status` | 设置自定义在线状态 | ✗ | ✓ | ✓ | ✓ | STATUS | EXP | False | |
| `set_input_status` | 设置输入状态 | ✗ | ✓ | ✓ | ✓ | STATUS | EXP | False | |
| `nc_get_user_status` | 获取用户在线状态 | ✗ | ✓ | ✓ | ✓ | STATUS | EXP | False | |

#### L. 表情 / 自定义表情

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `fetch_custom_face` | 获取收藏表情 | ✗ | ✓ | ✓ | ✓ | EMOJI_EXT | EXP | False | |
| `add_custom_face` | 添加收藏表情 | ✗ | ✓ | ✓ | ✓ | EMOJI_EXT | EXP | False | |
| `delete_custom_face` | 删除收藏表情 | ✗ | ✓ | ✓ | ✓ | EMOJI_EXT | EXP | False | |
| `fetch_custom_face_detail` | 获取自定义表情详情 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |
| `set_custom_face_desc` | 修改自定义表情描述 | ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 独有，OE 未包装 |
| `modify_custom_face` | 修改收藏表情备注 | ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 独有，OE 未包装 |
| `move_custom_face_to_front` | 收藏表情移到最前 | ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 独有，OE 未包装 |

#### M. AI 语音

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `get_ai_characters` | 获取 AI 角色列表 | ✗ | ✓ | ✓ | ✓ | AI_VOICE | EXP | False | |
| `get_ai_record` | 获取 AI 语音 URL | ✗ | ✓ | ✓ | ✓ | AI_VOICE | EXP | False | |
| `send_group_ai_record` | 发送群 AI 语音 | ✗ | ✓ | ✓ | ✓ | AI_VOICE | EXP | False | |

#### N. 凭证

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `get_cookies` | 获取 Cookies | ✓ | ✓ | ✓ | ✓ | NAPCAT_EXT | NC | **True** | napcat_only 应改为 False |
| `get_csrf_token` | 获取 CSRF Token | ✓ | ✓ | ✓ | ✓ | NAPCAT_EXT | NC | **True** | napcat_only 应改为 False |
| `get_credentials` | 获取凭证 | ✓ | ✓ | ✓ | ✓ | CRED | EXP | False | |
| `get_clientkey` | 获取 clientkey | ✗ | ✓ | ✓ | ✓ | CRED | EXP | False | |

#### O. 系统状态 / 能力检查

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `get_status` | 获取运行状态 | ✓ | ✓ | ✓ | ✓ | NAPCAT_EXT | NC | False | |
| `get_version_info` | 获取版本信息 | ✓ | ✓ | ✓ | ✓ | NAPCAT_EXT | NC | False | |
| `can_send_image` | 是否支持发送图片 | ✓ | ✓ | ✓ | ✓ | NAPCAT_EXT | NC | False | |
| `can_send_record` | 是否支持发送语音 | ✓ | ✓ | ✓ | ✓ | NAPCAT_EXT | NC | False | |
| `set_restart` | 重启 OneBot 实现 | ✓ | ✓ | ○ | ✓ | NAPCAT_EXT | NC | **True** | napcat_only 应改为 False |
| `clean_cache` | 清理缓存 | ✓ | ✓ | ○ | ✓ | NAPCAT_EXT | NC | **True** | napcat_only 应改为 False |
| `bot_exit` | 退出机器人 | ✗ | ✓ | ✓ | ✓ | MISC | EXP | False | |
| `nc_get_packet_status` | 获取 packet 状态 | ✗ | ✓ | ○ | ✓ | MISC | EXP | False | SnowLuma 占位 |
| `get_online_clients` | 获取在线客户端列表 | ✗ | ✓ | ○ | ✓ | NAPCAT_EXT | NC | **True** | napcat_only 应改为 False；SnowLuma 占位 |

#### P. 机型 / 其他

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `._get_model_show` | 获取机型展示 | ✗ | ✓ | ○ | ✓ | MISC | EXP | False | SnowLuma mock |
| `._set_model_show` | 设置机型展示 | ✗ | ✓ | ○ | ✓ | MISC | EXP | False | SnowLuma 占位 |
| `translate_en2zh` | 英译中 | ✗ | ✓ | ✓ | ✓ | MISC | EXP | False | |
| `create_collection` | 创建收藏 | ✗ | ✓ | ○ | ✓ | MISC | EXP | False | SnowLuma 未实现 |
| `get_collection_list` | 获取收藏列表 | ✗ | ✓ | ○ | ✓ | MISC | EXP | False | SnowLuma 占位 |
| `send_packet` | 发送原始 SSO 包（主名）| ✗ | ✓ | ✓ | ✓ | MISC | EXP | False | 别名：.send_packet |
| `.send_packet` | 发送 SSO 包（别名）| ✗ | ✓ | ✓ | ✗ | - | - | - | OE 应纳入 aliases |
| `request_decrypt_key` | 请求数据库解密密钥 | ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 独有，OE 未包装 |
| `.handle_quick_operation` | 快速操作（隐藏 API）| ○ | ✓ | ✓ | ✗ | - | - | - | OneBot v11 隐藏 API，OE 未包装 |
| `.get_word_slices` | 中文分词（NapCat 未注册）| ✗ | ○ | ✗ | ✗ | - | - | - | NapCat 枚举有定义但无 handler |

#### Q. 群相册

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `get_qun_album_list` | 获取群相册列表（NapCat 名）| ✗ | ✓ | ✓ | ✓ | GROUP_ALBUM | EXP | False | |
| `get_group_album_list` | 获取群相册列表（SnowLuma 主名）| ✗ | ✗ | ✓ | ✗ | - | - | - | SnowLuma 独有名，OE 未包装 |
| `upload_image_to_qun_album` | 上传图片到群相册 | ✗ | ✓ | ✓ | ✓ | GROUP_ALBUM | EXP | False | |
| `get_group_album_media_list` | 获取群相册媒体列表 | ✗ | ✓ | ✓ | ✓ | GROUP_ALBUM | EXP | False | |
| `do_group_album_comment` | 评论群相册 | ✗ | ✓ | ✓ | ✓ | GROUP_ALBUM | EXP | False | |
| `set_group_album_media_like` | 点赞群相册媒体 | ✗ | ✓ | ✓ | ✓ | GROUP_ALBUM | EXP | False | |
| `cancel_group_album_media_like` | 取消点赞群相册媒体 | ✗ | ✓ | ✓ | ✓ | GROUP_ALBUM | EXP | False | |
| `del_group_album_media` | 删除群相册媒体 | ✗ | ✓ | ✓ | ✓ | GROUP_ALBUM | EXP | False | |

#### R. QQ 空间

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `get_qzone_msg_list` | 获取说说列表 | ✗ | ✗ | ✓ | ✓ | QZONE | EXP | False | |
| `get_qzone_feeds` | 获取好友动态 | ✗ | ✗ | ✓ | ✓ | QZONE | EXP | False | SnowLuma 独有，OE 已包装 |
| `send_qzone_msg` | 发表说说 | ✗ | ✗ | ✓ | ✓ | QZONE | EXP | False | |
| `delete_qzone_msg` | 删除说说 | ✗ | ✗ | ✓ | ✓ | QZONE | EXP | False | |
| `like_qzone` | 给说说点赞 | ✗ | ✗ | ✓ | ✓ | QZONE | EXP | False | |
| `unlike_qzone` | 取消点赞说说 | ✗ | ✗ | ✓ | ✓ | QZONE | EXP | False | |
| `comment_qzone` | 评论说说 | ✗ | ✗ | ✓ | ✓ | QZONE | EXP | False | |

#### S. Ark 分享

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `share_peer` | 分享用户 Ark 卡片 | ✗ | ✗ | ✓ | ✓ | ARK | EXP | False | SnowLuma 主名 |
| `send_ark_share` | 分享 Ark 卡片（NapCat 名）| ✗ | ✓ | ✓ | ✓ | ARK | EXP | False | 功能等价 share_peer |
| `share_group_ex` | 分享群 Ark 卡片 | ✗ | ✗ | ✓ | ✓ | ARK | EXP | False | SnowLuma 主名 |
| `send_group_ark_share` | 分享群 Ark（NapCat 名）| ✗ | ✓ | ✓ | ✓ | ARK | EXP | False | 功能等价 share_group_ex |
| `ArkSharePeer` | 分享用户 Ark（废弃旧名）| ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 已废弃，OE 未包装 |
| `ArkShareGroup` | 分享群 Ark（废弃旧名）| ✗ | ✓ | ✗ | ✗ | - | - | - | NapCat 已废弃，OE 未包装 |

#### T. QQ 频道（NapCat 空实现）

| Action | 功能 | 标准 | NC | SL | OE | OE 分类 | OE source | OE napcat_only | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| `get_guild_list` | 获取频道列表 | ✗ | ○ | ✗ | ✗ | - | - | - | NapCat 空实现，OE 未包装 |
| `get_guild_service_profile` | 获取频道个人信息 | ✗ | ○ | ✗ | ✗ | - | - | - | NapCat 空实现，OE 未包装 |

### 13.4 三方对照统计汇总

#### 按实现状态统计

| 状态 | 数量 | 说明 |
|---|---|---|
| 三方都实现 | 约 150 个 | OneBot v11 标准 + 大部分扩展 |
| 仅 NapCat 实现 | 19 个 | 在线文件 6 + 流式 6 + 频道 2 + 表情详情 2 + 其他 3 |
| 仅 SnowLuma 实现 | 11 个 | 表情管理 2 + 闪传管理 3 + 解密密钥 1 + 转发上传 2 + 群反应 1 + 文件夹 2 |
| OneBot v11 标准但实现不全 | 少量 | 如 set_restart 在 SnowLuma 是不支持 |
| OE 已包装 | 158 个 | 当前 |
| OE 未包装但三方有 | 约 30 个 | 见附录 A |

#### 按来源+实现交叉统计（OE 当前 158 个）

| OE source | 数量 | 其中 napcat_only=True | 应改为 False 数 |
|---|---|---|---|
| ONEBOT_V11 | 约 35 | 0 | 0 |
| NAPCAT_EXT | 15 | 12 | 12 |
| GOCQHTTP_COMPAT | 约 20 | 0 | 0 |
| EXPAND | 约 88 | 0 | 0 |

### 13.5 别名组完整对照

| 主名 | 别名 | NapCat 实现 | SnowLuma 实现 | OE 当前 | OE 应纳入 |
|---|---|---|---|---|---|
| `get_rkey` | `nc_get_rkey` | 同 handler 数组 | 独立 defineAction | 主名已包装，别名未 | ✓ 纳入 aliases |
| `set_group_sign` | `send_group_sign` | 同 handler 数组 | 同 handler 数组 | 主名已包装，别名未 | ✓ 纳入 aliases |
| `send_packet` | `.send_packet` | 同 handler 数组 | 同 handler 数组 | 主名已包装，别名未 | ✓ 纳入 aliases |
| `ocr_image` | `.ocr_image` | 同 handler 数组 | 同 handler 数组 | 主名已包装，别名未 | ✓ 纳入 aliases |
| `fetch_ptt_text` | `get_ptt_text`, `get_record_text` | 同 handler 数组 | 同 handler 数组 | 主名已包装，别名未 | ✓ 纳入 aliases |
| `send_poke` | `friend_poke`, `group_poke` | 同 handler 共享实现 | 独立 defineAction | 三者都包装为独立 API | ✗ 不纳入（实现独立）|
| `share_peer` | `send_ark_share` | 独立 defineAction | 独立 defineAction | 三者都包装为独立 API | ✗ 不纳入（实现独立）|
| `share_group_ex` | `send_group_ark_share` | 独立 defineAction | 独立 defineAction | 三者都包装为独立 API | ✗ 不纳入（实现独立）|

### 13.6 napcat_only 标志错误统计

SnowLuma 实际支持但 OE 标 `napcat_only=True` 的 12 个 API：

| Action | SnowLuma 实现位置 | SnowLuma 状态 |
|---|---|---|
| `send_poke` | actions/extended.ts:177 | ✓ 已实现（自动路由）|
| `send_forward_msg` | actions/extended.ts:1979 | ✓ 已实现（自动路由）|
| `get_file` | actions/extended.ts:1643 | ✓ 已实现（图片/语音缓存）|
| `get_file_url` | actions/group-file.ts:59 | ✓ 已实现 |
| `get_group_detail_info` | actions/extended.ts:1611 | ✓ 已实现 |
| `set_msg_emoji_like` | actions/extended.ts:710 | ✓ 已实现 |
| `get_essence_msg_list` | actions/extended.ts:915 | ✓ 已实现 |
| `get_online_clients` | actions/extended.ts:1224 | ○ 占位 |
| `get_cookies` | actions/extended.ts:593 | ✓ 已实现（指定域名）|
| `get_csrf_token` | actions/extended.ts:616 | ✓ 已实现 |
| `set_restart` | actions/extended.ts:665 | ○ 不支持但有响应 |
| `clean_cache` | actions/extended.ts:674 | ○ no-op |

### 13.7 source 标注矛盾统计

OE 当前 source 与常量类归属矛盾的 6 个 API：

| Action | OE source | OE 常量类 | 应改为 source | 应搬到常量类 | 原因 |
|---|---|---|---|---|---|
| `set_friend_add_request` | ONEBOT_V11 | ExpandAction | ONEBOT_V11 ✓ | OneBotAction | OneBot v11 标准 |
| `set_group_add_request` | ONEBOT_V11 | ExpandAction | ONEBOT_V11 ✓ | OneBotAction | OneBot v11 标准 |
| `get_group_system_msg` | GOCQHTTP_COMPAT | GoCqhttpCompatAction | ONEBOT_V11 | OneBotAction | OneBot v11 标准 |
| `set_qq_profile` | EXPAND | ExpandAction | GOCQHTTP_COMPAT | GoCqhttpCompatAction | NapCat 在 go-cqhttp 目录实现 |
| `ocr_image` | EXPAND | ExpandAction | GOCQHTTP_COMPAT | GoCqhttpCompatAction | go-cqhttp 兼容 |
| `get_essence_msg_list` | NAPCAT_EXT | NapCatAction | GOCQHTTP_COMPAT | GoCqhttpCompatAction | go-cqhttp 兼容 |

## 14. 附录

### 附录 A：未覆盖 API 清单

NapCatQQ/SnowLuma 有但 onebot_expand 未包装的 API（不在本次重构范围），共 30 个：

#### A.1 NapCatQQ 独有（19 个）

**流式传输系列（6 个）**：
- `clean_stream_temp_file` — 清理流式传输临时文件
- `upload_file_stream` — 上传文件流（分块）
- `download_file_stream` — 下载文件流（分块）
- `download_file_record_stream` — 下载语音文件流（含格式转换）
- `download_file_image_stream` — 下载图片文件流
- `test_download_stream` — 测试下载流

**在线文件系列（6 个）**：
- `send_online_file` — 发送在线文件
- `send_online_folder` — 发送在线文件夹
- `get_online_file_msg` — 获取在线文件消息列表
- `receive_online_file` — 接收在线文件
- `refuse_online_file` — 拒绝在线文件
- `cancel_online_file` — 取消在线文件

**QQ 频道（2 个，空实现）**：
- `get_guild_list` — 获取频道列表
- `get_guild_service_profile` — 获取频道个人信息

**自定义表情扩展（2 个）**：
- `fetch_custom_face_detail` — 获取自定义表情详情列表
- `set_custom_face_desc` — 修改自定义表情描述

**其他（3 个）**：
- `get_robot_uin_range` — 获取机器人 UIN 范围
- `ArkSharePeer` — 分享用户 Ark（已废弃旧名）
- `ArkShareGroup` — 分享群 Ark（已废弃旧名）

#### A.2 SnowLuma 独有（11 个）

- `modify_custom_face` — 修改收藏表情备注
- `move_custom_face_to_front` — 收藏表情移到最前
- `list_filesets` — 列出所有闪传文件集
- `delete_flash_file` — 删除闪传文件
- `rename_flash_file` — 重命名闪传文件
- `request_decrypt_key` — 请求数据库解密密钥
- `upload_forward_msg` — 上传转发消息（返回 res_id）
- `upload_foward_msg` — 上传转发消息（拼写错误别名）
- `set_group_reaction` — 群聊表情回应
- `delete_group_file_folder` — 删除群文件夹
- `rename_group_file_folder` — 重命名群文件夹

### 附录 B：完整别名组表

| 主名 | aliases | source | category | 行号 |
|---|---|---|---|---|
| `get_rkey` | `("nc_get_rkey",)` | EXPAND | CRED | 1602 |
| `set_group_sign` | `("send_group_sign",)` | EXPAND | GROUP_EXT | 1289 |
| `send_packet` | `(".send_packet",)` | EXPAND | MISC | 1720 |
| `ocr_image` | `(".ocr_image",)` | GOCQHTTP_COMPAT | CRED | 1618 |
| `fetch_ptt_text` | `("get_ptt_text", "get_record_text")` | EXPAND | NAPCAT_EXT | 1039 |

### 附录 C：完整 source 修正表

| 行号 | action | 当前 source | 应改为 | 当前常量类 | 应搬到 |
|---|---|---|---|---|---|
| 1303 | set_friend_add_request | ONEBOT_V11 | ONEBOT_V11 ✓ | ExpandAction | OneBotAction |
| 1314 | set_group_add_request | ONEBOT_V11 | ONEBOT_V11 ✓ | ExpandAction | OneBotAction |
| 1326 | get_group_system_msg | GOCQHTTP_COMPAT | ONEBOT_V11 | GoCqhttpCompatAction | OneBotAction |
| 1396 | set_qq_profile | EXPAND | GOCQHTTP_COMPAT | ExpandAction | GoCqhttpCompatAction |
| 1618 | ocr_image | EXPAND | GOCQHTTP_COMPAT | ExpandAction | GoCqhttpCompatAction |
| 919 | get_essence_msg_list | NAPCAT_EXT | GOCQHTTP_COMPAT | NapCatAction | GoCqhttpCompatAction |

### 附录 D：完整 napcat_only 修正表

| 行号 | action | 当前 napcat_only | 应改为 | 当前 snowluma_compat | 应改为 |
|---|---|---|---|---|---|
| 515 | send_poke | True | False | False | True |
| 533 | send_forward_msg | True | False | False | True |
| 784 | get_file | True | False | False | True |
| 815 | get_file_url | True | False | False | True |
| 889 | get_group_detail_info | True | False | False | True |
| 913 | set_msg_emoji_like | True | False | False | True |
| 924 | get_essence_msg_list | True | False | False | True |
| 934 | get_online_clients | True | False | False | True |
| 945 | get_cookies | True | False | False | True |
| 954 | get_csrf_token | True | False | False | True |
| 974 | set_restart | True | False | False | True |
| 983 | clean_cache | True | False | False | True |

### 附录 E：API 数量对照

| 项目 | 独立 action | 含别名 | 备注 |
|---|---|---|---|
| OneBot v11 标准 | 39 | 39 | 38 公开 + 1 隐藏 |
| NapCatQQ | 176 | 176 | 每个 action 自动派生 `_async` / `_rate_limited` |
| SnowLuma | 172 | 178 | 6 个别名 |
| **onebot_expand（当前）** | **158** | **158** | 无别名机制 |
| **onebot_expand（重构后）** | **158** | **163** | 5 组纯别名（5 个主名 + 6 个别名 action 串）|

### 附录 F：相关文件路径

- 主文件：`E:\codearts\1`\Neo-MoFox\plugins\onebot_expand\api_defs.py`
- 配置：`E:\codearts\1`\Neo-MoFox\plugins\onebot_expand\config.py`
- 插件入口：`E:\codearts\1`\Neo-MoFox\plugins\onebot_expand\plugin.py`
- Tool 层：`E:\codearts\1`\Neo-MoFox\plugins\onebot_expand\tools\`
- Service 层：`E:\codearts\1`\Neo-MoFox\plugins\onebot_expand\services\`
- 配置文件：`config/plugins/onebot_expand/config.toml`

### 附录 G：NapCatQQ & SnowLuma API 全集参考

完整 API 清单见记忆文件：
`C:\Users\Administrator\.claude\projects\E--codearts-1--Neo-MoFox-plugins-onebot-expand\memory\napcat_snowluma_apis.md`

---

## 文档结束

本文档涵盖：
- ✅ 当前状态分析（文件结构、现有机制、问题统计）
- ✅ 完整问题清单（6 类问题，逐条列出）
- ✅ 别名机制设计（schema、默认值、兼容性）
- ✅ 主名选取规则（6 条优先级）
- ✅ 别名组完整清单（5 组纯别名 + 3 组语义等价）
- ✅ source 标注修正清单（6 个 API）
- ✅ napcat_only 标志修正清单（12 个 API）
- ✅ 加载期校验设计（6 项检查 + 伪代码）
- ✅ Service 层集成设计（resolve_action + 调用流程）
- ✅ 配置开关设计（主名生成 + 别名映射）
- ✅ 迁移步骤（4 阶段 19 步）
- ✅ 风险评估（7 项风险 + 缓解）
- ✅ **三方 API 完整对照表（13 章，覆盖 OneBot v11 标准 39 + NapCatQQ 176 + SnowLuma 172 + onebot_expand 158，按 A-T 共 20 个功能域分组的完整字典序对照）**
- ✅ 附录（未覆盖 API 30 个、别名组表、修正表、数量对照、文件路径）
