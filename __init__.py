"""onebot_expand 插件包。

OneBot v11 标准 API 与协议端扩展 API 的工具化封装插件。
通过 onebot_adapter 适配器的 WebSocket 连接调用全部 216 个 OneBot API，
以 Tool + Service 双层组件形式提供能力。

组件概览:
    - Tool (216): 21 个功能域，每个主名 action 对应一个 Tool
    - Service (23): message / group / file / account / napcat_ext / emoji / path_mapper
                    / group_file / group_notice / group_ext / request / user_ext
                    / status / poke / emoji_ext / ai_voice / cred / misc
                    / flash / group_album / group_todo / qzone / ark
    - Config (1): OnebotExpandConfig
"""

__all__: list[str] = []
