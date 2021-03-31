# coding = utf8
import os
import sys

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System, sleep
from toolsbar.excel_tools import read_excel_for_page_element

os.path.abspath(".")
"""
    @File:onetouchbooster_page.py
    @Author:Bruce
    @Date:2021/1/14
    @Description:Onetouchbooster page，控制设备Onetouchbooster应用的函数、控件
    @param:继承System，传入Main_Page实例完成设备Device、Poco初始化
"""


# 该函数用于简化元素获取操作
def get_element_parametrize(element_name="guide_page_text"):
    form_name = "./page/page_sheet.xlsx"
    element_data = read_excel_for_page_element(form=form_name, sheet_name="onetouchbooster_page",
                                               element_name=element_name)
    return element_data


class Onetouchbooster_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.guide_close = self.poco(get_element_parametrize("guide_close"))
        self.guide_text = self.poco(get_element_parametrize("guide_text"))
        self.battery = self.poco(text=get_element_parametrize("battery"))
        self.battery_settings = self.poco(get_element_parametrize("battery_settings"))
        self.intelligent_power_saving_title = self.poco(text=get_element_parametrize("intelligent_power_saving_title"))

    """
       @description:启动onetouchbooster应用
    """

    def start_onetouchbooster(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动one touch booster app:")
        self.device.start_app("com.tct.onetouchbooster")
        sleep(1)

    """
      @description:关闭onetouchbooster应用
    """

    def stop_onetouchbooster(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭one touch booster app:")
        sleep(1)
        self.device.stop_app("com.tct.onetouchbooster")

    """
        @description:跳过onetouchbooster向导页
    """

    def skip_guide(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":跳过设置向导:")
        try:
            guide_close = self.guide_close.wait()
            if guide_close.exists():
                guide_close.click()
        except PocoNoSuchNodeException as ex:
            self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                ":无需跳过one touch booster设置向导:" + str(ex))

    """
        @description:进入电池设置
    """

    def enter_battery_settings(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Battery settings:")
            self.battery.wait().click()
            self.battery_settings.wait().click()
        except Exception as ex:
            self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                ":进入Battery settings失败:" + str(ex))

    """
        @description:更改Intelligent power saving设置
    """

    def change_intelligent_power_saving_status(self):
        result = ""
        try:
            intelligent_power_t = self.intelligent_power_saving_title.wait()
            intelligent_power_s = intelligent_power_t.parent().child("com.tct.onetouchbooster:id/switch_button")
            intelligent_power_s.click()
            intelligent_power_s.invalidate()
            result = intelligent_power_t.get_text() + ":" + str(
                intelligent_power_s.attr("checked"))
        except Exception as ex:
            self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                ":更改intelligent power saving status失败:" + str(ex))
        return result
