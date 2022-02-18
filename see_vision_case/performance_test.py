# coding = utf8
import logging
import multiprocessing
import os
import time
from time import sleep

from airtest.core.api import connect_device
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

from config import SERIAL_NUMBER, install_app_necessary, push_file_into_device
from page_android.main_page import Main_Page
from page_android.system.system import System
from page_windows.clock.clock_page import Clock_Page
from page_windows.ev_recorder.ev_recorder_page import Ev_Recorder_Page
from page_windows.ffmpeg.ffmpeg_page import Ffmpeg_Page
from page_windows.potplayer.potplayer_page import PotPlayer_Page
from see_vision_case.calendar_test_case import calendar_case_chooser
from see_vision_case.performance_test_case import case_chooser
from toolsbar import email_tools
from toolsbar.common import test_device
from toolsbar.permissionGrant import grant_permission

os.path.abspath(".")
# 过滤airtest log只打印ERROR的Log
logger_airtest = logging.getLogger("airtest")
logger_airtest.setLevel(logging.ERROR)
cur_time = time.strftime("%Y%m%d_%H%M%S")

"""
    @File:run_test.py
    @Author:Bruce
    @Date:2020/12/15
    @Description:项目运行函数，存放测试和调试函数
    For seevision automation framework
"""

"""
    单个设备poco、device不需要初始化
    多个设备poco、device都需要创建新对象poco_item
    后续将poco_item传入使用即可，airtest相关api，使用对应device_item进行调用
    case不需要重复写
    UI 进程和底部进程不要在同一个进程中容易出问题
"""

# 多机测试进程池:兼容单机和多机运行
"""
    @description:多进程创建进行多台设备测试
    @tip:
        Pycharm调用adb缺陷，需要使用terminal输入charm来启动pycharm，以获得dash权限
        执行case前，手动将pocoservice.apk的contniue安装好并将授权界面点掉，防止后续错误发生
"""


def start_test(case_number):
    test_pool = multiprocessing.Pool(len(SERIAL_NUMBER))
    for device_ in SERIAL_NUMBER:
        result = test_pool.apply_async(func=system_test_area, args=(device_, case_number,))
        # result = test_pool.apply_async(func=performance_test_area, args=(device_, case_number,))
        sleep(10)
    test_pool.close()
    test_pool.join()
    return result


"""
    @description:性能测试函数执行区域
    @param:
        device_:设备序列号
        case_number:测试用例的号码（数量）
"""


def performance_test_area(device_, case_number):
    device_ = connect_device("Android:///{}".format(device_))
    device_.wake()
    device_.unlock()
    poco = AndroidUiautomationPoco(device=device_, use_airtest_input=False,
                                   screenshot_each_action=False)
    main_page = Main_Page(device_, poco)
    system = System(main_page)
    system.unlock_screen()
    system.kill_all_apps()

    # 根据case编号来执行case
    sleep(2)
    return case_chooser(case_number, main_page)


"""
    @description:系统测试函数执行区域
    @param:
        device_:设备序列号
        case_number:测试用例的号码（数量）
"""


def system_test_area(device_, case_number):
    device_ = connect_device("Android:///{}".format(device_))
    device_.wake()
    device_.unlock()
    poco = AndroidUiautomationPoco(device=device_, use_airtest_input=False,
                                   screenshot_each_action=False)
    grant_permission(device_)
    main_page = Main_Page(device_, poco)
    system = System(main_page)
    system.unlock_screen()
    system.kill_all_apps()

    # 根据case编号来执行case
    sleep(2)
    return calendar_case_chooser(case_number, main_page)
    # return clock_case_chooser(case_number, main_page)


"""
    @description:测试前准备函数
    @param:
        test_device:设备序列号
"""


def test_prepare(test_device):
    print("当前设备数量：" + str(len(SERIAL_NUMBER)))
    if len(SERIAL_NUMBER) > 1:
        for i in test_device:
            install_app_necessary(i)
            grant_permission(i)
            push_file_into_device(r"D:\For_Work\PandaOs性能测试_study\test_resource\push_into_device", i)
            # pass
    else:
        install_app_necessary(test_device)
        grant_permission(test_device)
        push_file_into_device(r"D:\For_Work\PandaOs性能测试_study\test_resource\push_into_device", test_device)
        # pass


"""
    @description:性能测试执行工作流
    @param:
        i:用于case后续报错重跑的的数量（number）
        j:用于case后续报错重跑执行次数
        case_count:case数量（number）
        case_running_times:case执行次数
"""


