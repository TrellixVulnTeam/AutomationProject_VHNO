# coding = utf8
import os

os.path.abspath(".")
from toolsbar.common import test_device, poco
"""
    @File:dialer_page.py
    @Author:Bruce
    @Date:2021/1/12
"""


class Dialer_Page:

    def __init__(self):
        # Ui element
        self.settings_menu = poco("com.google.android.dialer:id/three_dot_menu_or_clear_icon_view")
        self.settings_menu_Settings = poco(text="Settings")
        self.settings_menu_Settings_Display_options = poco(text="Display options")
        self.settings_menu_Settings_Display_options_Sort_by = poco(text="Sort by")
        self.settings_menu_Settings_Display_options_Sort_by_First_name = poco(text="First name")
        self.settings_menu_Settings_Display_options_Sort_by_Last_name = poco(text="Last name")

        self.end_call = poco("com.google.android.dialer:id/incall_end_call")

    def call(self, number="10086"):
        test_device.shell("am start -a android.intent.action.CALL tel:%s" % number)
        print("Called number is {}".format(number))
        return number
