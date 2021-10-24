#!/usr/bin/python python3
# coding=utf-8
"""
Author: WhaleFall
Date: 2021-10-10 03:28:54
LastEditTime: 2021-10-10 03:42:55
Description: 利用opencv拍照文件
"""
import traceback

import cv2
from datetime import datetime
from pathlib import Path
from utils.submit import submit_photo
from utils import current_config
from utils import log
import threading
from retrying import retry

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


@retry(stop_max_attempt_number=3)
def take() -> str:
    """
    拍照代码,遇到错误重试 3 次
    :return: 拍摄的图片路径
    :exception
        在 `windows` 下可以正常拍照,但在树莓派就会错误.
    """
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    flag = cap.isOpened()

    photo_path = str(mk())  # 生成文件名

    while flag:
        ret, frame = cap.read()  # 将这帧转换为灰度图
        font = cv2.FONT_HERSHEY_SIMPLEX  # 定义字体

        # 图像,文字内容,坐标,字体,大小,颜色,字体厚度
        cv2.putText(frame, get_time(1), (50, 50), font,
                    1.2, (255, 255, 255), 2)

        cv2.imwrite(filename=photo_path, img=frame)
        break
    log.logger.info(f"图片{photo_path}保存成功!")
    cap.release()  # 释放摄像头
    return photo_path


def main():
    """
    拍照主运行函数,处理拍照产生的异常
    :return:
    """
    # 拍照需要加锁
    try:
        with lock:
            photo = take()
    except:
        log.logger.error(f"拍照出现异常{traceback.format_exc()}")
    else:
        # 上传无需异常处理
        submit_photo(photo)
