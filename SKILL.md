---
name: onebot-expand-sync
description: 同步 onebot_expand 插件与 NapCat/SnowLuma 上游 API，做查漏补缺、Tool 生成、Service 适配、去重与测试
when_to_use: 当需要维护 E:\plugins\onebot_expand 插件、新增/更新 API、生成 Tool/Service、或与上游 NapCat/SnowLuma 做对照时
version: 1.0.0
languages: python, typescript
---

# OneBot Expand 同步 Skill

> 一次编写永久使用。本文件是维护 `E:\plugins\onebot_expand` 插件的唯一入口。
> 后续所有维护工作都由 AI 阅读本 skill 后执行，不再修改本文件本身。

## 0. 总体目标

把 `E:\plugins\onebot_expand` 插件与两个上游协议端（NapCat、SnowLuma）的 API 保持同步：

1. 拉取两个上游仓库的最新代码
2. 扫描各自的 action 名单
3. 与本插件 `api_defs.py` 已适配的 action 做对照，找出"多/少/重复"
4. 按本文件定义的规则补全 api_defs、生成 Tool、聚合 Service
5. 默认所有 Tool 关闭，逐一测试可用性
6. 去重，处理别名

**关键铁律：**
- **Tool 默认全部关闭**（`enable_<action> = false`，`enable_all_tools = false`）。Service 路径不受开关影响，始终可用。
- **多类 Tool 规划为一个 Service**——按功能域聚合，不按 action 数量切分。
- **本插件目录**：`E:\plugins\onebot_expand`
- **NapCat 源**：`E:\NapCatQQ`
- **SnowLuma 源**：`E:\SnowLuma`
- **LLBot 源**：`E:\LLBot`
- **参考文档**：`E:\plugins\onebot_expand\docs\ACTION_INDEX.md` 与 `E:\plugins\onebot_expand\docs\API_DEFS_REFACTOR.md`（已迁移至 docs/）

## 1. 工作流（每次维护都按此顺序执行）

### Step 1 — 拉取上游最新

```bash
cd E:/SnowLuma && git pull
cd E:/NapCatQQ && git pull
cd E:/LLBot && git pull
```

如已克隆但很久未拉，先确认分支在 `main`，再 fast-forward。

### Step 2 — 扫描上游 action 名单

**NapCat 全量 action 名单**位于：

```
E:\NapCatQQ\packages\napcat-onebot\action\router.ts
```

读取其中的 `export const ActionName = { ... } as const;` 对象。每个键的字符串值就是一个 action 名。**忽略**以下项：
- `TestAutoRegister01/02`、`test_download_stream`、`unknown`（测试/占位）
- 已标注 `@deprecated` 的（如 `ArkSharePeer`、`ArkShareGroup`，已由 `share_peer`/`share_group_ex` 取代）

**SnowLuma 全量 action 名单**位于：

```
E:\SnowLuma\packages\onebot\src\actions\*.ts
```

SnowLuma 把每个 action 写成 `{ name: '<action>', ... }` 形式，注册在 `ACTION_GROUPS`（见 `actions/index.ts`）。提取方式：

```bash
cd E:/SnowLuma && grep -hoE "name:\s*'[a-z_.][a-z_0-9.]*'" packages/onebot/src/actions/*.ts \
  | grep -oE "'[a-z_.][a-z_0-9.]*'" | tr -d "'" | sort -u
```

SnowLuma 在 `api-handler.ts` 里还手动注册了 `.handle_quick_operation`，需要单独加入。

**LLBot 全量 action 名单**位于：

```
E:\LLBot\src\onebot11\action\types.ts
```

LLBot 把所有 action 名写在 `export enum ActionName { ... }` 枚举里，每个枚举成员的字符串值就是一个 action 名。提取方式：

```bash
cd E:/LLBot && grep -oE "'[a-z_.][a-z_0-9.]*'" src/onebot11/action/types.ts | tr -d "'" | sort -u
```

LLBot 的 action 分为三段（在 enum 中以注释分隔）：
- `// llbot`：LLBot 独有扩展（如 `scan_qrcode`、`create_group_album`、`batch_delete_group_member` 等）
- `// onebot 11`：OneBot v11 标准
- `// go-cqhttp`：go-cqhttp 兼容

**LLBot 独有 action**（`// llbot` 段）是同步重点，它们对应本插件 `api_defs.py` 中 `source=APISource.EXPAND` 且描述含"LLBot 扩展"的条目。LLBot 仓库根目录还提供 `llbot_actions.txt`（全量 action 文本名单，每行一个），可作为快速对照的权威清单。

**LLBot action 文件结构**：

```
E:\LLBot\src\onebot11\action\
├── types.ts              # ActionName 枚举（全量 action 名单）
├── BaseAction.ts         # action 基类
├── index.ts              # action 注册总表
├── llbot/                # LLBot 独有 action 实现
│   ├── system/           # get_config/set_config/get_event/llonebot_debug
│   ├── group/            # 群相关扩展
│   ├── msg/              # 消息相关扩展
│   ├── user/             # 用户相关扩展
│   └── file/             # 文件相关扩展
├── go-cqhttp/            # go-cqhttp 兼容 action
├── msg/ group/ file/ system/ user/  # OneBot v11 标准 action
```

