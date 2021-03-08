# coding = utf8
import logging
import multiprocessing
import subprocess

import pytest
from airtest.core.api import *

from config import install_app_necessary, SERIAL_NUMBER
from toolsbar.common import test_device
from toolsbar.permissionGrant import grant_permission
from toolsbar.save2csv import Save2Csv

os.path.abspath(".")

# 过滤airtest log只打印ERROR的Log
logger_airtest = logging.getLogger("airtest")
logger_airtest.setLevel(logging.ERROR)
cur_time = time.strftime("%Y%m%d_%H%M%S")
"""
    @File:run_test.py
    @Author:Bruce
    @Date:2020/12/15
"""


# 单机运行
# debugger area
def debug():
    try:
        # test_device.unlock()
        # home()
        # poco = AndroidUiautomationPoco()
        # # debugger area
        # main_page = Main_Page(test_device, poco)
        pytest.main(["-v", "-s", "--reruns={}".format(3),
                     "--alluredir={}".format("./temp/need_data[{}_{}]/".format(cur_time, test_device.serialno))])
        subprocess.Popen(
            args=["allure", "generate", "./temp/need_data[{}_{}]/".format(cur_time, test_device.serialno), "-o",
                  "./report/test_report[{}_{}]/".format(cur_time, test_device.serialno),
                  "--clean"],
            shell=False).communicate()[0]
    except Exception as ex:
        print(ex)


"""
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
    camera_page = Camera_Page(main_page)
    camera_page.enter_camera_settings()
    pytest.main()
    # for i in range(20):
    #     print("Current device :{} 's navigation is {}".format(device_item.serialno,
    #                                                           settings_page.get_current_navigation()))
"""

"""
单个设备poco、device不需要初始化
多个设备poco、device都需要创建新对象poco_item
后续将poco_item传入使用即可，airtest相关api，使用对应device_item进行调用
case不需要重复写
UI 进程和底部进程不要在同一个进程中容易出问题
"""


# 单机测试
def _run():
    """
        Pycharm调用adb缺陷，需要使用terminal输入charm来启动pycharm，以获得dash权限
        执行case前，手动将pocoservice.apk的contniue安装好并将授权界面点掉，防止后续错误发生
        """
    """
    # 多机运行由于pytest无提供多机运行pytest，故当前多机运行函数可用于非pytest或自建框架 -- 保留
    # if device_count > 1:
    #     run_multiple_device()
    # else:
    #     run_single_device()
    # 当前使用pytest框架测试，仅针对单机运行
    """
    """
        跑一次，把那些结果计入到excel中，然后手动升级，下一次再跑，如果这个excel表格存在，
        说明已经跑过一次，然后就执行升级后的那一套,进行对比
    """

    install_app_necessary(test_device)
    grant_permission(test_device)
    # 后续项目去使用直接将lib包拷贝过去即可无需重复下载模块
    pytest.main(["-v", "-s", "--reruns={}".format(3),
                 "--alluredir={}".format("./temp/need_data[{}_{}]/".format(cur_time, test_device.serialno))])
    subprocess.Popen(
        args=["allure", "generate", "./temp/need_data[{}_{}]/".format(cur_time, test_device.serialno), "-o",
              "./report/test_report[{}_{}]/".format(cur_time, test_device.serialno),
              "--clean"],
        shell=False).communicate()[0]
    # 这里将获取到到值传下去存到Excel表格中
    save2csv = Save2Csv()
    csv_list = save2csv.getDataFromCsv("Fota_Before.csv")
    print(csv_list)


# 多机测试进程池:兼容单机和多机运行
def start_test():
    if len(SERIAL_NUMBER) > 1:
        for i in test_device:
            install_app_necessary(i)
            grant_permission(i)
    else:
        install_app_necessary(test_device)
        grant_permission(test_device)
    test_pool = multiprocessing.Pool(len(SERIAL_NUMBER))
    for device_ in SERIAL_NUMBER:
        test_pool.apply_async(func=fota_test_area, args=(device_,))
        sleep(10)
    test_pool.close()
    test_pool.join()


# debug
def debug_area():
    if len(SERIAL_NUMBER) > 1:
        for i in test_device:
            pass
            # install_app_necessary(i)
            # grant_permission(i)
    else:
        pass
        # install_app_necessary(test_device)
        # grant_permission(test_device)
    test_pool = multiprocessing.Pool(len(SERIAL_NUMBER))
    for device_ in SERIAL_NUMBER:
        test_pool.apply_async(func=fota_test_area, args=(device_,))
        sleep(10)
    test_pool.close()
    test_pool.join()


def fota_test_area(device_):
    pytest.main(["-v", "-s", "--cmdopt={}".format(device_), "--reruns={}".format(0),
                 "--alluredir={}".format("./temp/need_data[{}_{}]/".format(cur_time, device_))])
    # subprocess.Popen(
    #     args=["allure", "generate", "./temp/need_data[{}_{}]/".format(cur_time, device_), "-o",
    #           "./report/test_report[{}_{}]/".format(cur_time, device_),
    #           "--clean"],
    #     shell=False).communicate()[0]
    # subprocess.Popen(
    #     "allure generate ./temp/need_data[{}_{}] -o ./report/test_report[{}_{}]/ --clean".format(cur_time, device_,
    #                                                                                              cur_time, device_),
    #     shell=True).communicate()[0]
    save2csv = Save2Csv()
    csv_list = save2csv.getDataFromCsv(form_name=str(device_) + "Fota_Before.csv")
    print(csv_list)


if __name__ == '__main__':
    # _run()
    # start_test()
    # debug()
    debug_area()
    # device = connect_device("Android:///{}".format("7c2440fd"))
    # poco = AndroidUiautomationPoco()
    # device.shell("settings put system screen_brightness_mode 0")
    # device.shell("settings put system screen_brightness 999999")
    # device.shell("settings put system screen_off_timeout 1")
    # result = system.get_app_version("com.android.settings")
    # print((result))
