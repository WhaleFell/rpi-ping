#!/usr/bin/python python3
# coding=utf-8
"""
Author: whalefall
Date: 2021-06-17 11:19:31
LastEditTime: 2021-10-04 11:32:36
Description: 日志设置文件
"""
import logging
from logging import handlers
import datetime
from time import struct_time
import pytz
from pathlib import Path
from . import current_config


def get_beijing_time(sec=None, what=None) -> struct_time:
    """获取中国时间的转换函数,需返回时间元组"""
    local_tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(local_tz).timetuple()


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }  # 日志关系映射

    def __init__(self, filename, level='info', backCount=10,
                 fmt='%(asctime)s - %(threadName)s - %(pathname)s[line:%(lineno)d func:%(funcName)s] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)  # 创建日志记录器对象

        format_str = logging.Formatter(fmt)  # 设置日志格式
        logging.Formatter.converter = get_beijing_time  # 设置日志时区-要求函数返回时间元组

        self.logger.setLevel(self.level_relations.get(level))  # 设置对象日志级别

        sh = logging.StreamHandler()  # 往屏幕上输出对象
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        sh.setLevel(self.level_relations.get(level))
        self.logger.addHandler(sh)  # 把对象加到logger里

        # 按大小分割日志文件
        # fh = handlers.RotatingFileHandler(filename=f"{filename}.log")   # 往文件上输出对象
        # 按时间分割回滚日志
        Path.mkdir(Path(current_config.LOG_DIR), exist_ok=True)  # 建立文件夹
        # interval: 滚动周期，单位有when指定，比如：when=’D’,interval=1，表示每天产生一个日志文件；
        # backupCount: 表示日志文件的保留个数 encoding:指定编码
        fh = handlers.TimedRotatingFileHandler(
            filename=str(Path(current_config.LOG_DIR, 'run.log')), when='D', interval=1, backupCount=50,
            encoding='utf-8')
        fh.setLevel(self.level_relations.get(level))
        fh.setFormatter(format_str)  # 设置文件里写入的格式
        self.logger.addHandler(fh)


log = Logger('run.log', level=current_config.LOG_LEVEL)

if __name__ == '__main__':
    # log = Logger('run.log', level='debug')
    log.logger.debug('详细信息，调试使用')
    log.logger.info('正常信息')
    log.logger.warning('警告信息')
    log.logger.error('错误信息')
    log.logger.critical('问题很严重')

    # 解决日志时区问题
    # local_tz = pytz.timezone('Asia/Shanghai')
    # print(datetime.datetime.now(local_tz).strftime('%Y-%m-%d %H:%M:%S'))
    # print(get_beijing_time())
    # print(get_beijing_time().tm_mday)
