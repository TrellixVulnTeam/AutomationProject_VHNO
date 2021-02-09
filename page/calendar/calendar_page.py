# coding = utf8
import os
from time import sleep

from poco.exceptions import PocoNoSuchNodeException
from page.system.system import System, logger

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
        self.add_title_edittext = self.poco("com.google.android.calendar:id/title")
        self.save_button = self.poco("com.google.android.calendar:id/save")
        self.created_calendar_frame = self.poco("com.google.android.calendar:id/alternate_timeline_holder")

    def start_calendar(self):
        self.device.start_app("com.google.android.calendar")
        sleep(1)

    def stop_calendar(self):
        sleep(1)
        self.device.stop_app("com.google.android.calendar")

    def skip_guide(self):
        self.start_calendar()
        try:
            if self.guide_page_text.wait().exists():
                for i in range(2):
                    guide_next = self.guide_next_arrow.wait()
                    guide_next.click()
                self.guide_got_it.wait().click()
                a = self.guide_got_it.wait().get_text()
                print(a)
        except PocoNoSuchNodeException as ex:
            print("no need skip calendar guide anymore: " + str(ex))
        finally:
            # operate
            print("Welcome to calendar app!")
            pass

    def create_calendar(self, title="Test"):
        self.create_calendar_button.wait().click()
        self.add_title_edittext.wait().set_text(title)
        self.save_button.wait().click()

        created_calendar = self.created_calendar_frame.children()[1].children()[0].children()[2].wait()
        calendar_desc = created_calendar.attr("desc")
        print(calendar_desc)





