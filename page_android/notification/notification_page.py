# coding = utf8
import os
from time import sleep

from page_android.system.system import System

os.path.abspath(".")

"""
    @File:notification_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Notification page_android，控制设备Notification应用的函数、控件
"""


class Notification_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

    """
        @description:该函数用于从状态栏上拖下通知中心面板
    """

    def drag_down_notification_center(self):
        self.device.touch([0, 0])
        sleep(0.5)
        self.device.swipe((500, 0.01), (500, 300), duration=0)

    """
        @description:该函数用于从状态栏上拖下通知中心列表
    """

    def drag_down_notification_list(self):
        self.poco.start_gesture((0.5, 0)).hold(0).to((0.5, 1)).up()

    """
        @description:该函数用于在通知列表中通过对应通知标题点击特定的通知
    """

    def click_dest_notification(self, notification_title=""):
        sleep(1)
        if self.poco("com.android.systemui:id/dismiss_view").wait().exists():
            self.poco("com.android.systemui:id/dismiss_view").click()
            sleep(2)
            self.drag_down_notification_list()
        dest_notification = self.scroll_to_find_element(element_text=notification_title)
        dest_notification.click()
