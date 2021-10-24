#!/usr/bin/python python3
# coding=utf-8
"""
Author: WhaleFall
Date: 2021-10-10 03:12:03
LastEditTime: 2021-10-17 12:03:11
Description: 主运行入口
"""
import traceback
import time

import schedule
import threading
from utils import log
from config import current_config
from concurrent.futures import ThreadPoolExecutor

log.logger.info(f"开始运行!,当前配置{current_config}")

# 新开线程池,限制线程上限
pool = ThreadPoolExecutor(max_workers=30)


# def run_threaded(job_func):
#     """提供一个函数新开运行线程"""
#     job_thread = threading.Thread(target=job_func)
#     # job_thread.setDaemon(True)  # 设置线程守护,主线程下线,子线程同时结束.
#     job_thread.start()
#     # job_thread.join() 堵塞了主线程.主进程无法分配任务!

def run_threaded(job_func):
    """将任务异步提交到线程池"""
    pool.submit(job_func)


# 注册任务

# 拍照任务
from utils.jobs.job_take_photo import main as take_photo_main

schedule.every(current_config.TAKE_PHOTO_TIME).minutes.do(run_threaded, take_photo_main)

# 获取温度任务
from utils.jobs.job_get_temp import main as get_temp_main

schedule.every(current_config.TEMP_TIME).minutes.do(run_threaded, get_temp_main)

# 校园网登录任务
from utils.jobs.job_login_fsszNetwork import main as login_fsszNetwork

schedule.every(current_config.LOGIN_TIME).minutes.do(run_threaded, login_fsszNetwork)

# schedule.run_all()  # 运行所有任务,调试使用

if __name__ == "__main__":
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
            # schedule.run_all()  # 运行所有任务,调试使用
        except:
            log.logger.critical(f"主运行出错!!{traceback.format_exc()}")
