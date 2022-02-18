# coding = utf8
import os
import sys

from page_android.calendar.calendar_page import Calendar_Page

os.path.abspath(".")
"""
    @Project:AutomationProject
    @File:calendar_test_case.py
    @Author:十二点前要睡觉
    @Date:2022/2/18 10:48
"""
os.path.abspath(".")
from functools import wraps
from toolsbar.log_control import log_control

logger = log_control.log_single_item(name="日历测试")


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " begin test!")
        logger.info(func.__name__ + " begin test!")
        return func(*args, **kwargs)

    return with_logging


@logit
def case1_create500Schedule(main_page):
    main_page.device.wake()
    calendar_page = Calendar_Page(main_page)
    result = []
    calendar_page.launchCalendar()
    for i in range(500):
        result.append(calendar_page.createSchedule("测试批量创建日程{}".format(str(i + 1))))
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    result.insert(0, sys._getframe().f_code.co_name + "\n")
    return result


@logit
def default(main_page):
    pass


def calendar_case_chooser(case_number, main_page):
    return switch.get(case_number, default)(main_page)


switch = {1: case1_create500Schedule}
