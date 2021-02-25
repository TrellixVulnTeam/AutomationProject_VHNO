# coding = utf8
import os
import sys

import allure
import pytest

from page.system.system import System
from toolsbar.save2csv import Save2Csv

os.path.abspath(".")
"""
    @File:test_before_fota.py
    @Author:Bruce
    @Date:2021/2/13
"""

"""
    Fota差异化设置，并excel记录下修改后控件都status、信息，供后续比对
"""

# function name , previous_data, set_data
saved_data = []

"""
    同一文件下，用例执行顺序，从上往下
"""


@allure.feature("Fota前置差异化设置")
class TestBeforeFota:

    # case 1:
    @allure.description("APK版本差异化设置")
    @allure.step("启动camera->进入camera settings菜单->更改ai scene 状态->保存变量")
    @pytest.mark.parametrize("packageName", ["com.android.settings", "com.android.deskclock"])
    def test_apk_version(self, before_all_case_execute, packageName):
        system = System(before_all_case_execute)
        result = system.get_app_version(packageName)
        saved_data.append([sys._getframe().f_code.co_name + "[" +packageName + "]", result, "\\"])
        assert result is not None

    # Not case, test data sort function
    @allure.description("非测试Case:"
                        "\n作用:最后对saved_data进行处理并保存写入")
    @allure.step("初始化Save2Csv对象->将获取到的每个测试结果写入Excel表格保存")
    def test_sort_all_data(self):
        save2csv = Save2Csv()
        save2csv.writeInCsv(saved_data)
        assert saved_data is not None
