import os

from see_vision_case.performance_test import system_test_work_flow

os.path.abspath(".")

"""
    @description:该函数用于执行一个完整的测试项：
        当前工作流有：性能测试工作流
        测试前：
        1、关闭护眼模式
        2、休眠时间设置永不
"""
if __name__ == '__main__':
    # performance_test_work_flow(0, 0, case_count=28, case_running_times=30)
    clock_case_number = 5
    # calendar_case_number = 1
    # system_test_work_flow(calendar_case_number)
    system_test_work_flow(clock_case_number)
