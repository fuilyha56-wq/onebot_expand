# OneBot Expand Upstream Sync Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the five verified upstream actions missing from `onebot_expand`, synchronize both plugin copies and the documentation site, release version 1.0.12, and publish it after all validation gates pass.

**Architecture:** Keep the existing `APIDef -> Tool/Service -> api_client` architecture and the 23 stable Service domains. Add three NapCat group actions, one SnowLuma user action, and one LLBot misc action as distinct primary actions because none share wire-compatible parameters with an existing action.

**Tech Stack:** Python 3.11, pytest, Pylance, Neo-MoFox plugin components, TypeScript upstream schemas, VitePress, npm, mpdt.

## Global Constraints

- The canonical plugin is `E:\plugins\onebot_expand`; the runtime copy is `E:\Neo-mofox-instance\bot-3693525299\neo-mofox\plugins\onebot_expand`.
- Every Tool switch and `enable_all_tools` must default to `false`; Services are always available.
- Preserve the existing uncommitted README dependency section and all unrelated user changes.
- Do not modify `SKILL.md` or `docs/API_DEFS_REFACTOR.md`.
- Do not clean or reset the untracked upstream `*_actions.txt` files.
- Do not publish unless unit tests, contract checks, Pylance, documentation build, copy comparison, and required protocol checks pass.
- `set_friends_category` is not an alias of `set_friend_category`: their wire parameters are incompatible.
- `send_pb` is not an alias of `send_packet`: it requires `cmd` and protobuf `hex`, while `send_packet` accepts `cmd` and structured `data`.

---

### Task 1: Establish Synchronization Contract Tests

**Files:**
- Modify: `tests/test_tool_registration.py`
- Create: `tests/test_api_contract.py`

**Interfaces:**
- Consumes: `ALL_APIS`, `resolve_action`, `ALL_TOOLS`, `ALL_SERVICES`, `SelfIdInjectHandler`, `OnebotExpandConfig`.
- Produces: executable contracts for 211 primary actions, 18 aliases, 211 Tools, 211 default-disabled action switches, unique action names, and correct always-on components.

- [ ] **Step 1: Correct the stale always-on component expectation**

Change the three assertions that currently compare `get_components()` with only `ALL_SERVICES` so they compare with:

```python
ALWAYS_ON_COMPONENTS = ALL_SERVICES + [SelfIdInjectHandler]
```

Keep the enabled-Tool test expecting:

```python
assert plugin.get_components() == ALWAYS_ON_COMPONENTS + [
    SendGroupMsgTool,
    SendPrivateMsgTool,
]
```

- [ ] **Step 2: Run the corrected registration test as a green baseline**

Run:

```powershell
$env:PYTHONPATH = 'E:\plugins;E:\Neo-mofox-instance\bot-3693525299\neo-mofox'
e:/plugins/onebot_expand/.venv/Scripts/python.exe -m pytest tests/test_tool_registration.py -q
```

Expected: four tests pass. A failure here is a pre-existing component registration defect and must be repaired before adding actions.

- [ ] **Step 3: Add the failing API synchronization contract**

Create `tests/test_api_contract.py` with tests equivalent to:

```python
"""onebot_expand API registry synchronization contracts."""

from dataclasses import fields

from onebot_expand.api_defs import ALL_APIS, resolve_action
from onebot_expand.config import ApiSwitchesSection
from onebot_expand.tools import ALL_TOOLS

EXPECTED_ACTIONS = {
    "send_pb": {"cmd": "str", "hex": "str"},
    "set_friends_category": {
        "uin": "int",
        "categoryId": "int",
        "categoryName": "str",
    },
    "set_group_member_invite_policy": {"group_id": "str", "policy": "str"},
    "set_group_member_permissions": {
        "group_id": "str",
        "allow_member_upload_album": "bool",
        "allow_member_temporary_session": "bool",
        "allow_member_create_group": "bool",
    },
    "set_group_new_member_history_visibility": {
        "group_id": "str",
        "visible": "bool",
    },
}


def test_api_registry_has_expected_upstream_actions() -> None:
    assert len(ALL_APIS) == 211
    for action, params in EXPECTED_ACTIONS.items():
        assert ALL_APIS[action].params == params


def test_api_tools_switches_and_aliases_are_one_to_one() -> None:
    tool_names = [tool.tool_name for tool in ALL_TOOLS]
    aliases = [alias for api in ALL_APIS.values() for alias in api.aliases]
    switch_fields = {
        field.name.removeprefix("enable_")
        for field in fields(ApiSwitchesSection)
        if field.name.startswith("enable_") and field.name != "enable_all_tools"
    }

    assert len(ALL_TOOLS) == len(ALL_APIS) == len(tool_names) == 211
    assert len(set(tool_names)) == len(tool_names)
    assert set(tool_names) == set(ALL_APIS)
    assert switch_fields == set(ALL_APIS)
    assert len(aliases) == len(set(aliases)) == 18
    assert not set(aliases) & set(ALL_APIS)
    assert all(resolve_action(alias) in ALL_APIS for alias in aliases)


def test_all_tool_switches_default_to_disabled() -> None:
    switches = ApiSwitchesSection()
    assert not switches.enable_all_tools
    assert all(
        not getattr(switches, field.name)
        for field in fields(ApiSwitchesSection)
        if field.name.startswith("enable_")
    )
```

