# coding = utf8
import os
import sys
import time
from functools import wraps

from page_android.system.system import System
from toolsbar.log_control import log_control

os.path.abspath(".")
"""
    @Project:AutomationProject
    @File:system_test_case.py
    @Author:十二点前要睡觉
    @Date:2022/4/11 9:20
"""
logger = log_control.log_single_item(name="时钟测试")
cur_time = time.strftime("%Y%m%d_%H%M%S")


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " begin test!")
        logger.info(func.__name__ + " begin test!")
        return func(*args, **kwargs)

    return with_logging


@logit
def case1_boot_speed(main_page):
    main_page.device.wake()
    system = System(main_page)
    result = []
    times = 1000
    for i in range(times):
        result.append(system.device_reboot(cur=i + 1))
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    result.insert(0, sys._getframe().f_code.co_name + "\n")
    return result


@logit
def default():
    pass


def system_case_chosser(case_number, main_page):
    return switch.get(case_number, default)(main_page)


switch = {1: case1_boot_speed}
