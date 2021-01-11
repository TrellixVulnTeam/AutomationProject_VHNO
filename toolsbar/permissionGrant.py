# coding = utf8
import os

from airtest.core.error import AdbShellError
import re

os.path.abspath(".")

"""
    @File:permissionGrant.py
    @Author:Bruce
    @Date:2020/12/23
"""


def list_apps(devices):
    app_list = devices.shell("pm list packages")
    app_list = re.findall("package:(.*)", app_list)
    return app_list


def list_permission(package_name, devices):
    permission_list = devices.shell("dumpsys package {} | grep permission | grep granted=false".format(package_name))
    permission_list = re.findall("\s*(.*):\sgranted", permission_list)
    return permission_list


def grant_permission(devices):
    app_permission = data_deal(list_apps(devices), devices)
    for app_ in app_permission:
        for permission_ in app_[1]:
            try:
                devices.shell("pm grant {} {}".format(app_[0], permission_))
                print("{} \nPackage:{} granted p: {}".format(devices, app_[0], permission_))
            except AdbShellError as adb_ex:
                # 一些vender系统应用存在无法授权，即continue跳过该应用
                print("We will keep going next cycle \n + {}".format(adb_ex))
                continue


def data_deal(app_list, devices):
    app_permission = []
    for package_name in app_list:
        try:
            permission_name = list_permission(package_name, devices)
            app_permission.append([package_name, permission_name])
        except AdbShellError:
            print("{} no need permission granted!".format(package_name))
    return app_permission

