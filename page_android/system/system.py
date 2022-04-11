# coding = utf8
import os
import sys
import time
from time import sleep

from airtest.core.api import connect_device
from airtest.core.error import AdbShellError
from poco.exceptions import PocoNoSuchNodeException

from toolsbar.common import logger_config
from toolsbar.permissionGrant import list_apps

os.path.abspath(".")

"""
    @File:system.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:System page_android，控制设备System应用的函数、控件
"""


class System:
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        self.device = main_page.device
        self.poco = main_page.poco
        self.logger = logger_config(log_path="./log/{}_{}.log".format("System", "性能测试"),
                                    logging_name="性能测试")
        self.screen_width = self.device.display_info["width"]
        self.screen_height = self.device.display_info["height"]

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

    """
        @description:该函数用于通过adb命令筛选并kill掉其他的所有app进程等
    """

    def kill_all_apps(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭后台所有app:")
        sleep(1)
        app_list = list_apps(self.device)
        for app_package in app_list:
            format_package_name = app_package.replace("\r", "")
            if "poco" in format_package_name:
                continue
            elif "yosemite" in format_package_name:
                continue
            elif "pocoservice" in format_package_name:
                continue
            elif "shell" in format_package_name:
                continue
            try:
                if self.device.shell("dumpsys package {} | grep category.LAUNCHER".format(format_package_name)).replace(
                        " ",
                        "") is not None:
                    self.logger.info(
                        "function:" + sys._getframe().f_code.co_name + ":当前已关闭app:{}".format(format_package_name))
                    self.device.stop_app(format_package_name)
                    # print("function:" + sys._getframe().f_code.co_name + ":当前已关闭app:{}".format(format_package_name))
            except AdbShellError:
                continue
        print("Poco service & Yosemite no need to killed, others were killed!!!")

    """
        @description:该函数用于使用adb指令直接reboot设备并判断是否重启成功
    """

    def reboot_device_and_wait(self):
        device_serialno = self.device.serialno
        self.device.shell("reboot")
        device_reboot_result = False
        count_time = 0
        while True:
            sleep(1)
            count_time += 1
            try:
                device_ready_now = connect_device("Android:///{}".format(device_serialno))
                sleep(1)
                device_ready_now.wake()
                if "com.youdao.hardware.panda" in device_ready_now.shell("dumpsys window | grep mCurrentFocus"):
                    device_reboot_result = True
                    break
                elif count_time >= 600:
                    device_reboot_result = False
                    break
            except Exception as ex:
                print("等待设备重启时间：{}s:_______:exception:{}".format(count_time, str(ex)))
                continue
            finally:
                print("Device boot status:{}".format(device_reboot_result))
        return device_reboot_result

    def device_reboot(self, cur):
        result_list = []
        device_serialno = self.device.serialno
        sleep(1)
        """
            实现区域：begin
        """
        print("第{}次重启测试".format(cur))
        self.device.shell("reboot")
        device_start_reboot_time = time.strftime("%Y%m%d_%H%M%S")
        device_end_reboot_time = 0
        device_reboot_result = False
        count_time = 0
        while True:
            sleep(1)
            count_time += 1
            try:
                device_ready_now = connect_device("Android:///{}".format(device_serialno))
                device_ready_now.wake()
                device_ready_now.unlock()
                if "com.youdao.hardware.panda" in device_ready_now.shell("dumpsys window | grep mCurrentFocus"):
                    device_reboot_result = True
                    device_end_reboot_time = time.strftime("%Y%m%d_%H%M%S")
                    break
                elif count_time >= 600:
                    device_reboot_result = False
                    break
            except Exception as ex:
                print("等待设备重启时间：{}s:_______:exception:{}".format(count_time, str(ex)))
                continue
        """
            实现区域：end
        """
        result_list.append(
            [cur,
             "第{}次重启测试开始时间:{}".format(cur, device_start_reboot_time) + " " +
             "第{}次重启测试结束时间:{}".format(cur,
                                      device_end_reboot_time)
                , "此次升级结果为{}".format(device_reboot_result)])
        print("第{}次重启测试_时间{}——————结果{}".format(cur, device_start_reboot_time, device_reboot_result))
        return result_list

    """
        @description:该函数用于使用keyevent进行设备灭屏
    """

    def rest_screen(self):
        result = False
        sleep(3)
        if self.device.is_screenon():
            self.device.keyevent("POWER")
        else:
            self.device.wake()
            sleep(3)
            self.device.keyevent("POWER")
        sleep(2)
        if not self.device.is_screenon():
            result = True
        return result

    """
        @description:该函数用于使用keyevent进行锁屏
    """

    def lock_screen(self):
        sleep(1)
        if self.device.is_screenon():
            self.device.keyevent("POWER")

    """
        @description:该函数用于解锁屏幕
    """

    def unlock_screen(self):
        sleep(1)
        self.device.wake()
        self.device.unlock()

    """
        @description:该函数用于通过滑动方式进行解锁设备
    """

    def unlock_screen_by_slide(self):
        result = False
        sleep(1)
        self.device.wake()
        print("开始滑动解锁！")
        self.poco.scroll(direction="vertical", percent=0.6, duration=0.5)
        # width = self.device.display_info["width"]
        # height = self.device.display_info["height"]
        # self.device.swipe((width / 2, height - 50), (width / 2, 50))
        result = self.check_on_home_screen()
        return result

    """
        @description:该函数用于检测当前是否在home主界面
    """

    def check_on_home_screen(self):
        result = False
        sleep(3)
        if "com.android.launcher3" in self.device.shell("dumpsys window | grep mCurrentFocus"):
            result = True
        return result

    """
        @description:该函数用于检测当前是否在锁屏界面
    """

    def check_on_lock_screen(self):
        result = False
        sleep(1)
        result = self.poco("com.android.systemui:id/clock_view").exists()
        return result

    """
        @description:该函数用于通过keyevent点亮屏幕
    """

    def light_up_screen(self):
        self.lock_screen()
        sleep(1)
        self.device.keyevent("POWER")
        sleep(1)
        result = self.check_on_home_screen()
        return result

    """
        @description:该函数用于通过nova launcher的indicator指示器来唤起主菜单
    """

    def wake_up_main_menu(self):
        self.device.unlock()
        self.poco("com.teslacoilsw.launcher:id/bottomsheet_expand_indicator").wait().click()

    """
        @description:该函数用于通过上滑手势回到Launcher界面
    """

    def slide_back_to_launcher(self):
        self.poco.start_gesture([0.5, 0.99]).hold(2).to([0.5, 0.5]).up()

    def enter_recentMenu(self):
        self.logger.info("Enter recent menu now！")
        print("Enter recent menu now！")
        self.poco.start_gesture([0.5, 0.99]).hold(1).to([0.5, 0.8]).hold(1).up()
        self.poco.start_gesture([0.5, 0.99]).hold(1).to([0.5, 0.8]).hold(1).up()
        sleep(1)

    def slide_to_close_CurAPP(self):
        self.logger.info("Slide to close current app")
        print("Slide to close current app")
        self.poco.start_gesture([0.5, 0.6]).to([0.5, 0.1]).up()
