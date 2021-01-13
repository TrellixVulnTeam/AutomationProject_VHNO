# coding = utf8
import os

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

    def call(self, number="10086"):
        self.device.shell("am start -a android.intent.action.CALL tel:%s" % number)
        print("Called number is {}".format(number))
        return number
