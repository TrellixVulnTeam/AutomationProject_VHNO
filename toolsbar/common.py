# coding = utf8
import logging

from airtest.core.api import *

from config import SERIAL_NUMBER

os.path.abspath(".")
cur_time = time.strftime("%Y%m%d_%H%M%S")

"""
    @File:common.py
    @Author:Bruce
    @Date:2020/12/23
    @Description:公共函数库，存放一些设备操控的函数、变量
"""

"""
    @description:初始化单个设备
"""


def single_device():
    austinDevice = connect_device("Android:///{}".format(SERIAL_NUMBER[0]))
    return austinDevice


"""
    @description:初始化多个设备
"""


def multiple_device():
    device_list = []
    for serial_no in SERIAL_NUMBER:
        austinDevice = connect_device("Android:///{}".format(serial_no))
        device_list.append(austinDevice)
    return device_list


"""
    @description:返回当前以初始化完成的设备
"""


def init_all_device():
    if len(SERIAL_NUMBER) > 1:
        device_init = multiple_device()
    else:
        device_init = single_device()

    return device_init


"""
    @description:logger构建器
    @param:
        log_path:log生成路径
        logging_name:log名称
"""


def logger_config(log_path, logging_name):
    # 获取logger对象,取名
    logger = logging.getLogger(logging_name)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_path, encoding='UTF-8')
    # 生成并设置文件日志格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # 为logger对象添加句柄
    logger.addHandler(handler)

    return logger


"""
    @description:连接设备数量
"""
device_count = len(SERIAL_NUMBER)
"""
    @description:初始化所有设备
"""
test_device = init_all_device()
"""
    @description:创建logger用于保存自定义的错误或info信息
"""
if not os.path.exists("./log"):
    os.makedirs("./log")
logger = logger_config(log_path="./log/{}_{}_{}.log".format(cur_time, "OK", "性能测试"),
                       logging_name="性能测试")
