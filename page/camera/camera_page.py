# coding = utf8
import os
from time import sleep

os.path.abspath(".")
"""
    @File:camera_page.py
    @Author:Bruce
    @Date:2021/1/14
"""

class Camera_Page:

    def __init__(self, main_page):
        self.device = main_page.device
        self.poco = main_page.poco
        self.top_function_bar = self.poco("com.tcl.camera:id/picker_list_layout")
        self.camera_settings_ai_scene_detection = self.poco(text="AI scene detection")

    def start_camera(self):
        self.device.start_app("com.tcl.camera")
        sleep(1)

    def stop_camera(self):
        sleep(1)
        self.device.stop_app("com.tcl.camera")

    def enter_camera_settings(self):
        camera_settings = self.top_function_bar.wait().children()[0]
        print(camera_settings.attr("desc"))
        camera_settings.click()
        ai_scene_detection_switch = self.camera_settings_ai_scene_detection.wait().parent().parent().children()[1].children()
        ai_scene_detection_switch.click()
        ai_scene_detection_switch.invalidate()
        print(ai_scene_detection_switch.attr("checked"))




