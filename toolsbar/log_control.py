from toolsbar.common import logger_config


class Log_Control(object):
    def log_single_item(self):
        logger = logger_config(log_path="./log/{}_{}.log".format("System", "性能测试_case_record"),
                               logging_name="性能测试_case_record")
        return logger


log_control = Log_Control()
