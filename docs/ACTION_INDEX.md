# onebot_expand API 索引名单

> 共 **205** 个主名 action + **18** 个别名 · 覆盖 OneBot v11 / NapCat / SnowLuma / LLBot 四方协议端

**来源标记**：`OB11`=OneBot v11 标准 · `NapCat`=NapCat 扩展 · `go-cqhttp`=go-cqhttp 兼容 · `Expand`=插件扩展 · `LLBot`=LLBot 扩展

**兼容性标记**：`napcat_only` 列 `✓`=NapCat 专属（SnowLuma 不支持）· `snowluma_compat` 列 `✓`=SnowLuma 兼容 · `—`=不适用/默认值

---

## 按分类

### 消息 (message, 20 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `send_group_msg` | OB11 | — | ✓ | — |
| `send_private_msg` | OB11 | — | ✓ | — |
| `send_msg` | OB11 | — | ✓ | — |
| `delete_msg` | OB11 | — | ✓ | — |
| `get_msg` | OB11 | — | ✓ | — |
| `get_forward_msg` | OB11 | — | ✓ | — |
| `send_like` | OB11 | — | ✓ | — |
| `send_poke` | NapCat | — | ✓ | — |
| `send_forward_msg` | NapCat | — | ✓ | — |
| `send_group_forward_msg` | go-cqhttp | — | ✓ | — |
| `send_private_forward_msg` | go-cqhttp | — | ✓ | — |
| `get_group_msg_history` | go-cqhttp | — | ✓ | — |
| `get_friend_msg_history` | go-cqhttp | — | ✓ | — |
| `forward_friend_single_msg` | Expand | — | ✓ | — |
| `forward_group_single_msg` | Expand | — | ✓ | — |
| `mark_msg_as_read` | go-cqhttp | — | ✓ | — |
| `mark_group_msg_as_read` | Expand | — | ✓ | — |
| `mark_private_msg_as_read` | Expand | — | ✓ | — |
| `_mark_all_as_read` | Expand | — | ✓ | — |
| `upload_forward_msg` | Expand | — | ✓ | upload_foward_msg |

### 群操作 (group, 10 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `set_group_kick` | OB11 | — | ✓ | — |
| `set_group_ban` | OB11 | — | ✓ | — |
| `set_group_anonymous_ban` | OB11 | — | ✓ | — |
| `set_group_whole_ban` | OB11 | — | ✓ | — |
| `set_group_admin` | OB11 | — | ✓ | — |
| `set_group_anonymous` | OB11 | — | ✓ | — |
| `set_group_card` | OB11 | — | ✓ | — |
| `set_group_name` | OB11 | — | ✓ | — |
| `set_group_leave` | OB11 | — | ✓ | — |
| `set_group_special_title` | OB11 | — | ✓ | — |

### 文件操作 (file, 16 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `upload_group_file` | OB11 | — | ✓ | — |
| `upload_private_file` | OB11 | — | ✓ | — |
| `get_file` | NapCat | — | ✓ | — |
| `get_image` | OB11 | — | ✓ | — |
| `get_record` | OB11 | — | ✓ | — |
| `send_online_file` | NapCat | ✓ | ✗ | — |
| `send_online_folder` | NapCat | ✓ | ✗ | — |
| `get_online_file_msg` | NapCat | ✓ | ✗ | — |
| `receive_online_file` | NapCat | ✓ | ✗ | — |
| `refuse_online_file` | NapCat | ✓ | ✗ | — |
| `cancel_online_file` | NapCat | ✓ | ✗ | — |
| `clean_stream_temp_file` | Expand | — | ✓ | — |
| `upload_file_stream` | Expand | — | ✓ | — |
| `download_file_stream` | Expand | — | ✓ | — |
| `download_file_record_stream` | Expand | — | ✓ | — |
| `download_file_image_stream` | Expand | — | ✓ | — |

### 账号信息 (account, 10 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `get_login_info` | OB11 | — | ✓ | — |
| `get_stranger_info` | OB11 | — | ✓ | — |
| `get_friend_list` | OB11 | — | ✓ | — |
| `get_group_list` | OB11 | — | ✓ | — |
| `get_group_member_list` | OB11 | — | ✓ | — |
| `get_group_member_info` | OB11 | — | ✓ | — |
| `get_group_info` | OB11 | — | ✓ | — |
| `get_group_detail_info` | NapCat | — | ✓ | — |
| `get_group_honor_info` | OB11 | — | ✓ | — |
| `get_robot_uin_range` | Expand | ✓ | ✗ | — |

