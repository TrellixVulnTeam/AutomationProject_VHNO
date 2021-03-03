# coding = utf8
import os
import sys
from time import sleep

from page.system.system import System

os.path.abspath(".")
"""
    @File:messaging_page.py
    @Author:Bruce
    @Date:2021/1/13
"""


class Messaging_Page(System):

    # Ui element
    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.settings_menu_advanced = self.poco(text="Advanced")
        self.settings_menu_advanced_phone_number = self.poco(text="Phone number")

        self.send_sms = self.poco("com.google.android.apps.messaging:id/send_message_button_icon")
        self.hear_out_going_message_button = self.poco(
            text="Hear outgoing message sounds").wait().parent().sibling().child(
            "com.google.android.apps.messaging:id/switchWidget")

    def start_message(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动message app:")
        self.device.start_app("com.google.android.apps.messaging")
        sleep(1)

    def stop_message(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭message app:")
        sleep(1)
        self.device.stop_app("com.google.android.apps.messaging")

    def send_message(self, number="1", content="Test"):
        global receiver_content
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name +
                             ":创建并发送短信,number:{},content:{}:".format(number, content))
            self.device.shell("am start -a android.intent.action.SENDTO -d sms:%s --es sms_body %s" % (number, content))
            self.send_sms.wait().click()
            receiver_content = self.poco("android:id/list").children()[0].children()[1].get_text()
            if number[-4:] in receiver_content:
                self.logger.info("function:" + sys._getframe().f_code.co_name + ":短信发送成功:")
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":send message出现问题，请检查代码:" + str(ex))
        return receiver_content

    def get_phone_number(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取当前手机号码:")
        self.device.start_app_timing(package="com.google.android.apps.messaging",
                                     activity=".ui.appsettings.PerSubscriptionSettingsActivity")
        sim_number = self.settings_menu_advanced_phone_number.parent().children()[1].wait().get_text()
        sim_number = sim_number.replace(" ", "")
        return sim_number

    def enter_messaging_settings(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Messaging Settings菜单:")
            self.device.start_app_timing(package="com.google.android.apps.messaging",
                                         activity="com.google.android.apps.messaging.ui.appsettings"
                                                  ".ApplicationSettingsActivity")
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":enter messaging settings出现问题，请检查代码:" + str(ex))
