# coding = utf8
import os
import sys

from page.system.system import System, sleep
from toolsbar.excel_tools import read_excel_for_page_element

os.path.abspath(".")
"""
    @File:messaging_page.py
    @Author:Bruce
    @Date:2021/1/13
    @Description:Messaging page，控制设备Messaging应用的函数、控件
    @param:继承System，传入Main_Page实例完成设备Device、Poco初始化
"""


# 该函数用于简化元素获取操作
def get_element_parametrize(element_name="guide_page_text"):
    form_name = "./page/page_sheet.xlsx"
    element_data = read_excel_for_page_element(form=form_name, sheet_name="messaging_page",
                                               element_name=element_name)
    return element_data


class Messaging_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.settings_menu_advanced = self.poco(text=get_element_parametrize("settings_menu_advanced"))
        self.settings_menu_advanced_phone_number = self.poco(
            text=get_element_parametrize("settings_menu_advanced_phone_number"))
        self.send_sms = self.poco(get_element_parametrize("send_sms"))
        self.hear_out_going_message_button = self.poco(
            text=get_element_parametrize("hear_out_going_message_button_1")).wait().parent().sibling().child(
            get_element_parametrize("hear_out_going_message_button_2"))

    """
        @description:启动Message应用
    """

    def start_message(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动message app:")
        self.device.start_app("com.google.android.apps.messaging")
        sleep(1)

    """
        @description:关闭Message应用
    """

    def stop_message(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭message app:")
        sleep(1)
        self.device.stop_app("com.google.android.apps.messaging")

    """
        @description:发送短信
        @param:
            number:收件人号码
            content:短信内容
    """

    def send_message(self, number="1", content="Test"):
        receiver_content = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name +
                             ":创建并发送短信,number:{},content:{}:".format(number, content))
            self.device.shell("am start -a android.intent.action.SENDTO -d sms:%s --es sms_body %s" % (number, content))
            self.send_sms.wait().click()
            receiver_content = self.poco("com.google.android.apps.messaging:id/tombstone_message").get_text()
            if number[-4:] in receiver_content:
                self.logger.info("function:" + sys._getframe().f_code.co_name + ":短信发送成功:")
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":send message出现问题，请检查代码:" + str(ex))
        return receiver_content

    """
        @description:获取设备当前SIM卡电话号码
    """

    def get_phone_number(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取当前手机号码:")
        self.device.start_app_timing(package="com.google.android.apps.messaging",
                                     activity=".ui.appsettings.PerSubscriptionSettingsActivity")
        sim_number = self.settings_menu_advanced_phone_number.parent().children()[1].wait().get_text()
        sim_number = sim_number.replace(" ", "")
        return sim_number

    """
        @description:进入Message设置界面
    """

    def enter_messaging_settings(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Messaging Settings菜单:")
            self.device.start_app_timing(package="com.google.android.apps.messaging",
                                         activity="com.google.android.apps.messaging.ui.appsettings"
                                                  ".ApplicationSettingsActivity")
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":enter messaging settings出现问题，请检查代码:" + str(ex))

    """
        @description:更改Message设置Hear outgoing message sounds设置
    """

    def change_hear_outgoing_status(self):
        result = ""
        try:
            hear_out_going_message_button = self.hear_out_going_message_button
            hear_out_going_message_button.click()
            hear_out_going_message_button.invalidate()
            result = "Hear outgoing message sounds" + ":" + str(hear_out_going_message_button.attr("checked"))
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":更改hear outgoing status出现问题，请检查代码:" + str(ex))
        return result
