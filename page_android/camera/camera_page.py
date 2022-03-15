# coding = utf8
import os
import time
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

    """
        @description:该函数用于从主菜单中启动相机
    """

    def boot_camera_from_main_menu(self):
        launcher_page = Launcher_Page(self)
        launcher_page.wake_up_main_menu()
        camera = launcher_page.search_app_in_main_menu(app_text="相机")
        sleep(1)
        camera.click()

    def launch_camera(self):
        sleep(1)
        print("Launch Camera!")
        self.logger.info("Launch Camera!")
        self.device.start_app("com.android.camera2")
        sleep(1)

    def close_camera(self):
        sleep(1)
        print("Close Camera!")
        self.logger.info("Close Camera!")
        self.device.stop_app("com.android.camera2")
        sleep(1)

    """
        @description:该函数用于使用相机进行拍照
    """

    def take_picture(self):
        self.launch_camera()
        sleep(2)
        self.logger.info("Take picture")
        print("Take picture")
        self.poco("com.android.camera2:id/shutter_button").wait(3).click()
        sleep(3)

    def rename_current_picture(self, name):
        self.logger.info("Rename current picture {}".format(name))
        print("Rename current picture {}".format(name))
        sleep(2)
        self.poco("com.android.camera2:id/preview_thumb").wait().click()
        sleep(2)
        self.poco("com.android.gallery:id/action_bar").wait().children()[1].click()
        sleep(1)
        self.poco(text="重命名").wait().click()
        sleep(1)
        current_time = time.strftime("%Y%m%d_%H%M%S")
        pic_name = "第{}次_{}".format(name, current_time)
        self.poco("com.android.gallery:id/InputText").wait().set_text(
            pic_name)
        self.poco(text="确定").wait(3).click()
        return pic_name

    """
        @description:该函数用于检查当前在相机界面的缩略图控件是否存在
    """

    def check_thumbnail_picture(self):
        return self.poco("com.android.camera2:id/preview_thumb").exists()
