# coding = utf8
import os
from time import sleep

import pyautogui

from page_windows import main_page

os.path.abspath(".")


class Clock_Page:

    def __init__(self):
        self.title = "OnlyStopWatch 2.62"
        self.handle = 0
        self.reset_begin = "F5"
        self.continue_pause = "F6"
        self.full = "F11"

    def start_clock(self):
        main_page.open_program(path=r"D:\For_Work\PandaOs性能测试_study\OnlyStopWatch.exe")
        sleep(1)
        self.handle = main_page.find_handle(self.title)
        return self.handle

    def stop_clock(self, handle):
        main_page.stop_program(handle)

    def reset_and_begin(self):
        pyautogui.press(self.reset_begin)

    def continue_and_pause(self):
        pyautogui.press(self.continue_pause)

    def get_focus(self, handle):
        # main_page.put_window_focus(self.handle)
        main_page.put_window_focus(handle)

    def full_screen(self):
        pyautogui.press(self.full)


if __name__ == '__main__':
    clock = Clock_Page()
    clock.start_clock()
    sleep(5)
    clock.get_focus()
    clock.continue_and_pause()
    clock.full_screen()
    # sleep(3)
    # clock.stop_clock()
