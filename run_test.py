# coding = utf8
import logging
import multiprocessing
import subprocess

import pytest
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from config import install_app_necessary, SERIAL_NUMBER
from page.fota.fota_page import Fota_Page
from page.main_page import Main_Page
from page.system.system import System
from toolsbar.common import test_device
from toolsbar.permissionGrant import grant_permission

os.path.abspath(".")

# 过滤airtest log只打印ERROR的Log
logger_airtest = logging.getLogger("airtest")
logger_airtest.setLevel(logging.ERROR)
cur_time = time.strftime("%Y%m%d_%H%M%S")
"""
    @File:run_test.py
    @Author:Bruce
    @Date:2020/12/15
    @Description:项目运行函数，存放测试和调试函数
    For seevision automation framework
"""

"""
    单个设备poco、device不需要初始化
    多个设备poco、device都需要创建新对象poco_item
    后续将poco_item传入使用即可，airtest相关api，使用对应device_item进行调用
    case不需要重复写
    UI 进程和底部进程不要在同一个进程中容易出问题
"""

# 多机测试进程池:兼容单机和多机运行
"""
    @description:多进程创建进行多台设备测试
    @tip:
        Pycharm调用adb缺陷，需要使用terminal输入charm来启动pycharm，以获得dash权限
        执行case前，手动将pocoservice.apk的contniue安装好并将授权界面点掉，防止后续错误发生
"""


def start_test():
    print("当前设备数量：" + str(len(SERIAL_NUMBER)))
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


"""
    @description:Fota checklist测试函数执行区域
    @param:
        device_:设备序列号
"""


def fota_test_area(device_):
    pytest.main(["-v", "-s", "--cmdopt={}".format(device_), "{}".format("./test_case/test_before_fota.py"),
                 "--reruns={}".format(1),
                 "--alluredir={}".format("./temp/need_data[{}_{}]/".format(cur_time, device_))])
    # 设置差异化
    subprocess.Popen(
        args=["allure", "generate", "./temp/need_data[{}_{}]/".format(cur_time, device_), "-o",
              "./report/test_report[{}_{}]/".format(cur_time, device_),
              "--clean"],
        shell=False).communicate()[0]
    updatesw(device_)

    # subprocess.Popen(
    #     "allure generate ./temp/need_data[{}_{}] -o ./report/test_report[{}_{}]/ --clean".format(cur_time, device_,
    #                                                                                              cur_time, device_),
    #     shell=True).communicate()[0]


"""
    @description:Fota checklist测试软件升级函数执行区域
    @param:
        device_:设备序列号
"""


def updatesw(device_):
    print("开始新版本升级")
    try:
        device_c = connect_device("Android:///{}".format(device_))
        poco = AndroidUiautomationPoco(device=device_c, use_airtest_input=False,
                                       screenshot_each_action=False)
        main_page = Main_Page(device_c, poco)
        system = System(main_page)
        system.unlock_screen()
        fota_page = Fota_Page(main_page)
        fota_page.start_fota_page()
        fota_page.skip_guide()
        fota_page.updatesw()
        print("升级结果：" + str(fota_page.check_update_result(device_)))
        print("Fota升级测试结束")
    except Exception as ex:
        print(str(ex))


"""
    @description:Fota checklist测试函数区域
"""


def fota_checklist_test_module():
    start_test()


"""
    @description:main函数，主要运行函数
"""
if __name__ == '__main__':
    print("脚本开始测试，Fota checklist模块测试正在运行中……")
    for i in range(5):
        print("这是第{}次测试该脚本".format(i))
        fota_checklist_test_module()
        print("OK -- Test")
        print("This is {} times running and time is {}".format(str(i), time.strftime("%Y%m%d_%H%M%S")))
    print("脚本测试结束，请检查测试结果")
