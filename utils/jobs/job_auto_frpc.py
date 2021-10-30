# -*- coding: utf-8 -*-
# @Time : 2021/10/24 13:27
# @Author : WhaleFall
# @Site : 自动获取`Frpc.ini`配置,并更新
# @File : job_auto_frpc.py
# @Software: PyCharm
from utils.submit import get_frpc_config
from utils import current_config, log
from pathlib import Path
import os


def main():
    online_frpc = get_frpc_config()  # 获取在线的配置
    frpc_path = current_config.FRPC_INI_PATH
    Path(frpc_path).touch(exist_ok=True)
    local_frpc = Path(frpc_path).read_text(encoding='utf-8')
    if online_frpc and online_frpc != local_frpc:
        log.logger.info("本地配置与服务器配置不同!需要更新!")
        Path(frpc_path).write_text(online_frpc)
        os.system('sudo systemctl restart frpc')
        log.logger.info("更新结束(⊙﹏⊙)~")
    else:
        print("frpc当前无更新")
        pass
