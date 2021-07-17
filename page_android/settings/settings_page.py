# coding = utf8
import os
from time import sleep

from page_android.launcher.launcher_page import Launcher_Page
from page_android.system.system import System

os.path.abspath(".")

"""
    @File:settings_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Settings page_android，控制设备Settings应用的函数、控件
"""


class Settings_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

    def boot_settings_from_main_menu(self):
        launcher_page = Launcher_Page(self)
        launcher_page.wake_up_main_menu()
        settings = launcher_page.search_app_in_main_menu(app_text="设置")
        sleep(1)
        settings.click()
        sleep(1)

    def check_on_settings(self):
        result = False
        sleep(1)
        if "com.android.settings" in self.device.shell("dumpsys window | grep mCurrentFocus"):
            result = True
        return result

    def open_wifi(self):
        self.device.shell("svc wifi enable")

    def enter_wifi_settings(self):
        self.open_wifi()
        self.boot_settings_from_main_menu()
        self.poco(text="无线局域网").wait().click()
        sleep(1)
        result = self.poco(text="手动添加网络").wait().exists()
        sleep(1)
        return result
