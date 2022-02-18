from toolsbar.common import logger_config

"""
    @description:当前性能测试Log控制
    单例模式控制log对象
"""


class Log_Control(object):
    def log_single_item(self, name):
        logger = logger_config(log_path="./log/{}_{}.log".format("System", name),
                               logging_name="{}_case_record".format(name))
        return logger


log_control = Log_Control()
