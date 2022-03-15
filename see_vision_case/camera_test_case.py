# coding = utf8
import os
import sys
from time import sleep

from page_android.camera.camera_page import Camera_Page

os.path.abspath(".")
"""
    @Project:AutomationProject
    @File:camera_test_case.py
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
def case1_snapshot1000(main_page):
    main_page.device.wake()
    camera_page = Camera_Page(main_page)
    result = []
    for i in range(1000):
        camera_page.take_picture()
        result.append(camera_page.rename_current_picture(name=i + 1))
        camera_page.close_camera()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    result.insert(0, sys._getframe().f_code.co_name + "\n")
    return result


def case2_open_closeCamera500(main_page):
    main_page.device.wake()
    camera_page = Camera_Page(main_page)
    result = []
    for i in range(500):
        camera_page.launch_camera()
        sleep(1)
        camera_page.close_camera()
        result.append("当前测试开关Camera第{}次，结果为{}".format(i + 1, camera_page.check_on_home_screen()))
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    result.insert(0, sys._getframe().f_code.co_name + "\n")
    return result


def case3_slideToCloseCamera500(main_page):
    main_page.device.wake()
    camera_page = Camera_Page(main_page)
    result = []
    for i in range(500):
        camera_page.launch_camera()
        sleep(1)
        camera_page.enter_recentMenu()
        camera_page.slide_to_close_CurAPP()
        result.append("当前测试上滑关闭相机进程Camera第{}次,结果：{}".format(i + 1, camera_page.check_on_home_screen()))
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    result.insert(0, sys._getframe().f_code.co_name + "\n")
    return result


@logit
def default(main_page):
    pass


def camera_case_chooser(case_number, main_page):
    return switch.get(case_number, default)(main_page)


switch = {1: case1_snapshot1000, 2: case2_open_closeCamera500, 3: case3_slideToCloseCamera500}
