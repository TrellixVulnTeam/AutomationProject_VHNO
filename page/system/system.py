# coding = utf8
import os

from page.Messaging.messaging_page import Messaging_Page

os.path.abspath(".")
from toolsbar.common import test_device, poco

"""
    @File:system.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Current py test is contained some system function
"""


def get_app_version(packageName="com.android.settings"):
    exists_app = test_device.check_app(packageName)
    if exists_app:
        versionName = test_device.shell("pm dump %s|grep versionName" % packageName)
        print("[Device:" + test_device.serialno + "]" + versionName)


def get_phone_number():
    test_device.start_app_timing(package="com.google.android.apps.messaging",
                                 activity=".ui.appsettings.PerSubscriptionSettingsActivity")
    messaging_page = Messaging_Page()
    sim_number = messaging_page.settings_menu_advanced_phone_number.parent().children()[1].wait().get_text()
    sim_number = sim_number.replace(" ", "")
    test_device.home()
    return sim_number
