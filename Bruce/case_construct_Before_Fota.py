# coding = utf8
import re
from time import sleep

from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException
from airtest.core.error import AdbShellError

os.path.abspath("..")
"""
    @File:case_construct_Before_Fota.py
    @Author:Bruce
    @Date:2020/12/15
"""

poco = AndroidUiautomationPoco()
austinDevice = connect_device("Android:///7c2440fd")
# austinDevice = connect_device("Android:///b3e5b958")

# Fota前操作&后对比Case
# 将case进行分解->剔出通用common方法->将APP分页处理->case整合->架构完善
# 状态更改需要先进行判断设置为除自身外其它状态,如默认checked = true，则设置为false，并记录前后状态以及Fota后状态

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
    common 方法2：启动chrome并跳过guide&引擎选择
"""


def launch_chrome_and_guide_skip():
    start_app("com.android.chrome")
    try:
        guide_first_button = poco("com.android.chrome:id/terms_accept").wait()
        if guide_first_button.exists():
            guide_first_button.click()
            poco("com.android.chrome:id/negative_button").wait().click()
    except PocoNoSuchNodeException:
        print("Chrome guide is finished!")
    finally:
        try:
            search_engine_choose = poco("com.android.chrome:id/button_secondary").wait()
            if search_engine_choose.exists():
                search_engine_choose.click()
        except PocoNoSuchNodeException:
            print("Search engine is finished!")
        finally:
            pass


"""
    common 方法3：chrome进入特定网址
"""


def chrome_enter_website(url="https://www.baidu.com"):
    launch_chrome_and_guide_skip()
    chrome_url_bar = poco("com.android.chrome:id/url_bar").wait()
    chrome_url_bar.click()
    chrome_url_bar.set_text(url)
    keyevent("KEYCODE_ENTER")


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


def check_sms_sender_receiver(number="18512026630", content="Test"):
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
        com.google.android.contacts
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
        检查APP存在->点击Settings->点击->点击AI scene detection更改状态
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
    # apps_menu = None
    # start_app("com.android.settings")
    # menu_exists = False
    # while not menu_exists:
    #     apps_menu = poco(text="Sound & vibration").wait()
    #     menu_exists = apps_menu.exists()
    #     if menu_exists:
    #         break
    #     poco.scroll(direction="vertical", percent=0.8, duration=1)
    # apps_menu.click()
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
    gesture_menu = scroll_to_find_element("Button & gestures")
    gesture_menu.click()
    poco(text="Gestures").wait(3).click()
    three_finger_screenshot = poco(text="3-finger screenshot").parent().parent().children()[2] \
        .child("com.android.settings:id/switchWidget").wait(3)
    checked_default = three_finger_screenshot.attr("checked")
    print(checked_default)
    three_finger_screenshot.click()
    three_finger_screenshot.invalidate()
    checked_changed = three_finger_screenshot.attr("checked")
    print(checked_changed)


"""
    Case 14:验证Security设置是否被保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->Security & biometrics->Screen lock->PIN->输入1234->Next->输入1234->Confirm->Done->
        记录默认、修改、升级后元素状态(invalidate进行元素刷新)
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def reenter_pin():
    stop_app("com.android.settings")
    start_app("com.android.settings")
    scroll_to_find_element("Security & biometrics").click()
    scroll_to_find_element("Screen lock").click()
    poco("com.android.settings:id/password_entry").wait().set_text("1234")
    poco(text="Next").wait().click()


def change_security_settings():
    stop_app("com.android.settings")
    start_app("com.android.settings")
    scroll_to_find_element("Security & biometrics").click()
    scroll_to_find_element("Screen lock").click()
    scroll_to_find_element("PIN").click()
    poco("com.android.settings:id/password_entry").wait().set_text("1234")
    poco(text="Next").wait().click()
    poco("com.android.settings:id/password_entry").wait().set_text("1234")
    poco(text="Confirm").wait().click()
    poco(text="Done").wait().click()

    reenter_pin()


"""
    Case 15:验证Lock设置是否被保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->Security & biometrics->SIM card lock->Lock SIM card->Click it switch->输入1234->OK->
        记录默认、修改、升级后元素状态(invalidate进行元素刷新)
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def change_lock_settings():
    start_app("com.android.settings")


"""
    Case 16:验证Sim management设置是否被保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->SIM cards & cellular network->SIM card settings->
        点击SIM1右边齿轮("com.tct.phone:id/settings_button")->修改SIM name("com.tct.phone:id/sim_name")->输入Test->点击OK
        记录默认、修改、升级后元素状态(invalidate进行元素刷新)
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def change_sim_management():
    start_app("com.android.settings")


