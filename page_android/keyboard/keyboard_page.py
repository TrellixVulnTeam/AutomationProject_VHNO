# coding = utf8
import os
from time import sleep

from page_android.settings.settings_page import Settings_Page
from page_android.system.system import System

os.path.abspath(".")

"""
    @File:keyboard_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Keyboard page_android，控制设备Keyboard应用的函数、控件
"""


class Keyboard_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

    def wake_up_keyboard_inSettings(self):
        settings_page = Settings_Page(self)
        settings_page.boot_settings_from_main_menu()
        self.poco(text="搜索").wait().click()
        sleep(1)

    def check_keyboard_inSettings(self):
        result = False
        sleep(1)
        if "com.panda.settings.search.SearchActivity" in self.device.shell("dumpsys window | grep mCurrentFocus"):
            result = True
        return result

    # english keyboard - android original keyboard
    def search_inSettings_by_keyboard(self, input_content="Work"):
        keyboard_page = Keyboard_Page(self)
        keyboard_page.wake_up_keyboard_inSettings()
        sleep(1)
        self.keyboard_singleword_input(input_content)
        sleep(1)

    def keyboard_singleword_input(self, input_content="work"):
        for single_word in input_content:
            self.device.keyevent(keycode_chooser(single_word.upper()))

    def get_content_frome_search_box(self, search_content="w"):
        sleep(1)
        return self.poco("com.android.settings:id/mc_search_edit").wait().get_text().upper() == search_content


keycode_switch = {"0": "KEYCODE_0", "1": "KEYCODE_1", "2": "KEYCODE_2", "3": "KEYCODE_3", "4": "KEYCODE_4",
                  "5": "KEYCODE_5", "6": "KEYCODE_6", "7": "KEYCODE_7", "8": "KEYCODE_8", "9": "KEYCODE_9",
                  "A": "KEYCODE_A", "B": "KEYCODE_B", "C": "KEYCODE_C", "D": "KEYCODE_D", "E": "KEYCODE_E",
                  "F": "KEYCODE_F", "G": "KEYCODE_G", "H": "KEYCODE_H", "I": "KEYCODE_I", "J": "KEYCODE_J",
                  "K": "KEYCODE_K", "L": "KEYCODE_L", "M": "KEYCODE_M", "N": "KEYCODE_N", "O": "KEYCODE_O",
                  "P": "KEYCODE_P", "Q": "KEYCODE_Q", "R": "KEYCODE_R", "S": "KEYCODE_S", "T": "KEYCODE_T",
                  "U": "KEYCODE_U", "V": "KEYCODE_V", "W": "KEYCODE_W", "X": "KEYCODE_X", "Y": "KEYCODE_Y",
                  "Z": "KEYCODE_Z"}


def keycode_chooser(keycode_number):
    return keycode_switch.get(keycode_number)
