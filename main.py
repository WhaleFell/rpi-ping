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
from utils._log import log
from config import current_config
from concurrent.futures import ThreadPoolExecutor

log.logger.info(f"开始运行!,当前配置{current_config}")

# 新开线程池,限制线程上限
pool = ThreadPoolExecutor(max_workers=current_config.THREADS)


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
# from utils.jobs import job_get_temp
# from utils.jobs import job_take_photo
# from utils.jobs import job_login_fsszNetwork
import utils.jobs.job_auto_frpc as job_auto_frpc
import utils.jobs.job_login_fsszNetwork as job_login_fsszNetwork

# 任务列表 [任务函数,执行间隔时间(min)]
TASKS = [
    [job_auto_frpc, current_config.CHECK_FRPC],
    [job_login_fsszNetwork, current_config.LOGIN_TIME]
]

for task in TASKS:
    schedule.every(task[1]).minutes.do(run_threaded, task[0].main)

# schedule.run_all()  # 运行所有任务,调试使用
if __name__ == "__main__":
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
            # schedule.run_all()  # 运行所有任务,调试使用
        except KeyboardInterrupt:
            log.logger.critical("用户手动终止进程!")
        except:
            log.logger.critical(f"主运行出错!!{traceback.format_exc()}")
