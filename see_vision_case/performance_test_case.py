# coding = utf8

import os

from page_android.system.system import System

os.path.abspath(".")


def case1_boot_speed(main_page):
    print("case1_boot_speed begin test!")
    main_page.device.wake()
    system = System(main_page)
    result = system.reboot_device_and_wait()
    return result


def case2_screen_off_speed(main_page):
    pass


def case3_unlock_speed(main_page):
    pass


def case4_wake_speed(main_page):
    pass


def case5_slide_speed(main_page):
    pass


def case6_expand_folder_speed(main_page):
    pass


def case7_cold_boot_camera_speed(main_page):
    pass


def case8_camera_capture_speed(main_page):
    pass


def case9_camera_to_desktop_speed(main_page):
    pass


def case10_cold_boot_gallery_speed(main_page):
    pass


def case11_check_picture_speed(main_page):
    pass


def case12_cold_boot_settings_speed(main_page):
    pass


def case13_enter_wifi_speed(main_page):
    pass


def case14_cold_boot_music_speed(main_page):
    pass


def case15_cold_boot_video_speed(main_page):
    pass


def case16_play_local_video_speed(main_page):
    pass


def case17_cold_boot_filemanager_speed(main_page):
    pass


def case18_pull_down_notification_speed(main_page):
    pass


def case19_cold_boot_wechat_speed(main_page):
    pass


def case20_check_notification_speed(main_page):
    pass


def case21_launch_task_manager_speed(main_page):
    pass


def case22_wake_keyboard_speed(main_page):
    pass


def case23_keyboard_show_speed(main_page):
    pass


def case24_cold_boot_calendar_speed(main_page):
    pass


def case25_cold_boot_clock_speed(main_page):
    pass


def case26_cold_boot_browser_speed(main_page):
    pass


def case27_wechat_install_speed(main_page):
    pass


def case28_cold_boot_wangzhe_speed(main_page):
    pass


def default():
    pass


def case_chooser(case_number, main_page):
    return switch.get(case_number, default)(main_page)


switch = {1: case1_boot_speed, 2: case2_screen_off_speed, 3: case3_unlock_speed, 4: case4_wake_speed,
          5: case5_slide_speed, 6: case6_expand_folder_speed, 7: case7_cold_boot_camera_speed,
          8: case8_camera_capture_speed, 9: case9_camera_to_desktop_speed, 10: case10_cold_boot_gallery_speed,
          11: case11_check_picture_speed, 12: case12_cold_boot_settings_speed, 13: case13_enter_wifi_speed,
          14: case14_cold_boot_music_speed, 15: case15_cold_boot_video_speed, 16: case16_play_local_video_speed,
          17: case17_cold_boot_filemanager_speed, 18: case18_pull_down_notification_speed,
          19: case19_cold_boot_wechat_speed, 20: case20_check_notification_speed,
          21: case21_launch_task_manager_speed, 22: case22_wake_keyboard_speed, 23: case23_keyboard_show_speed,
          24: case24_cold_boot_calendar_speed, 25: case25_cold_boot_clock_speed,
          26: case26_cold_boot_browser_speed, 27: case27_wechat_install_speed, 28: case28_cold_boot_wangzhe_speed}
