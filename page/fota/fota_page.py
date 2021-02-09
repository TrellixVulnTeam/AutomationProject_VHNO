# coding = utf8
import os
from time import sleep

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System, logger

os.path.abspath(".")
"""
    @File:fota_page.py
    @Author:Bruce
    @Date:2021/1/14
"""

class Fota_Page(System):

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.guide_page_text = self.poco("com.tcl.fota.system:id/app_guide_title")
        self.guide_continue = self.poco("com.tcl.fota.system:id/guide_continue_button")
        self.download_progress_button = self.poco("com.tcl.fota.system:id/download_progress_button")

    def start_fota_page(self):
        self.device.start_app(package="com.tcl.fota.system", activity="SystemUpdatesActivity")
        sleep(1)

    def stop_fota_page(self):
        sleep(1)
        self.device.stop_app("com.tcl.fota.system")

    def skip_guide(self):
        self.start_fota_page()
        try:
            if self.guide_page_text.wait().exists():
                self.guide_continue.wait().click()
        except PocoNoSuchNodeException as ex:
            print("no need skip fota guide anymore: " + str(ex))
        finally:
            # operate
            print("Welcome to guide app!")
        self.stop_fota_page()

    def check_new_version(self):
        self.start_fota_page()
        searching_fota = False
        while not searching_fota:
            self.double_click_element(self.download_progress_button)
            self.download_progress_button.invalidate()
            progress_text = self.download_progress_button.attr("desc")
            print(progress_text)
            if progress_text == "Checking..." or progress_text == "Checking for updates...":
                searching_fota = True
            if searching_fota:
                break
        if self.poco(text="No update available").wait(10).exists():
            print("No new version for update available!")
        self.stop_fota_page()

