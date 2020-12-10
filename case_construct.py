# coding = utf8
from time import sleep

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

os.path.abspath(".")

poco = AndroidUiautomationPoco()
austinDevice = connect_device("Android:///7c2440fd")

# 将case进行分解->剔出通用common方法->将APP分页处理->case整合->架构完善
# 状态更改需要先进行判断设置为除自身外其它状态,如默认checked = true，则设置为false，并记录前后状态以及Fota后状态

"""
    Case 1:获取本地应用程序版本被保留
    relate app:
        com.android.settings
    test step：
        检查APP存在->获取APP版本并保存->Fota升级后再次获取版本号与升级前对比是否相同判定结果
"""


def get_app_version(packageName="com.android.settings"):
    exists_app = austinDevice.check_app(packageName)
    if exists_app:
        versionName = austinDevice.shell("pm dump %s|grep versionName" % packageName)
        print(versionName)


"""
    Case 2:通话配置修改被保留
    relate app:
        com.google.android.dialer
    test step:
        检查APP存在->进入Dialer->点击菜单->Settings->Display options->Sort by->更改值并保存->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def change_calling_settings():
    start_app("com.google.android.dialer")


"""
    Case 3:验证通话记录被保留
    relate app:
        com.google.android.dialer
    test step:
        检查APP存在->通过adb拨打电话->进入APP->Recents->保存Top 1通话记录->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_calling_history(number="10086"):
    start_app("com.google.android.dialer")
    austinDevice.shell("am start -a android.intent.action.CALL tel:%s" % number)


"""
    Case 4:验证短信已发送、接受、草稿被保留
    relate app:
        com.google.android.apps.messaging
    test step:
        检查APP存在->通过adb发送短信给自身号码->检查是否发送成功并保存结果->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_sms_sender_receiver(number="18575211714", content="Test"):
    start_app("com.google.android.apps.messaging")
    austinDevice.shell("am start -a android.intent.action.SENDTO -d sms:%s --es sms_body %s" % (number, content))
    poco(text="SMS").click()
    sleep(3)
    receiver_content = poco("android:id/list").children()[2].get_name()
    print(receiver_content)
    if number[-4:] in receiver_content:
        print("PASS")


"""
    Case 5:验证短信相关设置是否被保留
    relate app:
        com.google.android.apps.messaging
    test step:
        检查APP存在->点击menu->Settings->Disable "Hear outgoing message sounds"->记录默认、修改、升级后元素状态(invalidate进行元素刷新)->
        Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def change_message_settings():
    stop_app("com.google.android.apps.messaging")
    sleep(1)
    start_app("com.google.android.apps.messaging")
    switch_on_off = poco('com.google.android.apps.messaging:id/switchWidget')
    print(switch_on_off.attr("checked"))


"""
    Case 6:验证手机联系人是否被保留
    relate app:
        com.google.android.apps.messaging
    test step:
        检查APP存在->adb创建联系人->Save->记录当前联系人->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_contact_reserved(contact_name="Test", phone_number="18575211714"):
    austinDevice.shell("am start -a android.intent.action.INSERT -t vnd.android.cursor.dir/"
                       "contact -e name %s -e phone %s" % (contact_name, phone_number))


"""
    Case 7:验证创建的Clock是否被保留
    relate app:
        com.android.deskclock
    test step:
        检查APP存在->点击"+"->记录Hour + Minutes->点击保存闹钟->在列表界面check闹钟创建成功->记录闹钟时间->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_clock_reserved():
    start_app("com.android.deskclock")


"""
    Case 8:验证创建的Calendar是否被保留
    relate app:
        com.google.android.calendar
    test step:
        检查APP存在->跳过Guide->点击"+"->输入Test->点击Save->记录Title->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_calendar_reserved():
    start_app("com.google.android.calendar")


"""
    Case 9:验证Battery management设置是否被保留
    relate app:
        com.tct.onetouchbooster
    test step:
        检查APP存在->点击x关闭guide->点击Battery->点击Settings->Disable "Intelligent power saving"
        ->记录默认、修改、升级后元素状态(invalidate进行元素刷新)->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def change_battery_management_settings():
    start_app("com.tct.onetouchbooster")


