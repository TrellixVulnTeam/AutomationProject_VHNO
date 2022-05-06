import multiprocessing
import os
import subprocess

from see_vision_case.performance_test import system_test_work_flow, performance_test_work_flow

os.path.abspath(".")

"""
    @description:该函数用于执行一个完整的测试项：
        当前工作流有：性能测试工作流
        测试前：
        1、关闭护眼模式
        2、休眠时间设置永不
"""


def logcat_run():
    if not os.path.exists("./log/"):
        os.mkdir("./log/")
    log_process = subprocess.Popen("adb logcat -b all>./log/logcat.log",
                                   shell=True).communicate()[0]


if __name__ == '__main__':
    performance_test_work_flow(0, 0, case_count=28, case_running_times=10)

    # calendar_case_number = 1
    # system_test_work_flow(calendar_case_number)

    # clock_case_number = 3
    # system_case_number = 1
    # test_pool = multiprocessing.Pool(2)
    # test_pool.apply_async(func=logcat_run, )
    # test_pool.apply_async(func=system_test_work_flow(system_case_number))
    # test_pool.close()
    # test_pool.join()

    # system_test_work_flow(clock_case_number)
