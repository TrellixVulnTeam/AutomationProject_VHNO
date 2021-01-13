# coding = utf8
import os

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
