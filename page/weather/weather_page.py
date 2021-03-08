# coding = utf8
import os
import sys

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System

os.path.abspath(".")

"""
    @File:weather_page.py
    @Author:Bruce
    @Date:2021/2/1
"""


class Weather_Page(System):

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.package_name = "com.tcl.tct.weather"
        self.guide_alert = self.poco(text="Weather notification")
        self.guide_agree = self.poco(text="AGREE")

    def start_weather(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动weather app:")
        self.device.start_app("com.tcl.tct.weather")
        sleep(1)

    def stop_weather(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭weather app:")
        sleep(1)
        self.device.stop_app("com.tcl.tct.weather")

    def skip_guide(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":跳过设置向导:")
        try:
            if self.guide_alert.wait().exists():
                self.guide_agree.wait().click()
        except PocoNoSuchNodeException as ex:
            self.logger.warning("function:" + sys._getframe().f_code.co_name +
                           ":无需跳过weather设置向导:" + str(ex))

    def get_location(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":开启定位，定位当前城市:")
        global location
        try:
            location = self.poco("com.tcl.tct.weather:id/tv_bar_city").wait(timeout=20).get_text()
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                         ":当前定位出错,请检查代码:" + str(ex))
            location = ""
        return location
