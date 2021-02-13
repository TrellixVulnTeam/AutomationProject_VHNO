# coding = utf8
import os

from page.camera.camera_page import Camera_Page
from page.settings.settings_page import Settings_Page

os.path.abspath(".")
"""
    @File:test_before_fota.py
    @Author:Bruce
    @Date:2021/2/13
"""

"""
    Fota差异化设置，并excel记录下修改后控件都status、信息，供后续比对
"""
class TestBeforeFota:

    # case 1:
    def test_camera(self, before_case_execute):
        camera_page = Camera_Page(before_case_execute)
        result = camera_page.enter_camera_settings()
        assert result is not None

    # case 1:
    def test_settings(self, before_case_execute):
        settings_page = Settings_Page(before_case_execute)
        result = settings_page.get_imei_cu()
        assert result is not None

