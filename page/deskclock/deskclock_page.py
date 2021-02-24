# coding = utf8
import os
import re
import sys
from time import sleep

from page.system.system import System, logger

os.path.abspath(".")

"""
    @File:deskclock_page.py
    @Author:Bruce
    @Date:2021/1/13
"""


class Deskclock_Page(System):

    # Ui element
    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.create_clock = self.poco("com.android.deskclock:id/fab")
        self.create_clock_hour = self.poco("com.android.deskclock:id/timerpicker_hour")
        self.create_clock_minute = self.poco("com.android.deskclock:id/timerpicker_minute")
        self.create_clock_save = self.poco("com.android.deskclock:id/toolbar_confirm_btn")

    def start_deskclock(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":启动desk clock app:")
        self.device.start_app("com.android.deskclock")
        sleep(1)

    def stop_deskclock(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":关闭desk clock app:")
        sleep(1)
        self.device.stop_app("com.android.deskclock")

    def add_clock(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":添加闹钟:")
        self.create_clock.wait().click()
        hour = self.create_clock_hour.wait().attr("desc")
        minute = self.create_clock_minute.wait().attr("desc")
        self.create_clock_save.wait().click()
        hour = re.search("picker (.*)", hour).group(1)
        minute = re.search("picker (.*)", minute).group(1)
        return hour + ":" + minute
