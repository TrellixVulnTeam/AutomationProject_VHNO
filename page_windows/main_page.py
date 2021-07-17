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


def open_program(path):
    win32api.ShellExecute(1, "open", path, "", "", 1)


def stop_program(handle):
    win32gui.SendMessage(handle, win32con.WM_CLOSE)


def find_handle(title):
    # 查找窗口句柄
    para_hld = win32gui.FindWindow(None, title)
    print(para_hld)
    return para_hld


def put_window_focus(handle):
    win32gui.SetForegroundWindow(handle)
