# coding = utf8
import os
from time import sleep

from poco.exceptions import PocoNoSuchNodeException

os.path.abspath(".")
"""
    @File:dialer_page.py
    @Author:Bruce
    @Date:2021/1/12
"""


class Dialer_Page:

    # Ui element
    def __init__(self, main_page):
        self.device = main_page.device
        self.poco = main_page.poco
        self.settings_menu = self.poco("com.google.android.dialer:id/three_dot_menu_or_clear_icon_view")
        self.settings_menu_Settings = self.poco(text="Settings")
        self.settings_menu_Settings_Display_options = self.poco(text="Display options")
        self.settings_menu_Settings_Display_options_Sort_by = self.poco(text="Sort by")
        self.settings_menu_Settings_Display_options_Sort_by_First_name = self.poco(text="First name")
        self.settings_menu_Settings_Display_options_Sort_by_Last_name = self.poco(text="Last name")

        self.end_call = self.poco("com.google.android.dialer:id/incall_end_call")

    def start_dialer(self):
        self.device.start_app("com.google.android.dialer")
        sleep(1)

    def stop_dialer(self):
        sleep(1)
        self.device.stop_app("com.google.android.dialer")

    def call(self, number="10086"):
        self.device.shell("am start -a android.intent.action.CALL tel:%s" % number)
        print("Called number is {}".format(number))
        return number

    def get_svn(self):
        global value_returned
        self.device.shell("am start -a android.intent.action.DIAL -d tel:*%23*%2306%23*%23*")
        try:
            value_returned = self.poco("android:id/message").wait().get_text()
            if "SVN" in value_returned:
                value_returned = value_returned.split("SVN:")[1]
                print("Current svn is:" + value_returned)
                self.poco(text="OK").wait().click()
        except PocoNoSuchNodeException:
            print("Can't find needed element, please check!")
        finally:
            current_app = self.device.get_top_activity()[0]
            self.device.stop_app(current_app)
            self.device.home()
        return value_returned
