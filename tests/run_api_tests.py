"""批量测试所有 API 的可调用性。

对每个 action 用空参数（或最小占位参数）调用一次 NapCat，
记录 status/retcode/msg，输出到 tests/api_test_report.md。

分类：
- OK: status=ok
- PARAM_ERR: retcode=1400/1404 等参数错误（说明 action 被识别，只是缺参数）
- FAILED: status=failed
- ERROR: 适配器连接异常

运行：
    python tests/run_api_tests.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import sys
# 插件根目录（向上两级到 plugins/.. 不一定有 onebot_expand 包）
# onebot_expand 包就是本目录的父目录
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from onebot_expand.api_defs import ALL_APIS
from onebot_expand.tests import call_napcat, is_available

# 某些 action 用空参数会崩溃或产生副作用，用最小占位参数
MIN_PARAMS: dict[str, dict] = {
    "send_msg": {"message": [{"type": "text", "data": {"text": "test"}}]},
    "send_group_msg": {"group_id": 1, "message": []},
    "send_private_msg": {"user_id": 1, "message": []},
    "delete_msg": {"message_id": 1},
    "get_msg": {"message_id": 1},
    "get_forward_msg": {"id": "1"},
    "set_group_kick": {"group_id": 1, "user_id": 1},
    "set_group_ban": {"group_id": 1, "user_id": 1, "duration": 0},
    "set_group_anonymous_ban": {"group_id": 1, "anonymous": ""},
    "set_group_whole_ban": {"group_id": 1, "enable": False},
    "set_group_admin": {"group_id": 1, "user_id": 1, "enable": False},
    "set_group_anonymous": {"group_id": 1, "enable": False},
    "set_group_card": {"group_id": 1, "user_id": 1, "card": ""},
    "set_group_name": {"group_id": 1, "group_name": "test"},
    "set_group_leave": {"group_id": 1},
    "set_group_special_title": {"group_id": 1, "user_id": 1, "special_title": ""},
    "set_group_kick_members": {"group_id": 1, "user_id_list": [1]},
    "set_group_portrait": {"group_id": 1, "file": ""},
    "set_group_remark": {"group_id": 1, "remark": ""},
    "set_group_add_option": {"group_id": 1},
    "set_group_search": {"group_id": 1},
    "set_group_robot_add_option": {"group_id": 1},
    "upload_group_file": {"group_id": 1, "file": "", "name": "t"},
    "upload_private_file": {"user_id": 1, "file": "", "name": "t"},
    "get_file": {"file_id": "1"},
    "get_image": {"file": "1"},
    "get_record": {"file": "1", "out_format": "mp3"},
    "get_stranger_info": {"user_id": 1},
    "get_group_member_info": {"group_id": 1, "user_id": 1},
    "get_group_info": {"group_id": 1},
    "get_group_detail_info": {"group_id": 1},
    "get_group_honor_info": {"group_id": 1, "type": "talkative"},
    "get_group_files_by_folder": {"group_id": 1, "folder_id": "1"},
    "delete_group_file": {"group_id": 1, "file_id": "1"},
    "create_group_file_folder": {"group_id": 1, "name": "t"},
    "delete_group_file_folder": {"group_id": 1, "folder_id": "1"},
    "delete_group_folder": {"group_id": 1, "folder_id": "1"},
    "get_group_file_url": {"group_id": 1, "file_id": "1"},
    "get_group_root_files": {"group_id": 1},
    "get_group_file_system_info": {"group_id": 1},
    "move_group_file": {"group_id": 1, "file_id": "1", "parent_folder_id": "1"},
    "rename_group_file": {"group_id": 1, "file_id": "1", "new_name": "t"},
    "rename_group_file_folder": {"group_id": 1, "folder_id": "1", "new_name": "t"},
    "trans_group_file": {"group_id": 1, "file_id": "1"},
    "get_private_file_url": {"user_id": 1, "file_id": "1"},
    "send_online_file": {"group_id": 1, "files": [{}]},
    "send_online_folder": {"group_id": 1, "files": [{}]},
    "get_online_file_msg": {"group_id": 1},
    "receive_online_file": {"group_id": 1, "file_uuid": "1"},
    "refuse_online_file": {"group_id": 1, "file_uuid": "1"},
    "cancel_online_file": {"group_id": 1, "file_uuid": "1"},
    "set_msg_emoji_like": {"message_id": 1, "emoji_id": "1"},
    "send_poke": {"user_id": 1},
    "send_forward_msg": {"messages": []},
    "send_group_forward_msg": {"group_id": 1, "messages": []},
    "send_private_forward_msg": {"user_id": 1, "messages": []},
    "get_group_msg_history": {"group_id": 1},
    "get_friend_msg_history": {"user_id": 1},
    "forward_friend_single_msg": {"user_id": 1, "message_id": 1},
    "forward_group_single_msg": {"group_id": 1, "message_id": 1},
    "mark_msg_as_read": {"message_id": 1},
    "mark_group_msg_as_read": {"group_id": 1},
    "mark_private_msg_as_read": {"user_id": 1},
    "set_essence_msg": {"message_id": 1},
    "delete_essence_msg": {"message_id": 1},
    "get_group_at_all_remain": {"group_id": 1},
    "set_friend_add_request": {"flag": "1", "approve": True},
    "set_group_add_request": {"flag": "1", "sub_type": "add", "approve": True},
    "delete_friend": {"user_id": 1},
    "set_friend_remark": {"user_id": 1, "remark": ""},
    "set_qq_profile": {"nickname": "t"},
    "set_qq_avatar": {"file": ""},
    "set_self_longnick": {"long_nick": "t"},
    "get_profile_like": {"user_id": 1},
    "get_recent_contact": {},
    "set_online_status": {"status": 1},
    "set_diy_online_status": {"text": "t"},
    "set_input_status": {"user_id": 1, "content": "t"},
    "friend_poke": {"user_id": 1},
    "group_poke": {"group_id": 1, "user_id": 1},
    "add_custom_face": {"file": ""},
    "delete_custom_face": {"face_id": "1"},
    "set_custom_face_desc": {"face_id": "1", "desc": ""},
    "modify_custom_face": {"face_id": "1"},
    "move_custom_face_to_front": {"face_id": "1"},
    "fetch_emoji_like": {"emoji_id": "1"},
    "get_emoji_likes": {"message_id": 1, "emoji_id": "1"},
    "set_group_reaction": {"group_id": 1, "message_id": 1, "emoji_id": "1"},
    "get_ai_record": {"character_id": "1", "text": "t"},
    "send_group_ai_record": {"group_id": 1, "character_id": "1", "text": "t"},
    "ocr_image": {"image": ""},
    "check_url_safely": {"url": "http://t"},
    "download_file": {"url": "http://t"},
    "click_inline_keyboard_button": {"bot_appid": 1, "button_id": "1"},
    "get_mini_app_ark": {"word": "t"},
    "translate_en2zh": {"words": ["t"]},
    "create_collection": {"summary": "t"},
    "send_packet": {"cmd": "t"},
    "create_flash_task": {"group_id": 1, "files": [{}]},
    "send_flash_msg": {"group_id": 1, "files": [{}]},
    "get_flash_file_url": {"group_id": 1, "file_id": "1"},
    "get_share_link": {"group_id": 1, "file_id": "1"},
    "download_fileset": {"fileset_id": "1"},
    "get_fileset_info": {"fileset_id": "1"},
    "get_fileset_id": {"code": "t"},
    "list_filesets": {"group_id": 1},
    "delete_flash_file": {"group_id": 1, "file_id": "1"},
    "rename_flash_file": {"group_id": 1, "file_id": "1", "new_name": "t"},
    "get_group_album_media_list": {"group_id": 1, "album_id": "1"},
    "upload_image_to_qun_album": {"group_id": 1, "file": ""},
    "do_group_album_comment": {"group_id": 1, "album_id": "1", "media_id": "1", "content": "t"},
    "set_group_album_media_like": {"group_id": 1, "album_id": "1", "media_id": "1"},
    "cancel_group_album_media_like": {"group_id": 1, "album_id": "1", "media_id": "1"},
    "del_group_album_media": {"group_id": 1, "album_id": "1", "media_id_list": ["1"]},
    "set_group_todo": {"group_id": 1, "content": "t"},
    "complete_group_todo": {"group_id": 1, "todo_id": "1"},
    "cancel_group_todo": {"group_id": 1, "todo_id": "1"},
    "send_qzone_msg": {"message": "t"},
    "delete_qzone_msg": {"dynamic_id": "1"},
    "like_qzone": {"dynamic_id": "1"},
    "unlike_qzone": {"dynamic_id": "1"},
    "comment_qzone": {"dynamic_id": "1", "content": "t"},
    "set_qzone_ban": {"user_id": 1, "duration": 1},
    "set_qzone_msg_right": {"user_id": 1},
    "share_peer": {"user_id": 1},
    "send_ark_share": {"user_id": 1, "ark": {}},
    "share_group_ex": {"group_id": 1},
    "send_group_ark_share": {"group_id": 1, "ark": {}},
    "set_group_sign": {"group_id": 1},
    "fetch_ptt_text": {"file_id": "1"},
    "get_doubt_friends_add_request": {},
    "set_doubt_friends_add_request": {"flag": "1", "approve": True},
    "request_decrypt_key": {"encrypted_file": ""},
    "set_qq_avatar": {"file": ""},
    "nc_get_user_status": {"user_id": 1},
    "get_cookies": {"domain": ""},
    "set_restart": {"delay": 0, "clean_cache": False},
    "set_input_status": {"user_id": 1, "content": ""},
    "get_robot_uin_range": {},
    "set_group_add_option": {"group_id": 1},
    "nc_get_rkey": {},
    "get_rkey": {},
    "get_rkey_server": {},
    "download_file_stream": {"url": "http://t"},
    "download_file_record_stream": {"url": "http://t"},
    "download_file_image_stream": {"url": "http://t"},
    "upload_file_stream": {"file": ""},
    "clean_stream_temp_file": {},
    "upload_forward_msg": {"messages": []},
    "handle_quick_operation": {"context": {}, "operation": {}},
    ".handle_quick_operation": {"context": {}, "operation": {}},
    ".get_word_slices": {"content": "t"},
    "get_group_system_msg": {},
    "get_group_ignore_add_request": {"group_id": 1},
    "get_group_ignored_notifies": {"group_id": 1},
    "get_group_shut_list": {"group_id": 1},
    "get_group_info_ex": {"group_id": 1},
    "get_group_signed_list": {"group_id": 1},
    "get_unidirectional_friend_list": {},
    "get_friends_with_category": {},
    "fetch_custom_face": {"count": 1},
    "fetch_custom_face_detail": {"face_id": "1"},
    "get_essence_msg_list": {"group_id": 1},
    "get_group_album_list": {"group_id": 1},
    "get_qun_album_list": {"group_id": 1},
    "get_qzone_msg_list": {},
    "get_qzone_feeds": {"count": 1},
    "get_ai_characters": {},
    "get_clientkey": {},
    "get_credentials": {"domain": ""},
    "get_csrf_token": {},
    "_get_model_show": {"model": "t"},
    "_set_model_show": {"model": "t", "show_type": 0},
    "._get_model_show": {"model": "t"},
    "._set_model_show": {"model": "t", "show_type": 0},
    "bot_exit": {},
    "nc_get_packet_status": {},
    "get_collection_list": {"count": 1},
    "_mark_all_as_read": {},
    "_send_group_notice": {"group_id": 1, "content": "t"},
    "_get_group_notice": {"group_id": 1},
    "_del_group_notice": {"group_id": 1, "notice_id": "1"},
    "get_status": {},
    "get_version_info": {},
    "get_login_info": {},
    "can_send_image": {},
    "can_send_record": {},
    "clean_cache": {},
    "get_friend_list": {},
    "get_group_list": {},
    "get_group_member_list": {"group_id": 1},
    "fetch_emoji_like": {"emoji_id": "1"},
    "set_msg_emoji_like": {"message_id": 1, "emoji_id": "1"},
    "send_like": {"user_id": 1, "times": 1},
    ".ocr_image": {"image": ""},
    ".send_packet": {"cmd": "t"},
}


def categorize(resp: dict) -> str:
    status = resp.get("status")
    retcode = resp.get("retcode", 0)
    if status == "ok":
        return "OK"
    if status == "error":
        return "ERROR"
    if status == "failed":
        if retcode in (1400, 1404) or "参数" in str(resp.get("msg", "")) or "不支持" in str(resp.get("msg", "")):
            return "PARAM_ERR"
        return "FAILED"
    return "UNKNOWN"


def main() -> None:
    if not is_available():
        print("NapCat 不可达，退出")
        return

    actions = list(ALL_APIS.keys())
    # 也测试别名
    aliases: list[str] = []
    for api_def in ALL_APIS.values():
        aliases.extend(api_def.aliases)

    results: list[dict] = []
    total = len(actions) + len(aliases)
    for i, action in enumerate(actions + aliases, 1):
        params = MIN_PARAMS.get(action, {})
        # 重试 3 次，每次 20s 超时
        resp = None
        for attempt in range(3):
            resp = call_napcat(action, params, timeout=20.0)
            if resp.get("status") != "error":
                break
            time.sleep(2.0)
        if resp is None:
            resp = {"status": "error", "retcode": -1, "msg": "no response"}
        cat = categorize(resp)
        results.append({
            "action": action,
            "is_alias": action in aliases,
            "category": cat,
            "status": resp.get("status", ""),
            "retcode": resp.get("retcode", ""),
            "msg": str(resp.get("msg", resp.get("wording", "")))[:120],
        })
        print(f"[{i:>3}/{total}] {action:<35} {cat:<10} {resp.get('retcode', '')}", flush=True)
        time.sleep(0.3)

    # 输出报告
    report_path = Path(__file__).parent / "api_test_report.md"
    with report_path.open("w", encoding="utf-8") as f:
        f.write("# API 测试报告\n\n")
        f.write(f"测试时间：{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"NapCat 登录账号：3693525299 (Navinatte)\n")
        f.write(f"测试总数：{len(results)}（主名 {len(actions)} + 别名 {len(aliases)}）\n\n")
        # 统计
        from collections import Counter
        stat = Counter(r["category"] for r in results)
        f.write("## 统计\n\n")
        f.write("| 类别 | 数量 | 说明 |\n|---|---|---|\n")
        f.write(f"| OK | {stat.get('OK', 0)} | 调用成功 |\n")
        f.write(f"| PARAM_ERR | {stat.get('PARAM_ERR', 0)} | 参数错误（action 被识别） |\n")
        f.write(f"| FAILED | {stat.get('FAILED', 0)} | 调用失败 |\n")
        f.write(f"| ERROR | {stat.get('ERROR', 0)} | 连接/适配器异常 |\n")
        f.write(f"| UNKNOWN | {stat.get('UNKNOWN', 0)} | 未知状态 |\n\n")
        # 明细
        f.write("## 明细\n\n")
        f.write("| action | 类型 | 类别 | status | retcode | msg |\n")
        f.write("|---|---|---|---|---|---|\n")
        for r in results:
            kind = "别名" if r["is_alias"] else "主名"
            msg = r["msg"].replace("|", "\\|")
            f.write(f"| `{r['action']}` | {kind} | {r['category']} | {r['status']} | {r['retcode']} | {msg} |\n")
    print(f"\n报告已写入：{report_path}")


if __name__ == "__main__":
    main()
