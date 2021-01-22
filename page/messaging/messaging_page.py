# coding = utf8
import os
from time import sleep


os.path.abspath(".")
"""
    @File:messaging_page.py
    @Author:Bruce
    @Date:2021/1/13
"""


class Messaging_Page:

    # Ui element
    def __init__(self, main_page):
        self.device = main_page.device
        self.poco = main_page.poco
        self.settings_menu_advanced = self.poco(text="Advanced")
        self.settings_menu_advanced_phone_number = self.poco(text="Phone number")

        self.hear_outgoing_message_sounds = self.poco("com.google.android.apps.messaging:id/switchWidget")
        self.send_sms = self.poco("com.google.android.apps.messaging:id/send_message_button_icon")

    def start_message(self):
        self.device.start_app("com.google.android.apps.messaging")
        sleep(1)

    def stop_message(self):
        sleep(1)
        self.device.stop_app("com.google.android.apps.messaging")

    def send_message(self, number="1", content="Test"):
        self.device.shell("am start -a android.intent.action.SENDTO -d sms:%s --es sms_body %s" % (number, content))
        self.send_sms.wait().click()
        receiver_content = self.poco("android:id/list").children()[0].children()[1].get_text()
        print(receiver_content)
        if number[-4:] in receiver_content:
            print("PASS")
        return content, number

