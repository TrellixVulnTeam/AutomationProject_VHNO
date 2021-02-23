# coding = utf8
import allure
import pytest
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from page.main_page import Main_Page
from toolsbar.common import test_device

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
def before_all_case_execute():
    test_device.unlock()
    home()
    poco = AndroidUiautomationPoco()
    main_page = Main_Page(test_device, poco)
    return main_page

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    获取每个用例状态的钩子函数
    :param item:
    :param call:
    :return:
    '''
    # 获取钩子方法的调用结果
    outcome = yield
    rep = outcome.get_result()
    # 仅仅获取用例call 执行结果是失败的情况, 不包含 setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        # 添加allure报告截图
        with allure.step('添加失败截图...'):
            allure.attach(test_device.snapshot("./screenshot/{}.png".format(item)), "失败截图", allure.attachment_type.PNG)

