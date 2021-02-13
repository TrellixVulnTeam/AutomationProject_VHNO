# coding = utf8

from multiprocessing.dummy import Process

import pytest
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from page.main_page import Main_Page
from toolsbar.common import test_device, device_count

os.path.abspath(".")

"""
    @File:conftest.py
    @Author:Bruce
    @Date:2020/12/15
"""

"""
    a py file which saved pytest's fixture for use
"""

# 测试前初始化poco和device
@pytest.fixture(scope="session", autouse=True)
def before_case_execute():
    test_device.unlock()
    home()
    poco = AndroidUiautomationPoco()
    main_page = Main_Page(test_device, poco)
    return main_page



