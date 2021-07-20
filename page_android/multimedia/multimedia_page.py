# coding = utf8
import os
from time import sleep

from page_android.launcher.launcher_page import Launcher_Page
from page_android.system.system import System

os.path.abspath(".")

"""
    @File:multimedia_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Multimedia page_android，控制设备Multimedia应用的函数、控件
"""


class Multimedia_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

    def boot_music_from_main_menu(self):
        launcher_page = Launcher_Page(self)
        launcher_page.wake_up_main_menu()
        music = launcher_page.search_app_in_main_menu(app_text="音乐")
        sleep(1)
        music.click()
        sleep(1)

    def check_on_music(self):
        result = False
        sleep(1)
        if "com.android.music.MusicBrowserActivity" in self.device.shell("dumpsys window | grep mCurrentFocus"):
            result = True
        return result

    def boot_video_from_main_menu(self):
        launcher_page = Launcher_Page(self)
        launcher_page.wake_up_main_menu()
        video = launcher_page.search_app_in_main_menu(app_text="视频")
        sleep(1)
        video.click()
        sleep(1)

    def check_on_video(self):
        result = False
        sleep(1)
        if "com.android.music.VideoBrowserActivity" in self.device.shell("dumpsys window | grep mCurrentFocus"):
            result = True
        return result

    def check_on_video_playing(self):
        result = False
        sleep(1)
        if "com.yd.gallery.videoplayer.MovieActivity" in self.device.shell("dumpsys window | grep mCurrentFocus"):
            result = True
        return result

    def play_100m_video(self):
        system = System(self)
        dest_video = system.scroll_to_find_element(element_text="百战成诗")
        dest_video.click()
        if self.poco(text="打开方式").wait().exists():
            self.poco(text="打开方式").click()
            sleep(1)
            if self.poco(text="相册").wait().exists():
                self.poco(text="相册").click()
                if self.poco(text="始终").wait().exists():
                    self.poco(text="始终").click()
        if self.poco(text="START OVER").wait().exists():
            self.poco(text="START OVER").click()
