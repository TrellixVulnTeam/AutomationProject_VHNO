# coding = utf8
import logging
import multiprocessing
import subprocess

import pytest
from airtest.core.api import *

from config import install_app_necessary, SERIAL_NUMBER
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
"""


# 多机测试进程池:兼容单机和多机运行


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


"""
    @description:Fota checklist测试函数区域
"""


def fota_checklist_test_module():
    start_test()


if __name__ == '__main__':
    print("脚本开始测试，Fota checklist模块测试正在运行中……")
    for i in range(5):
        print("这是第{}次测试该脚本".format(i))
        fota_checklist_test_module()
        print("OK -- Test")
        print("This is {} times running and time is {}".format(str(i), time.strftime("%Y%m%d_%H%M%S")))
    print("脚本测试结束，请检查测试结果")
