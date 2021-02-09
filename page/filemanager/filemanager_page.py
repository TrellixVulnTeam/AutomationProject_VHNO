# coding = utf8
import os
from time import sleep
from page.system.system import System, logger

os.path.abspath(".")
"""
    @File:filemanager_page.py
    @Author:Bruce
    @Date:2021/1/14
"""

class FileManager_Page(System):

    def __init__(self, main_page):
        System.__init__(self, main_page)

        self.internal_storage = self.poco("com.tcl.tct.filemanager:id/phone_name")
        self.menu = self.poco("com.tcl.tct.filemanager:id/iv_bar_more")
        self.create_folder_text = self.poco(text="Create folder")
        self.create_folder_name = self.poco(text="Folder name")
        self.create_folder_create = self.poco(text="CREATE")

    def start_filemanager(self):
        self.device.start_app("com.tcl.tct.filemanager")
        sleep(1)

    def stop_filemanager(self):
        sleep(1)
        self.device.stop_app("com.tcl.tct.filemanager")

    def create_folder(self, name="Test"):
        self.start_filemanager()
        self.internal_storage.wait().click()
        self.menu.wait().click()
        self.create_folder_text.wait().click()
        create_folder_name = self.create_folder_name.wait()
        create_folder_name.invalidate()
        create_folder_name.set_text(name)
        self.create_folder_create.wait().click()
        self.stop_filemanager()


