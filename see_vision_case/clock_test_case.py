# coding = utf8
import os
import sys
from time import sleep

from page_android.clock.clock_page import Clock_Page

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


"""
    case1_create500Clock
    创建闹钟会间隔1min创建一个闹钟，晚上挂着，第二天来测试会响铃即可
"""


@logit
def case1_createGapClock(main_page):
    main_page.device.wake()
    clock_page = Clock_Page(main_page)
    clock_page.launchClock()
    result = []
    # 创建60个闹钟
    for i in range(60):
    # for i in range(2):
        result.append(clock_page.createClock("case1_createGapClock - 测试创建大量间隔1min时钟{}".format(str(i + 1))))
        # 每隔1min创建一个闹钟
        sleep(60)
        # sleep(1)
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    result.insert(0, sys._getframe().f_code.co_name + "\n")
    return result


"""
    case2_create500Clock
    创建批量闹钟，挂着即可，创建500个,第二天来查看,自行手动重启,再查看,滑动,再全选删除
"""


@logit
def case2_create500Clock(main_page):
    main_page.device.wake()
    clock_page = Clock_Page(main_page)
    clock_page.launchClock()
    result = []
    try:
        for i in range(500):
        # for i in range(50):
            result.append(clock_page.createClock("case2_create500Clock - 测试批量创建时钟{}".format(str(i + 1))))
        logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    except Exception as ex:
        print("Ignore unreal exception : {}".format(str(ex)))
        result.append("Ignore unreal exception : {}".format(str(ex)))
    finally:
        result.insert(0, sys._getframe().f_code.co_name + "\n")
    return result


"""
    case3_createWholeWorldClock
    会去先获取所有的世界时钟，再逐个添加城市时钟，后续自行测试即可
"""


@logit
def case3_createWholeWorldClock(main_page):
    main_page.device.wake()
    clock_page = Clock_Page(main_page)
    clock_page.launchClock()
    result = clock_page.createWorldClock("case3_createWholeWorldClock - 测试创建所有世界时钟")
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    result.insert(0, sys._getframe().f_code.co_name + "\n")
    return result


"""
    case4_timerPauseContinueTest
    计时器每隔500ms暂停继续压力测试,最终会返回测试次数
"""


@logit
def case4_timerPauseContinueTest(main_page):
    main_page.device.wake()
    clock_page = Clock_Page(main_page)
    clock_page.launchClock()
    result = [clock_page.timerTest()]
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    result.insert(0, sys._getframe().f_code.co_name + "\n")
    return result


"""
    case5_stopwatchQuickCount
    秒表每隔100ms计次按钮压测
"""


@logit
def case5_stopwatchQuickCount(main_page):
    main_page.device.wake()
    clock_page = Clock_Page(main_page)
    clock_page.launchClock()
    result = [clock_page.stopwatchQuickCountTest()]
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    result.insert(0, sys._getframe().f_code.co_name + "\n")
    return result


@logit
def default(main_page):
    pass


def clock_case_chooser(case_number, main_page):
    return switch.get(case_number, default)(main_page)


switch = {1: case1_createGapClock, 2: case2_create500Clock, 3: case3_createWholeWorldClock,
          4: case4_timerPauseContinueTest, 5: case5_stopwatchQuickCount}
