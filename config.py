# coding = utf8

from airtest.core.api import *
import re
import os

os.path.abspath(".")

"""
    @File:config.py
    @Author:Bruce
    @Date:2020/12/15
"""


# ['7c2440fd', 'b3e5b958']
def get_serial_number():
    devices_stream = os.popen("adb devices")
    devices = devices_stream.read()
    serial_no = re.findall("(.*)\tdevice", devices)
    devices_stream.close()
    return serial_no


# Return devices serial number
SERIAL_NUMBER = get_serial_number()


