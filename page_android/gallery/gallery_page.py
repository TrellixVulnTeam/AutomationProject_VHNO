# coding = utf8
import os
from time import sleep

from page_android.launcher.launcher_page import Launcher_Page
from page_android.system.system import System

os.path.abspath(".")

"""
    @File:gallery_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Gallery page_android，控制设备Gallery应用的函数、控件
"""


class Gallery_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

    """
        @description:该函数用于从主菜单中启动图库
    """

    def boot_gallery_from_main_menu(self):
        launcher_page = Launcher_Page(self)
        launcher_page.wake_up_main_menu()
        gallery = launcher_page.search_app_in_main_menu(app_text="相册")
        sleep(1)
        gallery.click()
        sleep(1)

    """
        @description:该函数用于检查当前是否在图库界面
    """

    def check_on_gallery(self):
        result = False
        sleep(1)
        if "com.android.gallery" in self.device.shell("dumpsys window | grep mCurrentFocus"):
            result = True
        return result

    """
        @description:该函数用于从图库中打开第一张图片
    """

    def click_first_img(self):
        sleep(3)
        self.poco("com.android.gallery:id/id_recycle_view").children()[0].children()[2].children()[0].click()
        sleep(1)

    """
        @description:该函数用于从检测图片的发送按钮是否存在
    """

    def check_on_img_interface(self):
        return self.poco(text="发送").wait().exists()
