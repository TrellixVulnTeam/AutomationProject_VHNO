# coding = utf8
import os
from time import sleep

from page_android.system.system import System

os.path.abspath(".")

"""
    @File:launcher_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Launcher page_android，控制设备Launcher应用的函数、控件
"""


class Launcher_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

    def search_app_in_main_menu(self, app_text=""):
        sleep(1)
        app = self.poco(text=app_text).wait()
        # print(app.attr("pos"))
        # apps_location = (app.attr("pos")[0] * self.screen_width, app.attr("pos")[1] * self.screen_height)
        # print("{}'s location is:{}".format(app_text, apps_location))
        # self.device.touch([apps_location[0], apps_location[1]])
        # app.long_click(duration=1)
        # app.drag_to((0.8, 0.5), duration=3)
        return app

    def drag_app_to_new_screen(self, elements):
        elements.start_gesture().hold(1).to([0.9, 0.5]).up()
        sleep(1)

    def slide_to_new_screen(self):
        self.poco.start_gesture([0.9, 0.5]).hold(0).to([0.5, 0.5]).up()
        sleep(1)

    def drag_app_to_current_screen(self, elements):
        elements.start_gesture().hold(1).to([0.5, 0.5]).up()
        sleep(1)

    def drag_2app_to_create_folder(self, app1_text, app2_text):
        self.wake_up_main_menu()
        app1 = self.search_app_in_main_menu(app_text=app1_text)
        self.drag_app_to_current_screen(app1)
        self.wake_up_main_menu()
        app2 = self.search_app_in_main_menu(app_text=app2_text)
        self.drag_app_to_current_screen(app2)