If `ApiSwitchesSection` is a Pydantic model rather than a dataclass at runtime, use `ApiSwitchesSection.model_fields` to enumerate the same field names; do not weaken the equality assertion.

- [ ] **Step 4: Run the contract and verify RED**

Run:

```powershell
$env:PYTHONPATH = 'E:\plugins;E:\Neo-mofox-instance\bot-3693525299\neo-mofox'
e:/plugins/onebot_expand/.venv/Scripts/python.exe -m pytest tests/test_api_contract.py -q
```

Expected: fail because the five actions are absent and counts are still 206.

---

### Task 2: Implement Five Upstream Actions

**Files:**
- Modify: `api_defs.py`
- Modify: `config.py`
- Modify: `tools/group_tools.py`
- Modify: `tools/user_ext_tools.py`
- Modify: `tools/misc_tools.py`
- Modify: `tools/__init__.py`
- Modify: `services/group_service.py`
- Modify: `services/user_ext_service.py`
- Modify: `services/misc_service.py`

**Interfaces:**
- Consumes: NapCat TypeBox payload schemas, SnowLuma action-kit schema, LLBot schemastery payload schema.
- Produces: five primary actions, five Tools, five default-disabled switches, and five methods on existing Services.

- [ ] **Step 1: Add constants and `APIDef` metadata**

Add these constants:

```python
class NapCatAction:
    SET_GROUP_MEMBER_INVITE_POLICY = "set_group_member_invite_policy"
    SET_GROUP_MEMBER_PERMISSIONS = "set_group_member_permissions"
    SET_GROUP_NEW_MEMBER_HISTORY_VISIBILITY = "set_group_new_member_history_visibility"

class ExpandAction:
    SET_FRIENDS_CATEGORY = "set_friends_category"
    SEND_PB = "send_pb"
```

Add `APIDef` entries with these exact contracts:

| action | category | source | napcat_only | snowluma_compat | params |
|---|---|---|---|---|---|
| `set_group_member_invite_policy` | `GROUP` | `NAPCAT_EXT` | `True` | `False` | `group_id: str`, `policy: str` |
| `set_group_member_permissions` | `GROUP` | `NAPCAT_EXT` | `True` | `False` | `group_id: str`, three optional boolean permission fields |
| `set_group_new_member_history_visibility` | `GROUP` | `NAPCAT_EXT` | `True` | `False` | `group_id: str`, `visible: bool` |
| `set_friends_category` | `USER_EXT` | `EXPAND` | `False` | `True` | `uin: int`, optional `categoryId: int`, optional `categoryName: str` |
| `send_pb` | `MISC` | `EXPAND` | `False` | `True` | `cmd: str`, `hex: str` |

Descriptions must identify SnowLuma or LLBot for the two `EXPAND` entries. Do not add aliases.

- [ ] **Step 2: Add default-disabled configuration switches**

Add one `Field(default=False, description=...)` for every new primary action under `ApiSwitchesSection`:

```python
enable_set_group_member_invite_policy: bool = Field(default=False, ...)
enable_set_group_member_permissions: bool = Field(default=False, ...)
enable_set_group_new_member_history_visibility: bool = Field(default=False, ...)
enable_set_friends_category: bool = Field(default=False, ...)
enable_send_pb: bool = Field(default=False, ...)
```

- [ ] **Step 3: Add three group Tools and Service methods**

Add `SetGroupMemberInvitePolicyTool`, `SetGroupMemberPermissionsTool`, and `SetGroupNewMemberHistoryVisibilityTool` to `tools/group_tools.py` and export them through `tools/__init__.py` exactly once.

Use these Tool signatures:

```python
async def execute(self, group_id: Annotated[str, "目标群号"], policy: Annotated[str, "disabled/require_approval/no_approval/no_approval_under_100"]) -> tuple[bool, str]

async def execute(
    self,
    group_id: Annotated[str, "目标群号"],
    allow_member_upload_album: Annotated[bool | None, "是否允许成员上传群相册"] = None,
    allow_member_temporary_session: Annotated[bool | None, "是否允许成员发起临时会话"] = None,
    allow_member_create_group: Annotated[bool | None, "是否允许成员发起新群聊"] = None,
) -> tuple[bool, str]

async def execute(self, group_id: Annotated[str, "目标群号"], visible: Annotated[bool, "新成员是否可见最近聊天记录"]) -> tuple[bool, str]
```

