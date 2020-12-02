# coding = utf8
import os
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from time import sleep
os.path.abspath(".")

poco = AndroidUiautomationPoco()
austinDevice = connect_device("Android:///7c2440fd")


# 将case进行分解->剔出通用common方法->将APP分页处理->case整合->架构完善

"""
    Case 1:获取本地应用程序版本被保留
    relate app:
        com.android.settings
    test step：
        检查APP存在->获取APP版本并保存->Fota升级后再次获取版本号与升级前对比是否相同判定结果
"""
def get_app_version(packageName = "com.android.settings"):
    exists_app = austinDevice.check_app(packageName)
    if exists_app:
        versionName = austinDevice.shell("pm dump %s|grep versionName" %packageName)
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
def check_calling_history(number = "10086"):
    start_app("com.google.android.dialer")
    austinDevice.shell("am start -a android.intent.action.CALL tel:%s" %number)

"""
    Case 4:验证短信已发送、接受、草稿被保留
    relate app:
        com.google.android.apps.messaging
    test step:
        检查APP存在->通过adb发送短信给自身号码->检查是否发送成功并保存结果->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""
def check_sms_sender_receiver(number = "18575211714", content = "Test"):
    start_app("com.google.android.apps.messaging")
    austinDevice.shell("am start -a android.intent.action.SENDTO -d sms:%s --es sms_body %s" %(number, content))
    poco(text = "SMS").click()
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
        检查APP存在->点击menu->Settings->Disable "Hear outgoing message sounds"->记录当前状态->Fota升级后再次获取该值与升级前对比是否相同判定结果
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
def check_contact_reserved(contact_name = "Test", phone_number = "18575211714"):
    austinDevice.shell("am start -a android.intent.action.INSERT -t vnd.android.cursor.dir/"
                       "contact -e name %s -e phone %s" %(contact_name, phone_number))

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
        检查APP存在->点击x关闭guide->点击Battery->点击Settings->Disable "Intelligent power saving"->记录当前状态->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""
def change_battery_management_settings():
    start_app("com.tct.onetouchbooster")


if __name__ == "__main__":
    home()