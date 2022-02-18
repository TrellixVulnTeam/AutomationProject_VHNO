# coding = utf8
import os
import sys

from poco.exceptions import PocoNoSuchNodeException

from toolsbar.common import logger_config, cur_time
from time import sleep

os.path.abspath(".")

"""
    @File:system.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:System page，控制设备System应用的函数、控件
"""


class System:
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        self.device = main_page.device
        self.poco = main_page.poco
        self.logger = logger_config(log_path="./log/{}_{}_{}.log".format(cur_time, "System", "Fota测试"),
                                    logging_name="Fota测试")

    """
        @description:获取APP版本
        @param:
            packageName:包名
    """

    def get_app_version(self, packageName="com.android.settings"):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取当前{}版本:".format(packageName))
            exists_app = self.device.check_app(packageName)
            if exists_app:
                versionName = self.device.shell("pm dump %s|grep versionName" % packageName)
                result = versionName.strip()
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":get app version出现问题:" + str(ex))
        return result

    """
        @description:滚动查找元素
        @param:
            element_text:元素text属性
            element_id:元素id属性
    """

    def scroll_to_find_element(self, element_text="", element_id=""):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":滚动查找元素:")
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

    """
        @description:解锁屏幕
    """

    def unlock_screen(self):
        """
           亮屏并解锁屏幕操作，SIM PIN 1234解锁
        """
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":进行屏幕解锁:")
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
                self.logger.error("function:" + sys._getframe().f_code.co_name +
                                  ":锁屏界面异常,请检查代码:" + str(ex))
        except PocoNoSuchNodeException as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":未设置屏幕锁,无需解锁:" + str(ex))
        finally:
            self.device.home()

    """
        @description:锁定屏幕
    """

    def lock_screen(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":按下power键锁定屏幕:")
        self.device.keyevent("KEYCODE_POWER")

    """
        @description:双击元素
        @param:
            element_item:元素控件对象
    """

    def double_click_element(self, element_item):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":双击{}元素:".format(element_item))
        position = element_item.get_position()
        position = (position[0] * self.device.get_display_info()["width"],
                    position[1] * self.device.get_display_info()["height"])
        self.device.double_click(position)

    """
        @description:获取当前所在父框架的被checked的元素
        @param:
            element_id:需要遍历的元素所在父框架id
        @sample:
            遍历在父框架"com.android.settings:id/recycler_view"中的被选中的checkbox
            self.poco("com.android.settings:id/recycler_view").wait().offspring(checked=True)
            ->
            self.get_checked_element(element_id="com.android.settings:id/recycler_view")
        @return:list or single element
    """

    def get_checked_element(self, element_id="", element_text=""):
        if element_id:
            return self.poco(element_id).wait().offspring(checked=True)
        else:
            return self.poco(text=element_text).wait().offspring(checked=True)
