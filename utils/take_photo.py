#!/usr/bin/python python3
# coding=utf-8
"""
Author: WhaleFall
Date: 2021-10-10 03:28:54
LastEditTime: 2021-10-10 03:42:55
Description: 利用opencv拍照文件
"""
import cv2
from datetime import datetime
from pathlib import Path
from .submit import submit_photo
from . import current_config
from . import log
import threading

lock = threading.Lock()


def get_time(type: int):
    """根据类型获取当前时间"""
    if type == 1:
        """写在图片中的时间"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if type == 2:
        """创建时间文件夹名"""
        return datetime.now().strftime("%Y-%m-%d")
    if type == 3:
        """图片文件名"""
        return datetime.now().strftime("%Y-%m-%d %H-%M-%S")


def mk():
    """初始化"""
    day = get_time(2)
    now = get_time(3)
    Path.mkdir(
        Path(
            current_config.PHOTOS_DIR,
            day
        ),
        exist_ok=True
    )
    return Path(
        current_config.PHOTOS_DIR,
        day,
        f"{now}.jpg"
    )


def take() -> str:
    """拍照函数,返回图片路径"""
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    flag = cap.isOpened()
    while flag:
        ret, frame = cap.read()  # 将这帧转换为灰度图
        font = cv2.FONT_HERSHEY_SIMPLEX  # 定义字体

        # 图像,文字内容,坐标,字体,大小,颜色,字体厚度
        cv2.putText(frame, get_time(1), (50, 50), font,
                    1.2, (255, 255, 255), 2)

        photo_path = str(mk())
        cv2.imwrite(filename=photo_path, img=frame)
        break
    log.logger.info(f"图片{photo_path}保存成功!")
    cap.release()  # 释放摄像头
    return photo_path


def main():
    """运行"""
    try:
        with lock:
            # 拍照需要加锁
            photo_path = take()
        submit_photo(photo_path)
    except Exception as e:
        log.logger.error(f"{photo_path}拍照上传时出现错误,{e}")
