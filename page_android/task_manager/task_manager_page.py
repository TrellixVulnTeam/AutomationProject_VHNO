# coding = utf8
import os
from time import sleep

from page_android.system.system import System

os.path.abspath(".")

"""
    @File:task_manager_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:TaskManager page_android，控制设备TaskManager应用的函数、控件
"""


class Task_Manager_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

    def boot_task_manager_from_main_menu(self):
        self.poco.start_gesture([0.5, 0.99]).hold(0).to([0.5, 0.88]).hold(1).up()
        sleep(1)

    def check_on_task_manager(self):
        result = False
        sleep(1)
        if "com.android.systemui.recents.RecentsActivity" in self.device.shell("dumpsys window | grep mCurrentFocus"):
            result = True
        return result
