"""
佛山三中校园网登录.
"""

import requests
from utils import log

from retrying import retry


def check(result=None) -> bool:
    """
    访问百度检测是否与外网联通
    :return: bool
    """
    try:
        resp = requests.get(LoginNetwork.test_url, headers=LoginNetwork.header)
        if resp.status_code == 200 and resp.url == LoginNetwork.test_url:
            # 防止重定向影响判断
            # log.logger.info(f"百度访问成功!校园网状态:{result}")
            return False
    except Exception as e:
        if result is True:
            log.logger.warning(f"百度外网访问错误{e}但校园网似乎正常!")
        else:
            log.logger.warning(f"百度外网访问错误:{e}而且登录校园网异常!")
        return True


class LoginNetwork(object):
    test_url = 'https://www.baidu.com/'
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50",
    }

    def __init__(self) -> None:
        self.url = "http://192.168.101.100:8000/portal.cgi"
        self.data = {
            "username": "21wlm1",
            "password": "123456",
            "submit": "submit"
        }
        self.test_url = 'https://baidu.com/'
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.50",
        }

    @retry(stop_max_attempt_number=10, retry_on_result=check)
    def auth(self, *args, **kwargs) -> bool:
        """
        请求佛山三中校园网登录接口,此函数异常需要处理.
        auth函数的返回值传递给check的result，判断result.
        auth函数返回Treu或者None表示需要重试，
        重试结束后抛出RetryError，返回False表示不重试。
        :return: bool
        """
        try:
            resp = requests.post(self.url, data=self.data, headers=self.header, timeout=5)
            log.logger.info(f"佛山三中校园网响应:{resp.text}")
        except requests.exceptions.ConnectionError:
            log.logger.warning(f"佛山三中校园网接口超时,当前可能不在校园网环境.")
        except Exception as e:
            log.logger.warning(f"请求校园网时发生错误{e}")
        else:
            return True
        return False


def main():
    """
    佛山三中校园网登录主运行函数
    :return:
    """
    try:
        LoginNetwork().auth()
    except Exception as e:
        log.logger.critical(f"请求校园网时发生未知错误")
