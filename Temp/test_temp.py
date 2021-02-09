# coding = utf8
import os

os.path.abspath("..")
"""
    @File:test_temp.py
    @Author:Bruce
    @Date:2020/12/23
"""


from airtest.core.api import connect_device
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

device = connect_device("android:///b3e5b958")
poco = AndroidUiautomationPoco()

device.start_app("com.google.android.dialer")
poco("com.google.android.dialer:id/three_dot_menu_or_clear_icon_view").wait().click()
poco(text="Settings").wait().click()
#
# device_1 = connect_device('android:///XWNNPN7XBQFA7HUO')
# # device_2 = connect_device('android:///b3e5b958')
#
# poco_1 = AndroidUiautomationPoco(device_1, use_airtest_input=False, screenshot_each_action=False)
# # poco_2 = AndroidUiautomationPoco(device_2, use_airtest_input=False, screenshot_each_action=False)
# device_1.home()
# # device_2.home()
# poco_1("com.tcl.tct.weather:id/tct_widget_main_layout").click()
# # poco_2("com.tcl.tct.weather:id/tct_widget_main_layout").click()
# device_1.home()
# # device_2.home()


# command = "sh ./apk/install_apk.sh"
# screenData = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
# while True:
#     line = screenData.stdout.readline()
#     print(line.decode("utf-8"))
#     if line == b"" or subprocess.Popen.poll(screenData) == 0:
#         screenData.stdout.close()
#         break

def func(x):
    return x + 1


def test_answer():
    assert func(4) == 5

