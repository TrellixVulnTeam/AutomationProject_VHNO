# coding = utf8
import os


os.path.abspath(".")
"""
    @File:dialer_main_page.py
    @Author:Bruce
    @Date:2021/1/12
"""


class Dialer_Main_Page():

    def __init__(self, main_page):
        self.main_page = main_page
        self.poco = self.main_page.poco
        self.device = self.main_page.device

        self.settings_menu = self.poco("com.google.android.dialer:id/three_dot_menu_or_clear_icon_view").wait()


