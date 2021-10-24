#!/usr/bin/python python3
# coding=utf-8
"""
Author: WhaleFall
Date: 2021-10-10 03:23:07
LastEditTime: 2021-10-17 10:16:10
Description: 配置文件
"""
from pathlib import Path
import os


class Config:
    SUBMIT_URI = 'https://whalefall2021.pythonanywhere.com'  # 上传信息的接口结尾不带/

    BASEDIR = os.path.abspath(os.path.dirname(__file__))  # 项目目录

    Path.mkdir(Path(BASEDIR, 'photos'), exist_ok=True)  # 建立图片文件夹
    PHOTOS_DIR = Path(BASEDIR, 'photos')  # 图片目录

    LOG_DIR = Path(BASEDIR, 'logs')  # 日志目录
    LOG_LEVEL = 'info'  # 日志级别

    # API接口字典
    APIS = {
        "temp": "/rpi/ping/",
        "photo": "/rpi/upload_photo/",
        "frpc": "/rpi/get_frpc/"
    }

    # 每隔多长时间拍照和获取温度,默认2分钟上传温度;5分钟拍照
    TEMP_TIME = 2
    TAKE_PHOTO_TIME = 5
    LOGIN_TIME = 60  # 每一小时登录一次校园网.
    CHECK_FRPC = 1  # 检查frpc配置

    FRPC_INI_PATH = str(Path("/home/pi/frp/frpc.ini"))  # frpc.ini 文件位置


class Test(Config):
    TEMP_TIME = 0.1
    TAKE_PHOTO_TIME = 0.1


config = {
    "default": Config,
    "test": Test
}

current_config = config[os.environ.get('CONFIG') or 'default']
