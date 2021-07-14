# coding = utf8
import os
import sys
import time

import allure
import pytest
from airtest.core.api import connect_device

os.path.abspath(".")
from page.settings.settings_page import Settings_Page
from page.system.system import System
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
    @allure.description("APK版本差异化")
    @allure.step("获取当前应用的版本号->保存当前版本号")
    @pytest.mark.parametrize("packageName", read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
                                                                            case_name="test_apk_version"))
    def test_apk_version(self, before_all_case_execute, packageName):
        system = System(before_all_case_execute)
        result = system.get_app_version(packageName)
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
