# coding = utf8
import os
import sys
import time

import allure
import pytest
from airtest.core.api import connect_device

from page_windows.clock.clock_page import Clock_Page

os.path.abspath(".")
from page_android.system.system import System
from toolsbar.excel_tools import read_excel_for_case_parametrize
from toolsbar.save2csv import Save2Csv

cur_time = time.strftime("%Y%m%d_%H%M%S")
"""
    @File:test_performance.py
    @Author:Bruce
    @Date:2021/2/13
    @Description:性能测试
"""

"""
    性能测试，并excel记录下修改后控件的status、信息，供后续比对
"""

# function name , previous_data, set_data
saved_data = []

"""
    同一文件下，用例执行顺序，从上往下
"""


@allure.feature("性能测试")
class TestPerformance:

    # case 1:
    @allure.description("开机速度测试")
    @allure.step("开始录屏->秒表reset->设备wake->进入home界面->reboot设备->进入到锁屏界面则->停止录屏->保存录屏->切帧图片")
    @pytest.mark.parametrize("packageName", read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
                                                                            case_name="test_apk_version"))
    def test_apk_version(self, before_all_case_execute, packageName):
        system = System(before_all_case_execute)
        result = system.get_app_version(packageName)
        system.kill_all_apps()
        system.get_app_version(packageName)
        system.device.start_app("com.android.settings")
        system.scroll_to_find_element(element_text="蓝牙").click()
        clock = Clock_Page()
        clock.start_clock()
        saved_data.append([sys._getframe().f_code.co_name + "[" + packageName + "]", result, "\\"])
        assert result is not None

    @allure.description("非测试Case:"
                        "\n作用:最后对saved_data进行处理并保存写入")
    @allure.step("初始化Save2Csv对象->将获取到的每个测试结果写入Excel表格保存")
    def test_sort_all_data(self, cmdopt):
        device_ = connect_device("Android:///{}".format(cmdopt))
        save2csv = Save2Csv()
        save2csv.writeInCsv(saved_data,
                            form_name="device_" + str(device_.serialno) + "_performance_test_{}.csv".format(cur_time))
        assert saved_data is not None
