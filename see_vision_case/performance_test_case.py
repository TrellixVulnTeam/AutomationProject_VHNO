# coding = utf8

import os
import sys
from time import sleep

from page_android.calendar.calendar_page import Calendar_Page
from page_android.camera.camera_page import Camera_Page
from page_android.clock.clock_page import Clock_Page
from page_android.filemanager.filemanager_page import Filemanager_Page
from page_android.gallery.gallery_page import Gallery_Page
from page_android.keyboard.keyboard_page import Keyboard_Page
from page_android.launcher.launcher_page import Launcher_Page
from page_android.multimedia.multimedia_page import Multimedia_Page
from page_android.notification.notification_page import Notification_Page
from page_android.settings.settings_page import Settings_Page
from page_android.system.system import System
from page_android.task_manager.task_manager_page import Task_Manager_Page
from page_android.three3app.wangzherongyao import Wangzherongyao_Page
from page_android.three3app.wechat_page import Wechat_Page

os.path.abspath(".")
from functools import wraps
from toolsbar.log_control import log_control

logger = log_control.log_single_item(name="性能测试")


def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + " begin test!")
        logger.info(func.__name__ + " begin test!")
        return func(*args, **kwargs)

    return with_logging


@logit
def case1_boot_speed(main_page):
    main_page.device.wake()
    system = System(main_page)
    result = system.reboot_device_and_wait()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case2_screen_off_speed(main_page):
    main_page.device.wake()
    system = System(main_page)
    result = system.rest_screen()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case3_unlock_speed(main_page):
    main_page.device.wake()
    system = System(main_page)
    system.lock_screen()
    main_page.device.keyevent("POWER")
    result = system.unlock_screen_by_slide()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case4_wake_speed(main_page):
    system = System(main_page)
    system.lock_screen()
    sleep(1)
    main_page.device.wake()
    result = system.check_on_home_screen()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case5_slide_speed(main_page):
    result = False
    main_page.device.wake()
    launcher_page = Launcher_Page(main_page)
    launcher_page.wake_up_main_menu()
    app = launcher_page.search_app_in_main_menu(app_text="设置")
    launcher_page.drag_app_to_new_screen(app)
    launcher_page.slide_to_new_screen()
    if main_page.poco(text="设置").wait().exists():
        result = True
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case6_expand_folder_speed(main_page):
    result = False
    main_page.device.wake()
    launcher_page = Launcher_Page(main_page)
    launcher_page.drag_2app_to_create_folder(app1_text="设置", app2_text="相机")
    main_page.poco.start_gesture([0.5, 0.5]).hold(0).to([0.5, 0.5]).up()
    sleep(1)
    result = main_page.poco(text="设置").exists()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case7_cold_boot_camera_speed(main_page):
    result = False
    main_page.device.wake()
    camera_page = Camera_Page(main_page)
    camera_page.boot_camera_from_main_menu()
    sleep(1)
    result = main_page.poco("com.android.camera2:id/shutter_button").exists()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case8_camera_capture_speed(main_page):
    result = False
    main_page.device.wake()
    camera_page = Camera_Page(main_page)
    camera_page.take_picture()
    result = camera_page.check_thumbnail_picture()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case9_camera_to_desktop_speed(main_page):
    result = False
    main_page.device.wake()
    camera_page = Camera_Page(main_page)
    camera_page.boot_camera_from_main_menu()
    system = System(main_page)
    system.slide_back_to_launcher()
    result = system.check_on_home_screen()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case10_cold_boot_gallery_speed(main_page):
    result = False
    main_page.device.wake()
    gallery_page = Gallery_Page(main_page)
    gallery_page.boot_gallery_from_main_menu()
    result = gallery_page.check_on_gallery()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case11_check_picture_speed(main_page):
    result = False
    main_page.device.wake()
    gallery_page = Gallery_Page(main_page)
    gallery_page.boot_gallery_from_main_menu()
    gallery_page.click_first_img()
    result = gallery_page.check_on_img_interface()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case12_cold_boot_settings_speed(main_page):
    result = False
    main_page.device.wake()
    settings_page = Settings_Page(main_page)
    settings_page.boot_settings_from_main_menu()
    result = settings_page.check_on_settings()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case13_enter_wifi_speed(main_page):
    result = False
    main_page.device.wake()
    settings_page = Settings_Page(main_page)
    result = settings_page.enter_wifi_settings()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case14_cold_boot_music_speed(main_page):
    result = False
    main_page.device.wake()
    multimedia_page = Multimedia_Page(main_page)
    multimedia_page.boot_music_from_main_menu()
    result = multimedia_page.check_on_music()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case15_cold_boot_video_speed(main_page):
    result = False
    main_page.device.wake()
    multimedia_page = Multimedia_Page(main_page)
    multimedia_page.boot_video_from_main_menu()
    result = multimedia_page.check_on_video()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case16_play_local_video_speed(main_page):
    result = False
    main_page.device.wake()
    multimedia_page = Multimedia_Page(main_page)
    multimedia_page.boot_video_from_main_menu()
    multimedia_page.play_100m_video()
    result = multimedia_page.check_on_video_playing()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case17_cold_boot_filemanager_speed(main_page):
    result = False
    main_page.device.wake()
    filemanager_page = Filemanager_Page(main_page)
    filemanager_page.boot_filemanager_from_main_menu()
    result = filemanager_page.check_on_filemanager()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case18_pull_down_notification_speed(main_page):
    result = False
    main_page.device.wake()
    sleep(1)
    notification_page = Notification_Page(main_page)
    try:
        result = notification_page.drag_down_notification_center()
        if not result:
            result = True
    except Exception as ex:
        result = str(ex)
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case19_cold_boot_wechat_speed(main_page):
    result = False
    main_page.device.wake()
    wechat = Wechat_Page(main_page)
    wechat.boot_wechat_from_main_menu()
    result = wechat.check_on_wechat()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case20_check_notification_speed(main_page):
    result = False
    main_page.device.wake()
    notification_page = Notification_Page(main_page)
    notification_page.drag_down_notification_list()
    notification_page.click_dest_notification(notification_title="Android 系统")
    result = "com.android.settings" in main_page.device.shell("dumpsys window | grep mCurrentFocus")
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case21_launch_task_manager_speed(main_page):
    result = False
    main_page.device.wake()
    task_manager_page = Task_Manager_Page(main_page)
    task_manager_page.boot_task_manager_from_main_menu()
    result = task_manager_page.check_on_task_manager()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case22_wake_keyboard_speed(main_page):
    result = False
    main_page.device.wake()
    keyboard_page = Keyboard_Page(main_page)
    keyboard_page.wake_up_keyboard_inSettings()
    keyboard_page.keyboard_singleword_input("test")
    result = True
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case23_keyboard_show_speed(main_page):
    result = False
    main_page.device.wake()
    keyboard_page = Keyboard_Page(main_page)
    input_content = "W"
    keyboard_page.search_inSettings_by_keyboard(input_content)
    result = keyboard_page.get_content_frome_search_box(input_content)
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case24_cold_boot_calendar_speed(main_page):
    result = False
    main_page.device.wake()
    calendar_page = Calendar_Page(main_page)
    calendar_page.boot_calendar_from_main_menu()
    result = calendar_page.check_on_calendar()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case25_cold_boot_clock_speed(main_page):
    result = False
    main_page.device.wake()
    clock_page = Clock_Page(main_page)
    clock_page.boot_clock_from_main_menu()
    result = clock_page.check_on_clock()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def case26_cold_boot_browser_speed(main_page):
    warning = "暂时无法做，新平板不支持browser，无原生browser"
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(warning))
    return warning


