# coding = utf8
import os
from time import sleep

from airtest.core.error import AdbShellError

from page.system.system import System

os.path.abspath(".")
"""
    @File:settings_page.py
    @Author:Bruce
    @Date:2021/1/14
"""


class Settings_Page:

    def __init__(self, main_page):
        self.main_page = main_page
        self.device = main_page.device
        self.poco = main_page.poco
        self.sound_vibration_silent_mode_text = self.poco(text="Silent mode")
        self.display_sleep = self.poco(text="Sleep")
        self.display_sleep_never = self.poco(text="Never")
        self.button_gestures_gestures = self.poco(text="Gestures")
        self.button_gestures_gestures_3_finger_screenshot = self.poco(text="3-finger screenshot")
        self.security_sim_card_lock_locksimcard_text = self.poco(text="Lock SIM card")
        self.sim_card_settings = self.poco(text="SIM card settings")
        self.sim_card_settings_sim1_settings = self.poco("com.tct.phone:id/settings_button")
        self.sim_card_settings_sim1_settings_sim_name = self.poco("com.tct.phone:id/sim_name")
        self.sim_card_settings_sim1_settings_sim_name_ok = self.poco(text="OK")

    def start_settings(self):
        self.device.start_app("com.android.settings")
        sleep(1)

    def stop_settings(self):
        sleep(1)
        self.device.stop_app("com.android.settings")

    def set_screen_lock(self):
        self.start_settings()
        System.scroll_to_find_element(self.main_page, element_text="Security & biometrics").click()
        self.poco(text="Screen lock").wait().click()
        self.poco(text="PIN").wait().click()
        self.poco("com.android.settings:id/password_entry").wait().set_text("1234")
        sleep(0.5)
        self.poco(text="Next").wait().click()
        self.poco("com.android.settings:id/password_entry").wait().set_text("1234")
        sleep(0.5)
        self.poco(text="Confirm").wait().click()
        self.poco(text="Done").wait().click()
        self.stop_settings()

    def clear_screen_lock(self):
        self.start_settings()
        System.scroll_to_find_element(self.main_page, element_text="Security & biometrics").click()
        self.poco(text="Screen lock").wait().click()
        self.poco("com.android.settings:id/password_entry").wait().set_text("1234")
        sleep(0.5)
        self.poco(text="Next").wait().click()
        self.poco(text="Swipe").wait().click()
        self.poco(text="YES, REMOVE").wait().click()
        self.stop_settings()

    def get_imei_cu(self):
        self.start_settings()
        System.scroll_to_find_element(self.main_page, element_text="System").click()
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

    def connect_wifi(self, wifi_name="Test", wifi_password="88888888"):
        global current_wifi
        self.enable_wifi()
        self.start_settings()
        System.scroll_to_find_element(self.main_page, element_text="Wi-Fi").click()
        sleep(0.5)
        System.scroll_to_find_element(self.main_page, element_text=wifi_name).click()
        sleep(0.5)
        self.poco("com.android.settings:id/password").wait().set_text(wifi_password)
        sleep(0.5)
        connect_button = self.poco(text="Connect").wait()
        connect_button.click()
        while True:
            current_wifi = self.get_current_wifi_name()
            if current_wifi is not None:
                print("Current Wifi is {}".format(current_wifi))
                break
        self.stop_settings()
        return current_wifi

    def forget_wifi(self, wifi_name="Test"):
        self.enable_wifi()
        self.start_settings()
        System.scroll_to_find_element(self.main_page, element_text="Wi-Fi").click()
        sleep(0.5)
        System.scroll_to_find_element(self.main_page, element_text=wifi_name).click()
        sleep(0.5)
        self.poco(text="FORGET").wait().click()
        self.stop_settings()

    def set_wifi_direct_name(self, new_name="Test"):
        self.start_settings()
        self.enable_wifi()
        System.scroll_to_find_element(self.main_page, element_text="Wi-Fi").click()
        sleep(0.5)
        System.scroll_to_find_element(self.main_page, element_text="Wi-Fi preferences").click()
        sleep(0.5)
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
        System.scroll_to_find_element(self.main_page, element_text="Wi-Fi").click()
        sleep(0.5)
        System.scroll_to_find_element(self.main_page, element_text="Wi-Fi preferences").click()
        sleep(0.5)
        self.poco(text="Advanced").wait().click()
        self.poco(text="Wi-Fi Direct").wait().click()
        direct_name = self.poco("com.android.settings:id/preference_content").wait().child().child().get_text()
        self.stop_settings()
        return direct_name
