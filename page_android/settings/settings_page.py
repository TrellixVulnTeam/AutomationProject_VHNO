# coding = utf8
import os
import sys

from airtest.core.error import AdbShellError
from poco.exceptions import PocoNoSuchNodeException

from page_android.system.system import System
from time import sleep
from toolsbar.excel_tools import read_excel_for_page_element

os.path.abspath(".")
"""
    @File:settings_page.py
    @Author:Bruce
    @Date:2021/1/14
    @Description:Settings page_android，控制设备Settings应用的函数、控件
    @param:继承System，传入Main_Page实例完成设备Device、Poco初始化
"""


# 该函数用于简化元素获取操作
def get_element_parametrize(element_name="guide_page_text"):
    form_name = "./page_android/page_sheet.xlsx"
    element_data = read_excel_for_page_element(form=form_name, sheet_name="settings_page",
                                               element_name=element_name)
    return element_data


class Settings_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.sound_vibration = get_element_parametrize("sound_vibration")
        self.button_gesture = get_element_parametrize("button_gesture")
        self.security_biometrics = get_element_parametrize("security_biometrics")
        self.simcard_cellularnetwork = get_element_parametrize("simcard_cellularnetwork")
        self.accessibility = get_element_parametrize("accessibility")
        self.wifi = get_element_parametrize("wifi")
        self.location = get_element_parametrize("location")
        self.connected_devices = get_element_parametrize("connected_devices")
        self.display = get_element_parametrize("display")
        self.advanced_features = get_element_parametrize("advanced_features")
        self.simcard_settings = self.poco(text=get_element_parametrize("simcard_settings"))
        self.simcard_settings_icon = self.poco(get_element_parametrize("simcard_settings_icon"))
        self.sound_vibration_silent_mode_text = self.poco(
            text=get_element_parametrize("sound_vibration_silent_mode_text"))
        self.display_sleep = self.poco(text=get_element_parametrize("display_sleep"))
        self.display_sleep_never = self.poco(text=get_element_parametrize("display_sleep_never"))
        self.button_gestures_gestures = self.poco(text=get_element_parametrize("button_gestures_gestures"))
        self.button_gestures_gestures_3_finger_screenshot = self.poco(
            text=get_element_parametrize("button_gestures_gestures_3_finger_screenshot"))
        self.security_sim_card_lock_text = get_element_parametrize("security_sim_card_lock_text")
        self.security_sim_card_lock_locksimcard_text = self.poco(
            text=get_element_parametrize("security_sim_card_lock_locksimcard_text"))
        self.imei = self.poco(get_element_parametrize("imei"))
        self.cu = self.poco(get_element_parametrize("cu"))
        self.hotspot_tethering = self.poco(text=get_element_parametrize("hotspot_tethering"))
        self.mobile_hotspot = self.poco(text=get_element_parametrize("mobile_hotspot"))
        self.hotspot_name = self.poco(text=get_element_parametrize("hotspot_name"))
        self.vpn = self.poco(text=get_element_parametrize("vpn"))
        self.vpn_create = self.poco(get_element_parametrize("vpn_create"))
        self.display_statusbar_notch = self.poco(text=get_element_parametrize("display_statusbar_notch"))
        self.notch = self.poco(text=get_element_parametrize("notch"))
        self.advanced_features_screenrecorder = self.poco(
            text=get_element_parametrize("advanced_features_screenrecorder"))

    """
        @description:启动settings应用
    """

    def start_settings(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动settings app:")
        self.device.start_app("com.android.settings")
        sleep(1)

    """
        @description:关闭settings应用
    """

    def stop_settings(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭settings app:")
        sleep(1)
        self.device.stop_app("com.android.settings")

    """
        @description:进入Accessibility应用
    """

    def enter_accessibility(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Accessibility界面:")
            accessibility = self.scroll_to_find_element(element_text=self.accessibility)
            self.double_click_element(element_item=accessibility)
        except Exception as ex:
            self.logger.error(
                "function:" + sys._getframe().f_code.co_name + ":进入Accessibility界面出现问题:" + str(ex))

    """
        @description:更改Remove animations状态
    """

    def change_animations_status(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":更改remove animation状态:")
            remove_animation = self.scroll_to_find_element(element_text="Remove animations")
            remove_animation_switch = remove_animation.parent().sibling().child("android:id/switch_widget")
            remove_animation_switch.click()
            remove_animation_switch.invalidate()
            result = "Remove animations" + ":" + str(remove_animation_switch.attr("checked"))
        except Exception as ex:
            self.logger.error(
                "function:" + sys._getframe().f_code.co_name + ":更改remove animation状态出现问题:" + str(ex))
        return result

    """
        @description:进入SIM card & cellular network
    """

    def enter_simcard_cellular(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入SIM card & cellular network界面:")
            simcard_cellular = self.scroll_to_find_element(element_text=self.simcard_cellularnetwork)
            self.double_click_element(element_item=simcard_cellular)
        except Exception as ex:
            self.logger.error(
                "function:" + sys._getframe().f_code.co_name + ":进入SIM card & cellular network界面出现问题:" + str(ex))

    """
        @description:更改simcard名称
    """

    def change_simcard_name(self, name="Test"):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":更改sim card name:")
            self.simcard_settings.wait().click()
            self.simcard_settings_icon.wait().click()
            self.poco("com.tct.phone:id/sim_name").wait().set_text(name)
            self.poco(text="OK").wait().click()
            result = "SIM card Name" + ":" + self.poco(text=name).wait().get_text()
        except Exception as ex:
            self.logger.error(
                "function:" + sys._getframe().f_code.co_name + ":更改sim card name出现问题:" + str(ex))
        return result

    """
        @description:进入Security
    """

    def enter_security(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Security & biometrics界面:")
            security_biometrics = self.scroll_to_find_element(element_text=self.security_biometrics)
            self.double_click_element(element_item=security_biometrics)
        except Exception as ex:
            self.logger.error(
                "function:" + sys._getframe().f_code.co_name + ":进入Security & biometrics界面出现问题:" + str(ex))

    """
        @description:更改SIM card lock状态
    """

    def change_sim_card_lock_status(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":修改sim card lock状态:")
            self.scroll_to_find_element(element_text=self.security_sim_card_lock_text).click()
            lock_sim_card = self.security_sim_card_lock_locksimcard_text.wait()
            sleep(1)
            lock_sim_card_switch = lock_sim_card.parent().parent().children()[1].child("android:id/switch_widget")
            sleep(1)
            lock_sim_card_switch.click()
            self.poco("android:id/edit").wait().set_text("1234")
            self.poco(text="OK").wait().click()
            lock_sim_card_switch.invalidate()
            result = lock_sim_card.get_text() + ":" + str(lock_sim_card_switch.attr("checked"))
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":修改sim card lock状态出现问题:" + str(ex))
        return result

    """
        @description:设置屏幕锁
    """

    def set_screen_lock(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":设置屏幕锁1234:")
        self.poco(text="Screen lock").wait().click()
        result = ""
        try:
            if self.poco(text="Confirm your PIN").wait().exists():
                self.logger.warning("function:" + sys._getframe().f_code.co_name + ":当前屏幕锁已存在:")
                result = "Screen lock:exists"
            else:
                self.poco(text="PIN").wait().click()
                self.poco("com.android.settings:id/password_entry").wait().set_text("1234")
                sleep(0.5)
                self.poco(text="Next").wait().click()
                self.poco("com.android.settings:id/password_entry").wait().set_text("1234")
                sleep(0.5)
                self.poco(text="Confirm").wait().click()
                self.poco(text="Done").wait().click()
                result = "Screen lock:PIN"
        except PocoNoSuchNodeException as ex:
            self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                ":屏幕锁不存在,所以设置一个屏幕锁:" + str(ex))
        return result

    """
        @description:清除屏幕锁
    """

    def clear_screen_lock(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":清除屏幕锁:")
        security = self.scroll_to_find_element(element_text="Security & biometrics")
        security.click()
        self.poco(text="Screen lock").wait().click()
        self.poco("com.android.settings:id/password_entry").wait().set_text("1234")
        sleep(0.5)
        self.poco(text="Next").wait().click()
        self.poco(text="Swipe").wait().click()
        self.poco(text="YES, REMOVE").wait().click()

    """
        @description:获取设备IMEI & CU
    """

    def get_imei_cu(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取设备IMEI&CU:")
            self.device.shell("am start -a android.intent.action.DIAL -d tel:*%2307%23")
            imei = self.imei.wait().get_text().replace("\n", ",")
            cu = self.cu.wait().get_text()
            result = "IMEI:{}, CU:{}".format(imei, cu)
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":获取设备IMEI&CU出现问题:" + str(ex))
        return result

    """
        @description:获取设备当前连接的WI-FI名称
    """

    def get_current_wifi_name(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取当前wifi名称:")
            global wifi_name
            try:
                netstats = self.device.shell("dumpsys netstats | grep -E 'iface=wlan.*networkId'")
            except AdbShellError as ex:
                self.logger.error("function:" + sys._getframe().f_code.co_name +
                                  ":当前未连接wifi,请确认成功连接后再进行测试:" + str(ex))
            else:
                if netstats is not None:
                    wifi_name = netstats.split('networkId="')[1].split('",')[0]
                else:
                    print("WiFi connection is abnormal, please check it")
                    self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                        ":当前Wifi连接异常,请检查:")
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":获取当前wifi名称出现问题:" + str(ex))
        return wifi_name

    """
        @description:开启Wi-Fi
    """

    def enable_wifi(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":开启wifi:")
        self.device.shell("svc wifi enable")

    """
        @description:关闭Wi-Fi
    """

    def disable_wifi(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭wifi:")
        self.device.shell("svc wifi disable")

    """
        @description:进入Wi-Fi
    """

    def enter_wifi(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Wi-Fi界面:")
            wifi = self.scroll_to_find_element(element_text=self.wifi)
            self.double_click_element(element_item=wifi)
        except Exception as ex:
            self.logger.error(
                "function:" + sys._getframe().f_code.co_name + ":进入Wi-Fi界面出现问题:" + str(ex))

    """
        @description:连接Wi-Fi
        @param:
            wifi_name:Wi-Fi名称
            wifi_password:Wi-Fi密码
    """

    def connect_wifi(self, wifi_name="AutomationTest", wifi_password="cgt19981002"):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name +
                             ":连接wifi,name:{},password:{}:".format(wifi_name, wifi_password))
            global current_wifi
            try:
                current_connected_wifi = self.poco(text="Connected").wait()
                current_connected_wifi.click()
                self.poco(text="FORGET").wait().click()
            except PocoNoSuchNodeException as ex:
                self.logger.warning(
                    "function:" + sys._getframe().f_code.co_name + ":当前无Wifi连接:" + str(ex))
            wifi_item = self.scroll_to_find_element(element_text=wifi_name)
            wifi_item.click()
            self.poco("com.android.settings:id/password").wait().set_text(wifi_password)
            connect_button = self.poco(text="Connect").wait()
            connect_button.click()
            sleep(5)
            while True:
                current_wifi = self.get_current_wifi_name()
                if current_wifi is not None:
                    self.logger.info(
                        "function:" + sys._getframe().f_code.co_name + ":当前连接的wifi为{}:".format(current_wifi))
                    result = "Connected WiFi" + ":" + current_wifi
                    break
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name +
                              ":连接wifi,name:{},password:{}出现问题:".format(wifi_name, wifi_password) + str(ex))
        return result

    """
        @description:忘记Wi-Fi
        @param:
            wifi_name:Wi-Fi名称
    """

    def forget_wifi(self, wifi_name="A_Test"):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":忘记该wifi:{}:".format(wifi_name))
        wifi = self.scroll_to_find_element(element_text="Wi-Fi")
        wifi.click()
        wifi_item = self.scroll_to_find_element(element_text=wifi_name)
        wifi_item.click()
        self.poco(text="FORGET").wait().click()

    """
        @description:设置Wi-Fi Direct名称
        @param:
            new_name:新名称
    """

    def set_wifi_direct_name(self, new_name="Test"):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":设置wifi direct name为:{}:".format(new_name))
        wifi = self.scroll_to_find_element(element_text="Wi-Fi")
        wifi.click()
        wifi_preference = self.scroll_to_find_element(element_text="Wi-Fi preferences")
        wifi_preference.click()
        self.poco(text="Advanced").wait().click()
        self.poco(text="Wi-Fi Direct").wait().click()
        self.poco("com.android.settings:id/action_bar").wait().children()[2].children()[1].click()
        self.poco(text="Rename device").wait().click()
        self.poco("com.android.settings:id/edittext").wait().set_text(new_name)
        self.poco(text="OK").wait().click()
        return new_name

    """
        @description:获取当前Wi-Fi Direct名称
    """

    def get_wifi_direct_name(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取wifi direct name:")
        wifi = self.scroll_to_find_element(element_text="Wi-Fi")
        wifi.click()
        wifi_preference = self.scroll_to_find_element(element_text="Wi-Fi preferences")
        wifi_preference.click()
        self.poco(text="Advanced").wait().click()
        self.poco(text="Wi-Fi Direct").wait().click()
        direct_name = self.poco("com.android.settings:id/preference_content").wait().child().child().get_text()
        return direct_name

    """
        @description:设置Hotspot名称
        @param:
            name:名称
    """

    def set_hotspot_name(self, name="Test"):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":设置wifi hotspot name为:{}:".format(name))
            self.hotspot_tethering.wait().click()
            self.mobile_hotspot.wait().click()
            self.hotspot_name.wait().click()
            self.poco("android:id/edit").wait().set_text(name)
            self.poco(text="OK").wait().click()
            hotspot_name_changed = self.poco(text="Hotspot name").sibling("android:id/summary").get_text()
            result = "New Hotspot Name" + ":" + hotspot_name_changed
        except Exception as ex:
            self.logger.info(
                "function:" + sys._getframe().f_code.co_name + ":设置wifi hotspot name为:{}出现问题:".format(name) + str(ex))
        return result

    """
        @description:进入Location
    """

    def enter_location(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Location界面:")
            location = self.scroll_to_find_element(element_text=self.location)
            self.double_click_element(element_item=location)
        except Exception as ex:
            self.logger.error(
                "function:" + sys._getframe().f_code.co_name + ":进入Location界面出现问题:" + str(ex))

    """
        @description:更改Location设置
    """

    def change_location_settings(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":改变定位功能设置:")
            wifi_bt_scanning = self.scroll_to_find_element(element_text="Wi-Fi and Bluetooth scanning")
            wifi_bt_scanning.click()
            wifi_scanning = self.scroll_to_find_element(element_text="Wi-Fi scanning")
            wifi_scanning.click()
            wifi_scan_switch = wifi_scanning.parent().sibling().child("android:id/switch_widget")
            wifi_scan_switch.invalidate()
            result = "Wi-Fi scanning status" + ":" + str(wifi_scan_switch.attr("checked"))
        except Exception as ex:
            self.logger.error(
                "function:" + sys._getframe().f_code.co_name + ":改变定位功能设置出现问题:" + str(ex))
        return result

    """
        @description:进入Connected devices
    """

    def enter_connected_devices(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Connected Devices界面:")
            connected_devices = self.scroll_to_find_element(element_text=self.connected_devices)
            self.double_click_element(element_item=connected_devices)
        except Exception as ex:
            self.logger.error(
                "function:" + sys._getframe().f_code.co_name + ":进入Connected Devices界面出现问题:" + str(ex))

    """
        @description:设置VPN
        @param:
            name:vpn名称
            address:vpn地址
    """

    def set_vpn(self, name="Test", address="Test"):
        # Before set vpn, you need set a screen lock first
        result = ""
        try:
            self.logger.info(
                "function:" + sys._getframe().f_code.co_name + ":设置vpn,name:{},address:{}:".format(name, address))
            self.vpn.wait().click()
            self.vpn_create.wait().click()
            self.poco("com.android.settings:id/name").wait().set_text(name)
            self.poco("com.android.settings:id/server").wait().set_text(address)
            sleep(0.5)
            self.poco(text="SAVE").wait().click()
            result = "New VPN Name" + ":" + self.poco(text=name).wait().get_text()
        except Exception as ex:
            self.logger.error(
                "function:" + sys._getframe().f_code.co_name + ":设置vpn,name:{},address:{}出现问题:".format(name,
                                                                                                       address) + str(
                    ex))
        return result

    """
        @description:获取设备数据使用情况
    """

    def get_data_usage(self):
        # First：close wifi， enter website，then get data usage
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取手机date usage:")
        sim_card_cellular_menu = self.scroll_to_find_element(self.main_page,
                                                             element_text="SIM card & cellular network")
        self.double_click_element(sim_card_cellular_menu)
        data_usage = self.poco(text="Data usage").wait().sibling("android:id/summary").get_text()
        return data_usage

    """
        @description:进入Button & gestures
    """

    def enter_button_gestures(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Button & gestures界面:")
            button_gestures = self.scroll_to_find_element(element_text=self.button_gesture)
            self.double_click_element(element_item=button_gestures)
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":进入Button & gestures界面出现问题:" + str(ex))

    """
        @description:设置Navigation为Gesture
    """

    def set_navigation_gesture(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":设置navigation gesture:")
            self.poco(text="System navigation").wait().click()
            navigation_gesture = self.poco(text="Gesture navigation").wait()
            navigation_gesture.click()
            navigation_gesture_switch = navigation_gesture.parent().sibling().child("android:id/checkbox").wait()
            result = navigation_gesture.get_text() + ":" + str(navigation_gesture_switch.attr("checked"))
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":设置navigation gesture出现问题:" + str(ex))
        return result

    """
        @description:获取当前Navigation样式
    """

    def get_current_navigation(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取当前导航手势类型:")
        global current_navigation
        self.poco(text="System navigation").wait().click()
        # 通过元素遍历并返回被选中的元素
        checked_box = self.get_checked_element(element_id="com.android.settings:id/recycler_view")
        current_navigation = checked_box.parent().sibling().child("android:id/title")
        current_navigation_title = current_navigation.get_text()
        return current_navigation_title

    """
        @description:进入Sound & vibration
    """

    def enter_sound_vibration(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Sound & vibration界面:")
            sound_vibration = self.scroll_to_find_element(element_text=self.sound_vibration)
            self.double_click_element(element_item=sound_vibration)
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":进入Sound & vibration界面出现问题:" + str(ex))

    """
        @description:更改Silent mode
    """

    def change_silent_mode(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":更改silent mode状态:")
            silent_mode_t = self.sound_vibration_silent_mode_text.wait()
            silent_mode_t.click()
            silent_mode_s = silent_mode_t.parent().sibling().child(
                "android:id/switch_widget").wait()
            silent_mode_s.invalidate()
            result = silent_mode_t.get_text() + ":" + str(silent_mode_s.attr("checked"))
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":更改silent mode状态出现问题:" + str(ex))
        return result

    """
        @description:更改屏幕亮度 & 休眠模式
    """

    def change_brightness_sleep_mode(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":更改Brightness&Sleep状态:")
            self.device.shell("settings put system screen_brightness 999999")
            self.device.shell("settings put system screen_off_timeout 1")
            result = "Brightness:100% & Sleep:Never"
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":更改Brightness&Sleep状态出现问题:" + str(ex))
        return result

    """
        @description:进入Display
    """

    def enter_display(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Display界面:")
            display = self.scroll_to_find_element(element_text=self.display)
            self.double_click_element(element_item=display)
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":进入Sound & vibration界面出现问题:" + str(ex))

    """
        @description:更改Notch样式
    """

    def change_notch_style(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":更改Notch风格:")
            self.display_statusbar_notch.wait().click()
            self.notch.wait().click()
            statusbar_hide_title = self.poco(text="Hide notch without moving status bar").wait()
            statusbar_hide_switch = statusbar_hide_title.parent().sibling().child(
                "com.android.settings:id/status_bar_btn2").wait()
            statusbar_hide_switch.click()
            statusbar_hide_switch.invalidate()
            result = "Notch Style" + ":" + str(statusbar_hide_switch.attr("checked"))
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":更改Notch风格出现问题:" + str(ex))
        return result

    """
        @description:进入Advanced features
    """

    def enter_advanced_features(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入Advanced features界面:")
            advanced_features = self.scroll_to_find_element(element_text=self.advanced_features)
            self.double_click_element(element_item=advanced_features)
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":进入Advanced features界面出现问题:" + str(ex))

    """
        @description:更改Screenrecorder设置
    """

    def change_screenrecorder_settings(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":更改screen recorder设置:")
            self.advanced_features_screenrecorder.wait().click()
            record_interactions_title = self.poco(text="Record touch interactions").wait()
            record_interactions_switch = record_interactions_title.parent().sibling().child(
                "android:id/switch_widget").wait()
            record_interactions_switch.click()
            record_interactions_switch.invalidate()
            result = "Screenrecorder touch interactions" + ":" + str(record_interactions_switch.attr("checked"))
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":更改screen recorder设置出现问题:" + str(ex))
        return result