"""
    Case 17:验证Accessibility设置是否被保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->Accessibility->Remove animations->CLick it->记录默认、修改、升级后元素状态(invalidate进行元素刷新)
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def change_accessibility_settings():
    start_app("com.android.settings")


"""
    Case 18:验证File manager文件是否被保留
    relate app:
        com.tcl.tct.filemanager
    test step:
        检查APP存在->File Manager->点击x("com.tcl.tct.filemanager:id/guide_close")
        ->Internal storage->more_menu("com.tcl.tct.filemanager:id/iv_bar_more")
        ->Create folder->输入Test("com.tcl.tct.filemanager:id/dialog_edit")->CREATE
        ->记录默认、修改、升级后元素状态(invalidate进行元素刷新)
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_file_manager_reserved():
    start_app("com.tcl.tct.filemanager")


"""
    Case 19:验证IMEI、CU升级前后一致
    relate app:
        com.android.settings
    test step:
        检查APP存在->拨号盘输入*#*#06#*#*(#需要转义所以是：*%23*%2306%23*%23*)
        ->记录SVN值->关闭当前APP
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_imei_cu():
    austinDevice.shell("am start -a android.intent.action.DIAL -d tel:*%23*%2306%23*%23*")
    try:
        value_returned = poco("android:id/message").wait().get_text()
        if "SVN" in value_returned:
            print(re.findall("IMEI1:(.*)", value_returned))
            poco(text="OK").wait().click()
    except PocoNoSuchNodeException:
        print("Can't find needed element, please check!")
    finally:
        current_app = austinDevice.get_top_activity()[0]
        stop_app(current_app)


"""
    Case 20:验证SVN升级前后一致
    relate app:
        com.google.android.dialer
    test step:
        检查APP存在->
        ->记录默认、修改、升级后元素状态(invalidate进行元素刷新)->拨号盘输入*#*#06#*#*(#需要转义所以是：*%23*%2306%23*%23*)
        ->记录SVN值->关闭当前APP
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_svn():
    # start_app("com.google.android.dialer")
    austinDevice.shell("am start -a android.intent.action.DIAL -d tel:*%23*%2306%23*%23*")
    try:
        value_returned = poco("android:id/message").wait().get_text()
        if "SVN" in value_returned:
            print("Current svn is:" + value_returned.split("SVN:")[1])
            poco(text="OK").wait().click()
    except PocoNoSuchNodeException:
        print("Can't find needed element, please check!")
    finally:
        current_app = austinDevice.get_top_activity()[0]
        stop_app(current_app)


"""
    Case 21:验证升级后WiFi AP自动连接,WiFi Direct name保留
    relate app:
        adb shell dumpsys netstats | grep -E 'iface=wlan.*networkId'
        com.android.settings
    test step:
        检查APP存在->
            case 1:打开Settings->Wi-Fi->打开WiFi->连接WiFi->保存当前连接WiFi名称      
            case 2:Wi-Fi preferences->Advanced->Wi-Fi Direct->menu->Rename device->Test->OK
            ->Fota upgrade
            ->adb指令获取当前连接的WiFi名称->与Fota前连接的WiFi名称对比
            ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_wifi_auto_connect_and_direct_name():
    # step 1: connect_wifi() -> save wifi name
    # step 2: modify_wifi_direct_name() -> save direct name
    # after fota
    # step 3: check wifi same as before
    # step 4: check wifi direct name same as before
    try:
        netstats = austinDevice.shell("dumpsys netstats | grep -E 'iface=wlan.*networkId'")
    except AdbShellError:
        print("Current WiFi is Empty, test item Failed!")
    else:
        if netstats is not None:
            wifi_name = netstats.split('networkId="')[1].split('",')[0]
            print(wifi_name)
        else:
            print("WiFi abnormal, please retest it")


"""
    Case 22:验证升级后热点配置可以保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->SIM cards & cellular network->Hotspot & tethering->Mobile hotspot
        ->Hotspot name->设置新热点名称为Test->OK->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_hotspot_config_reserved():
    start_app("com.android.settings")
    scroll_to_find_element("SIM cards & cellular network").wait().click()
    scroll_to_find_element("Hotspot & tethering").wait().click()
    scroll_to_find_element("Mobile hotspot").wait().click()
    scroll_to_find_element("Hotspot name").wait().click()
    poco("android:id/edit").wait().set_text("Test")
    poco(text="OK").wait().click()
    hotspot_name_changed = scroll_to_find_element("Hotspot name").sibling("android:id/summary").get_text()
    print(hotspot_name_changed)


