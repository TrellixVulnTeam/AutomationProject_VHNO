# coding = utf8
import os
import re
import sys
from time import sleep

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System, logger

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
        logger.info("function:" + sys._getframe().f_code.co_name + ":启动dialer app:")
        self.device.start_app("com.google.android.dialer")
        sleep(1)

    def stop_dialer(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":关闭dialer app:")
        sleep(1)
        self.device.stop_app("com.google.android.dialer")

    def call(self, number="10086"):
        logger.info("function:" + sys._getframe().f_code.co_name + ":拨打电话给:{}:".format(number))
        self.device.shell("am start -a android.intent.action.CALL tel:%s" % number)
        return number

    def get_svn(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":获取手机svn:")
        global value_returned
        self.device.shell("am start -a android.intent.action.DIAL -d tel:*%23*%2306%23*%23*")
        try:
            value_returned = self.poco("android:id/message").wait().get_text()
            if "SVN" in value_returned:
                value_returned = value_returned.split("SVN:")[1]
                self.poco(text="OK").wait().click()
        except PocoNoSuchNodeException as ex:
            logger.error("function:" + sys._getframe().f_code.co_name +
                         ":无法获取到指定元素,请检查代码:" + str(ex))
        return value_returned

    def get_imei(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":获取手机imei:")
        global value_returned
        self.device.shell("am start -a android.intent.action.DIAL -d tel:*%23*%2306%23*%23*")
        try:
            value_returned = self.poco("android:id/message").wait().get_text()
            if "IMEI" in value_returned:
                value_returned = re.findall("IMEI1:(.*)", value_returned)[0]
                self.poco(text="OK").wait().click()
        except PocoNoSuchNodeException as ex:
            logger.error("function:" + sys._getframe().f_code.co_name +
                         ":无法获取到指定元素,请检查代码:" + str(ex))
        return value_returned
