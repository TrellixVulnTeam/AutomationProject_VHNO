# coding = utf8
import os
import sys

import allure
import pytest
from airtest.core.api import connect_device

from page.calendar.calendar_page import Calendar_Page
from page.camera.camera_page import Camera_Page
from page.chrome.chrome_page import Chrome_Page
from page.contacts.contacts_page import Contacts_Page
from page.deskclock.deskclock_page import Deskclock_Page
from page.dialer.dialer_page import Dialer_Page
from page.filemanager.filemanager_page import FileManager_Page
from page.fota.fota_page import Fota_Page
from page.messaging.messaging_page import Messaging_Page
from page.onetouchbooster.onetouchbooster_page import Onetouchbooster_Page
from page.settings.settings_page import Settings_Page
from page.system.system import System
from toolsbar.excel_tools import read_excel_for_case_parametrize
from toolsbar.save2csv import Save2Csv

os.path.abspath(".")
"""
    @File:test_before_fota.py
    @Author:Bruce
    @Date:2021/2/13
    @Description:Fota差异化设置
"""

"""
    Fota差异化设置，并excel记录下修改后控件都status、信息，供后续比对
"""

# function name , previous_data, set_data
saved_data = []

"""
    同一文件下，用例执行顺序，从上往下
"""


@allure.feature("Fota前置差异化设置")
class TestBeforeFota:

    # # case 1:
    # @allure.description("APK版本差异化")
    # @allure.step("获取当前应用的版本号->保存当前版本号")
    # @pytest.mark.parametrize("packageName", read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
    #                                                                         case_name="test_apk_version"))
    # def test_apk_version(self, before_all_case_execute, packageName):
    #     system = System(before_all_case_execute)
    #     result = system.get_app_version(packageName)
    #     saved_data.append([sys._getframe().f_code.co_name + "[" + packageName + "]", result, "\\"])
    #     assert result is not None
    #
    # # case 2:
    # @allure.description("通话设置差异化")
    # @allure.step("进入Dialer->点击右上角Menu->Settings->Display options->Sort by->更改排序方式->保存更改后的结果")
    # def test_dialer_settings(self, before_all_case_execute):
    #     dialer_page = Dialer_Page(before_all_case_execute)
    #     dialer_page.start_dialer()
    #     result = dialer_page.change_sort_by()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 3:
    # @allure.description("通话记录差异化")
    # @allure.step("(测试前先插入一张SIM卡)使用adb命令拨打电话->挂断电话->保存当前拨打的电话号码")
    # @pytest.mark.parametrize("number", read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
    #                                                                    case_name="test_calling_history"))
    # def test_calling_history(self, before_all_case_execute, number):
    #     dialer_page = Dialer_Page(before_all_case_execute)
    #     dialer_page.call(number)
    #     dialer_page.end_call.wait().click()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", number])
    #     assert number is not None
    #
    # # case 4:
    # @allure.description("已发短信差异化")
    # @allure.step("使用adb命令发送短信给自身号码->点击SMS发送->获取发送的结果->保存当前发送的结果")
    # @pytest.mark.parametrize("number, content",
    #                          read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
    #                                                          case_name="test_send_message"))
    # def test_send_message(self, before_all_case_execute, number, content):
    #     messaging_page = Messaging_Page(before_all_case_execute)
    #     result = messaging_page.send_message(number, content)
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 5:
    # @allure.description("短信设置差异化")
    # @allure.step("通过adb进入Messaging setting界面->修改Hear outgoing message sounds状态->保存当前修改的状态")
    # def test_messaging_settings(self, before_all_case_execute):
    #     messaging_page = Messaging_Page(before_all_case_execute)
    #     messaging_page.enter_messaging_settings()
    #     result = messaging_page.change_hear_outgoing_status()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 6:
    # @allure.description("创建联系人差异化")
    # @allure.step("通过adb进入联系人创建界面->创建指定联系人->检查联系人是否创建成功->保存当前创建联系人状态")
    # @pytest.mark.parametrize("contact_name, phone_number",
    #                          read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
    #                                                          case_name="test_contact_reserved"))
    # def test_contact_reserved(self, before_all_case_execute, contact_name, phone_number):
    #     contacts_page = Contacts_Page(before_all_case_execute)
    #     result = contacts_page.create_contact(contact_name, phone_number)
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 7:
    # @allure.description("创建闹钟差异化")
    # @allure.step("启动deskclock->点击创建闹钟->点击save即创建当前时间闹钟->保存当前创建闹钟对时间状态")
    # def test_clock_reserved(self, before_all_case_execute):
    #     deskclock_page = Deskclock_Page(before_all_case_execute)
    #     deskclock_page.start_deskclock()
    #     result = deskclock_page.add_clock()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 8:
    # @allure.description("创建日历差异化")
    # @allure.step("启动calendar->检测跳过Guide页面->创建日历->检测当前日历是否创建成功->保存当前创建日历状态")
    # @pytest.mark.parametrize("title",
    #                          read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
    #                                                          case_name="test_calendar_reserved"))
    # def test_calendar_reserved(self, before_all_case_execute, title):
    #     calendar_page = Calendar_Page(before_all_case_execute)
    #     calendar_page.start_calendar()
    #     calendar_page.skip_guide()
    #     created_calendar = calendar_page.create_calendar(title)
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", created_calendar])
    #     assert created_calendar is not None
    #
    # # case 9:
    # @allure.description("电池管理差异化")
    # @allure.step("启动one touch booster界面->跳过Guide->进入电池设置->更改intelligent power saving title状态->保存当前更改的状态")
    # def test_battery_management_settings(self, before_all_case_execute):
    #     onetouchbooster_page = Onetouchbooster_Page(before_all_case_execute)
    #     onetouchbooster_page.start_onetouchbooster()
    #     onetouchbooster_page.skip_guide()
    #     onetouchbooster_page.enter_battery_settings()
    #     result = onetouchbooster_page.change_intelligent_power_saving_status()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 10:
    # @allure.description("相机设置差异化")
    # @allure.step("启动camera->进入camera settings->更改Ai scene status->保存当前更改的状态")
    # def test_camera_settings(self, before_all_case_execute):
    #     camera_page = Camera_Page(before_all_case_execute)
    #     camera_page.start_camera()
    #     camera_page.enter_camera_settings()
    #     result = camera_page.change_ai_scene_status()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 11:
    # @allure.description("Sound设置差异化")
    # @allure.step("启动Settings->进入Sound vibration->更改silent mode状态->保存当前更改的状态")
    # def test_sound_settings(self, before_all_case_execute):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     settings_page.start_settings()
    #     settings_page.enter_sound_vibration()
    #     result = settings_page.change_silent_mode()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #
    # # case 12:
    # @allure.description("显示设置差异化")
    # @allure.step("使用adb命令修改亮度和休眠时间")
    # def test_display_settings(self, before_all_case_execute):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     result = settings_page.change_brightness_sleep_mode()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 13:
    # @allure.description("Gesture设置差异化")
    # @allure.step("启动Settings->进入Button & gestures->设置navigation gesture->保存当前更改的navigation状态")
    # def test_gesture_settings(self, before_all_case_execute):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     settings_page.start_settings()
    #     settings_page.enter_button_gestures()
    #     result = settings_page.set_navigation_gesture()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 14:
    # @allure.description("Security屏幕锁差异化")
    # @allure.step("启动Settings->进入Security & biometrics->设置Screen lock->保存当前更改的屏幕锁状态")
    # def test_security_screen_lock(self, before_all_case_execute):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     settings_page.start_settings()
    #     settings_page.enter_security()
    #     result = settings_page.set_screen_lock()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 15:
    # @allure.description("SecuritySIM锁差异化")
    # @allure.step("启动Settings->进入Security & biometrics->SIM card lock->点击修改Lock SIM card 状态->保存当前更改的屏幕锁状态")
    # def test_security_sim_card(self, before_all_case_execute):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     settings_page.start_settings()
    #     settings_page.enter_security()
    #     result = settings_page.change_sim_card_lock_status()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 16:
    # @allure.description("SIM card name差异化")
    # @allure.step(
    #     "启动Settings->进入SIM card & cellular network->SIM card settings->设置小齿轮->修改Sim card name->保存当前更改的sim card name状态")
    # @pytest.mark.parametrize("name",
    #                          read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
    #                                                          case_name="test_simcard_name"))
    # def test_simcard_name(self, before_all_case_execute, name):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     settings_page.start_settings()
    #     settings_page.enter_simcard_cellular()
    #     result = settings_page.change_simcard_name(name)
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 17:
    # @allure.description("Accessibility差异化")
    # @allure.step("进入Accessibility->点击Remove animations->保存当前更改的Remove animations状态")
    # def test_remove_animation(self, before_all_case_execute):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     settings_page.start_settings()
    #     settings_page.enter_accessibility()
    #     result = settings_page.change_animations_status()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 18:
    # @allure.description("Filemanager差异化")
    # @allure.step("启动FileManager->进入Internal storage->创建文件夹->保存当前创建的文件夹的名字")
    # @pytest.mark.parametrize("name",
    #                          read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
    #                                                          case_name="test_create_folder"))
    # def test_create_folder(self, before_all_case_execute, name):
    #     filemanager_page = FileManager_Page(before_all_case_execute)
    #     filemanager_page.start_filemanager()
    #     result = filemanager_page.create_folder(name)
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 19:
    # @allure.description("IMEI&CU差异化检测")
    # @allure.step("adb *#07#->进入Regulatory&safety界面->获取设备IMEI&CU->保存当前IMEI&CU的值")
    # def test_imei_cu(self, before_all_case_execute):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     result = settings_page.get_imei_cu()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 20:
    # @allure.description("SVN差异化检测")
    # @allure.step("adb *#*#06#*#*->获取设备SVN->保存当前SVN的值")
    # def test_svn(self, before_all_case_execute):
    #     dialer_page = Dialer_Page(before_all_case_execute)
    #     result = dialer_page.get_svn()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 21:
    # @allure.description("Wifi AP差异化")
    # @allure.step("启动Settings->WiFi->adb打开Wifi->连接Wifi->adb获取当前连接的Wifi名称->保存当前WiFi的名称")
    # @pytest.mark.parametrize("wifi_name, wifi_password",
    #                          read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
    #                                                          case_name="test_wifi_ap"))
    # def test_wifi_ap(self, before_all_case_execute, wifi_name, wifi_password):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     settings_page.start_settings()
    #     settings_page.enter_wifi()
    #     settings_page.enable_wifi()
    #     result = settings_page.connect_wifi()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 22:
    # @allure.description("Wifi Hotspot name差异化")
    # @allure.step("启动Settings->进入SIM card & cellular network->更改Hotspot name->保存当前Hotspot名称")
    # @pytest.mark.parametrize("name",
    #                          read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
    #                                                          case_name="test_hotspot"))
    # def test_hotspot(self, before_all_case_execute, name):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     settings_page.start_settings()
    #     settings_page.enter_simcard_cellular()
    #     result = settings_page.set_hotspot_name(name)
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 23:
    # @allure.description("Location设置差异化")
    # @allure.step("启动Settings->进入Location->改变Wifi scanning状态->保存当前Wifi scanning状态")
    # def test_location_settings(self, before_all_case_execute):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     settings_page.start_settings()
    #     settings_page.enter_location()
    #     result = settings_page.change_location_settings()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 24:
    # @allure.description("Chrome下载记录差异化")
    # @allure.step("启动Chrome->跳过Guide->进入百度网页->下载百度首页图片->进入Download menu获取下载的文件的number->保存number")
    # @pytest.mark.parametrize("website",
    #                          read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
    #                                                          case_name="test_chrome_download"))
    # def test_chrome_download(self, before_all_case_execute, website):
    #     chrome_page = Chrome_Page(before_all_case_execute)
    #     chrome_page.start_chrome()
    #     chrome_page.skip_guide()
    #     chrome_page.enter_website(website)
    #     chrome_page.download_baidu_image()
    #     result = chrome_page.get_first_download_file()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 25:
    # @allure.description("Chrome书签差异化")
    # @allure.step("启动Chrome->跳过Guide->进入百度网页->点击保存为书签->保存书签名称")
    # @pytest.mark.parametrize("website",
    #                          read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
    #                                                          case_name="test_chrome_bookmarks"))
    # def test_chrome_bookmarks(self, before_all_case_execute, website):
    #     chrome_page = Chrome_Page(before_all_case_execute)
    #     chrome_page.start_chrome()
    #     chrome_page.skip_guide()
    #     result = chrome_page.save_bookmark(website)
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # # case 26:
    # @allure.description("VPN配置差异化")
    # @allure.step("启动Settings->检测是否有屏幕锁->没有即设置,有即进行VPN设置->进入Connected devices->设置VPN->保存当前设置的VPN名称")
    # @pytest.mark.parametrize("name, address",
    #                          read_excel_for_case_parametrize(form="./test_case/before_fota_data.xlsx",
    #                                                          case_name="test_vpn_config"))
    # def test_vpn_config(self, before_all_case_execute, name, address):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     settings_page.start_settings()
    #     settings_page.enter_security()
    #     settings_page.set_screen_lock()
    #     settings_page.stop_settings()
    #     settings_page.start_settings()
    #     settings_page.enter_connected_devices()
    #     result = settings_page.set_vpn(name, address)
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 27:
    # @allure.description("Notch设置差异化")
    # @allure.step("启动Settings->进入Display->更改Notch风格->保存当前Notch风格")
    # def test_notch_settings(self, before_all_case_execute):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     settings_page.start_settings()
    #     settings_page.enter_display()
    #     result = settings_page.change_notch_style()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 28:
    # @allure.description("ScreenRecorder设置差异化")
    # @allure.step("启动Settings->进入Advanced features->更改Record touch interactions状态->保存当前状态")
    # def test_screenrecorder_settings(self, before_all_case_execute):
    #     settings_page = Settings_Page(before_all_case_execute)
    #     settings_page.start_settings()
    #     settings_page.enter_advanced_features()
    #     result = settings_page.change_screenrecorder_settings()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None
    #
    # # case 29:
    # @allure.description("设备主软件版本检测")
    # @allure.step("使用adb获取当前设备主软件版本->保存当前主软件版本号")
    # def test_main_software_version(self, before_all_case_execute):
    #     dialer_page = Dialer_Page(before_all_case_execute)
    #     result = dialer_page.get_main_software_version()
    #     saved_data.append([sys._getframe().f_code.co_name, "\\", result])
    #     assert result is not None

    # case 30:
    @allure.description("设备Fota开始Fota升级")
    @allure.step("OK")
    def test_updatesw(self, before_all_case_execute):
        fota_page = Fota_Page(before_all_case_execute)
        # fota_page.updatesw()
        # print(str(fota_page.check_update_result()))

    @allure.description("非测试Case:"
                        "\n作用:最后对saved_data进行处理并保存写入")
    @allure.step("初始化Save2Csv对象->将获取到的每个测试结果写入Excel表格保存")
    def test_sort_all_data(self, cmdopt):
        device_ = connect_device("Android:///{}".format(cmdopt))
        save2csv = Save2Csv()
        save2csv.writeInCsv(saved_data, form_name=str(device_.serialno) + "Fota_Before.csv")
        assert saved_data is not None
