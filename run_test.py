# coding = utf8
import logging
from multiprocessing.dummy import Process

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from config import install_app_necessary
from page.chrome.chrome_page import Chrome_Page
from page.main_page import Main_Page
from page.settings.settings_page import Settings_Page
from page.weather.weather_page import Weather_Page
from toolsbar.common import test_device, device_count
from toolsbar.permissionGrant import grant_permission

os.path.abspath(".")

# 过滤airtest log只打印ERROR的Log
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

"""
    @File:run_test.py
    @Author:Bruce
    @Date:2020/12/15
"""


# 单机运行
def run_single_device():
    try:
        install_app_necessary(device=test_device)
        grant_permission(test_device)
        test_device.unlock()
        home()
        poco = AndroidUiautomationPoco()

        # debugger area
        main_page = Main_Page(test_device, poco)
        settings_page = Settings_Page(main_page)
        weather_page = Weather_Page(main_page)
        settings_page.enable_wifi()
        location = weather_page.get_location()
        if location == "Huicheng District":
            print(test_device.serialno + "Current location is: {}, and Get location PASS!".format(location))
    except Exception as ex:
        print(ex)


# 多机运行
def run_multiple_device():
    pau_list = []
    pui_list = []

    # 先启动Authorize进程
    for device_item in test_device:
        p_au = Process(target=authorize_task, args=(device_item,), )
        pau_list.append(p_au)

    for process_au in pau_list:
        process_au.start()
    for process_au in pau_list:
        process_au.join()

    # 待Authorize进程都结束后，再执行UI进程（Authorize进程和Ui进程不能同时进行，会出现时耗错误）

    if not p_au.is_alive():
        for device_item in test_device:
            poco_item = AndroidUiautomationPoco(device=device_item, use_airtest_input=False,
                                                screenshot_each_action=False)
            p_ui = Process(target=ui_task, args=(device_item, poco_item,))
            pui_list.append(p_ui)

        for process_ui in pui_list:
            process_ui.start()
        for process_ui in pui_list:
            process_ui.join()

    print("Current device number is: {}".format(device_count))


# Before test任务
def authorize_task(device_item):
    # try:
    #     grant_permission(device_item)
    #     pass
    # except Exception as ex:
    #     print(ex)
    # finally:
    #     pass
    # install_app_necessary(device_item)
    # grant_permission(device_item)
    pass


# ui测试任务
def ui_task(device_item, poco_item):
    try:
        pass
    except Exception as ex:
        print(ex)
    finally:
        pass

    device_item.unlock()
    device_item.home()

    # debugger area

    main_page = Main_Page(device_item, poco_item)
    chrome_page = Chrome_Page(main_page)
    chrome_page.enter_website()
    # for i in range(20):
    #     print("Current device :{} 's navigation is {}".format(device_item.serialno,
    #                                                           settings_page.get_current_navigation()))


"""
单个设备poco、device不需要初始化
多个设备poco、device都需要创建新对象poco_item
后续将poco_item传入使用即可，airtest相关api，使用对应device_item进行调用
case不需要重复写
UI 进程和底部进程不要在同一个进程中容易出问题
"""

if __name__ == '__main__':
    """
    Pycharm调用adb缺陷，需要使用terminal输入charm来启动pycharm，以获得dash权限
    执行case前，手动将pocoservice.apk的contniue安装好并将授权界面点掉，防止后续错误发生
    """
    if device_count > 1:
        run_multiple_device()
    else:
        run_single_device()
