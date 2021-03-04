# coding = utf8
import os
import re
import sys

from airtest.core.error import AdbShellError

from toolsbar.common import logger

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
    # 判断没有启动界面就放出来进行授权
    # 优化后app数量：67个，优化前app数量：330个
    if devices.shell("dumpsys package {} | grep category.LAUNCHER".format(package_name)).replace(" ", "") is not None:
        permission_list = devices.shell(
            "dumpsys package {} | grep permission | grep granted=false".format(package_name))
        permission_list = re.findall("\s*(.*):\sgranted", permission_list)
    return permission_list


def grant_permission(devices):
    print("机器正在授权中，请稍后")
    app_permission = data_deal(list_apps(devices), devices)
    for app_ in app_permission:
        for permission_ in app_[1]:
            try:
                devices.shell("pm grant {} {}".format(app_[0], permission_))
                logger.info(
                    "function:" + sys._getframe().f_code.co_name + "{} \n应用:{} 授权 p: {} 完成".format(devices,
                                                                                                   app_[0],
                                                                                                   permission_))
            except AdbShellError as adb_ex:
                # 一些vender系统应用存在无法授权，即continue跳过该应用
                logger.warning(
                    "function:" + sys._getframe().f_code.co_name + "当前系统应用无需授权,故跳过 \n + {}".format(adb_ex))
                continue


def data_deal(app_list, devices):
    app_permission = []
    for package_name in app_list:
        try:
            permission_name = list_permission(package_name, devices)
            app_permission.append([package_name, permission_name])
        except AdbShellError:
            logger.warning("function:" + sys._getframe().f_code.co_name + "{} 无需进行授权!".format(package_name))
    return app_permission