"""
    Case 10:验证相机设置是否被保留
    relate app:
        com.tcl.camera
        com.google.android.permissioncontroller
    test step:
        检查APP存在->点击WHILE USING THE APP进行授权->点击Settings->点击->点击AI scene detection更改状态
        ->记录默认、修改、升级后元素状态(invalidate进行元素刷新)->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def change_camera_settings():
    start_app("com.tcl.camera")
    sleep(1)
    camera_settings = (poco("com.tcl.camera:id/picker_list_layout").children()[0]).wait()
    sleep(1)
    camera_settings.click()
    sleep(1)
    print(poco(text="AI scene detection").parent().parent().children()[1].children().attr("checked"))


"""
    Case 11:验证声音设置是否被保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->Sound & vibration->Enable Silent mode->记录默认、修改、升级后元素状态(invalidate进行元素刷新)
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def change_sound_settings():
    apps_menu = None
    start_app("com.android.settings")
    menu_exists = False
    while not menu_exists:
        apps_menu = poco(text="Sound & vibration").wait()
        menu_exists = apps_menu.exists()
        if menu_exists:
            break
        poco.scroll(direction="vertical", percent=0.8, duration=1)
    apps_menu.click()
    silent_mode_switch = poco(text="Silent mode").parent().parent().children()[1].child(
        "android:id/switch_widget").wait()
    checked_result_default = silent_mode_switch.attr("checked")
    silent_mode_switch.click()
    # 清除该标志以重新获取该元素
    silent_mode_switch.invalidate()
    checked_result_changed = silent_mode_switch.attr("checked")
    checked_result_updated = silent_mode_switch.wait().attr("checked")
    print(str(checked_result_default) + "-" + str(checked_result_changed) + "-" + str(checked_result_updated))


"""
    Case 12:验证显示设置是否被保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->Display->Sleep->Never->记录默认、修改、升级后元素状态(invalidate进行元素刷新)
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def change_display_settings():
    start_app("com.android.settings")
    sleep(1)
    poco(text="Display").wait(3).click()
    sleep(1)
    sleep_time = poco(text="Sleep").sibling("android:id/summary").wait(3)
    sleep_time_default = sleep_time.get_text()
    print(sleep_time_default)
    poco(text="Sleep").wait(3).click()
    poco(text="Never").wait(3).click()
    sleep_time.invalidate()
    sleep_time_changed = sleep_time.get_text()
    print(sleep_time_changed)


"""
    Case 13:验证Gestures设置是否被保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->Button & gestures->Gestures->3-finger screenshot->Click it->记录默认、修改、升级后元素状态(invalidate进行元素刷新)
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def change_gestures_settings():
    start_app("com.android.settings")
    menu_exists = False
    search_count = 0
    while not menu_exists:
        apps_menu = poco(text="Button & gestures").wait()
        menu_exists = apps_menu.exists()
        if menu_exists:
            break
        poco.scroll(direction="vertical", percent=0.8, duration=1)
        search_count += 1
        # 给滑动查找增加向上滑动，兼容到底未找到的情况，即向下查找超过5次则开始向上查找
        if search_count >= 5 and not menu_exists:
            poco.scroll(direction="vertical", percent=-0.6, duration=1)
    apps_menu.click()
    poco(text="Gestures").wait(3).click()
    three_finger_screenshot = poco(text="3-finger screenshot").parent().parent().children()[2]\
        .child("com.android.settings:id/switchWidget").wait(3)
    checked_default = three_finger_screenshot.attr("checked")
    print(checked_default)
    three_finger_screenshot.click()
    three_finger_screenshot.invalidate()
    checked_changed = three_finger_screenshot.attr("checked")
    print(checked_changed)


if __name__ == "__main__":
    """
        亮屏并解锁屏幕操作
    """
    while not austinDevice.is_screenon():
        wake()
        while austinDevice.is_locked():
            austinDevice.unlock()
    home()
    # test  后续列表操作需要使用上下滑动进行查找元素保证兼容性




