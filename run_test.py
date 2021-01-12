# coding = utf8

from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from config import install_app_necessary
from page.dialer.dialer_main_page import Dialer_Main_Page
from page.main_page import Main_Page
from toolsbar.common import test_devices, device_count
from airtest.core.api import *
from multiprocessing import Process
from page.system.system import System
from toolsbar.permissionGrant import grant_permission

os.path.abspath(".")

"""
    @File:run_test.py
    @Author:Bruce
    @Date:2020/12/15
"""


# 单机运行
def run_single_device():
    # grant_permission(test_devices)
    test_devices.unlock()
    home()
    poco = AndroidUiautomationPoco()
    # poco(text="Settings").click()
    # print("Current device number is: {}".format(device_count))

    # debugger area
    # system = System(test_devices, poco)
    # system.get_app_version()
    main_page = Main_Page(test_devices, poco)
    System.get_app_version(main_page)

    dialer_main_page = Dialer_Main_Page(main_page)
    test_devices.start_app("com.google.android.dialer")
    dialer_main_page.settings_menu.click()
    dialer_main_page.settings_menu_Settings.click()


# 多机运行
def run_multiple_device():
    pau_list = []
    pui_list = []

    # 先启动Authorize进程
    for device_item in test_devices:
        p_au = Process(target=authorize_task, args=(device_item,), )
        pau_list.append(p_au)

    for process_au in pau_list:
        process_au.start()
    for process_au in pau_list:
        process_au.join()

    # 待Authorize进程都结束后，再执行UI进程（Authorize进程和Ui进程不能同时进行，会出现时耗错误）
    if not p_au.is_alive():
        for device_item in test_devices:
            poco_item = AndroidUiautomationPoco(device=device_item, use_airtest_input=False, screenshot_each_action=False)
            p_ui = Process(target=ui_task, args=(device_item, poco_item,))
            pui_list.append(p_ui)

        for process_ui in pui_list:
            process_ui.start()
        for process_ui in pui_list:
            process_ui.join()

    print("Current device number is: {}".format(device_count))


# 授权任务
def authorize_task(device_item):
    try:
        # grant_permission(device_item)
        pass
    except Exception as ex:
        print(ex)
    finally:
        pass


# ui测试任务
def ui_task(device_item, poco_item):
    try:
        device_item.unlock()
        device_item.home()
        # poco_item(text="Settings").wait().click()
        # poco_item(text="Wi-Fi").wait().click()

        # debugger area
        main_page = Main_Page(device_item, poco_item)
        System.get_app_version(main_page)
        dialer_main_page = Dialer_Main_Page(main_page)
        device_item.start_app("com.google.android.dialer")
        dialer_main_page.settings_menu.wait().click()
        dialer_main_page.settings_menu_Settings.wait().click()
    except Exception as ex:
        print(ex)
    finally:
        pass


# 单个设备poco、device不需要初始化
# 多个设备poco、device都需要创建新对象poco_item
# 后续将poco_item传入使用即可，airtest相关api，使用对应device_item进行调用
# case不需要重复写
# UI 进程和底部进程不要在同一个进程中容易出问题


if __name__ == '__main__':
    # Pycharm调用adb缺陷，需要使用terminal输入charm来启动pycharm，以获得dash权限
    # 执行case前，手动将pocoservice.apk的contniue安装好并将授权界面点掉，防止后续错误发生
    # install_app_necessary()
    if device_count > 1:
        run_multiple_device()
    else:
        run_single_device()
