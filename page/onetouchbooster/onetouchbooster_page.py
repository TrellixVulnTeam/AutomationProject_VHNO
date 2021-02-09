# coding = utf8
import os
from time import sleep

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System

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
        self.device.start_app("com.tct.onetouchbooster")
        sleep(1)

    def stop_onetouchbooster(self):
        sleep(1)
        self.device.stop_app("com.tct.onetouchbooster")

    def skip_guide(self):
        self.start_onetouchbooster()
        try:
            guide_close = self.guide_close.wait()
            print(self.guide_text.wait().get_text())
            if guide_close.exists():
                guide_close.click()
        except PocoNoSuchNodeException as ex:
            print("no need skip onetouchbooster guide anymore: " + str(ex))
        finally:
            # operate
            print("Welcome to onetouchbooster app!")
            pass