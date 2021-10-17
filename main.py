#!/usr/bin/python python3
# coding=utf-8
"""
Author: WhaleFall
Date: 2021-10-10 03:12:03
LastEditTime: 2021-10-17 12:03:11
Description: 主运行入口
"""
import schedule
import time
import threading
from utils import log
from config import current_config

log.logger.info(f"开始运行!,当前配置{current_config}")

def run_threaded(job_func):
    """提供一个函数新开运行线程"""
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


from utils.take_photo import main as take_photo_main

schedule.every(current_config.TAKE_PHOTO_TIME).minutes.do(run_threaded, take_photo_main)


# from utils.get_temp import main as get_temp_main

# schedule.every(current_config.TEMP_TIME).minutes.do(run_threaded, get_temp_main)

while True:
    try:
        schedule.run_pending()
        time.sleep(1)
    except Exception as e:
        log.logger.warning(f"主运行出错!!{e}")
