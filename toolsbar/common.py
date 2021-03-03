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
"""

device_count = len(SERIAL_NUMBER)


def single_device():
    austinDevice = connect_device("Android:///{}".format(SERIAL_NUMBER[0]))
    return austinDevice


def multiple_device():
    device_list = []
    for serial_no in SERIAL_NUMBER:
        austinDevice = connect_device("Android:///{}".format(serial_no))
        device_list.append(austinDevice)
    return device_list


def init_all_device():
    if len(SERIAL_NUMBER) > 1:
        device_init = multiple_device()
    else:
        device_init = single_device()

    return device_init


test_device = init_all_device()


def logger_config(log_path, logging_name):
    """
    配置log
    :param log_path: 输出log路径
    :param logging_name: 记录中name，可随意
    :return:
    """
    '''
    logger是日志对象，handler是流处理器
    '''

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


# 该log机制用于保存自定义的错误或info信息
logger = logger_config(log_path="./log/{}_{}_{}.log".format(cur_time, "OK", "Fota测试"),
                       logging_name="Fota测试")
