# coding = utf8
import os

os.path.abspath("system")
"""
    @File:main_page.py
    @Author:Bruce
    @Date:2021/1/12
    @Description:A main page to provide device item and poco for all page, so just init one reference in run_test.py
    
"""


class Main_Page:

    def __init__(self, device_item, poco_item):
        self.device = device_item
        self.poco = poco_item