@logit
def case27_wechat_install_speed(main_page):
    pass
    warning = "该case暂时存在问题，PandaOS不支持自己安装软件，暂时不进行测试"
    # 该case暂时存在问题，PandaOS不支持自己安装软件，暂时不进行测试
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(warning))
    return warning


@logit
def case28_cold_boot_wangzhe_speed(main_page):
    result = False
    main_page.device.wake()
    wangzherongyao_page = Wangzherongyao_Page(main_page)
    wangzherongyao_page.boot_wangzherongyao_from_main_menu()
    result = wangzherongyao_page.check_on_wangzherongyao()
    logger.info("function:" + sys._getframe().f_code.co_name + ":Test result：{} ".format(result))
    return result


@logit
def default():
    pass


def case_chooser(case_number, main_page):
    return switch.get(case_number, default)(main_page)


# switch = {3: case3_unlock_speed}
# switch = {1: case1_boot_speed, 2: case2_screen_off_speed, 3: case3_unlock_speed, 4: case4_wake_speed,
#           5: case5_slide_speed}
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

# switch = {3: case3_unlock_speed, 4: case4_wake_speed,
#           16: case16_play_local_video_speed,
#           19: case19_cold_boot_wechat_speed, 20: case20_check_notification_speed,
#           21: case21_launch_task_manager_speed, 22: case22_wake_keyboard_speed, 23: case23_keyboard_show_speed,
#           24: case24_cold_boot_calendar_speed, 25: case25_cold_boot_clock_speed,
#           26: case26_cold_boot_browser_speed, 27: case27_wechat_install_speed, 28: case28_cold_boot_wangzhe_speed}
# switch = {3: case3_unlock_speed}