### NapCat 扩展 (napcat_ext, 15 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `set_msg_emoji_like` | NapCat | — | ✓ | — |
| `get_essence_msg_list` | go-cqhttp | — | ✓ | — |
| `get_online_clients` | NapCat | — | ✓ | — |
| `get_cookies` | NapCat | — | ✓ | — |
| `get_csrf_token` | NapCat | — | ✓ | — |
| `get_status` | NapCat | — | ✓ | — |
| `set_restart` | NapCat | — | ✓ | — |
| `clean_cache` | NapCat | — | ✓ | — |
| `can_send_image` | NapCat | — | ✓ | — |
| `can_send_record` | NapCat | — | ✓ | — |
| `get_version_info` | NapCat | — | ✓ | — |
| `set_essence_msg` | go-cqhttp | — | ✓ | — |
| `delete_essence_msg` | go-cqhttp | — | ✓ | — |
| `get_group_at_all_remain` | go-cqhttp | — | ✓ | — |
| `fetch_ptt_text` | Expand | — | ✓ | get_ptt_text, get_record_text |

### 群文件管理 (group_file, 13 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `get_group_file_url` | go-cqhttp | — | ✓ | — |
| `get_group_root_files` | go-cqhttp | — | ✓ | — |
| `get_group_files_by_folder` | go-cqhttp | — | ✓ | — |
| `delete_group_file` | go-cqhttp | — | ✓ | — |
| `create_group_file_folder` | go-cqhttp | — | ✓ | — |
| `delete_group_folder` | go-cqhttp | — | ✓ | — |
| `get_group_file_system_info` | go-cqhttp | — | ✓ | — |
| `move_group_file` | Expand | — | ✓ | — |
| `rename_group_file` | Expand | — | ✓ | — |
| `rename_group_file_folder` | Expand | — | ✓ | — |
| `trans_group_file` | Expand | — | ✓ | — |
| `get_private_file_url` | Expand | — | ✓ | — |
| `set_group_file_forever` | LLBot | — | ✓ | — |

### 群公告 (group_notice, 3 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `_send_group_notice` | Expand | — | ✓ | — |
| `_get_group_notice` | Expand | — | ✓ | — |
| `_del_group_notice` | Expand | — | ✓ | — |

### 群管理扩展 (group_ext, 14 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `set_group_portrait` | Expand | — | ✓ | — |
| `set_group_remark` | Expand | — | ✓ | — |
| `set_group_add_option` | Expand | — | ✓ | — |
| `set_group_search` | Expand | — | ✓ | — |
| `set_group_robot_add_option` | Expand | — | ✓ | — |
| `set_group_kick_members` | Expand | — | ✓ | — |
| `get_group_shut_list` | Expand | — | ✓ | — |
| `get_group_ignored_notifies` | Expand | — | ✓ | — |
| `get_group_ignore_add_request` | Expand | — | ✓ | — |
| `get_group_info_ex` | Expand | — | ✓ | — |
| `set_group_sign` | Expand | — | ✓ | send_group_sign |
| `get_group_signed_list` | Expand | — | ✓ | — |
| `batch_delete_group_member` | LLBot | — | ✓ | — |
| `set_group_msg_mask` | LLBot | — | ✓ | — |

### 请求处理 (request, 5 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `set_friend_add_request` | OB11 | — | ✓ | — |
| `set_group_add_request` | OB11 | — | ✓ | — |
| `get_group_system_msg` | OB11 | — | ✓ | — |
| `get_doubt_friends_add_request` | Expand | — | ✓ | — |
| `set_doubt_friends_add_request` | Expand | — | ✓ | — |

