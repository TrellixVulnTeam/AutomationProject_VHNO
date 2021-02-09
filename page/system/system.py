# coding = utf8
import logging
import os

from poco.exceptions import PocoNoSuchNodeException

os.path.abspath(".")

"""
    @File:system.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Current py test is contained some system function
"""
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class System:

    def __init__(self, main_page):
        self.device = main_page.device
        self.poco = main_page.poco

    def get_app_version(self, packageName="com.android.settings"):
        exists_app = self.device.check_app(packageName)
        if exists_app:
            versionName = self.device.shell("pm dump %s|grep versionName" % packageName)
            print("[Device:" + self.device.serialno + "]" + versionName)

    def scroll_to_find_element(self, element_text="", element_id=""):
        global element
        menu_exists = False
        search_count = 0
        if element_text != "":
            while not menu_exists:
                element = self.poco(text=element_text).wait()
                menu_exists = element.exists()
                print("Current element {} exists status is {}".format(element, menu_exists))
                if menu_exists:
                    return element
                self.poco.scroll(direction="vertical", percent=0.6, duration=1)
                search_count += 1
                print("up: " + str(search_count) + str(menu_exists))
                # 给滑动查找增加向上滑动，兼容到底未找到的情况，即向下查找超过10次则开始向上查找
                while search_count >= 5 and not menu_exists:
                    self.poco.scroll(direction="vertical", percent=-0.6, duration=1)
                    element = self.poco(text=element_text).wait()
                    menu_exists = element.exists()
                    search_count += 1
                    print("down: " + str(search_count) + str(menu_exists))
                    if search_count >= 10:
                        search_count = 0
                        break
                    if menu_exists:
                        return element
        else:
            while not menu_exists:
                element = self.poco(element_id).wait()
                menu_exists = element.exists()
                print("Current element {} is {}".format(element, menu_exists))
                if menu_exists:
                    return element
                self.poco.scroll(direction="vertical", percent=0.6, duration=1)
                search_count += 1
                print("up: " + str(search_count) + str(menu_exists))
                # 给滑动查找增加向上滑动，兼容到底未找到的情况，即向下查找超过10次则开始向上查找
                while search_count >= 5 and not menu_exists:
                    self.poco.scroll(direction="vertical", percent=-0.6, duration=1)
                    element = self.poco(element_id).wait()
                    menu_exists = element.exists()
                    search_count += 1
                    print("down: " + str(search_count) + str(menu_exists))
                    if search_count >= 10:
                        search_count = 0
                        break
                    if menu_exists:
                        return element
        return element

    def unlock_screen(self):
        """
           亮屏并解锁屏幕操作，SIM PIN 1234解锁
        """
        self.device.unlock()
        try:
            self.poco("com.android.systemui:id/lock_icon").drag_to(self.poco("com.android.systemui:id"
                                                                             "/rectangle_frame"),
                                                                   duration=0.5)
            try:
                if self.poco(text="BACK").wait().exists():
                    for i in range(1, 5):
                        self.poco(text="%s" % i).wait().click()
                    self.device.keyevent("KEYCODE_ENTER")
            except PocoNoSuchNodeException:
                print("Screen lock interface not ok, please check!")
        except PocoNoSuchNodeException:
            print("No screen lock")
        finally:
            self.device.home()

    def lock_screen(self):
        self.device.keyevent("KEYCODE_POWER")

    def double_click_element(self, element_item):
        position = element_item.get_position()
        position = (position[0] * self.device.get_display_info()["width"],
                    position[1] * self.device.get_display_info()["height"])
        print(position)
        self.device.double_click(position)
