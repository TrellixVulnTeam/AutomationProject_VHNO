# coding = utf8
import os
from time import sleep

from page_android.launcher.launcher_page import Launcher_Page
from page_android.system.system import System

os.path.abspath(".")

"""
    @File:calendar_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Calendar page_android，控制设备Calendar应用的函数、控件
"""


class Calendar_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

    """
        @description:该函数用于从主菜单中启动日历
    """

    def boot_calendar_from_main_menu(self):
        launcher_page = Launcher_Page(self)
        launcher_page.wake_up_main_menu()
        calendar = launcher_page.search_app_in_main_menu(app_text="日历")
        sleep(1)
        calendar.click()
        sleep(1)

    """
        @description:该函数用于检测当前界面是否在日历
    """

    def check_on_calendar(self):
        result = False
        sleep(1)
        if "com.android.calendar" in self.device.shell("dumpsys window | grep mCurrentFocus"):
            result = True
        return result

    def launchCalendar(self):
        print("Launch calendar！")
        self.logger.info("Launch calendar！")
        self.device.start_app("com.android.calendar")
        sleep(1)

    def createSchedule(self, title):
        print("Let's create schedule its title is [{}]".format(title))
        self.logger.info("Let's create schedule its title is [{}]".format(title))
        print("Search com.android.calendar:id/action_create_events ")
        self.logger.info("Search com.android.calendar:id/action_create_events ")
        self.poco("com.android.calendar:id/action_create_events").wait(3).click()
        print("Search com.android.calendar:id/title")
        self.logger.info("Search com.android.calendar:id/title")
        self.poco("com.android.calendar:id/title").wait(3).set_text(title)

        if self.poco("com.sohu.inputmethod.sogou:id/doggyHead").exists():
            self.device.keyevent("KEYCODE_BACK")
        self.poco("com.android.calendar:id/reminders_row").wait(3).click()
        self.poco(text="不提醒").wait().click()

        print("Search com.android.calendar:id/edit_event_save")
        self.logger.info("Search com.android.calendar:id/edit_event_save")
        save_button = self.poco("com.android.calendar:id/edit_event_save").wait(3)
        save_button.invalidate()
        if save_button.attr("enabled"):
            save_button.click()
            create_status = True
        else:
            print("Current Schedule {} is not saved!".format(title))
            self.logger.info("Current Schedule {} is not saved!")
            create_status = False
        print("Saved status is [{}]".format(create_status))
        self.logger.info("Saved status is [{}]".format(create_status))
        return title, create_status
