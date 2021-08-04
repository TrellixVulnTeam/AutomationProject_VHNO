# coding = utf8
import os

import win32api
import win32con
import win32gui

os.path.abspath(".")
"""
    @File:main_page.py
    @Author:Bruce
    @Date:2021/1/13
    @Description:A main page_windows for all other page_windows to combine some normal functions
"""

"""
    @description:（通用函数）该函数用于通过win32api进行打开某个程序
"""


def open_program(path):
    win32api.ShellExecute(1, "open", path, "", "", 1)


"""
    @description:（通用函数）该函数用于通过win32api进行关闭某个程序
"""


def stop_program(handle):
    win32gui.SendMessage(handle, win32con.WM_CLOSE)


"""
    @description:（通用函数）该函数用于通过win32gui进行获取当前窗口的句柄
"""


def find_handle(title):
    # 查找窗口句柄
    para_hld = win32gui.FindWindow(None, title)
    print(para_hld)
    return para_hld


"""
    @description:（通用函数）该函数用于通过win32gui将某个程序获取到焦点
"""


def put_window_focus(handle):
    win32gui.SetForegroundWindow(handle)
