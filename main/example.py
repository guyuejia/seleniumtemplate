from utils.chromebrowser import Chromebrowser
from utils.mylogging import Mylogging

logger = Mylogging("mylogger").get_logger()
browser = Chromebrowser().get_browser()
browser.get("https://www.baidu.com")
try:
    browser.find_element_by_id("ttt")
except Exception as e:
    logger.error("查找元素报错！")

logger.info("程序结束")