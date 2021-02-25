# coding = utf8
import os
import sys

from poco.exceptions import PocoNoSuchNodeException

from toolsbar.common import logger

os.path.abspath(".")

"""
    @File:system.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Current py test is contained some system function
"""


class System:

    def __init__(self, main_page):
        self.device = main_page.device
        self.poco = main_page.poco

    def get_app_version(self, packageName="com.android.settings"):
        logger.info("function:" + sys._getframe().f_code.co_name + ":获取当前{}版本:".format(packageName))
        exists_app = self.device.check_app(packageName)
        if exists_app:
            versionName = self.device.shell("pm dump %s|grep versionName" % packageName)
            return versionName.strip()

    def scroll_to_find_element(self, element_text="", element_id=""):
        logger.info("function:" + sys._getframe().f_code.co_name + ":滚动查找元素:")
        global element
        menu_exists = False
        search_count = 0
        if element_text != "":
            while not menu_exists:
                element = self.poco(text=element_text).wait()
                menu_exists = element.exists()
                if menu_exists:
                    return element
                self.poco.scroll(direction="vertical", percent=0.6, duration=1)
                search_count += 1
                # 给滑动查找增加向上滑动，兼容到底未找到的情况，即向下查找超过10次则开始向上查找
                while search_count >= 5 and not menu_exists:
                    self.poco.scroll(direction="vertical", percent=-0.6, duration=1)
                    element = self.poco(text=element_text).wait()
                    menu_exists = element.exists()
                    search_count += 1
                    if search_count >= 10:
                        search_count = 0
                        break
                    if menu_exists:
                        return element
        else:
            while not menu_exists:
                element = self.poco(element_id).wait()
                menu_exists = element.exists()
                if menu_exists:
                    return element
                self.poco.scroll(direction="vertical", percent=0.6, duration=1)
                search_count += 1
                # 给滑动查找增加向上滑动，兼容到底未找到的情况，即向下查找超过10次则开始向上查找
                while search_count >= 5 and not menu_exists:
                    self.poco.scroll(direction="vertical", percent=-0.6, duration=1)
                    element = self.poco(element_id).wait()
                    menu_exists = element.exists()
                    search_count += 1
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
        logger.info("function:" + sys._getframe().f_code.co_name + ":进行屏幕解锁:")
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
            except PocoNoSuchNodeException as ex:
                logger.error("function:" + sys._getframe().f_code.co_name +
                             ":锁屏界面异常,请检查代码:" + str(ex))
        except PocoNoSuchNodeException as ex:
            logger.error("function:" + sys._getframe().f_code.co_name +
                         ":未设置屏幕锁,无需解锁:" + str(ex))
        finally:
            self.device.home()

    def lock_screen(self):
        logger.info("function:" + sys._getframe().f_code.co_name + ":按下power键锁定屏幕:")
        self.device.keyevent("KEYCODE_POWER")

    def double_click_element(self, element_item):
        logger.info("function:" + sys._getframe().f_code.co_name + ":双击{}元素:".format(element_item))
        position = element_item.get_position()
        position = (position[0] * self.device.get_display_info()["width"],
                    position[1] * self.device.get_display_info()["height"])
        self.device.double_click(position)
