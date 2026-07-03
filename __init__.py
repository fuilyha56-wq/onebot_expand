"""onebot_expand 插件包。

OneBot v11 标准 API 与 NapCat 扩展 API 的工具化封装插件。
通过 onebot_adapter 适配器的 WebSocket 连接调用全部 158 个 OneBot API，
以 Tool + Service 双层组件形式提供能力。

组件概览:
    - Tool (158): 消息(18) + 群操作(10) + 文件(7) + 账号(9) + NapCat扩展(15)
                  + 群文件(11) + 群公告(3) + 群管理扩展(11) + 请求处理(6)
                  + 用户信息扩展(9) + 在线状态(4) + 戳一拍(2) + 表情/收藏扩展(5)
                  + AI语音(3) + 凭证/安全/下载(6) + 机型/其他(10) + 闪传(8)
                  + 群相册(7) + 群待办(3) + QQ空间(7) + Ark分享(4)
    - Service (23): message / group / file / account / napcat_ext / emoji / path_mapper
                    / group_file / group_notice / group_ext / request / user_ext
                    / status / poke / emoji_ext / ai_voice / cred / misc
                    / flash / group_album / group_todo / qzone / ark
    - Config (1): OnebotExpandConfig
"""

__all__: list[str] = []