def performance_test_work_flow(i=0, j=0, case_count=28, case_running_times=10):
    """
        整体运行流程:看稳定性和case执行起来效果,移除pytest，自己搭建框架，独立开来，不然后续不利于拓展测试项
        最后再加上log进去
        case编写需要一定时间比较多
        因为自动化操作和手动有些许不同，注意标注好每条case怎么判断计时的开始与结束！！！
    """
    test_prepare(test_device=test_device)
    ev_recorder_page = Ev_Recorder_Page()
    ffmpeg_page = Ffmpeg_Page("D:\\For_Work\\PandaOs性能测试_study\\temp\\",
                              "D:\\For_Work\\PandaOs性能测试_study\\test_result_temp\\")
    potplayer_page = PotPlayer_Page()
    clock = Clock_Page()

    potplayer_handle = potplayer_page.start_potplayer()
    potplayer_page.open_camera()

    clock_handle = clock.start_clock()
    sleep(2)
    ev_handle = ev_recorder_page.start_ev_recorder()
    case_running_cycle(ev_recorder_page, clock, clock_handle, ffmpeg_page, i=i, j=j, case_count=case_count,
                       case_running_times=case_running_times)
    potplayer_page.stop_potplayer(potplayer_handle)
    clock.stop_clock(clock_handle)


"""
    系统测试压力测试脚本工作流
"""


def system_test_work_flow(case_count):
    i = 0
    for i in range(i, case_count):
        start_test(i + 1).get()


def rerun_case_construct(ev_recorder_page, clock, clock_handle, ffmpeg_page, case_count, case_running_times, i, j):
    # 重跑机制：适用于当case报错exception后，进行判断如果当前case执行失败则单独将该case进行重跑，不影响测试结果保存
    rerun_case_number = 0
    if i < case_count:
        rerun_case_number = i
        case_running_cycle(ev_recorder_page, clock, clock_handle, ffmpeg_page, case_count=case_count,
                           case_running_times=case_running_times, i=rerun_case_number, j=j)


# Case重跑次数限制
case_rerun_times_limit = 0

"""
    @description:case重跑机制
    @param:
        i:用于case后续报错重跑的的数量（number）
        j:用于case后续报错重跑执行次数
        case_count:case数量（number）
        case_running_times:case执行次数
        ev_recorder_page:传入EV录屏的对象
        clock:传入clock对象
        clock_handle:传入clock的handle
        ffmpeg_page:传入FFmpeg的对象
"""


def case_running_cycle(ev_recorder_page, clock, clock_handle, ffmpeg_page, i=0, j=0, case_count=28,
                       case_running_times=10):
    # 大循环控制case number
    # 小循环控制每条case执行次数
    current_case_number = 0
    current_case_running_times = 0
    try:
        for i in range(i, case_count):
            current_case_number = i
            for j in range(case_running_times):
                if j > 10:
                    break
                current_case_running_times = j
                print("case{}_第{}次_Test".format(i + 1, j + 1))
                # 手动改ev recorder路径，和后续ffmpeg一致
                ev_recorder_page.start_and_pause_record()
                sleep(2)
                clock.get_focus(clock_handle)
                clock.reset_and_begin()

                # operate in Android device
                """
                    Android Device operate area
                    传入case编号，执行相应case
                """
                case_number = i + 1
                print("当前case{}_第{}次测试结果为：{}".format(case_number, j + 1, start_test(case_number).get()))
                sleep(2)
                ev_recorder_page.stop_and_reserve_record()
                sleep(2)
                ev_recorder_page.change_record_video_name(i + 1, j + 1)
                sleep(2)
                ffmpeg_page.cut_video_into_pieces_frame_picture(i + 1, j + 1)
                sleep(2)
    except Exception as ex:
        # 如果开始重跑就发送邮件给792607724@qq.com，说明那一条发生错误，并继续尝试重跑
        feed_back = "Current time happened exception, please check current case code's logic is ok? case number:{}, and case running time is:{},and exception is {}".format(
            current_case_number, current_case_running_times, str(ex))
        email_tools.send_mail(message_content=feed_back, subject_content="测试错误邮件反馈")
        print(feed_back)
        if case_rerun_times_limit < 3:
            if current_case_running_times < case_running_times:
                case_running_times += 1
                rerun_case_construct(ev_recorder_page, clock, clock_handle, ffmpeg_page, case_count=case_count,
                                     case_running_times=case_running_times, i=current_case_number,
                                     j=current_case_running_times)


if __name__ == '__main__':
    # performance_test_work_flow()
    for i in range(1):
        print("当前case{}_第{}次测试结果为：{}".format(6, i + 1, start_test(1).get()))
