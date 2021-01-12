# coding = utf8
import os

os.path.abspath(".")

"""
    @File:system.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Current py test is contained some system function
"""


class System:
    #
    # def __init__(self, device_item, poco_item):
    #     self.test_device = device_item
    #     self.poco = poco_item

    # def get_app_version(self, packageName="com.android.settings"):
    #     exists_app = self.test_device.check_app(packageName)
    #     if exists_app:
    #         versionName = self.test_device.shell("pm dump %s|grep versionName" % packageName)
    #         print("[Device:" + self.test_device.serialno + "]" + versionName)

    def get_app_version(main_page, packageName="com.android.settings"):
        exists_app = main_page.device.check_app(packageName)
        if exists_app:
            versionName = main_page.device.shell("pm dump %s|grep versionName" % packageName)
            print("[Device:" + main_page.device.serialno + "]" + versionName)
