# coding = utf8
import os
import sys

from page.calendar.calendar_page import Calendar_Page
from page.camera.camera_page import Camera_Page
from page.chrome.chrome_page import Chrome_Page
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


class TestBeforeFota:

    # case 1:
    def test_camera(self, before_all_case_execute):
        global saved_data
        camera_page = Camera_Page(before_all_case_execute)
        camera_page.start_camera()
        camera_page.enter_camera_settings()
        result = camera_page.change_ai_scene_status()
        saved_data.append([sys._getframe().f_code.co_name, result[0], result[1]])
        assert 1 == 2

    def test_enter_chrome(self, before_all_case_execute):
        global saved_data
        chrome_page = Chrome_Page(before_all_case_execute)
        chrome_page.start_chrome()
        chrome_page.enter_website()
        assert 1 == 1

    def test_calendar(self, before_all_case_execute):
        calendar_page = Calendar_Page(before_all_case_execute)
        calendar_page.start_calendar()
        calendar_page.start_calendar()

    # 最后对saved_data进行处理并保存写入
    def test_sort_all_data(self):
        global saved_data
        save2csv = Save2Csv()
        for item in saved_data:
            save2csv.writeInCsv(item)
        assert saved_data is not None
