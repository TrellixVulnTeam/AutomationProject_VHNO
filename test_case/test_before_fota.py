# coding = utf8
import os
import sys

import allure
import pytest

from page.dialer.dialer_page import Dialer_Page
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
    @allure.description("APK版本差异化")
    @allure.step("获取当前应用的版本号->保存当前版本号")
    @pytest.mark.parametrize("packageName", ["com.android.settings", "com.android.deskclock"])
    def test_apk_version(self, before_all_case_execute, packageName):
        system = System(before_all_case_execute)
        result = system.get_app_version(packageName)
        saved_data.append([sys._getframe().f_code.co_name + "[" + packageName + "]", result, "\\"])
        assert result is not None

    # case 2:
    @allure.description("通话设置差异化")
    @allure.step("进入Dialer->点击右上角Menu->Settings->Display options->Sort by->更改排序方式->保存更改后的结果")
    def test_dialer_settings(self, before_all_case_execute):
        dialer_page = Dialer_Page(before_all_case_execute)
        dialer_page.start_dialer()
        sort_option = dialer_page.enter_sort_interface()
        first_name = sort_option[0]
        last_name = sort_option[1]
        if first_name.attr("checked"):
            last_name.click()
            dialer_page.settings_menu_Settings_Display_options_Sort_by.wait().click()
            last_name.invalidate()
            result = last_name.get_text() + ":" + str(last_name.attr("checked"))
        else:
            first_name.click()
            dialer_page.settings_menu_Settings_Display_options_Sort_by.wait().click()
            first_name.invalidate()
            result = first_name.get_text() + ":" + str(first_name.attr("checked"))
        saved_data.append([sys._getframe().f_code.co_name, "\\", result])
        assert result is not None

    # Not case, test data sort function
    @allure.description("非测试Case:"
                        "\n作用:最后对saved_data进行处理并保存写入")
    @allure.step("初始化Save2Csv对象->将获取到的每个测试结果写入Excel表格保存")
    def test_sort_all_data(self):
        save2csv = Save2Csv()
        save2csv.writeInCsv(saved_data)
        assert saved_data is not None