每个 LLBot action 的参数 schema 在对应实现文件的 `payloadSchema` 字段（使用 schemastery 库定义），适配时参考该 schema 填写 `APIDef.params`。

### Step 3 — 与本插件对照

本插件的 action 名单在 `api_defs.py` 各 `*Action` 常量类里。提取方式：

```bash
cd E:/plugins/onebot_expand && grep -E '^\s+[A-Z_]+\s*=\s*"[a-z_.][a-z_0-9.]*"' api_defs.py \
  | grep -oE '"[a-z_.][a-z_0-9.]*"' | tr -d '"' | sort -u
```

对照规则（三方对照：NapCat + SnowLuma + LLBot）：
- **上游有、插件没有** → 进入"待适配"清单（Step 4）
- **上游没有、插件有** → 检查是否上游已废弃；若是，标记 `deprecated`，但**保留**（向后兼容）
- **两边都支持但命名不同** → 走别名机制（见 `docs/ACTION_INDEX.md` 的"别名映射表"）
- **LLBot 独有 action** → 归入 `ExpandAction` 常量类，`source=APISource.EXPAND`，描述标注"LLBot 扩展"，`napcat_only=false`、`snowluma_compat=true`（LLBot 与 SnowLuma 实现高度重合）

### Step 4 — 适配缺失 API

对每个"待适配"action，按 `docs/API_DEFS_REFACTOR.md` 已确立的方法：

1. **判断来源**：放在 `OneBotAction` / `NapCatAction` / `GoCqhttpCompatAction` / `ExpandAction` 哪个常量类
2. **在 `ALL_APIS` 字典加 `APIDef` 条目**，包含：
   - `action`、`category`、`source`
   - `napcat_only`、`snowluma_compat`（按下方兼容性表确定）
   - `params`（参考上游 TS 文件的 schema）
   - `aliases`（如有）
3. **更新 `ACTION_INDEX.md`** 的对应分类表
4. **在 `tools/<domain>_tools.py` 加 Tool 类**
5. **在 `services/<domain>_service.py` 加 Service 方法**（聚合到现有 Service）
6. **在 `config.py` 加 `enable_<action>` 开关**，默认 `false`

### Step 5 — 生成 Tool

参考现有 `tools/<domain>_tools.py` 的模板：

```python
class SendGroupMsgTool(BaseActionTool):
    action = OneBotAction.SEND_GROUP_MSG

    async def execute(self, group_id: int, message: list[dict], ...) -> dict:
        return await self._call_onebot_api(
            action=self.action,
            group_id=group_id,
            message=message,
        )
```

- 每个 action 对应一个 Tool 类
- Tool 经 `tools/__init__.py` 的总开关包装器统一注册
- **Tool 独立开关默认 `false`**，且受 `enable_all_tools` 总开关约束

### Step 6 — 聚合 Service

按功能域聚合，不要按 action 数量切分。现有 23 个 Service 边界已稳定，新增 action 优先归入对应 Service；只有出现全新功能域才新建 Service。聚合规则见 §3。

### Step 7 — 去重

- **同义 action**：选一个为主名，其余作为 `aliases`
- **历史别名**：保留在 `aliases`，共用同一开关与 handler
- **重复 Tool 类**：检查 `tools/__init__.py` 的注册列表，确保一个 action 只注册一次

### Step 8 — 测试

每个新增/修改的 API 都要：
1. 启用对应 `enable_<action>=true` 与 `enable_all_tools=true`
2. 通过 **测试适配器**（`tests/napcat_test_adapter.py`）实际调用 NapCat
3. 验证返回结构与 `APIDef.params` 声明一致
4. 测试通过后，把开关改回 `false`（保留默认关闭）

#### 测试适配器

文件：`tests/napcat_test_adapter.py`

通过 WebSocket 连接 `ws://127.0.0.1:5326`（NapCat 反向 WS 服务端），提供同步式 API 调用：

```python
from tests.napcat_test_adapter import call_napcat, is_available

# 检查 NapCat 是否可达
if not is_available():
    print("NapCat 未运行或端口未就绪")

# 调用任意 action（主名或别名）
result = call_napcat("send_msg", {
    "message_type": "private",
    "user_id": 10000,
    "message": [{"type": "text", "data": {"text": "hello"}}],
})
# result: {"status": "ok", "retcode": 0, "data": {"message_id": ...}, "echo": "..."}

# 命令行直接调用
# python -m onebot_expand.tests.napcat_test_adapter get_login_info '{}'
# python tests/napcat_test_adapter.py get_login_info '{}'
```

**SnowLuma 测试**：SnowLuma 不保证长期在线，测试可选。若 SL 在线，可临时把 `url` 参数改为 SL 的反向 WS 端口：

