# coding = utf8
import logging
import multiprocessing
import subprocess

import pytest
from airtest.core.api import *

from config import install_app_necessary, SERIAL_NUMBER, push_file_into_device
from toolsbar.common import test_device
from toolsbar.permissionGrant import grant_permission

os.path.abspath(".")




"""
    @description:main函数，主要运行函数
"""
if __name__ == '__main__':
    print("脚本开始测试，性能验收模块测试正在运行中……")
    for i in range(10):
        print("这是第{}次测试该脚本".format(i + 1))
        performance_test_module()
        print("OK -- Test")
        print("This is {} times running and time is {}".format(str(i), time.strftime("%Y%m%d_%H%M%S")))
    print("脚本测试结束，请检查测试结果")
