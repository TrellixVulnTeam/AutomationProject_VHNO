# coding = utf8
import os
os.path.abspath(".")
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from time import sleep

"""
    初始化AndroidUiautomationPoco
"""
# poco = AndroidUiautomationPoco()
# Huawei P30 pro
"""
    一、以下为airtest操作API
        以下func大部分可单独运行：
            1.单独调用 - 当前Device
            2.指定device调用 - 控制不同设备（主要API选择）
            以下是Airtest的API的用法，它提供了一些方法的封装，同时还对接了图像识别等技术，但Airtest也有局限性，不能根据DOM树
            来选则对应但节点，依靠图像识别也有一定不精确之处，所以还需要另一个库Poco
"""
"""
    初始化设备
"""
device_huawei = init_device("Android", uuid = "MQS0219619020975")
# Austin 11#
# device_milan = init_device("Android", uuid = "11921b86")
# Milan 40#
# device_milan = init_device("Android", uuid = "AMBY9DWG59T8KVAU")
# 已修改源码以兼容Android 11版本
"""
    点击home键
"""
# device_huawei.home()
# sleep(1)
"""
    获取当前已连接的设备序列号
"""
# local_device = device_huawei.get_default_device()
# uuid_device = device_huawei.uuid
"""
    获取设备所有APP的列表
"""
# app_list = device_huawei.list_app()
"""
    打印输出APP.apk在系统中完整路径
"""
# app_path = device_huawei.path_app("com.danielstudio.app.wowtu")
"""
    检查某个APP是否在设备上
"""
# app_exist = device_huawei.check_app("com.danielstudio.app.wowtu")
"""
    启动某个APP
"""
# device_huawei.start_app("com.danielstudio.app.wowtu")
"""
    启动某个APP并返回启动时间
"""
# launch_time = device_huawei.start_app_timing("com.danielstudio.app.wowtu", "com.danielstudio.app.wowtu.activity.MainActivity")
"""
    停止某个APP
"""
# device_huawei.stop_app("com.android.settings")
"""
    清空某个APP数据
"""
# device_huawei.clear_app("com.danielstudio.app.wowtu")
"""
    安装APP
"""
# device_huawei.uninstall_app("com.danielstudio.app.wowtu")
"""
    删除APP
"""
# device_huawei.install_app("./apk/jandan.apk")
"""
    屏幕截图
"""
# screen_shot = device_huawei.snapshot("./screenshot/temp.jpg")
"""
    获取adb执行结果
"""
# shell_return = device_huawei.shell("dumpsys window | grep mCurrentFocus")
"""
    执行键盘操作
"""
# device_huawei.keyevent("keycode_home")
"""
    唤醒当前设备 - 如果有锁需要先解锁
"""
# device_huawei.wake()
"""
    点击home键
"""
# device_huawei.home()
"""
    打开短信并输入内容
"""
# device_huawei.start_app("com.android.mms")
# poco(text = "Search").click()
# device_huawei.text("Hello")
"""
    点击屏幕某处位置,绝对position
"""
# device_huawei.touch([317, 2144])
# touch([317, 2144])
"""
    双击屏幕某处位置,绝对position
"""
# device_huawei.double_click([317, 2144])
"""
    滑动屏幕,由一点到另一点
"""
# device_huawei.swipe([547, 1694], [1, 1694])
"""
    放大再缩小Gallery图片
"""
# device_huawei.stop_app("com.android.gallery3d")
# poco(text = "Gallery").click()
# poco(text = "All photos").click()
# device_huawei.touch([134, 365])
# sleep(1)
# device_huawei.pinch([522, 1230], percent = 0.1, in_or_out = "out")
# sleep(1)
# device_huawei.pinch([522, 1230], percent = 0.5, in_or_out = "in")
"""
    获取某个特定属性的值
"""
# prop_return = device_huawei.getprop("ro.product.locale")
"""
    获取该设备IP地址
"""
# ip_address = device_huawei.get_ip_address()
"""
    获取当前Activity
    获取当前Activity的名称和进程号
    获取当前Activity名称
"""
# top_activity = device_huawei.get_top_activity()
# top_activity_name_pid = device_huawei.get_top_activity_name_and_pid()
# top_activity_name = device_huawei.get_top_activity_name()
"""
    判断当前键盘是否出现
"""
# is_keyboard_show = device_huawei.is_keyboard_shown()
"""
    判断当前设备是否锁定了
"""
# is_locked = device_huawei.is_locked()
"""
    解锁设备
"""
# unlock_return = device_huawei.unlock()
"""
    获取当前设备显示信息，宽、高……
"""
# display_info = device_huawei.display_info
# device_huawei.get_display_info()
"""
    获取当前设备的设备分辨率
"""
# device_current_resolution = device_huawei.get_current_resolution()
"""
    获取当前渲染分辨率
"""
# device_render_resolution = device_huawei.get_render_resolution()
"""
    录制设备当前屏幕
"""
# device_huawei.start_recording(max_time = 30)
# sleep(1)
# poco(text = "Gallery").click()
# sleep(3)
# device_huawei.stop_recording(output = "./log/test.mp4")
"""
    调整设备屏幕至合适分辨率
"""
# device_huawei.adjust_all_screen()

"""
    二、以下为Poco操作API：
        1.利用Poco我们可以支持DOM选择
        2.Poco返回的是UIObjectProxy对象，提供了操作API
"""
"""
    初始化AndroidUiautomationPoco
"""
poco = AndroidUiautomationPoco()
"""
    连接设备
    Android:///uuid
"""
connect_device("Android:///MQS0219619020975")
home()
sleep(1)
"""
    child节点定位，根据节点树结构来定位元素
    children是获取所有子节点，即会在所有子节点中寻找
    对WebView支持不是很好，部分元素只用poco无法定位
"""
# poco(text = "Gallery").click()
# poco(text = "Gallery")
# poco(name = "com.huawei.android.launcher:id/layout").child().child(name = "Phone").click()
# poco(name = "android.view.ViewGroup").child("Gallery").click()
"""
    获取节点属性
    根据key获取
"""
# node_attr = poco(text = "Gallery").attr("name")
"""
    双击，需要结合airtest
    获取设备屏幕尺寸
    转换成绝对position
"""
# screen_size = [device_huawei.display_info["width"], device_huawei.display_info["height"]]
# gallery_abs_position = [poco(text = "Gallery").attr("pos")[0] * screen_size[0],
#                         poco(text = "Gallery").attr("pos")[1] * screen_size[1]]
# double_click(gallery_abs_position)