```python
call_napcat("send_msg", {...}, url="ws://127.0.0.1:<sl_port>")
```

#### 测试流程（每个新增 API）

```python
from onebot_expand.tests import call_napcat

# 1. 用最小合法参数调用
result = call_napcat("<action>", {<params>})

# 2. 检查 status
assert result.get("status") == "ok", f"调用失败: {result}"

# 3. 检查 data 字段存在（除非 API 声明返回 void）
# 4. 别名也要测一次（如果有别名）
```

#### 批量测试

维护后可对全部 184 个 API 跑一遍冒烟测试：

```python
from onebot_expand.api_defs import ALL_APIS
from onebot_expand.tests import call_napcat, is_available

if not is_available():
    print("跳过：NapCat 不可达")
else:
    for action, api_def in ALL_APIS.items():
        # 用空参数或最小参数调用（只读 API 适合，写操作需谨慎）
        result = call_napcat(action, {})
        status = result.get("status")
        print(f"{action}: {status}")
```

> 注意：写操作（如 `send_group_msg`、`set_group_kick`）会真实生效，测试时需用测试群/测试号。

## 2. 当前快照（截至 2026-07-08）

> 本节是参考快照，AI 在执行 Step 1-3 后应基于实际扫描结果对照，但不要修改本 skill 本身。

**当前规模**：184 个主名 action + 12 个别名，196 个可调用名。已通过 `tests/run_api_tests.py` 在 NapCat（账号 3693525299）上跑过冒烟测试，全部 action 名被协议端识别。完整报告见 `tests/api_test_report.md`。

### 2.1 已适配的 NapCat 扩展 action

| action | 归类 | 说明 |
|---|---|---|
| `send_msg` | message | 通用发消息（OB11），主名 |
| `.handle_quick_operation` → `handle_quick_operation` | misc | go-cqhttp 快速操作，别名 `.handle_quick_operation` |
| `.get_word_slices` | misc | go-cqhttp 分词 |
| `clean_stream_temp_file` | file | 流式临时文件清理 |
| `upload_file_stream` | file | 流式上传 |
| `download_file_stream` | file | 流式下载 |
| `download_file_record_stream` | file | 流式语音下载 |
| `download_file_image_stream` | file | 流式图片下载 |

### 2.2 已适配的 SnowLuma 扩展 action

| action | 归类 | 说明 |
|---|---|---|
| `request_decrypt_key` | cred | SnowLuma 独有解密 |
| `set_qzone_ban` | qzone | SnowLuma 独有空间封禁 |
| `set_qzone_msg_right` | qzone | SnowLuma 独有空间权限 |
| `upload_forward_msg` | message | SnowLuma 独有上传转发，别名 `upload_foward_msg`（拼写） |

### 2.3 已处理的别名

| 别名 | 主名 |
|---|---|
| `.handle_quick_operation` | `handle_quick_operation` |
| `._get_model_show` | `_get_model_show` |
| `._set_model_show` | `_set_model_show` |
| `.ocr_image` | `ocr_image` |
| `.send_packet` | `send_packet` |
| `delete_group_file_folder` | `delete_group_folder` |
| `get_group_album_list` | `get_qun_album_list` |
| `get_ptt_text` / `get_record_text` | `fetch_ptt_text` |
| `nc_get_rkey` | `get_rkey` |
| `send_group_sign` | `set_group_sign` |
| `upload_foward_msg` | `upload_forward_msg` |

### 2.4 明确不适配的 action

| action | 原因 |
|---|---|
| `test_auto_register_01` / `test_auto_register_02` | NapCat 内部测试占位 |
| `test_download_stream` | NapCat 内部测试占位 |
| `unknown` | NapCat 默认占位 |
| `reboot_normal` | 已废弃，由 `set_restart` 替代 |
| `reload_event_filter` | go-cqhttp 遗留，NapCat 默认不实现 |
| `qidian_get_account_info` | 企点 API，不在消费端范围 |
| `delete_unidirectional_friend` | SnowLuma 未实现，NapCat 端无对应 handler |
| `get_guild_service_profile` | 频道 API，不在 OneBot v11 消息域范围 |
| `ArkSharePeer` / `ArkShareGroup` | NapCat 已废弃，由 `share_peer`/`share_group_ex` 取代 |

### 2.5 插件独有但 NapCat/SnowLuma 都未实现

这些是插件对 NapCat 扩展的封装，SnowLuma 暂未实现。保留并标记 `napcat_only=true`、`snowluma_compat=false`：

```
cancel_online_file, fetch_custom_face_detail, fetch_ptt_text, get_rkey,
get_robot_uin_range, ocr_image, receive_online_file, refuse_online_file,
send_online_file, send_online_folder, send_packet, set_custom_face_desc,
set_group_sign
```

### 2.6 插件适配 Qzone 但 NapCat 暂未实现

```
comment_qzone, delete_qzone_msg, get_qzone_feeds, get_qzone_msg_list,
like_qzone, send_qzone_msg, unlike_qzone
```

