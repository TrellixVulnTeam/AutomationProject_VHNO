# coding = utf8

import allure
import pytest
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from page.main_page import Main_Page
from page.system.system import System
from toolsbar.common import logger

os.path.abspath(".")
cur_time = time.strftime("%Y%m%d_%H%M%S")

"""
    @File:conftest.py
    @Author:Bruce
    @Date:2020/12/15
    @Description:Pytest架构的conftest库作为插件存放,存放你的fixture函数,在里面写自己的本地插件
"""

"""
    @description:整个测试case执行前的操作
    @param:
        cmdopt:调用cmdopt获取cmd命令行传入的参数
    @fixture:
        scope:设置作用域为整个Session
        autouse:当pytest测试启动时自动运行该函数
"""


# 测试前初始化poco和device，手动调用获取main_page，只初始化一次，但全局使用同一个main_page
@pytest.fixture(scope="session", autouse=True)
def before_all_case_execute(cmdopt):
    device_ = connect_device("Android:///{}".format(cmdopt))
    device_.wake()
    device_.unlock()
    # 关闭自动调节亮度，并设置屏幕常亮、sleep为never或最大
    device_.shell("settings put system screen_brightness_mode 0")
    device_.shell("settings put system screen_brightness 999999")
    device_.shell("settings put system screen_off_timeout 1")
    poco = AndroidUiautomationPoco(device=device_, use_airtest_input=False,
                                   screenshot_each_action=False)
    main_page = Main_Page(device_, poco)
    system = System(main_page)
    system.unlock_screen()

    return main_page


"""
    @description:每条case执行后进行关闭当前APP操作
    @param:
        cmdopt:调用cmdopt获取cmd命令行传入的参数
    @fixture:
        scope:设置作用域为每条case(function)
        autouse:当pytest测试启动时自动运行该函数
"""


@pytest.fixture(scope="function", autouse=True)
def after_current_case_execute(cmdopt):
    yield
    device_ = connect_device("Android:///{}".format(cmdopt))

    logger.info("当前case测试结束，执行关闭APP操作：")
    top_activity = device_.get_top_activity()[0]
    if top_activity != "com.tcl.android.launcher":
        device_.stop_app(top_activity)
        logger.info("APP关闭完成")
    else:
        logger.info("当前界面为主界面")


"""
    @description:传参数，获取从命令行传入的存储的device序列号
    @param:
        parser:用户命令行参数与ini文件值的解析器
"""


def pytest_addoption(parser):
    parser.addoption(
        "--cmdopt", action="store", default="7c2440fd", help="current device serialno"
    )


"""
    @description:命令行接收参数
    @param:
        request:请求获取
    @fixture:
        scope:设置作用域为整个Session
"""


@pytest.fixture(scope="session")
def cmdopt(request):
    return request.config.getoption("--cmdopt")


"""
    @description:
        pytest测试抓取每个用例执行时的报错处理函数
        (在用例执行的三个阶段setup, call, teardown都会调用一次)
    @param:
        item:测试用例
    @hookimpl:
        tryfirst:作为第一个钩子函数使用,首先执行钩子函数装饰器
        hookwrapper:True在其他钩子函数周围执行
"""


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
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
            file_name = "./screenshot/{}_{}_{}.png".format(str(item).strip("<").strip(">").replace(" ", "_"),
                                                           time.strftime("%Y%m%d_%H%M%S"), "")
            snapshot(file_name)
            sleep(3)
            with open(file_name, mode="rb") as f:
                file = f.read()
            allure.attach(file, "{}:失败截图".format(item), allure.attachment_type.PNG)
