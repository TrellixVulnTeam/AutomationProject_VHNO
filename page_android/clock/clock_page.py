# coding = utf8
import os
from time import sleep

from page_android.launcher.launcher_page import Launcher_Page
from page_android.system.system import System

os.path.abspath(".")

"""
    @File:clock_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Clock page_android，控制设备Clock应用的函数、控件
"""


class Clock_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

    """
        @description:该函数用于从主菜单启动时钟
    """

    def boot_clock_from_main_menu(self):
        launcher_page = Launcher_Page(self)
        launcher_page.wake_up_main_menu()
        clock = launcher_page.search_app_in_main_menu(app_text="时钟")
        sleep(1)
        clock.click()
        sleep(1)

    """
        @description:该函数用于检测当前是否在时钟界面
    """

    def check_on_clock(self):
        result = False
        sleep(1)
        if "com.android.deskclock" in self.device.shell("dumpsys window | grep mCurrentFocus"):
            result = True
        return result
