# coding = utf8
from multiprocessing.dummy import Process

import airtest
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from config import install_app_necessary
from page.calendar.calendar_page import Calendar_Page
from page.camera.camera_page import Camera_Page
from page.dialer.dialer_page import Dialer_Page
from page.filemanager.filemanager_page import FileManager_Page
from page.fota.fota_page import Fota_Page
from page.main_page import Main_Page
from page.messaging.messaging_page import Messaging_Page
from page.onetouchbooster.onetouchbooster_page import Onetouchbooster_Page
from page.settings.settings_page import Settings_Page
from page.system.system import System
from toolsbar.common import test_device, device_count
from airtest.core.api import *

from toolsbar.permissionGrant import grant_permission

os.path.abspath(".")

"""
    @File:run_test.py
    @Author:Bruce
    @Date:2020/12/15
"""


# 单机运行
def run_single_device():
    try:
        # grant_permission(test_device)
        # test_device.unlock()
        home()
        poco = AndroidUiautomationPoco()

        # debugger area
        main_page = Main_Page(test_device, poco)
        number = System.get_phone_number(main_page)
        messaging_page = Messaging_Page(main_page)
        print(messaging_page.send_message(number))
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
        pass
    except Exception as ex:
        print(ex)
    finally:
        pass

    device_item.unlock()
    device_item.home()

    # debugger area

    main_page = Main_Page(device_item, poco_item)
    settings_page = Settings_Page(main_page)
    for i in range(20):
        print(settings_page.change_location_settings())


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
    # install_app_necessary()
    if device_count > 1:
        run_multiple_device()
    else:
        run_single_device()