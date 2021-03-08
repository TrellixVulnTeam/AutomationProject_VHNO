# coding = utf8
import os
import sys

from poco.exceptions import PocoNoSuchNodeException

from page.system.system import System, sleep

os.path.abspath(".")
"""
    @File:chrome_page.py
    @Author:Bruce
    @Date:2021/1/26
"""


class Chrome_Page(System):

    def __init__(self, main_page):
        System.__init__(self, main_page)
        self.menu_icon = self.poco("com.android.chrome:id/menu_button")
        self.menu_download = self.poco(text="Downloads")

    def start_chrome(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动chrome app:")
        self.device.start_app("com.android.chrome")
        sleep(1)

    def stop_chrome(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭chrome app:")
        sleep(1)
        self.device.stop_app("com.android.chrome")

    def skip_guide(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":跳过设置向导:")
            guide_first_button = self.poco("com.android.chrome:id/terms_accept").wait()
            if guide_first_button.exists():
                guide_first_button.click()
                self.poco("com.android.chrome:id/negative_button").wait().click()
        except PocoNoSuchNodeException as ex:
            self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                ":无需跳过chrome设置向导:" + str(ex))

    def enter_website(self, website="www.baidu.com"):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":进入网页{}:".format(website))
            # 检查并跳过 search_engine_choose 按钮
            search_engine_choose = self.poco("com.android.chrome:id/button_secondary").wait()
            if search_engine_choose.exists():
                search_engine_choose.click()
        except PocoNoSuchNodeException as ex:
            self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                ":无需跳过Search engine界面:" + str(ex))
        finally:
            chrome_url_bar = self.poco("com.android.chrome:id/url_bar").wait()
            chrome_url_bar.click()
            chrome_url_bar.set_text(website)
            self.device.keyevent("KEYCODE_ENTER")
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":成功进入网页{}:".format(website))
            try:
                # 检查并跳过 location_button 按钮
                location_button = self.poco("com.android.chrome:id/positive_button").wait()
                if location_button.exists():
                    location_button.click()
            except PocoNoSuchNodeException as ex:
                self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                    ":无需进行location授权界面:" + str(ex))

    def download_baidu_image(self):
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":下载百度首页图片:")
            self.poco(text="百度一下,你就知道").wait().long_click()
            self.poco(text="Download image").wait().click()
            try:
                popup_info = self.poco("com.android.chrome:id/infobar_close_button").wait()
                if popup_info.exists():
                    popup_info.click()
            except PocoNoSuchNodeException as ex:
                self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                    ":无需关闭弹出的Info弹框:" + str(ex))
            finally:
                try:
                    download_again_info = self.poco("com.android.chrome:id/infobar_close_button").wait()
                    if download_again_info.exists():
                        download_again_info.click()
                except PocoNoSuchNodeException as ex:
                    print("download_again_info closed!")
                    self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                        ":无需关闭弹出的Download again info信息弹框:" + str(ex))
                finally:
                    try:
                        self.poco("com.android.chrome:id/positive_button").wait().click()
                    except PocoNoSuchNodeException as ex:
                        self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                            ":非第一次下载，需要点击开始下载按钮:" + str(ex))
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":下载百度首页图片出现问题:" + str(ex))

    def get_first_download_file(self):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":获取下载记录中第一个文件number:")
            self.menu_icon.wait().click()
            self.menu_download.wait().click()
            download_file = self.poco("com.android.chrome:id/thumbnail").wait()
            download_file.click()
            download_file_number = self.poco("com.android.chrome:id/title_bar").wait().get_text()
            result = "Downloaded file Number" + ":" + download_file_number
        except Exception as ex:
            self.logger.error("function:" + sys._getframe().f_code.co_name + ":获取下载记录中第一个文件number出现问题:" + str(ex))
        return result

    def save_bookmark(self, website="www.baidu.com"):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":保存{}为书签:".format(website))
            self.enter_website(website)
            chrome_menu = self.menu_icon.wait()
            chrome_menu.click()
            self.poco("com.android.chrome:id/button_two").wait().click()
            try:
                if self.poco(text="Edit bookmark").wait().exists():
                    self.device.keyevent("KEYCODE_BACK")
            except PocoNoSuchNodeException as ex:
                self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                    ":书签{}添加成功:".format(website) + str(ex))
            finally:
                # 二次验证书签添加成功
                chrome_menu.click()
                self.poco(text="Bookmarks").wait().click()
                self.poco(text="Mobile bookmarks").wait().click()
                try:
                    current_bookmark = self.poco(text=website).wait()
                    result = "Saved bookmark Name" + ":" + current_bookmark.get_text()
                except PocoNoSuchNodeException as ex:
                    self.logger.warning("function:" + sys._getframe().f_code.co_name +
                                        ":书签{}添加失败:".format(website) + str(ex))
        except Exception as ex:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":保存{}为书签出现问题:".format(website) + str(ex))

        return result