#!/usr/bin/python python3
# coding=utf-8
"""
Author: WhaleFall
Date: 2021-10-10 03:22:12
LastEditTime: 2021-10-10 03:51:13
Description: 上传信息的所有函数,均用重试模块设置重试,
若重试后仍出现异常,通过修饰器写入日志.
--- !!有关网络的所有操作一定要在此处!! ---
"""
import httpx
from . import log
from . import current_config
from retrying import retry
from pathlib import Path
from functools import wraps
from utils.jobs.job_login_fsszNetwork import main, check


def if_stop_because_network(*args, **kwargs):
    """
    处理如果上传时因为校园网的问题而上传失败的问题,避免多次请求校园网
    :return:
    """
    # 如果百度连接成功就是接口的问题了
    if check() is False:
        pass
    else:
        # 如果百度也失败就是校园网的问题
        log.logger.warning("接口请求处网络访问失败,正在重新登录校园网!")
        main()

    return False


def catch_error(func):
    """

    :param func: 修饰的方法
    :return: 进行重试10次并将异常写入logs的修饰后函数
    """

    @wraps(func)
    def inner(*args, **kwargs):
        @retry(stop_max_attempt_number=10, retry_on_result=if_stop_because_network)
        def x():
            func(*args, **kwargs)

        try:
            x()
        except Exception as e:
            log.logger.error(f"接口上传错误!{e}")

    return inner


@catch_error
def submit_ping(temperature: float, humidity: float) -> bool:
    """
    上传温湿度函数到服务器
    :param temperature: 温度 浮点值
    :param humidity: 湿度 浮点值
    :return:
    """
    url = current_config.SUBMIT_URI + current_config.APIS['temp']
    data = {
        "temp": temperature,
        "humidity": humidity
    }
    with httpx.Client() as resp:
        response = resp.post(url=url, data=data)
        if response.json().get('code') != 200:
            # 如果请求接口不为200时
            log.logger.error(f"温湿度接口响应异常!响应{response.text}内容{data}")
            return False
        else:
            log.logger.debug(f"温湿度接口响应信息:{response.json().get('msg')}")
    return True


@catch_error
def submit_photo(photo_path: str) -> bool:
    """
    上传图片到服务器函数
    :param photo_path: 图片路径
    :return: bool
    """
    url = current_config.SUBMIT_URI + current_config.APIS['photo']
    with open(photo_path, "rb") as ph:
        with httpx.Client() as resp:
            body = {
                # 图片的名称、图片的绝对路径、图片的类型（就是后缀）
                'image': (Path(photo_path).name, ph, "jpg")
            }
            response = resp.post(url=url, files=body)
            if response.json().get('code') != 200:
                # 如果请求接口不为200时
                log.logger.error(f"上传图片接口响应异常!响应{response.text}")
                return False
            else:
                log.logger.debug(f"上传图片接口响应信息:{response.json().get('msg')}")
        return True