SnowLuma 已支持上述全部，外加 `set_qzone_ban`、`set_qzone_msg_right`。标记 `snowluma_compat=true`、`napcat_only=true`。

## 3. Service 聚合规则

23 个 Service 的功能域边界（新增 action 按此归位）：

| Service | 域 | 归位判据 |
|---|---|---|
| MessageService | message | 消息发送/撤回/已读/转发 |
| GroupService | group | 群禁言/踢出/管理/头衔/匿名 |
| FileService | file | 群私聊文件上传、图片/语音获取、流式文件 |
| AccountService | account | 登录号/好友/群列表与详情 |
| NapcatExtService | napcat_ext | NapCat 状态/Cookies/CSRF/精华/版本 |
| GroupFileService | group_file | 群文件 CRUD/文件夹/转存/重命名 |
| GroupNoticeService | group_notice | 群公告 |
| GroupExtService | group_ext | 群头像/备注/加群选项/签到/打卡 |
| RequestService | request | 好友/加群请求处理 |
| UserExtService | user_ext | 好友备注/分类/单向好友/资料/头像 |
| StatusService | status | 在线状态/DIY状态/输入状态 |
| PokeService | poke | 戳一拍 |
| EmojiExtService | emoji_ext | 收藏表情CRUD/详情/备注/移动/回应 |
| AiVoiceService | ai_voice | AI角色/语音生成 |
| CredService | cred | clientkey/credentials/rkey/URL安全/OCR/下载/解密 |
| MiscService | misc | 机型/退出/包状态/内联键盘/小程序/翻译/收藏/SSO包 |
| FlashService | flash | 闪传任务/消息/文件列表/URL/分享/下载/文件集CRUD |
| GroupAlbumService | group_album | 群相册列表/上传/评论/点赞/删除 |
| GroupTodoService | group_todo | 群待办设置/完成/取消 |
| QzoneService | qzone | QQ空间说说列表/动态/发表/删除/点赞/评论/封禁 |
| ArkService | ark | 用户/群Ark卡片分享 |
| EmojiService | emoji | QQ 表情映射（不发 API） |
| PathMapperService | path_mapper | 文件路径映射（不发 API） |

**新功能域才新建 Service**。例如未来出现"频道"完整功能集，可新建 `GuildService`，归入 `guild` 分类。

## 4. 兼容性标记规则

`APIDef` 的两个标志位：

| 标志 | 含义 | 默认值 |
|---|---|---|
| `napcat_only` | True=NapCat 专属，SnowLuma 不支持 | 一般 `false` |
| `snowluma_compat` | True=SnowLuma 兼容；False=不兼容 | 一般 `true` |

判定流程（三方：NapCat + SnowLuma + LLBot）：

