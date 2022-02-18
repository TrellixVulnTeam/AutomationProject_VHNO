# coding = utf8
import os
import sys

from page_android.system.system import System

os.path.abspath(".")
"""
    @Project:AutomationProject
    @File:clock_test_case.py
    @Author:十二点前要睡觉
    @Date:2022/2/18 10:40
"""
os.path.abspath(".")
from functools import wraps
from toolsbar.log_control import log_control

logger = log_control.log_single_item(name="时钟测试")


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
    result = system.unlock_screen_by_slide()
    print("OKOK1")
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case2_test(main_page):
    main_page.device.wake()
    system = System(main_page)
    result = system.unlock_screen_by_slide()
    print("OKOK2")
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def default(main_page):
    pass


def clock_case_chooser(case_number, main_page):
    return switch.get(case_number, default)(main_page)


switch = {1: case1_boot_speed, 2: case2_test}
