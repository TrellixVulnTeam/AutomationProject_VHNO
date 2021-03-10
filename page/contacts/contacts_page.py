# coding = utf8
import os
import sys

from page.system.system import System, sleep

os.path.abspath(".")

"""
    @File:contacts_page.py
    @Author:Bruce
    @Date:2021/1/13
    @Description:Contacts page，控制设备Contacts应用的函数、控件
    @param:继承System，传入Main_Page实例完成设备Device、Poco初始化
"""


class Contacts_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.save = self.poco("com.google.android.contacts:id/save_button")

    """
        @description:启动contacts应用
    """

    def start_contacts(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动contacts app:")
        self.device.start_app("com.google.android.contacts")
        sleep(1)

    """
        @description:关闭contacts应用
    """

    def stop_contacts(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭contacts app:")
        sleep(1)
        self.device.stop_app("com.google.android.contacts")

    """
        @description:创建联系人
        @param:
            contact_name:联系人名称
            phone_number:联系人号码
    """

    def create_contact(self, contact_name="Test", phone_number="18512026630"):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name +
                             ":创建联系人,名称:{},号码:{}:".format(contact_name, phone_number))
            self.device.shell("am start -a android.intent.action.INSERT -t vnd.android.cursor.dir/"
                              "contact -e name %s -e phone %s" % (contact_name, phone_number))
            created_contact = self.scroll_to_find_element(element_text=contact_name).get_text()
            result = created_contact, phone_number
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":创建联系人出现问题:" + str(ex))
        return result
