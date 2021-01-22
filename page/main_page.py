# coding = utf8
import os

os.path.abspath(".")
"""
    @File:main_page.py
    @Author:Bruce
    @Date:2021/1/13
    @Description:A main page for all other page to inherit to init poco and device driver
"""


class Main_Page:

    def __init__(self, device_item, poco_item):
        self.device = device_item
        self.poco = poco_item