The permissions Tool and Service method must omit `None` values and reject a call where all three permissions are `None`, matching NapCat's upstream rule.

Add snake_case Service methods with the same parameter contracts:

```python
GroupService.set_member_invite_policy(...)
GroupService.set_member_permissions(...)
GroupService.set_new_member_history_visibility(...)
```

- [ ] **Step 4: Add the SnowLuma friend-category Tool and Service method**

Add `SetFriendsCategoryTool` and:

```python
async def set_friends_category(
    self,
    uin: int,
    category_id: int | None = None,
    category_name: str | None = None,
) -> dict[str, Any]
```

Map the Python arguments to wire keys `uin`, `categoryId`, and `categoryName`. Require exactly one of `category_id` and `category_name`; do not route through or alias to the existing LLBot `set_friend_category` method.

- [ ] **Step 5: Add the LLBot protobuf Tool and Service method**

Add `SendPBTool` and:

```python
async def send_pb(self, cmd: str, hex_data: str) -> dict[str, Any]
```

Map `hex_data` to the wire key `hex`. Keep it separate from `send_packet`, which uses a structured `data` payload.

- [ ] **Step 6: Run the focused contract and registration tests as GREEN**

Run:

```powershell
$env:PYTHONPATH = 'E:\plugins;E:\Neo-mofox-instance\bot-3693525299\neo-mofox'
e:/plugins/onebot_expand/.venv/Scripts/python.exe -m pytest tests/test_api_contract.py tests/test_tool_registration.py -q
```

Expected: all tests pass with 211 APIs, 211 Tools, 18 aliases, and 211 action switches.

---

### Task 3: Synchronize Plugin Documentation, Runtime Copy, And Version

**Files:**
- Modify: `README.md`
- Modify: `docs/ACTION_INDEX.md`
- Modify: `manifest.json`
- Modify: `plugin.py`
- Modify: runtime-copy counterparts of every plugin file changed in Tasks 1-3
- Modify: `E:\onebot-expand-docs\index.md`
- Modify: `E:\onebot-expand-docs\guide\introduction.md`
- Modify: `E:\onebot-expand-docs\api\index.md`
- Modify: `E:\onebot-expand-docs\api\group\index.md`
- Create: three group API detail pages
- Modify: `E:\onebot-expand-docs\api\user-ext\index.md`
- Create: `E:\onebot-expand-docs\api\user-ext\set-friends-category.md`
- Modify: `E:\onebot-expand-docs\api\misc\index.md`
- Create: `E:\onebot-expand-docs\api\misc\send-pb.md`
- Modify: `E:\onebot-expand-docs\services\index.md`
- Modify: `E:\onebot-expand-docs\services\group-service.md`
- Modify: `E:\onebot-expand-docs\services\user-ext-service.md`
- Modify: `E:\onebot-expand-docs\services\misc-service.md`
- Modify: `E:\onebot-expand-docs\reference\compatibility-matrix.md`
- Modify: `E:\onebot-expand-docs\reference\napcat.md`
- Modify: `E:\onebot-expand-docs\reference\snowluma.md`
- Modify: `E:\onebot-expand-docs\reference\llbot.md`
- Modify: `E:\onebot-expand-docs\.vitepress\config.ts`

**Interfaces:**
- Consumes: runtime registry counts after Task 2.
- Produces: consistent 1.0.12 metadata, 211 API/Tool documentation, unchanged 23-Service boundary, and byte-equivalent synchronized plugin files.

- [ ] **Step 1: Derive all counts from code**

Run a Python count script and use its output, not hand-written assumptions. Expected post-change values are:

```text
primary=211
aliases=18
tools=211
services=23
group=13
user_ext=15
misc=19
onebot_v11=32
napcat_ext=23
gocqhttp_compat=20
expand=136
```

- [ ] **Step 2: Update plugin README and Action index**

Update all stale totals in `README.md`, including its existing stale 205/206 references and per-module table. Preserve the uncommitted `## 依赖` section already present.

Update `docs/ACTION_INDEX.md` to 211 primary actions plus 18 aliases, add all five rows to the correct category tables, and update category and source totals. Keep `get_guild_service_profile` excluded as required by `SKILL.md`.

- [ ] **Step 3: Update the VitePress API and Service documentation**

Create detail pages named:

```text
api/group/set-group-member-invite-policy.md
api/group/set-group-member-permissions.md
api/group/set-group-new-member-history-visibility.md
api/user-ext/set-friends-category.md
api/misc/send-pb.md
```

Each page must include compatibility badges, exact parameters, a safe request example, response shape, and four-platform differences. Update category indexes, Service method pages, global API/Service indexes, protocol reference pages, and the full compatibility matrix.

