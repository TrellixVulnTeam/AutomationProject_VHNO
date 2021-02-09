# coding = utf8
from time import sleep

from airtest.core.api import *
from airtest.core.error import AdbShellError, AirtestError
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException

os.path.abspath("..")

"""
    @File:case_construct_After_Fota.py
    @Author:Bruce
    @Date:2020/12/15
"""

poco = AndroidUiautomationPoco()
austinDevice = connect_device("Android:///7c2440fd")
# austinDevice = connect_device("Android:///b3e5b958")
# austinDevice = connect_device("Android:///MQS0219619020975")

# Fota后的独立操作Case
# 将case进行分解->剔出通用common方法->将APP分页处理->case整合->架构完善

"""
    common 方法1：上下滚动查找元素
"""


def scroll_to_find_element(element_text):
    global element
    menu_exists = False
    search_count = 0
    while not menu_exists:
        element = poco(text=element_text).wait()
        menu_exists = element.exists()
        if menu_exists:
            return element
        poco.scroll(direction="vertical", percent=0.8, duration=1)
        sleep(1)
        search_count += 1
        print("up: " + str(search_count) + str(menu_exists))
        # 给滑动查找增加向上滑动，兼容到底未找到的情况，即向下查找超过10次则开始向上查找
        while search_count >= 10 and not menu_exists:
            poco.scroll(direction="vertical", percent=-0.6, duration=1)
            element = poco(text=element_text).wait()
            menu_exists = element.exists()
            print("down: " + str(search_count) + str(menu_exists))
            if menu_exists:
                return element
    return element


"""
    common 方法2：获取屏幕点坐标用于操作
"""


def get_screen_point(point_name):
    device_display_info = austinDevice.get_display_info()
    screen_width = device_display_info["width"]
    screen_height = device_display_info["height"]
    # Such like Width: 720, Height: 1640
    print("Width: {}, Height: {}".format(screen_width, screen_height))
    if point_name == "center_point":
        return screen_width / 2, screen_height / 2
    elif point_name == "top_left_point":
        return 0, 0
    elif point_name == "top_right_point":
        return screen_width, 0
    elif point_name == "bottom_left_point":
        return 0, screen_height
    elif point_name == "bottom_right_point":
        return screen_width, screen_height
    elif point_name == "top_center_point":
        return screen_width / 2, 0
    elif point_name == "bottom_center_point":
        return screen_width / 2, screen_height
    elif point_name == "left_center_point":
        return 0, screen_height / 2
    elif point_name == "right_center_point":
        return screen_width, screen_height / 2


"""
    Case 1:验证Fota后能正常收发短信
    relate app:
        com.google.android.apps.messaging
    test step:
        检查APP存在->通过adb发送短信给自身号码->检查sms是否发送成功
"""


def check_sms_send_and_receiver(number="18512026630", content="Test_After_Fota"):
    start_app("com.google.android.apps.messaging")
    austinDevice.shell("am start -a android.intent.action.SENDTO -d sms:%s --es sms_body %s" % (number, content))
    poco(text="SMS").wait().click()
    receiver_content = poco("android:id/list").wait().children()[2].get_name()
    print(receiver_content)
    if number[-4:] in receiver_content:
        print("PASS")


"""
    Case 2:验证Fota后能正常创建联系人
    relate app:
        com.google.android.contacts
    test step:
        检查APP存在->adb创建联系人->Save->记录当前联系人->检查联系人是否创建成功
"""


def check_contact_create(contact_name="Test_After_Fota", phone_number="18575211714"):
    austinDevice.shell("am start -a android.intent.action.INSERT -t vnd.android.cursor.dir/"
                       "contact -e name %s -e phone %s" % (contact_name, phone_number))


"""
    Case 3:验证Fota后再次检测提示语
    relate app:
        com.tcl.fota.system
    test step:
        检查APP存在->点击CHECK FOR UPDATES->检测Checking for updates...存在即开始检测，验证提示语是否正常
"""


