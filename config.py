# coding = utf8
import os

from airtest.core.api import *
import re

os.path.abspath(".")

"""
    @File:config.py
    @Author:Bruce
    @Date:2020/12/15
"""


# ['7c2440fd', 'b3e5b958']
def get_serial_number():
    devices = os.popen("adb devices").read()
    serial_no = re.findall("(.*)\tdevice", devices)
    return serial_no


# Return devices serial number
SERIAL_NUMBER = get_serial_number()

