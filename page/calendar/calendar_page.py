# coding = utf8
import os
import sys

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System, sleep
from toolsbar.excel_tools import read_excel_for_page_element

os.path.abspath(".")
"""
    @File:calendar_page.py
    @Author:Bruce
    @Date:2021/1/13
    @Description:Calendar page，控制设备Calendar应用的函数、控件
    @param:继承System，传入Main_Page实例完成设备Device、Poco初始化
"""


# 该函数用于简化元素获取操作
def get_element_parametrize(element_name="guide_page_text"):
    form_name = "./page/page_sheet.xlsx"
    element_data = read_excel_for_page_element(form=form_name, sheet_name="calendar_page",
                                               element_name=element_name)
    return element_data


class Calendar_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

        print(get_element_parametrize("guide_page_text"))
        self.guide_page_text = self.poco(text=get_element_parametrize("guide_page_text"))
        self.guide_next_arrow = self.poco(get_element_parametrize("guide_next_arrow"))
        self.guide_got_it = self.poco(get_element_parametrize("guide_got_it"))
        self.create_calendar_button = self.poco(get_element_parametrize("create_calendar_button"))
        self.create_event_button = self.poco(text=get_element_parametrize("create_event_button"))
        self.add_title_edittext = self.poco(get_element_parametrize("add_title_edittext"))
        self.save_button = self.poco(get_element_parametrize("save_button"))

    """
        @description:启动calendar应用
    """

    def start_calendar(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动calendar app:")
        self.device.start_app("com.google.android.calendar")
        sleep(1)

    """
        @description:关闭calendar应用
    """

    def stop_calendar(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭calendar app:")
        sleep(1)
        self.device.stop_app("com.google.android.calendar")

    """
        @description:跳过calendar向导页
    """

    def skip_guide(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":跳过设置向导:")
        try:
            if self.guide_page_text.wait().exists():
                for i in range(2):
                    guide_next = self.guide_next_arrow.wait()
                    guide_next.click()
                self.guide_got_it.wait().click()
        except PocoNoSuchNodeException as ex:
            self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                ":无需跳过calendar设置向导:" + str(ex))

    """
        @description:创建日历事件
        @param:
            title:传入title指定创建的日历事件的名称
    """

    def create_calendar(self, title="Test"):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":创建一个名为{}的calendar:".format(title))
            self.create_calendar_button.wait().click()
            try:
                self.create_event_button.wait().click()
            except PocoNoSuchNodeException as ex:
                self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                    ":无需点击event按钮:" + str(ex))
            self.add_title_edittext.wait().set_text(title)
            self.save_button.wait().click()
            created_calendar = self.poco(
                "com.google.android.calendar:id/alternate_timeline_fragment_container").children()[0].wait().children()[
                2].attr("desc")
            result = created_calendar
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":创建日历出现问题:" + str(ex))
        return result
