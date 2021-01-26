# coding = utf8
import os
from time import sleep

from airtest.core.api import keyevent
from poco.exceptions import PocoNoSuchNodeException

from page.messaging.messaging_page import Messaging_Page

os.path.abspath(".")

"""
    @File:system.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Current py test is contained some system function
"""


class System:

    def get_app_version(main_page, packageName="com.android.settings"):
        exists_app = main_page.device.check_app(packageName)
        if exists_app:
            versionName = main_page.device.shell("pm dump %s|grep versionName" % packageName)
            print("[Device:" + main_page.device.serialno + "]" + versionName)

    def get_phone_number(main_page):
        main_page.device.start_app_timing(package="com.google.android.apps.messaging",
                                          activity=".ui.appsettings.PerSubscriptionSettingsActivity")
        messaging_page = Messaging_Page(main_page)
        sim_number = messaging_page.settings_menu_advanced_phone_number.parent().children()[1].wait().get_text()
        sim_number = sim_number.replace(" ", "")
        main_page.device.home()
        return sim_number

    def scroll_to_find_element(main_page, element_text="", element_id=""):
        global element
        menu_exists = False
        search_count = 0
        if element_text != "":
            while not menu_exists:
                element = main_page.poco(text=element_text).wait()
                menu_exists = element.exists()
                print("Current element {} exists status is {}".format(element, menu_exists))
                if menu_exists:
                    return element
                main_page.poco.scroll(direction="vertical", percent=0.6, duration=1)
                search_count += 1
                print("up: " + str(search_count) + str(menu_exists))
                # 给滑动查找增加向上滑动，兼容到底未找到的情况，即向下查找超过10次则开始向上查找
                while search_count >= 5 and not menu_exists:
                    main_page.poco.scroll(direction="vertical", percent=-0.6, duration=1)
                    element = main_page.poco(text=element_text).wait()
                    menu_exists = element.exists()
                    search_count += 1
                    print("down: " + str(search_count) + str(menu_exists))
                    if search_count >= 10:
                        search_count = 0
                        break
                    if menu_exists:
                        return element
        else:
            while not menu_exists:
                element = main_page.poco(element_id).wait()
                menu_exists = element.exists()
                print("Current element {} is {}".format(element, menu_exists))
                if menu_exists:
                    return element
                main_page.poco.scroll(direction="vertical", percent=0.6, duration=1)
                search_count += 1
                print("up: " + str(search_count) + str(menu_exists))
                # 给滑动查找增加向上滑动，兼容到底未找到的情况，即向下查找超过10次则开始向上查找
                while search_count >= 5 and not menu_exists:
                    main_page.poco.scroll(direction="vertical", percent=-0.6, duration=1)
                    element = main_page.poco(element_id).wait()
                    menu_exists = element.exists()
                    search_count += 1
                    print("down: " + str(search_count) + str(menu_exists))
                    if search_count >= 10:
                        search_count = 0
                        break
                    if menu_exists:
                        return element
        return element

    def unlock_screen(main_page):
        """
           亮屏并解锁屏幕操作，SIM PIN 1234解锁
        """
        main_page.device.unlock()
        try:
            main_page.poco("com.android.systemui:id/lock_icon").drag_to(main_page.poco("com.android.systemui:id"
                                                                                       "/rectangle_frame"),
                                                                        duration=0.5)
            try:
                if main_page.poco(text="BACK").wait().exists():
                    for i in range(1, 5):
                        main_page.poco(text="%s" % i).wait().click()
                    main_page.device.keyevent("KEYCODE_ENTER")
            except PocoNoSuchNodeException:
                print("Screen lock interface not ok, please check!")
        except PocoNoSuchNodeException:
            print("No screen lock")
        finally:
            main_page.device.home()

    def lock_screen(main_page):
        main_page.device.keyevent("KEYCODE_POWER")

    def double_click_element(main_page, element_item):
        position = element_item.get_position()
        position = (position[0] * main_page.device.get_display_info()["width"],
                    position[1] * main_page.device.get_display_info()["height"])
        print(position)
        main_page.device.double_click(position)



