# coding = utf8
import os
import sys
from time import sleep

from page.system.system import System, logger

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

        self.hear_outgoing_message_sounds = self.poco("com.google.android.apps.messaging:id/switchWidget")
        self.send_sms = self.poco("com.google.android.apps.messaging:id/send_message_button_icon")

    def start_message(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":启动message app:")
        self.device.start_app("com.google.android.apps.messaging")
        sleep(1)

    def stop_message(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":关闭message app:")
        sleep(1)
        self.device.stop_app("com.google.android.apps.messaging")

    def send_message(self, number="1", content="Test"):
        logger.info("function:" + sys._getframe().f_code.co_name +
                    ":创建并发送短信,number:{},content:{}:".format(number, content))
        self.device.shell("am start -a android.intent.action.SENDTO -d sms:%s --es sms_body %s" % (number, content))
        self.send_sms.wait().click()
        receiver_content = self.poco("android:id/list").children()[0].children()[1].get_text()
        if number[-4:] in receiver_content:
            logger.info("function:" + sys._getframe().f_code.co_name + ":短信发送成功:")
        return content, number

    def get_phone_number(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":获取当前手机号码:")
        self.device.start_app_timing(package="com.google.android.apps.messaging",
                                     activity=".ui.appsettings.PerSubscriptionSettingsActivity")
        sim_number = self.settings_menu_advanced_phone_number.parent().children()[1].wait().get_text()
        sim_number = sim_number.replace(" ", "")
        return sim_number