### 用户信息扩展 (user_ext, 13 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `delete_friend` | Expand | — | ✓ | — |
| `set_friend_remark` | Expand | — | ✓ | — |
| `get_friends_with_category` | Expand | — | ✓ | — |
| `get_unidirectional_friend_list` | Expand | — | ✓ | — |
| `set_qq_profile` | go-cqhttp | — | ✓ | — |
| `set_qq_avatar` | Expand | — | ✓ | — |
| `set_self_longnick` | Expand | — | ✓ | — |
| `get_recent_contact` | Expand | — | ✓ | — |
| `get_profile_like` | Expand | — | ✓ | — |
| `get_profile_like_me` | LLBot | — | ✓ | — |
| `get_profile_like_count` | LLBot | — | ✓ | — |
| `get_qq_avatar` | LLBot | — | ✓ | — |
| `set_friend_category` | LLBot | — | ✓ | — |

### 在线状态 (status, 4 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `set_online_status` | Expand | — | ✓ | — |
| `set_diy_online_status` | Expand | — | ✓ | — |
| `set_input_status` | Expand | — | ✓ | — |
| `nc_get_user_status` | Expand | — | ✓ | — |

### 戳一拍 (poke, 2 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `friend_poke` | Expand | — | ✓ | — |
| `group_poke` | Expand | — | ✓ | — |

### 表情/收藏扩展 (emoji_ext, 12 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `fetch_custom_face` | Expand | — | ✓ | — |
| `fetch_custom_face_detail` | Expand | ✓ | ✗ | — |
| `add_custom_face` | Expand | — | ✓ | — |
| `delete_custom_face` | Expand | — | ✓ | — |
| `set_custom_face_desc` | Expand | ✓ | ✗ | — |
| `modify_custom_face` | Expand | — | ✓ | — |
| `move_custom_face_to_front` | Expand | — | ✓ | — |
| `fetch_emoji_like` | Expand | — | ✓ | — |
| `get_emoji_likes` | Expand | — | ✓ | — |
| `set_group_reaction` | Expand | — | ✓ | — |
| `get_recommend_face` | LLBot | — | ✓ | — |
| `unset_msg_emoji_like` | LLBot | — | ✓ | — |

### AI语音 (ai_voice, 3 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `get_ai_characters` | Expand | — | ✓ | — |
| `get_ai_record` | Expand | — | ✓ | — |
| `send_group_ai_record` | Expand | — | ✓ | — |

### 凭证/安全/下载 (cred, 8 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `get_clientkey` | Expand | — | ✓ | — |
| `get_credentials` | Expand | — | ✓ | — |
| `get_rkey` | Expand | — | ✓ | nc_get_rkey |
| `get_rkey_server` | Expand | — | ✓ | — |
| `check_url_safely` | Expand | — | ✓ | — |
| `ocr_image` | go-cqhttp | — | ✓ | .ocr_image |
| `download_file` | Expand | — | ✓ | — |
| `request_decrypt_key` | Expand | — | ✓ | — |

### 机型/其他 (misc, 18 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `_get_model_show` | Expand | — | ✓ | ._get_model_show |
| `_set_model_show` | Expand | — | ✓ | ._set_model_show |
| `bot_exit` | Expand | — | ✓ | — |
| `nc_get_packet_status` | Expand | — | ✓ | — |
| `click_inline_keyboard_button` | Expand | — | ✓ | — |
| `get_mini_app_ark` | Expand | — | ✓ | — |
| `translate_en2zh` | Expand | — | ✓ | — |
| `create_collection` | Expand | — | ✓ | — |
| `get_collection_list` | Expand | — | ✓ | — |
| `send_packet` | Expand | — | ✓ | .send_packet |
| `handle_quick_operation` | go-cqhttp | — | ✓ | .handle_quick_operation |
| `get_word_slices` | go-cqhttp | ✓ | ✗ | .get_word_slices |
| `get_config` | LLBot | — | ✓ | — |
| `set_config` | LLBot | — | ✓ | — |
| `get_event` | LLBot | — | ✓ | — |
| `llonebot_debug` | LLBot | — | ✓ | — |
| `scan_qrcode` | LLBot | — | ✓ | — |
| `get_guild_list` | LLBot | — | ✓ | — |

