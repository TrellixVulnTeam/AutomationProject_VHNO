# coding = utf8
import os
from time import sleep

from page_android.launcher.launcher_page import Launcher_Page
from page_android.system.system import System

os.path.abspath(".")

"""
    @File:clock_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:Clock page_android，控制设备Clock应用的函数、控件
"""


class Clock_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化，初始化全局logger记录测试步骤
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

    """
        @description:该函数用于从主菜单启动时钟
    """

    def boot_clock_from_main_menu(self):
        launcher_page = Launcher_Page(self)
        launcher_page.wake_up_main_menu()
        clock = launcher_page.search_app_in_main_menu(app_text="时钟")
        sleep(1)
        clock.click()
        sleep(1)

    """
        @description:该函数用于检测当前是否在时钟界面
    """

    def check_on_clock(self):
        result = False
        sleep(1)
        if "com.android.deskclock" in self.device.shell("dumpsys window | grep mCurrentFocus"):
            result = True
        return result

    def launchClock(self):
        print("Launch Clock！")
        self.logger.info("Launch Clock！")
        self.device.start_app("com.android.deskclock")
        sleep(1)

    def createClock(self, tag):
        print("创建闹钟：{}".format(tag))
        self.logger.info("创建闹钟：{}".format(tag))
        self.poco(text="闹钟").wait(3).click()
        self.poco("com.android.deskclock:id/right_img").wait(3).click()
        self.poco("com.android.deskclock:id/edit_label_text").wait(3).set_text(tag)
        self.poco(text="保存").wait(3).click()
        return tag

    def deleteAllClock(self):
        print("删除所有闹钟")
        self.logger.info("删除所有闹钟")
        self.poco(text="编辑").wait(3).click()
        self.poco(text="全选").wait(3).click()
        self.poco(text="删除").wait(3).click()
        self.poco("com.android.deskclock:id/ok_button").wait(3).click()

    def createWorldClock(self, desc):
        print("创建世界时钟 - {}".format(desc))
        self.logger.info("创建世界时钟 - {}".format(desc))
        self.poco(text="世界时钟").wait(3).click()
        if self.poco("com.android.deskclock:id/city_container").exists():
            self.deleteAllClock()
        self.poco("com.android.deskclock:id/right_img").wait(3).click()
        city_list = []
        print("获取世界所有国家列表")
        self.logger.info("获取世界所有国家列表")
        while True:
            current_city_list = self.poco("com.android.deskclock:id/city_content").wait(3).child(
                "com.android.deskclock:id/item_name")
            for i in range(0, len(current_city_list)):
                city = current_city_list[i].attr("text")
                if city not in city_list:
                    city_list.append(city)
            self.poco.scroll(direction="vertical", percent=0.6, duration=1)
            current_city_list.invalidate()
            if "朱巴 （南苏丹共和国）" in city_list:
                print("总计{}个国家，所有国家获取结束：{}".format(len(city_list), city_list))
                self.logger.info("总计{}个国家，所有国家获取结束：{}".format(len(city_list), city_list))
                break


        # current_city_list = self.poco("com.android.deskclock:id/city_content").wait(3).child(
        #     "com.android.deskclock:id/item_name")
        # for i in range(0, len(current_city_list)):
        #     city = current_city_list[i].attr("text")
        #     if city not in city_list:
        #         city_list.append(city)


        print("将所有国家添加城市时钟")
        self.logger.info("将所有国家添加城市时钟")
        self.poco("com.android.deskclock:id/btn_close").wait(3).click()
        for city in city_list:
            print("添加城市时钟：{}".format(city))
            self.logger.info("添加城市时钟：{}".format(city))
            self.poco("com.android.deskclock:id/right_img").wait(3).click()
            search_edit = self.poco("com.android.deskclock:id/search_text").wait(3)
            search_edit.click()
            search_edit.set_text(city.split("（")[0])
            self.poco(text=city).wait(3).click()
        return city_list

    def timerTest(self):
        print("开始Timer开始继续暂停压力测试")
        self.logger.info("开始Timer开始继续暂停压力测试")
        self.poco(text="计时器").wait(3).click()
        for i in range(2):
            self.poco("com.android.deskclock:id/scroll2").wait(3).scroll(direction="vertical", percent=0.99, duration=1)
        sleep(1)
        position = self.poco(text="开始").get_position()
        self.poco(text="开始").wait(3).click()
        j = 0
        while True:
            j += 1
            print("第{}次循环测试".format(j))
            self.logger.info("第{}次循环测试".format(j))
            self.poco.click(position)
            sleep(0.5)
            self.poco.click(position)
            if j >= 300:
                print("循环测试结束，循环次数{}".format(j))
                self.logger.info("循环测试结束，循环次数{}".format(j))
                self.poco(text="取消").wait(3).click()
                break
        return "计时器开始继续暂停压力测试 - 循环测试结束，循环次数{}".format(j)

    def stopwatchQuickCountTest(self):
        print("启动秒表快速计次压测")
        self.logger.info("启动秒表快速计次压测")
        self.poco(text="秒表").wait(3).click()
        self.poco(text="启动").wait(3).click()
        position = self.poco(text="计次").wait(3).get_position()
        j = 0
        while True:
            j += 1
            print("第{}次循环测试".format(j))
            self.logger.info("第{}次循环测试".format(j))
            self.poco.click(position)
            sleep(0.1)
            if j >= 3000:
            # if j >= 3:
                print("循环测试结束，循环次数{}".format(j))
                self.logger.info("循环测试结束，循环次数{}".format(j))
                self.poco(text="停止").wait(3).click()
                self.poco(text="复位").wait(3).click()
                break
        return "秒表快速计次压测 - 循环测试结束，循环次数{}".format(j)
