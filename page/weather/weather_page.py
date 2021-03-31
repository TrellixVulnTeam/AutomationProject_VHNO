# coding = utf8
import os
import sys

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System, sleep
from toolsbar.excel_tools import read_excel_for_page_element

os.path.abspath(".")

"""
    @File:weather_page.py
    @Author:Bruce
    @Date:2021/2/1
    @Description:Weather page，控制设备Weather应用的函数、控件
    @param:继承System，传入Main_Page实例完成设备Device、Poco初始化
"""


# 该函数用于简化元素获取操作
def get_element_parametrize(element_name="guide_page_text"):
    form_name = "./page/page_sheet.xlsx"
    element_data = read_excel_for_page_element(form=form_name, sheet_name="weather_page",
                                               element_name=element_name)
    return element_data


class Weather_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.package_name = get_element_parametrize("package_name")
        self.guide_alert = self.poco(text=get_element_parametrize("guide_alert"))
        self.guide_agree = self.poco(text=get_element_parametrize("guide_agree"))

    """
        @description:启动weather应用
    """

    def start_weather(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动weather app:")
        self.device.start_app("com.tcl.tct.weather")
        sleep(1)

    """
        @description:关闭weather应用
    """

    def stop_weather(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭weather app:")
        sleep(1)
        self.device.stop_app("com.tcl.tct.weather")

    """
        @description:跳过weather向导页
    """

    def skip_guide(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":跳过设置向导:")
        try:
            if self.guide_alert.wait().exists():
                self.guide_agree.wait().click()
        except PocoNoSuchNodeException as ex:
            self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                ":无需跳过weather设置向导:" + str(ex))

    """
        @description:获取当前定位城市
    """

    def get_location(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":开启定位，定位当前城市:")
        global location
        try:
            location = self.poco("com.tcl.tct.weather:id/tv_bar_city").wait(timeout=20).get_text()
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":当前定位出错,请检查代码:" + str(ex))
            location = ""
        return location
