# coding = utf8
import os
from time import sleep

from page_android.launcher.launcher_page import Launcher_Page
from page_android.system.system import System

os.path.abspath(".")

"""
    @File:wangzherongyao_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Wangzherongyao page_android，控制设备Wangzherongyao应用的函数、控件
"""


class Wangzherongyao_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

    def boot_wangzherongyao_from_main_menu(self):
        launcher_page = Launcher_Page(self)
        launcher_page.wake_up_main_menu()
        wangzherongyao = launcher_page.search_app_in_main_menu(app_text="王者荣耀")
        sleep(1)
        wangzherongyao.click()
        sleep(1)

    def check_on_wangzherongyao(self):
        result = False
        sleep(1)
        if "com.tencent.tmgp.sgame" in self.device.shell("dumpsys window | grep mCurrentFocus"):
            result = True
        return result
