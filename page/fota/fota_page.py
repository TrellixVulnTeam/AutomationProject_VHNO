# coding = utf8
import os
import sys

from airtest.core.api import connect_device
from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System, sleep
from toolsbar.excel_tools import read_excel_for_page_element

os.path.abspath(".")
"""
    @File:fota_page.py
    @Author:Bruce
    @Date:2021/1/14
    @Description:Fota page，控制设备Fota应用的函数、控件
    @param:继承System，传入Main_Page实例完成设备Device、Poco初始化
"""


# 该函数用于简化元素获取操作
def get_element_parametrize(element_name="guide_page_text"):
    form_name = "./page/page_sheet.xlsx"
    element_data = read_excel_for_page_element(form=form_name, sheet_name="fota_page",
                                               element_name=element_name)
    return element_data


class Fota_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.new_version = get_element_parametrize("new_version")
        self.old_version = get_element_parametrize("old_version")

        self.launcher_package = get_element_parametrize("launcher_package")
        self.expect_update_time = int(get_element_parametrize("expect_update_time"))

        self.guide_page_text = self.poco(get_element_parametrize("guide_page_text"))
        self.guide_continue = self.poco(get_element_parametrize("guide_continue"))
        self.download_progress_button = self.poco(get_element_parametrize("download_progress_button"))
        self.download_version_available = self.poco(get_element_parametrize("download_version_available"))
        self.permission_agree = self.poco(text=get_element_parametrize("permission_agree"))
        self.update_restart_time = int(get_element_parametrize("update_restart_time"))

    """
        @description:启动Fota应用
    """

    def start_fota_page(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动fota app:")
        self.device.start_app(package="com.tcl.fota.system", activity="SystemUpdatesActivity")
        sleep(1)

    """
        @description:关闭Fota应用
    """

    def stop_fota_page(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭fota app:")
        sleep(1)
        self.device.stop_app("com.tcl.fota.system")

    """
        @description:跳过Fota向导页
    """

    def skip_guide(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":跳过设置向导:")
        try:
            if self.guide_page_text.wait().exists():
                self.guide_continue.wait().click()
        except PocoNoSuchNodeException as ex:
            self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                ":无需跳过fota向导界面:" + str(ex))
        finally:
            sleep(1)

    """
        @description:检查当前是否有新版本可以升级
    """

    def check_new_version(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":检查是否存在最新版本:")
        new_version_exists = False
        try:
            self.download_progress_button.wait().click()
            sleep(10)
            download_available = self.download_version_available.wait()
            download_available.invalidate()
            version_check_message = download_available.get_text()
            if version_check_message == "New version available":
                new_version_exists = True
                self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                    ":当前已是最新版本:" + str(new_version_exists))
                return new_version_exists
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":版本检测异常:" + str(ex))
        return new_version_exists

    def updatesw(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":开始新版本升级:")
        try:
            self.start_fota_page()
            self.skip_guide()
            if self.check_new_version():
                self.logger.info("function:" + sys._getframe().f_code.co_name + ":开始下载新版本:")
                self.download_progress_button.wait().click()
                self.permission_agree.wait().click()
                # 不同项目升级方式不一样，当前Austin，是在线升级后，需要手动点击重启
                while True:
                    if self.poco(text='INSTALL NOW').wait().exists():
                        self.logger.info("function:" + sys._getframe().f_code.co_name + ":差分包下载完成，升级完成，重启:")
                        self.poco(text='INSTALL NOW').wait().click()
                    elif self.poco(text="RESTART").wait().exists():
                        self.logger.info("function:" + sys._getframe().f_code.co_name + ":差分包下载完成，升级完成，手动重启:")
                        self.poco(text='RESTART').wait().click()
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":新版本软件升级异常:" + str(ex))

    def check_update_result(self, serialno_):
        update_result = False
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":等待升级安装完成:")
            # 等待升级安装完成
            if self.wait_update_finished_device_online(serialno_)[0]:
                device_cur = self.wait_update_finished_device_online(serialno_)[1]
                # 开机后检测当前版本是否为最新版本
                self.logger.info("function:" + sys._getframe().f_code.co_name + ":开机后检测当前版本是否为最新版本:")
                if self.new_version in device_cur.shell("getprop |grep ro.build.fingerprint").strip():
                    update_result = True
                elif self.old_version in device_cur.shell("getprop |grep ro.build.fingerprint").strip():
                    update_result = False
            else:
                self.logger.error("function:" + sys._getframe().f_code.co_name + ":软件升级过程中安装失败:")
                update_result = False
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":升级软件后检测版本异常:" + str(ex))
        return update_result

    def wait_update_finished_device_online(self, serialno_):
        current_device_serialno = serialno_
        # 等待升级完成与设备上线
        device_update_online = False
        times = 0
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":等待升级完成与设备上线:")
        while True:
            times += 1
            try:
                device = connect_device("Android:///{}".format(current_device_serialno))
                if "com.tcl.android.launcher" in device.shell("ps -A|grep " + "com.tcl.android.launcher"):
                    device_update_online = True
                    return device_update_online, device
                if times >= self.update_restart_time:
                    device_update_online = False
                    break
            except Exception as ex:
                self.logger.warning(
                    "function:" + sys._getframe().f_code.co_name + ":第 {} 次，等待机器 {} 开机重试中:  : {})".format(times,
                                                                                                          current_device_serialno,
                                                                                                          str(ex)))
                continue
            finally:
                self.logger.info(
                    "function:" + sys._getframe().f_code.co_name + ":设备当前是否在线: " + str(device_update_online))
        return device_update_online
