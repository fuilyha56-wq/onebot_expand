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
- **参考文档**：`E:\plugins\onebot_expand\docs\ACTION_INDEX.md` 与 `E:\plugins\onebot_expand\docs\API_DEFS_REFACTOR.md`（已迁移至 docs/）

## 1. 工作流（每次维护都按此顺序执行）

### Step 1 — 拉取上游最新

```bash
cd E:/SnowLuma && git pull
cd E:/NapCatQQ && git pull
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

### Step 3 — 与本插件对照

本插件的 action 名单在 `api_defs.py` 各 `*Action` 常量类里。提取方式：

```bash
cd E:/plugins/onebot_expand && grep -E '^\s+[A-Z_]+\s*=\s*"[a-z_.][a-z_0-9.]*"' api_defs.py \
  | grep -oE '"[a-z_.][a-z_0-9.]*"' | tr -d '"' | sort -u
```

对照规则：
- **上游有、插件没有** → 进入"待适配"清单（Step 4）
- **上游没有、插件有** → 检查是否上游已废弃；若是，标记 `deprecated`，但**保留**（向后兼容）
- **两边都支持但命名不同** → 走别名机制（见 `docs/ACTION_INDEX.md` 的"别名映射表"）

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

判定流程：

1. 查 NapCat router.ts 是否有该 action → 有则 NapCat 支持
2. 查 SnowLuma actions/*.ts 是否有该 action → 有则 SnowLuma 支持
3. 两边都支持 → `napcat_only=false, snowluma_compat=true`
4. 仅 NapCat → `napcat_only=true, snowluma_compat=false`
5. 仅 SnowLuma → `napcat_only=false, snowluma_compat=true`（NapCat 是 fallback 主路径，但实际不会路由到 SnowLuma 之外）

## 5. 别名机制

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

## 6. Tool 开关规则

- `config.py` 的 `api_switches` 节里，每个 action 对应 `enable_<action>` 开关
- **所有 `enable_<action>` 默认 `false`**
- 总开关 `enable_all_tools` 默认 `false`，为 `false` 时所有 Tool 一律禁用
- **Service 路径不受 `api_switches` 影响**，始终启用
- 启用单个 Tool 的步骤：`enable_all_tools=true` + 对应 `enable_<action>=true`

## 7. 常见错误与修正

| 症状 | 原因 | 修正 |
|---|---|---|
| Tool 调用直接返回"禁用" | 总开关或独立开关未开启 | `enable_all_tools=true` + 对应 `enable_<action>=true` |
| 同一 action 注册两次 | 别名未声明导致重复适配 | 把别名写入 `APIDef.aliases`，删除重复 Tool 类 |
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
   - "按来源统计"——按 `APISource` 分组计数

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
```
