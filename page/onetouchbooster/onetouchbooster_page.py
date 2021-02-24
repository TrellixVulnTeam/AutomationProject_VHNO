# coding = utf8
import os
import sys
from time import sleep

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System, logger

os.path.abspath(".")
"""
    @File:onetouchbooster_page.py
    @Author:Bruce
    @Date:2021/1/14
"""


class Onetouchbooster_Page(System):

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.guide_close = self.poco("com.tct.onetouchbooster:id/guide_close")
        self.guide_text = self.poco("com.tct.onetouchbooster:id/guide_text")
        self.battery = self.poco("Battery")
        self.battery_settings = self.poco("com.tct.onetouchbooster:id/battery_settings")
        self.intelligent_power_saving_title = self.poco("Intelligent power saving")

    def start_onetouchbooster(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":启动one touch booster app:")
        self.device.start_app("com.tct.onetouchbooster")
        sleep(1)

    def stop_onetouchbooster(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":关闭one touch booster app:")
        sleep(1)
        self.device.stop_app("com.tct.onetouchbooster")

    def skip_guide(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":跳过设置向导:")
        try:
            guide_close = self.guide_close.wait()
            if guide_close.exists():
                guide_close.click()
        except PocoNoSuchNodeException as ex:
            logger.warning("function:" + sys._getframe().f_code.co_name +
                           ":无需跳过one touch booster设置向导:" + str(ex))
