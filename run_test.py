import os

from see_vision_case.performance_test import performance_test_work_flow

os.path.abspath(".")

if __name__ == '__main__':
    performance_test_work_flow(0, 0, case_count=28, case_running_times=5)