### 闪传 (flash, 14 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `create_flash_task` | Expand | — | ✓ | — |
| `send_flash_msg` | Expand | — | ✓ | — |
| `get_flash_file_list` | Expand | — | ✓ | — |
| `get_flash_file_url` | Expand | — | ✓ | — |
| `get_share_link` | Expand | — | ✓ | — |
| `download_fileset` | Expand | — | ✓ | download_flash_file |
| `get_fileset_info` | Expand | — | ✓ | get_flash_file_info |
| `get_fileset_id` | Expand | — | ✓ | — |
| `list_filesets` | Expand | — | ✓ | — |
| `delete_flash_file` | Expand | — | ✓ | — |
| `rename_flash_file` | Expand | — | ✓ | — |
| `get_flash_file_download_urls` | LLBot | — | ✓ | — |
| `upload_flash_file` | LLBot | — | ✓ | — |
| `reshare_flash_file` | LLBot | — | ✓ | — |

### 群相册 (group_album, 9 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `get_qun_album_list` | Expand | — | ✓ | — |
| `upload_image_to_qun_album` | Expand | — | ✓ | upload_group_album |
| `get_group_album_media_list` | Expand | — | ✓ | — |
| `do_group_album_comment` | Expand | — | ✓ | — |
| `set_group_album_media_like` | Expand | — | ✓ | — |
| `cancel_group_album_media_like` | Expand | — | ✓ | — |
| `del_group_album_media` | Expand | — | ✓ | — |
| `create_group_album` | LLBot | — | ✓ | — |
| `delete_group_album` | LLBot | — | ✓ | — |

### 群待办 (group_todo, 3 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `set_group_todo` | Expand | — | ✓ | — |
| `complete_group_todo` | Expand | — | ✓ | — |
| `cancel_group_todo` | Expand | — | ✓ | — |

### QQ空间 (qzone, 9 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `get_qzone_msg_list` | Expand | — | ✓ | — |
| `get_qzone_feeds` | Expand | — | ✓ | — |
| `send_qzone_msg` | Expand | — | ✓ | — |
| `delete_qzone_msg` | Expand | — | ✓ | — |
| `like_qzone` | Expand | — | ✓ | — |
| `unlike_qzone` | Expand | — | ✓ | — |
| `comment_qzone` | Expand | — | ✓ | — |
| `set_qzone_ban` | Expand | — | ✓ | — |
| `set_qzone_msg_right` | Expand | — | ✓ | — |

### Ark分享 (ark, 4 个)

| action | 来源 | napcat_only | snowluma_compat | 别名 |
|---|---|---|---|---|
| `share_peer` | Expand | — | ✓ | — |
| `send_ark_share` | Expand | — | ✓ | — |
| `share_group_ex` | Expand | — | ✓ | — |
| `send_group_ark_share` | Expand | — | ✓ | — |

---

## 别名映射表

> 别名与主名共用同一开关和 handler，调用时通过 `resolve_action()` 解析为主名。

| 别名 | 主名 |
|---|---|
| `._get_model_show` | `_get_model_show` |
| `._set_model_show` | `_set_model_show` |
| `.handle_quick_operation` | `handle_quick_operation` |
| `.get_word_slices` | `get_word_slices` |
| `.ocr_image` | `ocr_image` |
| `.send_packet` | `send_packet` |
| `delete_group_file_folder` | `delete_group_folder` |
| `get_group_album_list` | `get_qun_album_list` |
| `get_ptt_text` | `fetch_ptt_text` |
| `get_record_text` | `fetch_ptt_text` |
| `nc_get_rkey` | `get_rkey` |
| `send_group_sign` | `set_group_sign` |
| `upload_foward_msg` | `upload_forward_msg` |
| `_delete_group_notice` | `_del_group_notice` |
| `download_flash_file` | `download_fileset` |
| `get_flash_file_info` | `get_fileset_info` |
| `upload_group_album` | `upload_image_to_qun_album` |
| `voice_msg_to_text` | `fetch_ptt_text` |

---

## 按来源统计

- **OB11**：32 个 — OneBot v11 标准 API
- **NapCat**：20 个 — NapCat 扩展 API
- **go-cqhttp**：20 个 — go-cqhttp 兼容 API
- **Expand**：133 个 — 插件扩展 API
- **LLBot**：20 个 — LLBot 扩展 API

**合计**：205 个主名 action + 18 个别名 = 223 个可调用名
