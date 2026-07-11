# API 测试报告

测试时间：2026-07-08 14:25:51
NapCat 登录账号：3693525299 (Navinatte)
测试总数：196（主名 184 + 别名 12）

## 统计

| 类别 | 数量 | 说明 |
|---|---|---|
| OK | 26 | 调用成功 |
| PARAM_ERR | 51 | 参数错误（action 被识别） |
| FAILED | 35 | 调用失败 |
| ERROR | 84 | 连接/适配器异常 |
| UNKNOWN | 0 | 未知状态 |

## 明细

| action | 类型 | 类别 | status | retcode | msg |
|---|---|---|---|---|---|
| `send_group_msg` | 主名 | FAILED | failed | 1200 | 消息体无法解析, 请检查是否发送了不支持的消息类型 |
| `send_private_msg` | 主名 | FAILED | failed | 1200 | 无法获取用户信息 |
| `send_msg` | 主名 | FAILED | failed | 1200 | 请指定正确的 group_id 或 user_id |
| `delete_msg` | 主名 | FAILED | failed | 1200 | Recall failed |
| `get_msg` | 主名 | FAILED | failed | 1200 | 消息不存在 |
| `get_forward_msg` | 主名 | FAILED | failed | 1200 | 消息已过期或者为内层消息，无法获取转发消息 |
| `send_like` | 主名 | FAILED | failed | 1200 | 点赞失败 被点赞 QQ 号非法 |
| `send_poke` | 主名 | OK | ok | 0 |  |
| `send_forward_msg` | 主名 | FAILED | failed | 1200 | 请指定正确的 group_id 或 user_id |
| `send_group_forward_msg` | 主名 | FAILED | failed | 1200 | 消息体无法解析, 请检查是否发送了不支持的消息类型 |
| `send_private_forward_msg` | 主名 | FAILED | failed | 1200 | 无法获取用户信息 |
| `get_group_msg_history` | 主名 | FAILED | failed | 1200 | 消息undefined不存在 |
| `get_friend_msg_history` | 主名 | FAILED | failed | 1200 | 记录1不存在 |
| `forward_friend_single_msg` | 主名 | FAILED | failed | 1200 | 无法找到消息1 |
| `forward_group_single_msg` | 主名 | FAILED | failed | 1200 | 无法找到消息1 |
| `mark_msg_as_read` | 主名 | FAILED | failed | 1200 | 缺少参数 group_id 或 user_id |
| `mark_group_msg_as_read` | 主名 | OK | ok | 0 |  |
| `mark_private_msg_as_read` | 主名 | FAILED | failed | 1200 | 私聊1不存在 |
| `_mark_all_as_read` | 主名 | ERROR | error | -1 | TimeoutError:  |
| `upload_forward_msg` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API upload_forward_msg |
| `set_group_kick` | 主名 | FAILED | failed | 1200 | get Uid Error |
| `set_group_ban` | 主名 | FAILED | failed | 1200 | uid error |
| `set_group_anonymous_ban` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API set_group_anonymous_ban |
| `set_group_whole_ban` | 主名 | FAILED | failed | 1200 | SetGroupWholeBan failed:  1010 |
| `set_group_admin` | 主名 | FAILED | failed | 1200 | get Uid Error |
| `set_group_anonymous` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API set_group_anonymous |
| `set_group_card` | 主名 | FAILED | failed | 1200 | 群(1)成员1不存在 |
| `set_group_name` | 主名 | FAILED | failed | 1200 | 设置群名称失败 ErrCode: 1010 ErrMsg:  |
| `set_group_leave` | 主名 | OK | ok | 0 |  |
| `set_group_special_title` | 主名 | FAILED | failed | 1200 | User not found |
| `upload_group_file` | 主名 | FAILED | failed | 1200 | EISDIR: illegal operation on a directory, read |
| `upload_private_file` | 主名 | FAILED | failed | 1200 | 无法获取用户信息 |
| `get_file` | 主名 | ERROR | error | -1 | TimeoutError:  |
| `get_image` | 主名 | ERROR | error | -1 | TimeoutError:  |
| `get_record` | 主名 | OK | ok | 0 |  |
| `send_online_file` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `send_online_folder` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `get_online_file_msg` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `receive_online_file` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `refuse_online_file` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `cancel_online_file` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `clean_stream_temp_file` | 主名 | OK | ok | 0 |  |
| `upload_file_stream` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `download_file_stream` | 主名 | FAILED | failed | 1200 | Download failed: file not found |
| `download_file_record_stream` | 主名 | FAILED | failed | 1200 | Download failed: file not found |
| `download_file_image_stream` | 主名 | FAILED | failed | 1200 | Download failed: file not found |
| `get_login_info` | 主名 | OK | ok | 0 |  |
| `get_stranger_info` | 主名 | OK | ok | 0 |  |
| `get_friend_list` | 主名 | OK | ok | 0 |  |
| `get_group_list` | 主名 | OK | ok | 0 |  |
| `get_group_member_list` | 主名 | OK | ok | 0 |  |
| `get_group_member_info` | 主名 | FAILED | failed | 1200 | Uin2Uid Error: 用户ID 1 不存在 |
| `get_group_info` | 主名 | FAILED | failed | 1200 | EventChecker Failed: NTEvent serviceAndMethod:NodeIKernelGroupService/getGroupDetailInfo ListenerName:NodeIKernelGroupLi |
| `get_group_detail_info` | 主名 | FAILED | failed | 1200 | EventChecker Failed: NTEvent serviceAndMethod:NodeIKernelGroupService/getGroupDetailInfo ListenerName:NodeIKernelGroupLi |
| `get_group_honor_info` | 主名 | OK | ok | 0 |  |
| `get_robot_uin_range` | 主名 | OK | ok | 0 |  |
| `set_msg_emoji_like` | 主名 | FAILED | failed | 1200 | msg not found |
| `get_essence_msg_list` | 主名 | OK | ok | 0 |  |
| `get_online_clients` | 主名 | OK | ok | 0 |  |
| `get_cookies` | 主名 | OK | ok | 0 |  |
| `get_csrf_token` | 主名 | OK | ok | 0 |  |
| `get_status` | 主名 | OK | ok | 0 |  |
| `set_restart` | 主名 | OK | ok | 0 |  |
| `clean_cache` | 主名 | ERROR | error | -1 | InvalidMessage: did not receive a valid HTTP response |
| `can_send_image` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `can_send_record` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_version_info` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_essence_msg` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `delete_essence_msg` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_group_at_all_remain` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `fetch_ptt_text` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_group_file_url` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_group_root_files` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_group_files_by_folder` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `delete_group_file` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `create_group_file_folder` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `delete_group_folder` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_group_file_system_info` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `move_group_file` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `rename_group_file` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `rename_group_file_folder` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `trans_group_file` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_private_file_url` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `_send_group_notice` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `_get_group_notice` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `_del_group_notice` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_group_portrait` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_group_remark` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_group_add_option` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_group_search` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_group_robot_add_option` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_group_kick_members` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_group_shut_list` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_group_ignored_notifies` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_group_ignore_add_request` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_group_info_ex` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_group_sign` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_group_signed_list` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_friend_add_request` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_group_add_request` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_group_system_msg` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_doubt_friends_add_request` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_doubt_friends_add_request` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `delete_friend` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_friend_remark` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_friends_with_category` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_unidirectional_friend_list` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_qq_profile` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_qq_avatar` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_self_longnick` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_recent_contact` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_profile_like` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_online_status` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_diy_online_status` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_input_status` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `nc_get_user_status` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `friend_poke` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `group_poke` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `fetch_custom_face` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `add_custom_face` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `delete_custom_face` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `fetch_custom_face_detail` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_custom_face_desc` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `modify_custom_face` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `move_custom_face_to_front` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `fetch_emoji_like` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_emoji_likes` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `set_group_reaction` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_ai_characters` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_ai_record` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `send_group_ai_record` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_clientkey` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_credentials` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_rkey` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `get_rkey_server` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `check_url_safely` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `ocr_image` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `download_file` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `request_decrypt_key` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `_get_model_show` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `_set_model_show` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `bot_exit` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `nc_get_packet_status` | 主名 | ERROR | error | -1 | ConnectionRefusedError: [WinError 1225] 远程计算机拒绝网络连接。 |
| `click_inline_keyboard_button` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `get_mini_app_ark` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected union value |
| `translate_en2zh` | 主名 | OK | ok | 0 |  |
| `create_collection` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `get_collection_list` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `send_packet` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `handle_quick_operation` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API handle_quick_operation |
| `create_flash_task` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected union value |
| `send_flash_msg` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `get_flash_file_list` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `get_flash_file_url` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `get_share_link` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `download_fileset` | 主名 | OK | ok | 0 |  |
| `get_fileset_info` | 主名 | OK | ok | 0 |  |
| `get_fileset_id` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `list_filesets` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API list_filesets |
| `delete_flash_file` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API delete_flash_file |
| `rename_flash_file` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API rename_flash_file |
| `get_qun_album_list` | 主名 | OK | ok | 0 |  |
| `upload_image_to_qun_album` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `get_group_album_media_list` | 主名 | OK | ok | 0 |  |
| `do_group_album_comment` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `set_group_album_media_like` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `cancel_group_album_media_like` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `del_group_album_media` | 主名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `set_group_todo` | 主名 | FAILED | failed | 1200 | 缺少参数 message_id 或 message_seq |
| `complete_group_todo` | 主名 | FAILED | failed | 1200 | 缺少参数 message_id 或 message_seq |
| `cancel_group_todo` | 主名 | FAILED | failed | 1200 | 缺少参数 message_id 或 message_seq |
| `get_qzone_msg_list` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API get_qzone_msg_list |
| `get_qzone_feeds` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API get_qzone_feeds |
| `send_qzone_msg` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API send_qzone_msg |
| `delete_qzone_msg` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API delete_qzone_msg |
| `like_qzone` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API like_qzone |
| `unlike_qzone` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API unlike_qzone |
| `comment_qzone` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API comment_qzone |
| `set_qzone_ban` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API set_qzone_ban |
| `set_qzone_msg_right` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API set_qzone_msg_right |
| `share_peer` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API share_peer |
| `send_ark_share` | 主名 | OK | ok | 0 |  |
| `share_group_ex` | 主名 | PARAM_ERR | failed | 1404 | 不支持的API share_group_ex |
| `send_group_ark_share` | 主名 | OK | ok | 0 |  |
| `upload_foward_msg` | 别名 | PARAM_ERR | failed | 1404 | 不支持的API upload_foward_msg |
| `get_ptt_text` | 别名 | PARAM_ERR | failed | 1404 | 不支持的API get_ptt_text |
| `get_record_text` | 别名 | PARAM_ERR | failed | 1404 | 不支持的API get_record_text |
| `delete_group_file_folder` | 别名 | PARAM_ERR | failed | 1404 | 不支持的API delete_group_file_folder |
| `send_group_sign` | 别名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `nc_get_rkey` | 别名 | OK | ok | 0 |  |
| `.ocr_image` | 别名 | ERROR | error | -1 | TimeoutError:  |
| `._get_model_show` | 别名 | PARAM_ERR | failed | 1404 | 不支持的API ._get_model_show |
| `._set_model_show` | 别名 | PARAM_ERR | failed | 1404 | 不支持的API ._set_model_show |
| `.send_packet` | 别名 | PARAM_ERR | failed | 1404 | 不支持的API .send_packet |
| `.handle_quick_operation` | 别名 | PARAM_ERR | failed | 1400 | Schema compilation error: Expected required property |
| `get_group_album_list` | 别名 | PARAM_ERR | failed | 1404 | 不支持的API get_group_album_list |
