# coding = utf8
import os
from time import sleep

import pyautogui

from page_windows import main_page

os.path.abspath(".")


class Ev_Recorder_Page:

    def __init__(self):
        self.title = "EV录屏"
        self.handle = 0
        self.start_pause_record = ("ctrl", "f1")
        self.stop_reserve_record = ("ctrl", "f2")

    def start_ev_recorder(self):
        main_page.open_program(path=r"D:\EVCapture\EVCapture.exe")
        sleep(2)
        self.handle = main_page.find_handle(self.title)
        return self.handle

    def stop_ev_recorder(self, handle):
        # 先手动设置关闭时，退出程序
        main_page.stop_program(handle)

    def get_focus(self, handle):
        # main_page.put_window_focus(self.handle)
        main_page.put_window_focus(handle)

    def start_and_pause_record(self):
        pyautogui.hotkey(self.start_pause_record[0], self.start_pause_record[1])

    def stop_and_reserve_record(self):
        pyautogui.hotkey(self.stop_reserve_record[0], self.stop_reserve_record[1])

    # 录制完成后将视频名称直接输入然后enter,测试时务必切换到英文输入法
    def change_record_video_name(self, case_number, case_count):
        name = "case{}_testVideo_{}".format(case_number, case_count)
        pyautogui.typewrite(message=name, interval=0.1)
        pyautogui.press("enter")

    # 每条case的10次都保存在特定的文件夹中,定位原因限制，目前先保留在相同文件夹
    # 28条case即280个视频
    # 需要手动调整好ev录屏软件的存放点，注意命名
    # 测试前添加英语为首选语言
    def change_video_to_specific_path(self, path):
        pass


if __name__ == '__main__':
    ev_recorder_page = Ev_Recorder_Page()
    for i in range(3):
        ev_recorder_page.start_ev_recorder()
        sleep(2)
        ev_recorder_page.change_video_to_specific_path(r"D:\For_Work\PandaOs性能测试_study\temp")
        sleep(2)
        ev_recorder_page.start_and_pause_record()
        sleep(10)
        ev_recorder_page.stop_and_reserve_record()
        sleep(2)
        ev_recorder_page.change_record_video_name(name="Record_Test_{}_and_Happy_Stable_Second_Test".format(i + 1))
        sleep(2)
        ev_recorder_page.stop_ev_recorder()
