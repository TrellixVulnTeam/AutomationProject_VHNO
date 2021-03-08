# coding = utf8
import os
import re
import sys

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System, sleep

os.path.abspath(".")
"""
    @File:dialer_page.py
    @Author:Bruce
    @Date:2021/1/12
"""


class Dialer_Page(System):

    # Ui element
    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.settings_menu = self.poco("com.google.android.dialer:id/three_dot_menu_or_clear_icon_view")
        self.settings_menu_Settings = self.poco(text="Settings")
        self.settings_menu_Settings_Display_options = self.poco(text="Display options")
        self.settings_menu_Settings_Display_options_Sort_by = self.poco(text="Sort by")
        self.settings_menu_Settings_Display_options_Sort_by_First_name = self.poco(text="First name")
        self.settings_menu_Settings_Display_options_Sort_by_Last_name = self.poco(text="Last name")

        self.end_call = self.poco("com.google.android.dialer:id/incall_end_call")

    def start_dialer(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动dialer app:")
        self.device.start_app("com.google.android.dialer")
        sleep(1)

    def stop_dialer(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭dialer app:")
        sleep(1)
        self.device.stop_app("com.google.android.dialer")

    def call(self, number="10086"):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":拨打电话给:{}:".format(number))
            self.device.shell("am start -a android.intent.action.CALL tel:%s" % number)
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":call出现问题，请检查代码:" + str(ex))
        return number

    def get_svn(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取手机svn:")
            global value_returned
            self.device.shell("am start -a android.intent.action.DIAL -d tel:*%23*%2306%23*%23*")
            try:
                value_returned = self.poco("android:id/message").wait().get_text()
                if "SVN" in value_returned:
                    result = value_returned.split("SVN:")[1].replace("\n", "")
                    self.poco(text="OK").wait().click()
            except PocoNoSuchNodeException as ex:
                self.logger.error("function:" + sys._getframe().f_code.co_name +
                                  ":无法获取到指定元素,请检查代码:" + str(ex))
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":获取手机svn出现问题，请检查代码:" + str(ex))
        return result

    def get_imei(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取手机imei:")
        global value_returned
        self.device.shell("am start -a android.intent.action.DIAL -d tel:*%23*%2306%23*%23*")
        try:
            value_returned = self.poco("android:id/message").wait().get_text()
            if "IMEI" in value_returned:
                value_returned = re.findall("IMEI1:(.*)", value_returned)[0]
                self.poco(text="OK").wait().click()
        except PocoNoSuchNodeException as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":无法获取到指定元素,请检查代码:" + str(ex))
        return value_returned

    def enter_sort_interface(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":点击右上角菜单")
            self.settings_menu.wait().click()
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入settings")
            self.settings_menu_Settings.wait().click()
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Display options")
            self.settings_menu_Settings_Display_options.wait().click()
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Sort by界面")
            self.settings_menu_Settings_Display_options_Sort_by.wait().click()
            first_name = self.settings_menu_Settings_Display_options_Sort_by_First_name.wait()
            last_name = self.settings_menu_Settings_Display_options_Sort_by_Last_name.wait()
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":enter sort interface 出现问题:" + str(ex))
        return first_name, last_name

    def change_sort_by(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进行更改Sort by方式")
            sort_option = self.enter_sort_interface()
            first_name = sort_option[0]
            last_name = sort_option[1]
            if first_name.attr("checked"):
                last_name.click()
                self.settings_menu_Settings_Display_options_Sort_by.wait().click()
                last_name.invalidate()
                result = last_name.get_text() + ":" + str(last_name.attr("checked"))
            else:
                first_name.click()
                self.settings_menu_Settings_Display_options_Sort_by.wait().click()
                first_name.invalidate()
                result = first_name.get_text() + ":" + str(first_name.attr("checked"))
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":更改Sort by方式出现问题:" + str(ex))
        return result

    def get_main_software_version(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取当前设备主软件版本:")
            self.device.shell("am start -a android.intent.action.DIAL -d tel:*%23*%233228%23*%23*")
            result = "Main Software Version" + ":" + self.poco("android:id/message").wait().get_text().replace("\n", ",")
            self.poco(text="OK").wait().click()
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":获取当前设备主软件版本出现问题:" + str(ex))
        return result