"""
    Case 23:验证升级后Location配置可以保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->Location->Wi-Fi and Bluetooth scanning->获取Wi-Fi scanning的状态->Click Wi-Fi scanning
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_location_config_reserved():
    start_app("com.android.settings")
    scroll_to_find_element("Location").click()
    scroll_to_find_element("Wi-Fi and Bluetooth scanning").click()
    wifi_scan_status = scroll_to_find_element("Wi-Fi scanning").parent().sibling().child("android:id/switch_widget")
    default_wifi_scan_status = wifi_scan_status.attr("checked")
    print(default_wifi_scan_status)
    scroll_to_find_element("Wi-Fi scanning").wait().click()
    wifi_scan_status.invalidate()
    changed_wifi_scan_status = wifi_scan_status.attr("checked")
    print(changed_wifi_scan_status)


"""
    Case 24:验证升级后下载的文件和下载记录可以保留
    relate app:
        com.android.chrome
    test step:
        检查APP存在->Chrome->跳过向导界面->->跳过搜索引擎选择->点击输入网址->下载百度首页图片
        ->关闭下载提示框及info弹框->进入Downloads查看下载的文件->点击下载的图片->记录编号
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_download_file_and_history_reserved():
    try:
        launch_chrome_and_guide_skip()
        chrome_url_bar = poco("com.android.chrome:id/url_bar").wait()
        chrome_url_bar.click()
        chrome_url_bar.set_text("https://www.baidu.com")
        keyevent("KEYCODE_ENTER")
        print("Search finished!")
        poco(text="百度一下,你就知道").wait().long_click()
        poco(text="Download image").wait().click()
        try:
            popup_info = poco("com.android.chrome:id/infobar_close_button").wait()
            if popup_info.exists():
                popup_info.click()
        except PocoNoSuchNodeException:
            print("popup_info closed!")
        finally:
            try:
                download_again_info = poco("com.android.chrome:id/infobar_close_button").wait()
                if download_again_info.exists():
                    download_again_info.click()
            except PocoNoSuchNodeException:
                print("download_again_info closed!")
            finally:
                try:
                    poco("com.android.chrome:id/positive_button").wait().click()
                except PocoNoSuchNodeException:
                    print("Not first download,so no need click download start icon!")
                finally:
                    poco("com.android.chrome:id/menu_button").wait().click()
                    poco(text="Downloads").wait().click()
                    download_file = poco("com.android.chrome:id/thumbnail").wait()
                    download_file.click()
                    download_file_number = poco("com.android.chrome:id/title_bar").get_text()
                    print(download_file_number)
    except PocoNoSuchNodeException:
        print("Some error happened, stop chrome!")
    finally:
        current_app = austinDevice.get_top_activity()[0]
        stop_app(current_app)


"""
    Case 25:验证升级后保存的书签可以保留
    relate app:
        com.android.chrome
    test step:
        检查APP存在->Chrome->跳过向导界面->->跳过搜索引擎选择->点击输入网址->Menu->保存书签
        ->Menu->Bookmarks->Mobile bookmarks->点击进入对应书签网页->检查进入成功对应网页信息OK
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_bookmarks_reserved(url="https://www.baidu.com"):
    stop_app("com.android.chrome")
    chrome_enter_website(url)
    chrome_menu_button = poco("com.android.chrome:id/menu_button").wait()
    chrome_menu_button.click()
    poco("com.android.chrome:id/button_two").wait().click()
    try:
        if poco(text="Edit bookmark").wait().exists():
            keyevent("KEYCODE_BACK")
    except PocoNoSuchNodeException:
        print("Already saved bookmark!")
    finally:
        chrome_menu_button.click()
        poco(text="Bookmarks").wait().click()
        try:
            bookmark_item = poco(text="www.baidu.com").wait()
            bookmark_item.click()
            try:
                bookmark_item_ok = poco(text="百度一下,你就知道").wait().exists()
                print(bookmark_item_ok)
            except PocoNoSuchNodeException:
                print("添加书签不一致")
        except PocoNoSuchNodeException:
            print("Add bookmark failed")
        finally:
            pass


"""
    Case 27:验证升级后vpn配置可以保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->Connected devices->VPN->Create VPN->记录当前VPN名称->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_vpn_config_reserved():
    try:
        stop_app("com.android.settings")
        start_app("com.android.settings")
        scroll_to_find_element("Connected devices").click()
        scroll_to_find_element("VPN").click()
        create_apn = poco("com.android.settings:id/vpn_create").wait()
        create_apn.click()
        try:
            if poco(text="Attention").exists():
                pass
            # set a screen lock
        except PocoNoSuchNodeException:
            print("Screen lock has been set!")
        finally:
            pass
    except Exception:
        print("Some thing error, please check!")


