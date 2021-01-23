import logging
import logging.config
import yaml

class Mylogging():
    def __init__(self):
        configPath = r"../configs/logging.yml"
        with open(configPath, 'r') as f_conf:
            dict_conf = yaml.load(f_conf, Loader=yaml.FullLoader)
        logging.config.dictConfig(dict_conf)
    #loggername必须是配置文件中定义的logger
    def get_logger(self,loggerName):
        return logging.getLogger(loggerName)

logger = Mylogging().get_logger("mylogger")

if __name__ == '__main__':
    logger.info("this is test!")
    logger.error("this is error log")