# coding = utf8
import os

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System

os.path.abspath(".")
from time import sleep
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
        self.device.start_app("com.tcl.tct.weather")
        sleep(1)

    def stop_weather(self):
        sleep(1)
        self.device.stop_app("com.tcl.tct.weather")

    def skip_guide(self):
        self.start_weather()
        try:
            if self.guide_alert.wait().exists():
                self.guide_agree.wait().click()
        except PocoNoSuchNodeException as ex:
            print("no need skip weather guide anymore: " + str(ex))
        finally:
            print("Welcome to weather app!")

    def get_location(self):
        global location
        self.skip_guide()
        try:
            location = self.poco("com.tcl.tct.weather:id/tv_bar_city").wait(timeout=20).get_text()
        except Exception:
            print("Some thing error, can't get location successfully, please check!")
            location = ""
        finally:
            self.stop_weather()
        return location
