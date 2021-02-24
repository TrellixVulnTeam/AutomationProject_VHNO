# coding = utf8

import allure
import pytest
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from page.main_page import Main_Page
from toolsbar.common import test_device, logger

os.path.abspath(".")

"""
    @File:conftest.py
    @Author:Bruce
    @Date:2020/12/15
"""

"""
    a py file which saved pytest's fixture for use
"""

# 测试前初始化poco和device，手动调用获取main_page，只初始化一次，但全局使用同一个main_page
@pytest.fixture(scope="session", autouse=True)
def before_all_case_execute():
    test_device.unlock()
    home()
    poco = AndroidUiautomationPoco()
    main_page = Main_Page(test_device, poco)
    return main_page


"""
    每条case执行后进行关闭当前APP操作 - 自动调用
"""
@pytest.fixture(scope="function", autouse=True)
def after_current_case_execute():
    logger.info("当前case测试结束，执行关闭APP操作：")
    yield
    test_device.stop_app(test_device.get_top_activity()[0])
    logger.info("APP关闭完成")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    '''
    获取每个用例状态的钩子函数
    :param item:测试用例
    '''
    # 获取钩子方法的调用结果
    outcome = yield
    rep = outcome.get_result()
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
            file_name = "./screenshot/{}.png".format(item)
            test_device.snapshot(file_name)
            with open(file_name, mode="rb") as f:
                file = f.read()
            allure.attach(file, "{}:失败截图".format(item), allure.attachment_type.PNG)

