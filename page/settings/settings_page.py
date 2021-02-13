# coding = utf8
import os
from time import sleep

from airtest.core.error import AdbShellError
from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System

os.path.abspath(".")
"""
    @File:settings_page.py
    @Author:Bruce
    @Date:2021/1/14
"""


class Settings_Page(System):

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.sound_vibration_silent_mode_text = self.poco(text="Silent mode")
        self.display_sleep = self.poco(text="Sleep")
        self.display_sleep_never = self.poco(text="Never")
        self.button_gestures_gestures = self.poco(text="Gestures")
        self.button_gestures_gestures_3_finger_screenshot = self.poco(text="3-finger screenshot")
        self.security_sim_card_lock_locksimcard_text = self.poco(text="Lock SIM card")

    def start_settings(self):
        self.device.start_app("com.android.settings")
        sleep(1)

    def stop_settings(self):
        sleep(1)
        self.device.stop_app("com.android.settings")

    def set_screen_lock(self):
        self.start_settings()
        security = self.scroll_to_find_element(element_text="Security & biometrics")
        self.double_click_element(security)
        self.poco(text="Screen lock").wait().click()
        try:
            if self.poco(text="Confirm your PIN").wait().exists():
                print("Screen lock exists")
            else:
                self.poco(text="PIN").wait().click()
                self.poco("com.android.settings:id/password_entry").wait().set_text("1234")
                sleep(0.5)
                self.poco(text="Next").wait().click()
                self.poco("com.android.settings:id/password_entry").wait().set_text("1234")
                sleep(0.5)
                self.poco(text="Confirm").wait().click()
                self.poco(text="Done").wait().click()
        except PocoNoSuchNodeException:
            print("Screen lock not exists, so set a screen lock:")
        finally:
            self.stop_settings()
        return "Screen lock OK"

    def clear_screen_lock(self):
        self.start_settings()
        security = self.scroll_to_find_element(element_text="Security & biometrics")
        security.click()
        self.poco(text="Screen lock").wait().click()
        self.poco("com.android.settings:id/password_entry").wait().set_text("1234")
        sleep(0.5)
        self.poco(text="Next").wait().click()
        self.poco(text="Swipe").wait().click()
        self.poco(text="YES, REMOVE").wait().click()
        self.stop_settings()

    def get_imei_cu(self):
        self.start_settings()
        system = self.scroll_to_find_element(element_text="System")
        system.click()
        self.poco(text="Regulatory & safety").wait().click()
        imei = self.poco("com.jrdcom.Elabel:id/imei").wait().get_text()
        cu = self.poco("com.jrdcom.Elabel:id/cu_reference_id_view").wait().get_text()
        self.stop_settings()
        return cu, imei

    def get_current_wifi_name(self):
        global wifi_name
        try:
            netstats = self.device.shell("dumpsys netstats | grep -E 'iface=wlan.*networkId'")
        except AdbShellError:
            print("Current WiFi is Empty, test item Failed!")
        else:
            if netstats is not None:
                wifi_name = netstats.split('networkId="')[1].split('",')[0]
                print(wifi_name)
            else:
                print("WiFi connection is abnormal, please check it")
        return wifi_name

    def enable_wifi(self):
        self.device.shell("svc wifi enable")

    def disable_wifi(self):
        self.device.shell("svc wifi disable")

    def connect_wifi(self, wifi_name="A_Test", wifi_password="88888888"):
        global current_wifi
        self.enable_wifi()
        self.start_settings()
        wifi = self.scroll_to_find_element(element_text="Wi-Fi")
        wifi.click()
        wifi_item = self.scroll_to_find_element(element_text=wifi_name)
        wifi_item.click()
        self.poco("com.android.settings:id/password").wait().set_text(wifi_password)
        connect_button = self.poco(text="Connect").wait()
        connect_button.click()
        while True:
            current_wifi = self.get_current_wifi_name()
            if current_wifi is not None:
                print("Current Wifi is {}".format(current_wifi))
                break
        self.stop_settings()
        return current_wifi

    def forget_wifi(self, wifi_name="A_Test"):
        self.enable_wifi()
        self.start_settings()
        wifi = self.scroll_to_find_element(element_text="Wi-Fi")
        wifi.click()
        wifi_item = self.scroll_to_find_element(element_text=wifi_name)
        wifi_item.click()
        self.poco(text="FORGET").wait().click()
        self.stop_settings()

    def set_wifi_direct_name(self, new_name="Test"):
        self.start_settings()
        self.enable_wifi()
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
        self.stop_settings()
        return new_name

    def get_wifi_direct_name(self):
        self.start_settings()
        self.enable_wifi()
        wifi = self.scroll_to_find_element(element_text="Wi-Fi")
        wifi.click()
        wifi_preference = self.scroll_to_find_element(element_text="Wi-Fi preferences")
        wifi_preference.click()
        self.poco(text="Advanced").wait().click()
        self.poco(text="Wi-Fi Direct").wait().click()
        direct_name = self.poco("com.android.settings:id/preference_content").wait().child().child().get_text()
        self.stop_settings()
        return direct_name

    def set_hotspot_name(self, name="Test"):
        self.start_settings()
        sim_cards_menu = self.scroll_to_find_element(element_text="SIM card & cellular network")
        sim_cards_menu.click()
        self.poco(text="Hotspot & tethering").wait().click()
        self.poco(text="Mobile hotspot").wait().click()
        self.poco(text="Hotspot name").wait().click()
        self.poco("android:id/edit").wait().set_text(name)
        self.poco(text="OK").wait().click()
        hotspot_name_changed = self.poco(text="Hotspot name").sibling("android:id/summary").get_text()
        self.stop_settings()
        return hotspot_name_changed

    def change_location_settings(self):
        self.start_settings()
        location = self.scroll_to_find_element(element_text="Location")
        self.double_click_element(location)
        wifi_bt_scanning = self.scroll_to_find_element(element_text="Wi-Fi and Bluetooth scanning")
        wifi_bt_scanning.click()
        wifi_scanning = self.scroll_to_find_element(element_text="Wi-Fi scanning")
        wifi_scanning.click()
        wifi_scan_status = wifi_scanning.parent().sibling().child("android:id/switch_widget")
        wifi_scan_status.invalidate()
        current_wifi_scanning_status = wifi_scan_status.attr("checked")
        self.stop_settings()
        return current_wifi_scanning_status

    def set_vpn(self, name="Test", address="Test"):
        # Before set vpn, you need set a screen lock first
        self.start_settings()
        connected_devices = self.scroll_to_find_element(element_text="Connected devices")
        self.double_click_element(connected_devices)
        self.poco(text="VPN").wait().click()
        self.poco("com.android.settings:id/vpn_create").wait().click()
        self.poco("com.android.settings:id/name").wait().set_text(name)
        self.poco("com.android.settings:id/server").wait().set_text(address)
        sleep(0.5)
        self.poco(text="SAVE").wait().click()
        return name

    def get_data_usage(self):
        # First：close wifi， enter website，then get data usage
        self.start_settings()
        sim_card_cellular_menu = self.scroll_to_find_element(self.main_page,
                                                               element_text="SIM card & cellular network")
        self.double_click_element(sim_card_cellular_menu)
        data_usage = self.poco(text="Data usage").wait().sibling("android:id/summary").get_text()
        self.stop_settings()
        return data_usage

    def set_navigation_gesture(self):
        self.start_settings()
        button_gestures = self.scroll_to_find_element(element_text="Button & gestures")
        self.double_click_element(button_gestures)
        self.poco(text="System navigation").wait().click()
        navigation_gesture = self.poco(text="Gesture navigation").wait()
        navigation_gesture.click()
        navigation_gesture_switch = navigation_gesture.parent().sibling().child("android:id/checkbox").wait()
        self.stop_settings()
        return navigation_gesture_switch.attr("checked")

    def get_current_navigation(self):
        global current_navigation
        self.start_settings()
        button_gestures = self.scroll_to_find_element(element_text="Button & gestures")
        self.double_click_element(button_gestures)
        self.poco(text="System navigation").wait().click()
        # 指定元素遍历并返回
        checked_box = self.poco("com.android.settings:id/recycler_view").wait().offspring(checked=True)
        current_navigation = checked_box.parent().sibling().child("android:id/title")
        current_navigation_title = current_navigation.get_text()
        self.stop_settings()
        return current_navigation_title
