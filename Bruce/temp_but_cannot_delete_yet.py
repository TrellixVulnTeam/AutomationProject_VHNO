# coding = utf8
import os

os.path.abspath("..")
"""
    @File:temp_but_cannot_delete_yet.py
    @Author:Bruce
    @Date:2020/12/15
"""
from airtest.core.api import *

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
# device_huawei = init_device("Android", uuid = "MQS0219619020975")
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
# screen_shot = device_huawei.snapshot("./screenshot/Bruce.jpg")
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
# poco = AndroidUiautomationPoco()
"""
    连接设备
    Android:///uuid
"""
# connect_device("Android:///e02af793")
# home()
# sleep(1)
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
"""
    drag_to:将某个节点拖到另一个节点
    如下：拖动亮度条至最大
"""
# start_app("com.android.settings")
# sleep(1)
# poco(text = "Display & brightness").click()
# sleep(1)
# poco("com.android.settings:id/seekbar").drag_to(poco("com.android.settings:id/brightness_indicator_right"), duration = 0.5)
"""
    exists:判断某个节点是否存在
    如下：判断QQMusic是否存在，存在即打开
"""
# if (poco("QQMusic").exists()):
#     poco("QQMusic").click()
"""
    focus:获得焦点
    如下：获得QQMusic的中心焦点
    可以用于一些拖拽功能，拖拽到某处，使用坐标等方式定义位置
"""
# poco(text = "QQMusic").focus("center")
"""
    get_bounds():获取边界
    如下:获取QQMusic的边界：与屏幕四边的绝对距离
    使用时如需要先换算
"""
# bounds = poco(text = "QQMusic").get_bounds()
"""
    get_name():获取节点名
"""
# node_name = poco(text = "QQMusic").get_name()
"""
    get_position():获取节点位置
    如下:获取QQMusic的中心position
"""
# center_position = poco(text = "QQMusic").get_position(focus = "center")
"""
    get_size():获取节点大小
    使用时如需要先换算
"""
# size = poco(text = "QQMusic").get_size()
"""
    get_text():获取节点文本内容
"""
# icon_text = poco(text = "QQMusic").get_text()
"""
    long_click():长按
    如下:长按QQMuic图标3s
"""
# poco("QQMusic").long_click(duration = 3)
"""
    offspring():获取UI的直接的所有后代
    如下：获取hotseat的所有后代中的name为Phone的元素
    该方法读取元素效率没有读取单个元素高，注意使用取舍
"""
# print(poco(name = "com.huawei.android.launcher:id/layout").offspring(name = "Phone").click())
# poco("Phone").click()
# poco(name = "Phone").click()
"""
    parent():获取该节点的父节点
"""
# parent_node = poco(name = "Phone").parent()
# parent_node.child(name = "Phone").click()
"""
    scroll():滑动
    如下：滑动Gallery的图片，percent:滑动的距离占屏幕对应方向的比例
"""
# stop_app("com.android.gallery3d")
# poco(text = "Gallery").click()
# poco(name = "com.android.gallery3d:id/album_cover_image").click()
# sleep(1)
# poco.scroll(percent = 0.8, duration = 0.1)
"""
    set_text():设置文字
"""
# poco(name = "messaging").click()
# poco(text = "Search").set_text("Hello")
"""
    sibling():兄弟节点
    获取同一级parent的兄弟的节点
"""
# poco(name = "messaging").sibling(name = "Phone").click()
"""
    swipe():滑动
    必须放入坐标，如下：是使用两个icon的坐标来达到一个滑动的效果
"""
# poco.swipe(poco(name = "Gallery").get_position(), poco(name = "QQMusic").get_position())
"""
    wait():等待节点
    如下：等待gallery节点出现
    意义：设计等待节点出现的时间段满足某些需求,用处不大
"""
# gallery_node = poco(name = "Gallery").wait(timeout = 3)
"""
    wait_for_appearence():等待某个节点出现
    无返回值，如果未出现会raise PocoTargetTimeout
    意义：设计等待节点是否出现，在一段时间后是否出现，主要用该等待
    
    wait_for_disappearance()：等待某个节点消失，效果与上相反
"""
# gallery_node = poco(name = "Gallery").wait_for_appearance(timeout = 10)
# poco(name = "Gallery").wait_for_disappearance()

"""
    Settings->Apps->查找元素
    循环查找列表是否存在元素
"""
# start_app("com.android.settings")
# sleep(1)
# item_exists = False
# while(not item_exists):
#     item_get = poco.scroll(percent = 0.8, duration = 1)
#     apps_menu = poco(text = "Apps").wait(3)
#     item_exists = apps_menu.exists()
# apps_menu.click()
# sleep(1)
# poco(text = "Special app access").click()
# sleep(1)
# # poco(text = "Battery optimization").click()
# poco(text = "Battery optimisation").click()
# sleep(1)
# app_exists = False
# app_get = ""
# while(not app_exists):
#     poco.scroll(percent = 0.8, duration = 1)
#     app_get = poco(text = "System Update")
#     app_exists = app_get.exists()
# print("Find this app %s: %s" %(app_get.get_text(), app_exists))

# poco = AndroidUiautomationPoco()
# austin_test = connect_device("Android:///7c2440fd")
# number = "18575211714"
# print(number[-4:])


"""
    poco.scroll:方法上下左右滑动使用方法
        percent range:
            up:(0.1, 0.9)
            down:(-0.1, -0.6)
            left:(0.8)
            right:(-0.8)
"""
# poco.scroll(direction="horizontal", percent=-0.8, duration=1)


"""
    Case construct template
"""
"""
    Case :验证升级后可以保留
    relate app:
        
    test step:
        检查APP存在->->Fota升级后再次获取该值与升级前对比是否相同判定结果
"""


def check_reserved():
    try:
        stop_app("")
        start_app("")
    except Exception:
        print("Some thing error, please check!")
