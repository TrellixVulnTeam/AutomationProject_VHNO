# coding = utf8
import os
from time import sleep

from page_android.launcher.launcher_page import Launcher_Page
from page_android.system.system import System

os.path.abspath(".")

"""
    @File:camera_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Camera page_android，控制设备Camera应用的函数、控件
"""


class Camera_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

    def boot_camera_from_main_menu(self):
        launcher_page = Launcher_Page(self)
        launcher_page.wake_up_main_menu()
        camera = launcher_page.search_app_in_main_menu(app_text="相机")
        sleep(1)
        camera.click()

    def take_picture(self):
        self.boot_camera_from_main_menu()
        sleep(2)
        self.poco("com.android.camera2:id/panda_root_layout").children()[0].children()[2].click()
        sleep(2)

    def check_thumbnail_picture(self):
        return self.poco("com.android.camera2:id/preview_thumb").exists()

