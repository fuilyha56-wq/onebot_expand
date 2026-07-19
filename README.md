# OneBot Expand

> OneBot v11 + NapCat 扩展 API 完整封装插件，通过 `onebot_adapter` 调用 NapCat / SnowLuma / LLBot 等协议端的全部扩展能力。

> 老实说，我并不清楚这是否违背了我的中心，在最开始只是想提供一点方便的api供后续的插件调用。不过……在这次执行中，我提供了一套简易的message id和对应的适配，让llm更方便的构建消息类型和使用工具。

| 指标 | 值 |
|---|---|
| 版本 | 1.0.6 |
| Tool 组件 | **205** 个 |
| Service 组件 | **23** 个 |
| 依赖插件 | `onebot_adapter` |
| 协议端兼容 | NapCat · SnowLuma · LLBot（按 API 单独标记兼容性） |

## 功能概览

| 模块 | Tool 数 | Service | 说明 |
|---|---|---|---|
| 消息 | 20 | MessageService | 群/私聊消息发送、转发、撤回、已读标记 |
| 群操作 | 10 | GroupService | 禁言、踢出、管理、头衔等 |
| 文件操作 | 16 | FileService | 群/私聊文件上传、图片/语音获取、在线文件、流式传输 |
| 账号信息 | 10 | AccountService | 登录号、好友、群列表与详情查询 |
| NapCat 扩展 | 15 | NapcatExtService | Cookies、CSRF、状态、精华消息等 |
| 群文件管理 | 13 | GroupFileService | 群文件 CRUD、文件夹、转存、永久保存 |
| 群公告 | 3 | GroupNoticeService | 群公告发布/查询/删除 |
| 群管理扩展 | 14 | GroupExtService | 群头像/备注/加群选项/签到/打卡列表/批量踢出/消息屏蔽 |
| 请求处理 | 5 | RequestService | 好友/加群请求处理 |
| 用户信息扩展 | 13 | UserExtService | 好友备注/分类/单向好友/资料/头像/点赞 |
| 在线状态 | 4 | StatusService | 在线状态/DIY状态/输入状态 |
| 戳一拍 | 2 | PokeService | 好友/群戳一拍 |
| 表情/收藏扩展 | 12 | EmojiExtService | 收藏表情CRUD/详情/备注/移动/回应/推荐表情 |
| AI语音 | 3 | AiVoiceService | AI角色/语音生成 |
| 凭证/安全/下载 | 8 | CredService | clientkey/credentials/rkey/URL安全/OCR/下载/解密 |
| 机型/其他 | 18 | MiscService | 机型/退出/包状态/内联键盘/小程序/翻译/收藏/SSO包/快速操作/分词/配置/事件/调试/扫码/频道 |
| 闪传 | 14 | FlashService | 闪传任务/消息/文件列表/URL/分享/下载/文件集CRUD/上传/重分享 |
| 群相册 | 9 | GroupAlbumService | 群相册列表/上传/评论/点赞/删除/创建 |
| 群待办 | 3 | GroupTodoService | 群待办设置/完成/取消 |
| QQ空间 | 9 | QzoneService | 说说列表/动态/发表/删除/点赞/评论/拉黑/权限 |
| Ark分享 | 4 | ArkService | 用户/群Ark卡片分享 |

## 架构

### 双层组件设计

- **Tool 层**：每个 API 对应一个 Tool 类（共 205 个），供 LLM 直接调用
- **Service 层**：一类功能聚合为一个 Service（共 23 个），供其他插件程序化调用

### 调用链

```text
插件加载 → 按总开关和独立开关注册 Tool → LLM 调用 Tool.execute → _call_onebot_api → onebot_adapter → NapCat/SnowLuma/LLBot
其他插件 → Service.method（独立开关检查）→ _call_onebot_api → onebot_adapter → NapCat/SnowLuma/LLBot
```

### 关键机制

#### 1. Tool 总开关 `enable_all_tools`

位于 `api_switches` 节，**默认 `false`**：

- **`true`**：只注册独立开关 `enable_<action> = true` 的 Tool
- **`false`（默认）**：不注册任何 Tool，工具不会出现在 LLM 组件列表和注册日志中

✅ **Service 不受总开关影响**——始终启用，确保其他插件通过 Service 调用的路径不会中断。

#### 2. Tool 独立开关 `enable_<action>`

每个 Tool 对应一个独立开关，**默认全部 `false`**。需要启用某个 Tool 时，显式在配置里设为 `true`，并将 `enable_all_tools` 也设为 `true`。

工具开关在插件注册阶段读取。修改配置后需要重载插件或重启 Bot，注册列表才会更新。执行阶段仍保留开关检查，作为配置异常时的第二层保护。

