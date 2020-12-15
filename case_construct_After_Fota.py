# coding = utf8
from time import sleep

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException


os.path.abspath(".")

poco = AndroidUiautomationPoco()
austinDevice = connect_device("Android:///7c2440fd")

# Fota后的独立操作Case
# 将case进行分解->剔出通用common方法->将APP分页处理->case整合->架构完善

"""
    common 方法：上下滚动查找元素
"""


def scroll_to_find_element(element_text):
    menu_exists = False
    search_count = 0
    while not menu_exists:
        element = poco(text=element_text).wait()
        menu_exists = element.exists()
        if menu_exists:
            break
        poco.scroll(direction="vertical", percent=0.8, duration=1)
        search_count += 1
        # 给滑动查找增加向上滑动，兼容到底未找到的情况，即向下查找超过5次则开始向上查找
        if search_count >= 5 and not menu_exists:
            poco.scroll(direction="vertical", percent=-0.6, duration=1)
    return element

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
    # Tip：
    # 1.当有外部事件如短信、通知等打断当前操作，容易导致元素识别不到 -- 采取方式多次识别元素？
    # 2.权限分配 -- 使用adb命令进行全应用权限授权，不使用单独UI授权方式
    # 3.某些单独只会出现一次的元素，需要加上提前判断是否存在，存在再对其进行操作
    # 4.Case 17 移除animation的第一个执行，可以提升测试稳定性和测试效率
    # 5.测试使用本机号码收发拨号等，切记勿添加本机号码为联系人



















