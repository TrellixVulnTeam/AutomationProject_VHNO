# coding = utf8
import os

os.path.abspath(".")
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from config import SERIAL_NUMBER

"""
    @File:common.py
    @Author:Bruce
    @Date:2020/12/23
"""

device_count = len(SERIAL_NUMBER)

def single_device():
    austinDevice = connect_device("Android:///{}".format(SERIAL_NUMBER[0]))
    return austinDevice


def multiple_device():
    device_list = []
    for serial_no in SERIAL_NUMBER:
        austinDevice = connect_device("Android:///{}".format(serial_no))
        device_list.append(austinDevice)
    return device_list


def init_all_device():
    if len(SERIAL_NUMBER) > 1:
        device_init = multiple_device()
    else:
        device_init = single_device()

    return device_init


devices = init_all_device()