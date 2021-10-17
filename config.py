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

SUBMIT_URI = 'http://192.168.3.2:5000'  # 上传信息的接口结尾不带/

BASEDIR = os.path.abspath(os.path.dirname(__file__))  # 项目目录

Path.mkdir(Path(BASEDIR, 'photos'), exist_ok=True)  # 建立图片文件夹
PHOTOS_DIR = Path(BASEDIR, 'photos')  # 图片目录

LOG_DIR = Path(BASEDIR, 'logs')  # 日志目录
LOG_LEVEL = 'debug'  # 日志级别

# API接口字典
APIS = {
    "temp": "/rpi/ping/",
    "photo": "/rpi/upload_photo/"
}
