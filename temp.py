# coding = utf8
import os
os.path.abspath(".")
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from time import sleep

# Huawei P30 pro
device_milan = init_device("Android", uuid = "MQS0219619020975")
# Austin 11#
# device_milan = init_device("Android", uuid = "11921b86")
# Milan 40#
# device_milan = init_device("Android", uuid = "AMBY9DWG59T8KVAU")
# 已修改源码以兼容Android 11版本
poco = AndroidUiautomationPoco()
keyevent("home")
if not device_milan.is_screenon():
    keyevent("power")
    sleep(1)
poco().click()
start_app("com.android.settings")
poco(text = "Display & brightness").click()
poco("com.android.settings:id/seekbar").drag_to(poco("com.android.settings:id/brightness_indicator_right"), duration = 0.05)