Update sidebar labels to `group (13)`, `user-ext (15)`, and `misc (19)`. Correct existing stale documentation counts encountered in touched pages, including the Service index's 205 link text and its current user/misc method-count drift.

- [ ] **Step 4: Increase the patch version in three plugin locations**

Change exactly:

```text
manifest.json: 1.0.11 -> 1.0.12
README.md: 1.0.11 -> 1.0.12
plugin.py: 1.0.11 -> 1.0.12
```

Update documentation-site version text in `index.md` and `guide/introduction.md` to 1.0.12.

- [ ] **Step 5: Synchronize the runtime copy**

Copy only files changed by Tasks 1-3 from the canonical plugin into the runtime copy, excluding `.git`, caches, `dist`, temporary scan files, and `docs/superpowers`. Compare each copied file by SHA-256 and require no mismatch.

- [ ] **Step 6: Validate documentation counts and build the site**

Run the `SKILL.md` count checks plus assertions for all category/source totals. Then run:

```powershell
npm --prefix E:\onebot-expand-docs run docs:build
```

Expected: VitePress exits 0 with no dead links.

---

### Task 4: Protocol Validation, Final Verification, And Publication

**Files:**
- Modify: `tests/run_api_tests.py` only to add safe minimum payloads for the two non-group actions
- Modify: `tests/api_test_report.md` only if an authorized real protocol run completes

**Interfaces:**
- Consumes: `tests.napcat_test_adapter.call_napcat`, NapCat endpoint `ws://127.0.0.1:5326`, mpdt credentials and market registration.
- Produces: fresh protocol evidence, complete validation output, GitHub Release 1.0.12, and market update.

- [ ] **Step 1: Add safe minimum protocol payloads**

Add only the non-group payloads to the general batch runner:

```python
"set_friends_category": {"uin": 1, "categoryId": 0},
"send_pb": {"cmd": "trpc.test", "hex": ""},
```

Do not add the three group-setting actions to the general batch runner. They must
only be called by the targeted workflow in Step 2 after the user selects a test
group from the connected account's `get_group_list` response. For unsupported
endpoints, a protocol-level parameter or unknown-action response is evidence of
recognition only, not success.

- [ ] **Step 2: Check protocol availability and run safe targeted calls**

Use `is_available()` before each endpoint. On NapCat, call `get_group_list`, show
the returned group IDs and names to the user, and request one explicit test-group
selection before any write call. After selection, call the three NapCat actions
with reversible values and record the original settings when the endpoint
exposes them. On SnowLuma, test `set_friends_category` only when an endpoint and
user-authorized test friend/category are available. On LLBot, test `send_pb` only
when an endpoint is available and the user provides or approves a known
non-destructive command/payload.

If a newly added action cannot receive a safe real call, record it as unverified and stop before publication, as required by the approved design.

- [ ] **Step 3: Run Python semantic and executable validation**

Run Pylance syntax/diagnostics for every changed Python file, followed by:

```powershell
$env:PYTHONPATH = 'E:\plugins;E:\Neo-mofox-instance\bot-3693525299\neo-mofox'
e:/plugins/onebot_expand/.venv/Scripts/python.exe -m pytest tests -q
e:/plugins/onebot_expand/.venv/Scripts/python.exe -m compileall -q .
e:/plugins/onebot_expand/.venv/Scripts/python.exe -m ruff check .
e:/plugins/onebot_expand/.venv/Scripts/python.exe -m ruff format --check .
```

Expected: all tests pass, compilation exits 0, and Ruff reports no errors or formatting drift caused by this change.

- [ ] **Step 4: Verify repository diffs and release contents**

Run `git diff --check`, inspect the complete plugin and documentation-site diffs, verify no temporary `.current.txt` files are tracked, and confirm the runtime copy checksums. Commit plugin and documentation-site changes separately with conventional commit messages and no AI attribution trailers.

- [ ] **Step 5: Publish 1.0.12**

Run only after every preceding gate succeeds:

```powershell
mpdt market package-update E:/plugins/onebot_expand
```

Verify the command output confirms package build, GitHub Release creation, and market submission. Then query `mpdt market info onebot_expand` and verify the visible market version is 1.0.12.

- [ ] **Step 6: Produce the maintenance report**

Report:

1. Upstream commit ranges: NapCat `33546b93..c4a09f01`, SnowLuma `7fd07f9..ebbe90be`, LLBot `7abca99a..a0337794`.
2. Scanned totals: NapCat 173 valid actions, SnowLuma 175 extracted actions before exclusions, LLBot 122 actions.
3. Added actions and explicitly excluded candidates.
4. Code, documentation, runtime-copy, and version changes.
5. Unit, Pylance, Ruff, VitePress, protocol, package, Release, and market results.
6. Any unverified endpoint behavior or remaining follow-up.