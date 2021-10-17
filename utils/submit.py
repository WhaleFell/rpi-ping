#!/usr/bin/python python3
# coding=utf-8
"""
Author: WhaleFall
Date: 2021-10-10 03:22:12
LastEditTime: 2021-10-10 03:51:13
Description: 上传信息的所有函数,均用重试模块设置重试,但仍需须在上传点处理异常
"""
import httpx
from . import log
from . import current_config
from retry import retry
from pathlib import Path


@retry(tries=10)
def submit_ping(temperature: float, humidity: float) -> bool:
    """上传温湿度函数"""
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
            log.logger.info(f"温湿度接口响应信息:{response.json().get('msg')}")
    return True


@retry(tries=10)
def submit_photo(photo_path: str) -> bool:
    """上传图片文件函数,需提供文件路径"""
    url = current_config.SUBMIT_URI + current_config.APIS['photo']
    with open(photo_path, "rb") as ph:
        body = {
            # 图片的名称、图片的绝对路径、图片的类型（就是后缀）
            'image': (Path(photo_path).name, ph, "jpg")
        }
        with httpx.Client() as resp:
            response = resp.post(url=url, files=body)
            if response.json().get('code') != 200:
                # 如果请求接口不为200时
                log.logger.error(f"上传图片接口响应异常!响应{response.text}")
                return False
            else:
                log.logger.info(f"上传图片接口响应信息:{response.json().get('msg')}")
        return True