#### 3. 别名机制

部分 action 有历史别名（如 `nc_get_rkey` → `get_rkey`、`.ocr_image` → `ocr_image`、`._get_model_show` → `_get_model_show`）。别名与主名共用同一开关和同一 handler，调用时通过 `resolve_action()` 解析为主名。

别名列表见 [ACTION_INDEX.md](./docs/ACTION_INDEX.md) 的"别名映射表"。

#### 4. 适配器兼容性标记

每个 API 在 `api_defs.py` 标记：

- `napcat_only`：True 表示 NapCat 专属，SnowLuma 不支持
- `snowluma_compat`：False 表示 SnowLuma 不兼容

调用方可根据标记选择合适的 API。详见 [ACTION_INDEX.md](./docs/ACTION_INDEX.md)。

## 配置

配置文件：`config/plugins/onebot_expand/config.toml`

### 主要配置节

| 配置节 | 说明 |
|---|---|
| `plugin` | 插件启用与版本 |
| `adapter` | 适配器签名、默认超时、协议端 |
| `api_switches` | API 级独立开关（含 `enable_all_tools` 总开关） |
| `emoji` | 表情发送与回应开关 |
| `file_transfer` | 文件传输模式（路径映射/base64/共享卷） |
| `protocol` | 协议端后端与兼容模式 |

### API 开关格式

每个 API 对应一个开关 `enable_<action>`，**默认全部 `false`**。示例：

```toml
[api_switches]
enable_all_tools = true          # Tool 总开关（默认 false，需显式开启）
enable_send_group_msg = true     # 群聊消息发送（默认 false）
enable_get_qzone_msg_list = true # QQ空间说说列表（默认 false）
# ... 共 205 个独立开关
```

✅ **Service 路径不受这些开关影响**——Service 方法始终可调用，供其他插件程序化使用。

## API 索引

完整 API 名单见 [ACTION_INDEX.md](./docs/ACTION_INDEX.md)，按分类组织，含：

- 主名 action 列表（205 个）
- 别名映射表（18 个别名）
- 每个 API 的来源标记、适配器兼容性
- 按分类统计

## 开发文档

| 文档 | 说明 |
|---|---|
| [ACTION_INDEX.md](./docs/ACTION_INDEX.md) | API 完整索引名单 |
| [API_DEFS_REFACTOR.md](./docs/API_DEFS_REFACTOR.md) | 重构历史与决策记录 |

## 模块结构

```text
onebot_expand/
├── plugin.py              # 插件入口
├── config.py              # 配置定义
├── api_defs.py            # API 元数据定义（205 个 APIDef）
├── manifest.json          # 组件清单
├── path_mapper.py         # 文件路径映射
├── emoji_tables.py        # QQ 表情映射表
├── tools/                 # 205 个 Tool 类
│   ├── __init__.py        # Tool 注册 + 总开关包装器
│   ├── message_tools.py
│   ├── group_tools.py
│   ├── file_tools.py
│   ├── account_tools.py
│   ├── napcat_tools.py
│   ├── group_file_tools.py
│   ├── group_notice_tools.py
│   ├── group_ext_tools.py
│   ├── request_tools.py
│   ├── user_ext_tools.py
│   ├── status_tools.py
│   ├── poke_tools.py
│   ├── emoji_ext_tools.py
│   ├── ai_voice_tools.py
│   ├── cred_tools.py
│   ├── misc_tools.py
│   ├── flash_tools.py
│   ├── group_album_tools.py
│   ├── group_todo_tools.py
│   ├── qzone_tools.py
│   └── ark_tools.py
├── services/              # 23 个 Service 类
│   ├── __init__.py
│   ├── message_service.py
│   ├── group_service.py
│   ├── file_service.py
│   ├── account_service.py
│   ├── napcat_service.py
│   ├── emoji_service.py
│   ├── path_mapper_service.py
│   ├── group_file_service.py
│   ├── group_notice_service.py
│   ├── group_ext_service.py
│   ├── request_service.py
│   ├── user_ext_service.py
│   ├── status_service.py
│   ├── poke_service.py
│   ├── emoji_ext_service.py
│   ├── ai_voice_service.py
│   ├── cred_service.py
│   ├── misc_service.py
│   ├── flash_service.py
│   ├── group_album_service.py
│   ├── group_todo_service.py
│   ├── qzone_service.py
│   └── ark_service.py
├── tools/__init__.py      # Tool 注册 + 总开关包装器
├── services/__init__.py   # Service 注册
├── docs/
│   ├── ACTION_INDEX.md    # API 索引名单
│   └── API_DEFS_REFACTOR.md # 重构历史
└── README.md
```

## 许可证

见 [LICENSE](../../LICENSE)。
