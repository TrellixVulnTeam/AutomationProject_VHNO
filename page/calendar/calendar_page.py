# coding = utf8
import os
import sys

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System, sleep

os.path.abspath(".")
"""
    @File:calendar_page.py
    @Author:Bruce
    @Date:2021/1/13
"""


class Calendar_Page(System):

    # Ui element
    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.guide_page_text = self.poco(text="Google Calendar")
        self.guide_next_arrow = self.poco("com.google.android.calendar:id/next_arrow")
        self.guide_got_it = self.poco("com.google.android.calendar:id/oobe_done_button")
        self.create_calendar_button = self.poco("com.google.android.calendar:id/floating_action_button")
        self.create_event_button = self.poco(text="Event")
        self.add_title_edittext = self.poco("com.google.android.calendar:id/title")
        self.save_button = self.poco("com.google.android.calendar:id/save")
        # self.created_calendar_container = self.poco(
        #     "com.google.android.calendar:id/alternate_timeline_fragment_container").children()[0]

    def start_calendar(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动calendar app:")
        self.device.start_app("com.google.android.calendar")
        sleep(1)

    def stop_calendar(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭calendar app:")
        sleep(1)
        self.device.stop_app("com.google.android.calendar")

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