def check_fota_hint():
    start_app(package="com.tcl.fota.system", activity="SystemUpdatesActivity")
    searching_fota = False
    while not searching_fota:
        poco("com.tcl.fota.system:id/text_download_progress_button").wait().click()
        searching_fota = poco(text="Checking for updates...").wait().exists()
        if searching_fota:
            break
    if poco(text="No update available").wait(10).exists():
        print("No update available, pass!")


"""
    Case 4:验证Fota后WiFi上网数据有增加
    relate app:
        dumpsys netstats | grep -E 'iface=wlan.*networkId
        com.android.settings
    test step:
        检查APP存在->检查WiFi是否连接，没有就先连接WiFi->Settings->SIM cards & cellular network
        ->Data usage->获取当前Data usage->大于0即判断有数据消耗
"""


def check_data_usage_normal():
    global netstats
    try:
        stop_app("com.android.settings")
        start_app("com.android.settings")
        # 检查WiFi是否连接，如果没有连接就先连接WiFi
        try:
            netstats = shell("dumpsys netstats | grep -E 'iface=wlan.*networkId'")
            if netstats is not None:
                wifi_name = netstats.split('networkId="')[1].split('",')[0]
                print(wifi_name)
        except AdbShellError:
            print("WiFi not connected!")
            # connect_wifi()
        finally:
            scroll_to_find_element("SIM cards & cellular network").click()
            print(scroll_to_find_element("Data usage").wait().sibling("android:id/summary").get_text())
    except Exception:
        print("Some thing error, please check!")


"""
    Case 5:验证Fota后GPS能够定位成功
    relate app:
        com.tcl.tct.weather
    test step:
        检查APP存在->检查WiFi是否连接，没有就先连接WiFi->检查weather app是否存在，不存在即安装一个->Fota升级后尝试去定位
        ->记录结果
"""


def check_gps_location_ok():
    # check whether app exists, if not exists install it
    package_name = "com.tcl.tct.weather"
    try:
        austinDevice.check_app(package_name)
    except AirtestError:
        print("Not found {}, we will install it, thank you!".format(package_name))
        install("../apk/TctWeather.apk")
    finally:
        clear_app(package_name)
        start_app(package_name)
        try:
            pass
            # try to get location then save result
        except Exception:
            print("Some thing error, please check!")


"""
    Case 6:验证Fota后Screen recorder能够正常录制
    relate app:
        com.android.settings
    test step:
        检查APP存在->下拉状态栏->展开quick settings面板->点击Screen recorder开始录制->休眠一段时间
        ->再次通过下拉状态栏进行停止录屏
        ->记录结果
"""


def screenrecorder(mark="Screen record", record_time=8, status=False):
    try:
        home()
        austinDevice.swipe(get_screen_point("top_center_point"), get_screen_point("center_point"))
        poco("com.android.systemui:id/quick_qs_status_icons").wait().drag_to(
            poco("com.android.systemui:id/header_label").wait(), duration=1)
        poco(text="Screen recorder").wait().click()
        print(mark)
        if status:
            sleep(record_time)
    except Exception as ex:
        print("Some thing error, please check!")
        print(ex)


def check_screenrecorder_ok():
    try:
        screenrecorder("Begin screen recorder!", 8, True)
        screenrecorder("Stop screen recorder!", 8, False)
        record_files = austinDevice.shell("ls /sdcard/DCIM/Screen\ Recorder | grep mp4")
        print(record_files)
    except Exception as ex:
        print("Some thing error, please check!")
        print(ex)


if __name__ == "__main__":
    """
        亮屏并解锁屏幕操作，SIM PIN 1234解锁
    """
    austinDevice.unlock()
    try:
        poco("com.android.systemui:id/lock_icon").drag_to(poco("com.android.systemui:id/rectangle_frame"), duration=0.5)
        try:
            if poco(text="BACK").wait().exists():
                for i in range(1, 5):
                    poco(text="%s" % i).wait().click()
                keyevent("KEYCODE_ENTER")
        except PocoNoSuchNodeException:
            print("Screen lock interface not ok, please check!")
    except PocoNoSuchNodeException:
        print("No screen lock")
    finally:
        home()
    # test
    check_screenrecorder_ok()
