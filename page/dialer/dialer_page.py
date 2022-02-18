# coding = utf8
import os
import re
import sys

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System, sleep
from toolsbar.excel_tools import read_excel_for_page_element

os.path.abspath(".")
"""
    @File:dialer_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Dialer page，控制设备Dialer应用的函数、控件
    @param:继承System，传入Main_Page实例完成设备Device、Poco初始化
"""


# 该函数用于简化元素获取操作
def get_element_parametrize(element_name="guide_page_text"):
    form_name = "./page/page_sheet.xlsx"
    element_data = read_excel_for_page_element(form=form_name, sheet_name="dialer_page",
                                               element_name=element_name)
    return element_data


class Dialer_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.settings_menu = self.poco(get_element_parametrize("settings_menu"))
        self.settings_menu_Settings = self.poco(text=get_element_parametrize("settings_menu_Settings"))
        self.settings_menu_Settings_Display_options = self.poco(
            text=get_element_parametrize("settings_menu_Settings_Display_options"))
        self.settings_menu_Settings_Display_options_Sort_by = self.poco(
            text=get_element_parametrize("settings_menu_Settings_Display_options_Sort_by"))
        self.settings_menu_Settings_Display_options_Sort_by_First_name = self.poco(
            text=get_element_parametrize("settings_menu_Settings_Display_options_Sort_by_First_name"))
        self.settings_menu_Settings_Display_options_Sort_by_Last_name = self.poco(
            text=get_element_parametrize("settings_menu_Settings_Display_options_Sort_by_Last_name"))

        self.end_call = self.poco(get_element_parametrize("end_call"))
        self.recents_button = self.poco(get_element_parametrize("recents_button"))

    """
        @description:启动Dialer应用
    """

    def start_dialer(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动dialer app:")
        self.device.start_app("com.google.android.dialer")
        sleep(1)

    """
        @description:关闭Dialer应用
    """

    def stop_dialer(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭dialer app:")
        sleep(1)
        self.device.stop_app("com.google.android.dialer")

    """
        @description:拨打电话
        @param:
            number:电话号码
    """

    def call(self, number="10086"):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":拨打电话给:{}:".format(number))
            self.device.shell("am start -a android.intent.action.CALL tel:%s" % number)
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":call出现问题，请检查代码:" + str(ex))
        return number

    """
        @description:获取设备svn号
    """

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

    """
        @description:获取设备imei号
    """

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

    """
        @description:进入Dialer设置Sort设置界面
    """

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

    """
        @description:更改当前Dialer列表排序方式
    """

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

    """
        @description:获取当前Dialer的列表排序方式
    """

    def get_sort_by(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取Sort by方式")
            sort_option = self.enter_sort_interface()
            first_name = sort_option[0]
            last_name = sort_option[1]
            if first_name.attr("checked"):
                result = first_name.get_text() + ":" + str(first_name.attr("checked"))
            else:
                result = last_name.get_text() + ":" + str(last_name.attr("checked"))
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":获取Sort by方式出现问题:" + str(ex))
        return result

    """
        @description:获取设备当前主软件版本
    """

    def get_main_software_version(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取当前设备主软件版本:")
            self.device.shell("am start -a android.intent.action.DIAL -d tel:*%23*%233228%23*%23*")
            result = "Main Software Version" + ":" + self.poco("android:id/message").wait().get_text().replace("\n",
                                                                                                               ",")
            self.poco(text="OK").wait().click()
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":获取当前设备主软件版本出现问题:" + str(ex))
        return result

    """
        @description:获取当前最新通话记录
        @param:
            number:根据number查找通话记录
    """

    def get_last_dialer_number(self, number):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取当前最新通话记录:")
            self.start_dialer()
            self.recents_button.wait().click()
            if self.poco(text=number).wait().exists():
                result = number
            else:
                result = "未找到该测试号码"
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":获取当前最新通话记录出现问题:" + str(ex))
        return result
