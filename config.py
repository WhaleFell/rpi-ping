#!/usr/bin/python python3
# coding=utf-8
'''
Author: WhaleFall
Date: 2021-10-10 03:23:07
LastEditTime: 2021-10-10 03:50:28
Description: 配置文件
'''
from pathlib import Path
import os
submit_uri = 'https://baidu.com'  # 上传信息的接口
basedir = os.path.abspath(os.path.dirname(__file__))  # 项目目录
Path.mkdir(Path(basedir, 'photos'), exist_ok=True)  # 建立图片文件夹
photodir = Path.joinpath(basedir, 'photos')  # 图片目录
