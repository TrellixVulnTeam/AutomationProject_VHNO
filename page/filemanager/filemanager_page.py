# coding = utf8
import os
import sys

from page.system.system import System, sleep
from toolsbar.excel_tools import read_excel_for_page_element

os.path.abspath(".")
"""
    @File:filemanager_page.py
    @Author:Bruce
    @Date:2021/1/14
    @Description:Filemanager page，控制设备Filemanager应用的函数、控件
    @param:继承System，传入Main_Page实例完成设备Device、Poco初始化
"""


# 该函数用于简化元素获取操作
def get_element_parametrize(element_name="guide_page_text"):
    form_name = "./page/page_sheet.xlsx"
    element_data = read_excel_for_page_element(form=form_name, sheet_name="filemanager_page",
                                               element_name=element_name)
    return element_data


class FileManager_Page(System):
    """
        @param:main_page:传入Main_Page实例完成设备的Device、Poco的初始化
    """

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.internal_storage = self.poco(get_element_parametrize("internal_storage"))
        self.menu = self.poco(get_element_parametrize("menu"))
        self.create_folder_text = self.poco(text=get_element_parametrize("create_folder_text"))
        self.create_folder_name = self.poco(text=get_element_parametrize("create_folder_name"))
        self.create_folder_create = self.poco(text=get_element_parametrize("create_folder_create"))

    """
        @description:启动Filemanager应用
    """

    def start_filemanager(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":启动filemanager app:")
        self.device.start_app("com.tcl.tct.filemanager")
        sleep(1)

    """
        @description:关闭Filemanager应用
    """

    def stop_filemanager(self):
        self.logger.info("function:" + sys._getframe().f_code.co_name + ":关闭filemanager app:")
        sleep(1)
        self.device.stop_app("com.tcl.tct.filemanager")

    """
        @description:创建文件夹
        @param:
            name:文件夹名称
    """

    def create_folder(self, name="Test"):
        result = ""
        try:
            self.logger.info("function:" + sys._getframe().f_code.co_name + ":创建文件夹:")
            self.internal_storage.wait().click()
            self.menu.wait().click()
            self.create_folder_text.wait().click()
            create_folder_name = self.create_folder_name.wait()
            create_folder_name.invalidate()
            create_folder_name.set_text(name)
            self.create_folder_create.wait().click()
            result = "Created Folder Name" + ":" + self.scroll_to_find_element(element_text=name).get_text()
        except Exception as ex:
            self.logger.error(
                "function:" + sys._getframe().f_code.co_name + ":创建文件夹出现问题:" + str(ex))
        return result
