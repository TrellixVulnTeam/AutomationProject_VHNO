# coding = utf8
import os


os.path.abspath(".")
"""
    @File:temp.py
    @Author:Bruce
    @Date:2020/12/23
"""


from airtest.core.api import connect_device
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

device_1 = connect_device('android:///7c2440fd')
device_2 = connect_device('android:///b3e5b958')

poco_1 = AndroidUiautomationPoco(device_1, use_airtest_input=False, screenshot_each_action=False)
poco_2 = AndroidUiautomationPoco(device_2, use_airtest_input=False, screenshot_each_action=False)
device_1.home()
device_2.home()
poco_1("com.tcl.tct.weather:id/tct_widget_main_layout").click()
poco_2("com.tcl.tct.weather:id/tct_widget_main_layout").click()
device_1.home()
device_2.home()
