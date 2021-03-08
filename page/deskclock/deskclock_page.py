# coding = utf8
import os
import re
import sys

from page.system.system import System, sleep

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
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动desk clock app:")
        self.device.start_app("com.android.deskclock")
        sleep(1)

    def stop_deskclock(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭desk clock app:")
        sleep(1)
        self.device.stop_app("com.android.deskclock")

    def add_clock(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":添加闹钟:")
            self.create_clock.wait().click()
            hour = self.create_clock_hour.wait().attr("desc")
            minute = self.create_clock_minute.wait().attr("desc")
            self.create_clock_save.wait().click()
            hour = re.search("picker (.*)", hour).group(1)
            minute = re.search("picker (.*)", minute).group(1)
            created_clock = self.scroll_to_find_element(element_text=hour + ":" + minute).get_text()
            result = created_clock
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":闹钟创建出现问题:" + str(ex))
        return result