# """
#     Case 28:验证升级后输入法设置可以保留
#     relate app:
#         com.android.settings
#     test step:
#         检查APP存在->
#         adb 设置输入法->adb获取当前输入法(脚本运行中会自动切换至Yosemite，此时判断之前存在即可)
#         ->Fota升级后再次获取该值与升级前对比是否相同判定结果
# """
#
#
# def check_input_method_reserved():
#     try:
#         # 需要先登录Google商店设置Play Protect->关闭Scan apps with Play Protect
#         # 以防止出现Blocked by Play Protect弹框占用top导致后续install apk以及元素获取失败
#         # disable_play_protect()
#         install("../apk/Sogouinput.apk")
#         default_input_method = shell("settings get secure default_input_method")
#         print(default_input_method)
#         shell("settings put secure default_input_method com.sohu.inputmethod.sogou/.SogouIME")
#         changed_input_method = shell("settings get secure default_input_method")
#         print(changed_input_method)
#     except Exception:
#         print("Some thing error, please check!")


"""
    Case 29:验证升级后Navigation bar设置可以保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->Button & gestures->System navigation->Switch to Gesture navigation
        ->记录当前navigation的状态
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_navigation_reserved():
    try:
        stop_app("com.android.settings")
        start_app("com.android.settings")
        scroll_to_find_element("Button & gestures").click()
        poco(text="System navigation").wait().click()
        navigation_gesture = poco(text="Gesture navigation").wait()
        navigation_gesture.click()
        navigation_gesture_switch = navigation_gesture.parent().sibling().child("android:id/checkbox").wait()
        print(navigation_gesture_switch.attr("checked"))

    except Exception:
        print("Some thing error, please check!")


"""
    Case 30:验证升级后Notch可以保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->Display->Status bar & notch->Notch
        ->Hide notch without moving status bar->Choose it
        ->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_notch_reserved():
    try:
        stop_app("com.android.settings")
        start_app("com.android.settings")
        scroll_to_find_element("Display").click()
        scroll_to_find_element("Status bar & notch").click()
        poco(text="Notch").wait().click()
        statusbar_hide = poco(text="Hide notch without moving status bar").wait()\
            .parent().sibling().child("com.android.settings:id/status_bar_btn2").wait()
        statusbar_hide.click()
        statusbar_hide.invalidate()
        print(statusbar_hide.attr("checked"))
    except Exception:
        print("Some thing error, please check!")


"""
    Case 31:验证升级后Screen recorder设置可以保留
    relate app:
        com.android.settings
    test step:
        检查APP存在->->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_screenrecorder_reserved():
    try:
        stop_app("com.android.settings")
        start_app("com.android.settings")
        scroll_to_find_element("Advanced features").click()
        poco(text="Screen Recorder").wait().click()
        record_interactions = poco(text="Record touch interactions").wait()
        record_interactions_switch = record_interactions.parent().sibling().child("android:id/switch_widget").wait()
        record_interactions_switch.click()
        record_interactions_switch.invalidate()
        print(record_interactions_switch.attr("checked"))
    except Exception:
        print("Some thing error, please check!")


"""
    Case 32:验证升级后SW version显示完整并与期望值一致
    relate app:
        com.android.settings
    test step:
        检查APP存在->Settings->System->About phone->
        定位到软件版本号->记录
        ->Fota升级后再次获取该值应该与Fota前版本不同，与Fota后当前测试的版本相同
"""


def check_sw_version_reserved():
    try:
        stop_app("com.android.settings")
        start_app("com.android.settings")
        scroll_to_find_element("System").click()
        scroll_to_find_element("About phone").click()
        sw_version = poco("com.android.settings:id/recycler_view").wait().children()[0].child("android:id/title").wait()
        print(sw_version.get_text())
    except Exception:
        print("Some thing error, please check!")


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
    # test  后续列表操作需要使用上下滑动进行查找元素保证兼容性
    # Tip：
    # 1.当有外部事件如短信、通知等打断当前操作，容易导致元素识别不到 -- 采取方式多次识别元素？
    # 2.权限分配 -- 使用adb命令进行全应用权限授权，不使用单独UI授权方式
    # 3.某些单独只会出现一次的元素，需要加上提前判断是否存在，存在再对其进行操作
    # 4.Case 17 移除animation的第一个执行，可以提升测试稳定性和测试效率
    # 5.测试使用本机号码收发拨号等，切记勿添加本机号码为联系人
    # 6.Case测试前先关闭当前应用程序
    # 7.设置手机usb stay awake
    # test
    check_imei_cu()
