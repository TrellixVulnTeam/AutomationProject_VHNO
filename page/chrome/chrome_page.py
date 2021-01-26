# coding = utf8
import os
from time import sleep

from airtest.core.api import keyevent
from poco.exceptions import PocoNoSuchNodeException

os.path.abspath(".")
"""
    @File:chrome_page.py
    @Author:Bruce
    @Date:2021/1/26
"""


class Chrome_Page:

    def __init__(self, main_page):
        self.main_page = main_page
        self.poco = main_page.poco
        self.device = main_page.device

    def start_chrome(self):
        self.device.start_app("com.android.chrome")
        sleep(1)

    def stop_chrome(self):
        sleep(1)
        self.device.stop_app("com.android.chrome")

    def skip_guide(self):
        self.start_chrome()
        try:
            guide_first_button = self.poco("com.android.chrome:id/terms_accept").wait()
            if guide_first_button.exists():
                guide_first_button.click()
                self.poco("com.android.chrome:id/negative_button").wait().click()
        except PocoNoSuchNodeException:
            print("Chrome guide is finished!")
        finally:
            self.stop_chrome()

    def enter_website(self, website="https://www.baidu.com"):
        self.start_chrome()
        try:
            # 检查并跳过 search_engine_choose 按钮
            search_engine_choose = self.poco("com.android.chrome:id/button_secondary").wait()
            if search_engine_choose.exists():
                search_engine_choose.click()
        except PocoNoSuchNodeException:
            print("Search engine is finished!")
        finally:
            chrome_url_bar = self.poco("com.android.chrome:id/url_bar").wait()
            chrome_url_bar.click()
            chrome_url_bar.set_text(website)
            self.device.keyevent("KEYCODE_ENTER")
            print("Enter website {} successful!".format(website))
            try:
                # 检查并跳过 location_button 按钮
                location_button = self.poco("com.android.chrome:id/positive_button").wait()
                if location_button.exists():
                    location_button.click()
            except PocoNoSuchNodeException:
                print("No need give location!")

    def download_baidu_image(self):
        self.poco(text="百度一下,你就知道").wait().long_click()
        self.poco(text="Download image").wait().click()
        try:
            popup_info = self.poco("com.android.chrome:id/infobar_close_button").wait()
            if popup_info.exists():
                popup_info.click()
        except PocoNoSuchNodeException:
            print("popup_info closed!")
        finally:
            try:
                download_again_info = self.poco("com.android.chrome:id/infobar_close_button").wait()
                if download_again_info.exists():
                    download_again_info.click()
            except PocoNoSuchNodeException:
                print("download_again_info closed!")
            finally:
                try:
                    self.poco("com.android.chrome:id/positive_button").wait().click()
                except PocoNoSuchNodeException:
                    print("Not first download,so no need click download start icon!")

    def get_first_download_file(self):
        self.start_chrome()
        self.poco("com.android.chrome:id/menu_button").wait().click()
        self.poco(text="Downloads").wait().click()
        download_file = self.poco("com.android.chrome:id/thumbnail").wait()
        download_file.click()
        download_file_number = self.poco("com.android.chrome:id/title_bar").get_text()
        self.stop_chrome()
        return download_file_number


