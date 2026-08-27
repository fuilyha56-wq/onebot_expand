"""Step 3 对照脚本：三方上游 action 名单 vs 插件 ALL_APIS。

从上游源码实时扫描，输出「上游有、插件没有」与「插件有、上游没有」清单。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PLUG = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUG.parent))

from onebot_expand.api_defs import ALL_APIS  # noqa: E402

IGNORE_NAPCAT = {
    "test_auto_register_01", "test_auto_register_02", "test_download_stream",
    "unknown", "ArkSharePeer", "ArkShareGroup", "get_guild_service_profile",
    "reboot_normal", "reload_event_filter", "qidian_get_account_info",
    "delete_unidirectional_friend", "get_guild_service_profile",
}


def scan_napcat() -> set[str]:
    text = Path(r"E:\NapCatQQ\packages\napcat-onebot\action\router.ts").read_text(encoding="utf-8")
    names = re.findall(r":\s*'([\w.]+)'", text)
    return {n for n in names if n not in IGNORE_NAPCAT}


def scan_snowluma() -> set[str]:
    root = Path(r"E:\SnowLuma\packages\onebot\src\actions")
    names: set[str] = set()
    for f in root.glob("*.ts"):
        if f.name in {"index.ts"}:
            continue
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r"^\s*name(\?)?:\s*('([^']+)'|\[([^\]]*)\])", text, re.M):
            if m.group(3):
                names.add(m.group(3))
            else:
                names.update(re.findall(r"'([^']+)'", m.group(4)))
    # api-handler.ts 手动注册
    names.add(".handle_quick_operation")
    return names - {"test_download_stream", "SnowLuma"}


def scan_llbot() -> set[str]:
    text = Path(r"E:\LLBot\src\onebot11\action\types.ts").read_text(encoding="utf-8")
    return set(re.findall(r"=\s*['\"]([\w.]+)['\"]", text))


def main() -> None:
    nap = scan_napcat()
    sl = scan_snowluma()
    ll = scan_llbot()
    plug = set(ALL_APIS.keys())
    plug_aliases: set[str] = set()
    for d in ALL_APIS.values():
        plug_aliases.update(d.aliases)
    plug_callable = plug | plug_aliases

    upstream_all = nap | sl | ll
    print(f"NapCat: {len(nap)}  SnowLuma: {len(sl)}  LLBot: {len(ll)}  联合: {len(upstream_all)}")
    print(f"插件主名: {len(plug)}  别名: {len(plug_aliases)}  可调用: {len(plug_callable)}")
    print()
    print("== 待适配（上游有、插件无） ==")
    for a in sorted(upstream_all - plug_callable):
        src = []
        if a in nap:
            src.append("N")
        if a in sl:
            src.append("S")
        if a in ll:
            src.append("L")
        print(f"  {a}  [{''.join(src)}]")
    print()
    print("== 插件有、三方上游均无（候选废弃） ==")
    for a in sorted(plug - upstream_all):
        print(f"  {a}")
    print()
    print("== 兼容性复核（snowluma_compat 标记 vs 实际注册） ==")
    for a, d in sorted(ALL_APIS.items()):
        actual_sl = a in sl or any(x in sl for x in d.aliases)
        if d.snowluma_compat != actual_sl:
            print(f"  {a}: 标记={d.snowluma_compat} 实际SL={actual_sl}")
    print()
    print("== napcat_only 复核 ==")
    for a, d in sorted(ALL_APIS.items()):
        actual_nap = a in nap or any(x in nap for x in d.aliases)
        if d.napcat_only and not actual_nap:
            print(f"  {a}: napcat_only=True 但 NapCat 未注册")


if __name__ == "__main__":
    main()