1. 查 NapCat router.ts 是否有该 action → 有则 NapCat 支持
2. 查 SnowLuma actions/*.ts 是否有该 action → 有则 SnowLuma 支持
3. 查 LLBot types.ts 的 `ActionName` 枚举是否有该 action → 有则 LLBot 支持
4. 三方都支持 → `napcat_only=false, snowluma_compat=true`
5. 仅 NapCat → `napcat_only=true, snowluma_compat=false`
6. 仅 SnowLuma → `napcat_only=false, snowluma_compat=true`（NapCat 是 fallback 主路径，但实际不会路由到 SnowLuma 之外）
7. 仅 LLBot → `napcat_only=false, snowluma_compat=true`（LLBot 与 SnowLuma 实现重合度高，按 SnowLuma 兼容处理）
8. LLBot 独有的 action（如 `batch_delete_group_member`、`get_config` 等），`source=APISource.EXPAND`，描述标注"LLBot 扩展"

## 5. 中文显示别名（WebUI）

中文显示别名只用于 WebUI 的组件列表与详情页。它不会修改 Tool 的
`tool_name`、组件签名、OneBot action 或 LLM 调用名。

- **不要**把中文显示名写进 `APIDef.aliases`。`aliases` 是可调用的协议
  action 别名，会被 `resolve_action()` 解析并共享开关与 handler。
- OneBot Tool 的默认中文显示名来自 `api_defs.py` 中对应 `APIDef.description`。
  例如 `send_msg` 会显示为 `发送消息通用（按 message_type 与
  user_id/group_id 自动路由）`，原始名仍为 `send_msg`。
- 需要为任意 Tool、Service、Action、Router、Adapter、Command、Agent 或
  Chatter 指定更短、更明确的中文名时，在组件类上声明 `display_name`：

```python
class SendMsgTool(BaseTool):
    """发送通用消息的 Tool。"""

    tool_name = "send_msg"
    tool_description = "按 message_type 自动向群或私聊发送消息"
    display_name = "发送通用消息"
```

- WebUI 优先级为：`display_name` / `component_display_name` → OneBot 的
  `APIDef.description` → 组件类型描述（例如 `tool_description`、
  `service_description`）→ 原始组件名。
- WebUI 组件信息会同时返回 `display_name` 与 `raw_name`；为兼容已构建的
  前端，`component_name` 会显示为 `中文显示名（原始名）`。例如：
  `发送通用消息（send_msg）`。
- 同一组件的显示名应简短、中文、面向操作结果；不要包含 action 下划线名、
  内部实现细节或重复的“Tool/Service”后缀。

## 6. 协议 action 别名机制

参考 `docs/API_DEFS_REFACTOR.md` §3 与 `docs/ACTION_INDEX.md` 的"别名映射表"。

- 主名优先选 OneBot v11 标准名；没有标准名时选 NapCat 实现名
- 别名写入 `APIDef.aliases` 元组
- 调用方传入别名时，由 `resolve_action()` 解析为主名
- 别名与主名共用同一开关与同一 handler

当前已建立的别名组（截至 1.4.0）：

| 别名 | 主名 |
|---|---|
| `._get_model_show` | `_get_model_show` |
| `._set_model_show` | `_set_model_show` |
| `.ocr_image` | `ocr_image` |
| `.send_packet` | `send_packet` |
| `get_ptt_text` | `fetch_ptt_text` |
| `get_record_text` | `fetch_ptt_text` |
| `nc_get_rkey` | `get_rkey` |
| `send_group_sign` | `set_group_sign` |
| `_delete_group_notice` | `_del_group_notice` |
| `download_flash_file` | `download_fileset` |
| `get_flash_file_info` | `get_fileset_info` |
| `upload_group_album` | `upload_image_to_qun_album` |
| `voice_msg_to_text` | `fetch_ptt_text` |

待新增别名（Step 4 执行时落实）：

| 别名 | 主名 |
|---|---|
| `delete_group_file_folder` | `delete_group_folder` |
| `get_group_album_list` | `get_qun_album_list` |
| `upload_foward_msg` | `upload_forward_msg` |

## 7. Tool 开关规则

- `config.py` 的 `api_switches` 节里，每个 action 对应 `enable_<action>` 开关
- **所有 `enable_<action>` 默认 `false`**
- 总开关 `enable_all_tools` 默认 `false`，为 `false` 时所有 Tool 一律禁用
- **Service 路径不受 `api_switches` 影响**，始终启用
- 启用单个 Tool 的步骤：`enable_all_tools=true` + 对应 `enable_<action>=true`

## 8. 常见错误与修正

| 症状 | 原因 | 修正 |
|---|---|---|
| Tool 调用直接返回"禁用" | 总开关或独立开关未开启 | `enable_all_tools=true` + 对应 `enable_<action>=true` |
| 同一 action 注册两次 | 别名未声明导致重复适配 | 把别名写入 `APIDef.aliases`，删除重复 Tool 类 |
| WebUI 名称变成额外可调用 action | 误把中文显示名写入 `APIDef.aliases` | 删除该别名；改在组件类声明 `display_name` |
| SnowLuma 路由失败但 API 标了兼容 | `snowluma_compat` 标错 | 按上方 §4 流程重新判定，更新 `APIDef` |
| Service 调用失败但 Tool 正常 | Service 不应受开关影响 | 检查 Service 是否误用了 Tool 包装器 |
| `action` 名前后不一致 | 常量类与 ALL_APIS 字典字面量分叉 | 统一引用常量类，禁止裸字符串 |

## 8. 维护执行清单

每次维护按本 skill 工作流执行后，AI 应在响应里报告：

1. 上游 pull 结果（commit hash 范围）
2. Step 2 扫描得到的两方 action 总数
3. Step 3 对照后的"待适配/待别名/待废弃"清单
4. Step 4-7 实际落地的 api_defs / tools / services / config / docs 变更
5. Step 8 测试结果（每个 API 在 NapCat 与 SnowLuma 的实测情况）
6. Step 9 文档同步结果
7. 未完成项与下次维护建议

## 9. 更新所有文档

每次维护落地新 API 或别名后，必须同步以下文档，保证文档与代码一致：

### 9.1 必须更新的文件

| 文件 | 更新内容 |
|---|---|
| `docs/ACTION_INDEX.md` | 主名总数、各分类表条目数、别名映射表、按来源统计 |
| `README.md` | 总 Tool 数、模块表 Tool 数、配置开关总数、目录树注释里的数量 |
| `manifest.json` | 如记录 Tool/Service 数量或 action 列表，需同步；不记录则跳过 |

### 9.2 更新流程

1. **统计当前实际数量**：
   ```python
   from onebot_expand.api_defs import ALL_APIS
   from onebot_expand.tools import ALL_TOOLS
   print(len(ALL_APIS), len(ALL_TOOLS))
   # 应相等，否则 Step 7 去重失败
   ```

2. **更新 `docs/ACTION_INDEX.md`**：
   - 首行"共 **N** 个主名 action + **M** 个别名"——`N = len(ALL_APIS)`，`M = sum(len(d.aliases) for d in ALL_APIS.values())`
   - 各分类表标题的"N 个"——按 `APICategory` 分组计数
   - 每个新 action 加一行到对应分类表
   - 每个新别名加一行到"别名映射表"
   - "按来源统计"——按 `APISource` 分组计数（含 LLBot）

3. **更新 `README.md`**：
   - 顶部"**N 个 Tool 组件** 和 **23 个 Service 组件*"——`N = len(ALL_TOOLS)`
   - 模块表每行 Tool 数——与 ACTION_INDEX 分类计数一致
   - "Tool 层...共 N 个" → `len(ALL_TOOLS)`
   - "共 N 个独立开关" → `len(ALL_APIS)`（不含 `enable_all_tools` 等非 action 开关）
   - "主名 action 列表（N 个）" → `len(ALL_APIS)`
   - 目录树注释"api_defs.py # API 元数据定义（N 个 APIDef）" / "tools/ # N 个 Tool 类" → `len(ALL_APIS)` / `len(ALL_TOOLS)`

4. **更新 `manifest.json`**（如包含数量字段）：
   - 检查是否有 `tool_count`、`service_count`、`actions` 等字段
   - 有则同步，无则跳过

### 9.3 校验文档与代码一致

更新后运行以下检查，确保文档数字与代码一致：

```python
import re
from onebot_expand.api_defs import ALL_APIS
from onebot_expand.tools import ALL_TOOLS

expected_apis = len(ALL_APIS)
expected_tools = len(ALL_TOOLS)
expected_aliases = sum(len(d.aliases) for d in ALL_APIS.values())

# 检查 ACTION_INDEX.md 首行
with open("docs/ACTION_INDEX.md", encoding="utf-8") as f:
    head = f.read(200)
m = re.search(r"共 \*\*(\d+)\*\* 个主名 action \+ \*\*(\d+)\*\* 个别名", head)
assert int(m.group(1)) == expected_apis, f"ACTION_INDEX 主名数 {m.group(1)} != {expected_apis}"
assert int(m.group(2)) == expected_aliases, f"ACTION_INDEX 别名数 {m.group(2)} != {expected_aliases}"

# 检查 README.md 顶部
with open("README.md", encoding="utf-8") as f:
    head = f.read(500)
m = re.search(r"\*\*(\d+) 个 Tool 组件\*\*", head)
assert int(m.group(1)) == expected_tools, f"README Tool 数 {m.group(1)} != {expected_tools}"

print("文档与代码一致")
```

### 9.4 不需要更新的文件

- `SKILL.md`（本文件）——一次编写永久使用，不修改
- `docs/API_DEFS_REFACTOR.md`——历史决策记录，不更新
- `plugin.py` / `__init__.py`——除非导出列表变化

### 9.5 文档 UI 风格指南

所有文档（`README.md`、`docs/ACTION_INDEX.md`）统一采用以下风格，保持视觉一致。

#### 9.5.1 通用原则

- **简洁优先**：信息密度高，避免冗余描述。每段不超过 3-5 行。
- **表格驱动**：能用表格就不用列表，能用列表就不用段落。
- **代码块标注语言**：所有代码块标注语言（`python`、`toml`、`bash`、`text`）。
- **emoji 克制使用**：仅用于状态标记（✅ ⚠️ ❌）和章节锚点，不用于装饰。

#### 9.5.2 README.md 风格

- **顶部 banner**：用引用块 `>` 包裹的一句话简介 + 关键指标（版本、Tool 数、Service 数）。
- **功能概览表**：`| 模块 | Tool 数 | Service | 说明 |` 四列，按功能域分组。
- **架构图**：用代码块画调用链，箭头用 `→`，关键节点加粗。
- **配置示例**：`toml` 代码块，关键行加行内注释。
- **目录树**：用代码块，每个文件/目录后跟 `#` 注释说明用途。

#### 9.5.3 ACTION_INDEX.md 风格

- **顶部摘要**：首行用加粗显示总数（`共 **N** 个主名 action + **M** 个别名`）。
- **来源标记说明**：紧跟一行说明各来源缩写含义。
- **分类表**：每个分类一个 `###` 三级标题，格式 `### 中文名 (category, N 个)`。
- **表格列**：`| action | 来源 | napcat_only | snowluma_compat | 别名 |`，固定五列。
- **兼容性标记**：用 `✓`（是）和 `✗`（否），`—`（不适用/默认值）。
- **分隔线**：大节之间用 `---` 分隔。
- **别名映射表**：两列 `| 别名 | 主名 |`，按主名字母序排列。
- **按来源统计**：末尾用无序列表，每行一个来源。

#### 9.5.4 数量一致性

文档中所有出现的数量必须来自代码统计，禁止手写。更新后必须运行 §9.3 的校验脚本。

### 9.6 文档站更新（VitePress）

OneBot Expand 有独立的 GitHub Pages 文档站，仓库地址：

```
https://github.com/fuilyha56-wq/onebot-expand-docs
```

本地克隆位置：`E:\onebot-expand-docs`

文档站基于 **VitePress + 自定义 MD3 主题**，部署到 GitHub Pages，base 路径为 `/onebot-expand-docs/`。

#### 9.6.1 文档站结构

```
E:\onebot-expand-docs\
├── .vitepress/
│   ├── config.ts              # VitePress 配置（导航/侧边栏/搜索）
│   ├── theme/
│   │   ├── index.ts           # 主题入口（注册组件/注入样式）
│   │   ├── styles/
│   │   │   ├── tokens.css     # MD3 设计令牌（颜色/排版/形状/动效）
│   │   │   └── overrides.css  # VitePress 默认样式覆盖
│   │   └── components/
│   │       ├── ApiBadge.vue   # 兼容性徽章（✓/★/✗ 三态）
│   │       ├── ApiCard.vue    # API 卡片
│   │       └── ApiTable.vue   # API 表格
│   └── dist/                  # 构建产物
├── index.md                   # 首页（Hero + Features）
├── guide/                     # 指南
│   ├── introduction.md        # 简介
│   ├── getting-started.md     # 快速开始
│   ├── architecture.md        # 架构设计
│   └── configuration.md       # 配置说明
├── api/                       # API 文档（21 个分类目录）
│   ├── index.md               # API 总览
│   ├── message/               # 每个分类一个目录
│   │   ├── index.md           # 分类概览（API 列表表）
│   │   ├── send-group-msg.md  # 每个 action 一个详情页
│   │   └── ...
│   └── ...
├── services/                  # Service 文档（23 个文件）
│   ├── index.md               # Service 总览
│   ├── message-service.md     # 每个 Service 一个详情页
│   └── ...
├── reference/                 # 参考资料
│   ├── index.md               # 参考首页
│   ├── onebot-v11.md          # OneBot v11 标准 API 索引
│   ├── napcat.md              # NapCat 扩展 API 索引
│   ├── snowluma.md            # SnowLuma 扩展 API 索引
│   └── compatibility-matrix.md # 完整四方兼容性矩阵
├── public/                    # 静态资源（logo.svg 等）
└── package.json               # 依赖与脚本
```

#### 9.6.2 必须更新的场景

| 场景 | 需更新的文档站内容 |
|---|---|
| 新增/删除 API | `api/<category>/index.md` 分类概览、`api/<category>/<action>.md` 详情页、`api/index.md` 总览、`reference/compatibility-matrix.md` 矩阵 |
| 新增/删除 Service 方法 | `services/<service>.md` 详情页、`services/index.md` 总览 |
| 新增/删除别名 | 对应 API 详情页的"别名"节、`reference/compatibility-matrix.md` |
| 修改 API 参数/响应 | 对应 `api/<category>/<action>.md` 详情页 |
| 新增功能域 | `api/` 新建分类目录、`config.ts` 侧边栏新增条目、`api/index.md` 总览新增行 |
| 版本号变更 | `index.md` 首页 tagline、`guide/introduction.md` |

#### 9.6.3 API 详情页模板

每个 action 对应一个 `api/<category>/<action-name>.md` 文件（action 名中的下划线改为连字符）。模板：

```markdown
# <action_name>

<中文描述>。

## 兼容性

<ApiBadge platform="onebot" status="supported" />
<ApiBadge platform="napcat" status="supported" />
<ApiBadge platform="snowluma" status="supported" />
<ApiBadge platform="llbot" status="supported" />

::: tip 来源
<来源说明，如"OneBot v11 标准 API" / "NapCat 扩展 API" / "LLBot 扩展 API">
:::

## 参数

| 参数名 | 类型 | 默认值 | 必填 | 说明 |
|---|---|---|---|---|
| `param1` | int | - | ✅ | 参数说明 |
| `param2` | str | "default" | ❌ | 参数说明 |

## 响应

| 字段 | 类型 | 说明 |
|---|---|---|
| `field1` | int | 字段说明 |

## 示例

**请求：**

\`\`\`json
{
  "action": "<action_name>",
  "params": { ... }
}
\`\`\`

**响应：**

\`\`\`json
{
  "status": "ok",
  "retcode": 0,
  "data": { ... }
}
\`\`\`

## 四方差异

<说明四方实现的差异，如"四方实现一致，无差异"。>

## 相关 API

- [`related_action`](./related-action) — 相关说明
```

**ApiBadge status 取值规则**：
- `supported`：该协议端支持此 API
- `exclusive`：该协议端专属（其他不支持）
- `unsupported`：该协议端不支持

**platform 取值**：`onebot` / `napcat` / `snowluma` / `llbot`

#### 9.6.4 Service 详情页模板

每个 Service 对应一个 `services/<service-name>.md` 文件。模板：

```markdown
# <ServiceName>

<中文描述>。

## 基本信息

| 属性 | 值 |
|---|---|
| Service 名称 | <ServiceName> |
| 说明 | <中文描述> |
| 版本 | 1.0.0 |
| 始终可用 | ✅ 是（不受 Tool 开关影响） |

## 方法列表

### <method_name>

<方法描述>。

对应 OneBot API: <action_name>

\`\`\`python
async def <method_name>(
    self,
    param1: int,
    param2: str = "default",
) -> dict[str, Any]:
\`\`\`

**参数：**

| 参数名 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| param1 | int | - | 参数说明 |
| param2 | str | "default" | 参数说明 |

**返回值：** dict[str, Any] — 适配器返回的响应字典。

**示例：**

\`\`\`python
from onebot_expand.services import <ServiceName>

service = <ServiceName>(plugin)
result = await service.<method_name>(param1=..., param2=...)
\`\`\`

---

### <next_method>
...
```

#### 9.6.5 分类概览页模板

每个功能域对应一个 `api/<category>/index.md`。模板：

```markdown
# <分类中文名> API

本分类包含 **N** 个<分类说明>API，涵盖<功能概述>。

## API 列表

| action | 说明 | 来源 | NapCat | SnowLuma |
|---|---|---|---|---|
| [`<action>`](./<action-name>) | <说明> | <来源> | ✓/✗ | ✓/✗ |
| ... | ... | ... | ... | ... |
```

#### 9.6.6 config.ts 侧边栏更新

新增功能域时，在 `.vitepress/config.ts` 的 `sidebar['/api/']` 数组中新增条目：

```typescript
{
  text: '分类名 (N)',
  collapsed: true,
  items: [{ text: '概览', link: '/api/<category>/' }],
},
```

#### 9.6.7 文档站 UI 风格指南

文档站采用**现代简约**风格，核心原则：

- **留白优先**：内容区最大宽度 688px，段落间距 1.5em，章节间距 2em
- **色彩克制**：主色仅用于链接/按钮/强调，正文用中性色，背景用 surface 层级
- **圆角统一**：卡片 12px、按钮 8px、徽章 6px、代码块 8px
- **阴影柔和**：仅卡片和悬浮元素使用 1-2 级海拔阴影，避免重阴影
- **字体层次**：标题用 600 字重，正文 400，代码用等宽字体
- **动效克制**：hover 过渡 150-200ms，无入场动画

主题文件位置：
- 设计令牌：`.vitepress/theme/styles/tokens.css`（颜色/排版/形状/动效）
- 样式覆盖：`.vitepress/theme/styles/overrides.css`（VitePress 变量映射）
- 组件：`.vitepress/theme/components/`（ApiBadge/ApiCard/ApiTable）

#### 9.6.8 本地开发与构建

```bash
cd E:/onebot-expand-docs
npm install          # 安装依赖
npm run docs:dev     # 本地开发服务器（http://localhost:5173/onebot-expand-docs/）
npm run docs:build   # 构建到 .vitepress/dist/
npm run docs:preview # 预览构建产物
```

构建产物部署到 GitHub Pages（通过 `.github/workflows/` 自动部署）。

#### 9.6.9 文档站校验

更新后检查：

1. **死链接**：`config.ts` 的 `ignoreDeadLinks` 设为 `false`，构建时自动检测
2. **数量一致**：API 详情页数 = `len(ALL_APIS)`，Service 页数 = 23
3. **侧边栏完整**：每个分类在 `config.ts` 侧边栏都有对应条目
4. **兼容性矩阵**：`reference/compatibility-matrix.md` 覆盖全部 205 个 API

## 10. 项目结构速查

```
E:\plugins\onebot_expand\
├── SKILL.md                    # 本文件（长期不变）
├── README.md                   # 用户文档（每次维护后同步）
├── plugin.py                   # 插件入口
├── config.py                   # 配置 + enable_<action> 开关
├── api_defs.py                 # APIDef 元数据
├── manifest.json               # 组件清单
├── path_mapper.py              # 文件路径映射
├── emoji_tables.py             # QQ 表情映射表
├── tools/                      # Tool 类
├── services/                   # 23 个 Service 类
├── tests/                      # 测试适配器
│   ├── __init__.py
│   └── napcat_test_adapter.py  # NapCat WS 测试客户端（ws://127.0.0.1:5326）
└── docs/
    ├── ACTION_INDEX.md         # API 完整索引名单（每次维护后同步）
    └── API_DEFS_REFACTOR.md    # 重构历史与决策记录（不更新）
```

上游：

```
E:\NapCatQQ\packages\napcat-onebot\action\router.ts   # NapCat ActionName 总表
E:\SnowLuma\packages\onebot\src\actions\*.ts          # SnowLuma action 定义
E:\SnowLuma\packages\onebot\src\actions\index.ts      # SnowLuma ACTION_GROUPS 总表
E:\LLBot\src\onebot11\action\types.ts                 # LLBot ActionName 枚举（全量 action 名单）
E:\LLBot\src\onebot11\action\index.ts                 # LLBot action 注册总表
E:\LLBot\src\onebot11\action\llbot\                   # LLBot 独有 action 实现
E:\LLBot\llbot_actions.txt                            # LLBot 全量 action 文本名单（快速对照）
```
