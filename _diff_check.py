"""三方 API 名单对照脚本（临时工具）。

对照插件 ALL_APIS 与 NapCat/SnowLuma 上游 action 名单，产出差异报告。
"""

from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api_defs import ALL_APIS  # noqa: E402

plugin = set(ALL_APIS.keys())

# 读取 NapCat 名单
napcat: set[str] = set()
with open(
    r"E:\NapCatQQ\packages\napcat-onebot\action\router.ts", encoding="utf-8"
) as f:
    content = f.read()
    for m in re.finditer(r":\s*'([^']+)'\s*,", content):
        napcat.add(m.group(1))

# 读取 SnowLuma 名单
snowluma: set[str] = set()
sl_dir = r"E:\SnowLuma\packages\onebot\src\actions"
for fn in os.listdir(sl_dir):
    if fn.endswith(".ts"):
        with open(os.path.join(sl_dir, fn), encoding="utf-8") as f:
            content = f.read()
            for m in re.finditer(r"name:\s*'([^']+)'", content):
                snowluma.add(m.group(1))

# 忽略项（测试/占位/废弃/不在范围）
ignore = {
    "test_auto_register_01",
    "test_auto_register_02",
    "test_download_stream",
    "unknown",
    "reboot_normal",
    "reload_event_filter",
    "qidian_get_account_info",
    "delete_unidirectional_friend",
    "get_guild_list",
    "get_guild_service_profile",
    "SnowLuma",
}
napcat -= ignore
snowluma -= ignore

# 别名归并到主名
napcat_aliases = {
    ".ocr_image": "ocr_image",
    ".handle_quick_operation": "handle_quick_operation",
    ".get_word_slices": "get_word_slices",
    "nc_get_rkey": "get_rkey",
    "send_group_sign": "set_group_sign",
    "ArkSharePeer": "share_peer",
    "ArkShareGroup": "share_group_ex",
}
snowluma_aliases = {"upload_foward_msg": "upload_forward_msg"}
for a, main in napcat_aliases.items():
    if a in napcat:
        napcat.discard(a)
        napcat.add(main)
for a, main in snowluma_aliases.items():
    if a in snowluma:
        snowluma.discard(a)
        snowluma.add(main)

print("=== 插件有但 NapCat 没有 ===")
for x in sorted(plugin - napcat):
    print(x)
print()
print("=== NapCat 有但插件没有 ===")
for x in sorted(napcat - plugin):
    print(x)
print()
print("=== 插件有但 SnowLuma 没有 ===")
for x in sorted(plugin - snowluma):
    print(x)
print()
print("=== SnowLuma 有但插件没有 ===")
for x in sorted(snowluma - plugin):
    print(x)
print()
print(f"统计: 插件={len(plugin)} NapCat={len(napcat)} SnowLuma={len(snowluma)}")
print(f"插件∩NapCat={len(plugin & napcat)} 插件∩SnowLuma={len(plugin & snowluma)}")
