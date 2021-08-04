# coding = utf8
import os
from time import sleep

import pyautogui

from page_windows import main_page

os.path.abspath(".")
pyautogui.FAILSAFE = False


class PotPlayer_Page:

    def __init__(self):
        self.title = "PotPlayer"
        self.handle = 0
        self.camera_config = ("alt", "d")
        self.open_config = ("alt", "o")
        self.enter = "enter"
        self.tv_camera = "TV/CAM/设备 - PotPlayer"
        self.tv_camera_size_60 = ("alt", "3")

    """
        @description:该函数用于通过win32api启动Potplayer视频程序
    """

    def start_potplayer(self):
        main_page.open_program(path=r"D:\PotPlayer\PotPlayerMini64.exe")
        sleep(2)
        self.handle = main_page.find_handle(self.title)
        return self.handle

    """
        @description:该函数用于通过win32api关闭Potplayer视频程序
    """

    def stop_potplayer(self, handle):
        main_page.stop_program(handle)

    """
        @description:该函数用于通过pyautogui启动指定的camera成像到Potplayer中
    """

    def open_camera(self):
        pyautogui.hotkey(self.camera_config[0], self.camera_config[1])
        sleep(1)
        pyautogui.hotkey(self.open_config[0], self.open_config[1])
        pyautogui.hotkey(self.open_config[0], self.open_config[1])
        pyautogui.press(self.enter)
        sleep(3)
        pyautogui.hotkey(self.tv_camera_size_60[0], self.tv_camera_size_60[1])
        sleep(2)

    """
        @description:该函数用于通过win32api获取当前Potplayer的焦点
    """

    def get_focus(self, handle):
        # main_page.put_window_focus(self.handle)
        main_page.put_window_focus(handle)


if __name__ == '__main__':
    potplayer_page = PotPlayer_Page()
    potplayer_page.start_potplayer()
    potplayer_page.open_camera()
    # potplayer_page.open_camera()
