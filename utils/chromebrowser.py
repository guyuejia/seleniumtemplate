from selenium import webdriver
from utils.myconfigParser import MyConfigParser
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import os

class Chromebrowser():
    __implicitly_wait_time = 0
    __driverpath = None
    #构造函数，主要用于读取配置文件，并完成浏览器的初始化配置
    def __init__(self):
        self.browser = None
        self.option =webdriver.ChromeOptions()
        #从配置文件中读取浏览器相关初始化配置
        configPath = r"../configs/browser.config"
        conf = MyConfigParser()
        conf.read(configPath, encoding='utf-8')
        basic_conf =dict(conf.items("BASIC"))
        option_conf = dict(conf.items("OPTION"))
        driverpath = basic_conf["driverpath"]
        downdir = basic_conf["downdir"]
        pageLoadStrategy = basic_conf["pageLoadStrategy"]
        implicitly_wait_time = basic_conf["implicitly_wait_time"]
        is_headless = option_conf["isheadless"]
        windowsize = option_conf["windowsize"]

        #设置隐式等待时间给类私有属性
        if implicitly_wait_time == "":
            self.__implicitly_wait_time = 0
        else:
            self.__implicitly_wait_time = int(implicitly_wait_time)

        #配置驱动程序
        if not os.path.isabs(driverpath):
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            driverpath =os.path.join(project_dir, driverpath)
        self.__driverpath = driverpath


        #判断配置的文件下载路径是否为绝对路径
        if not os.path.isabs((downdir)):
            project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            downdir = os.path.join(project_dir, downdir)
        prefs = {"download.default_directory": downdir}
        self.option.add_experimental_option("prefs", prefs)

        #配置加载策略
        if pageLoadStrategy != "":
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities["pageLoadStrategy"] = pageLoadStrategy

        #如果配置文件中给出了窗口大小，就照此设置；
        if windowsize != "":
            self.option.add_argument("--window-size={}".format(windowsize));

        #配置是否为无头浏览
        if is_headless == "True":
            self.option.add_argument('--headless')
            self.option.add_argument('--no-sandbox')
            self.option.add_argument('--disable-dev-shm-usage')


    def get_browser(self):
        self.browser = webdriver.Chrome(self.__driverpath,options=self.option)
        print(self.__implicitly_wait_time)
        self.browser.implicitly_wait(self.__implicitly_wait_time)
        #判断是否设置了无头浏览器，是的话，设置允许下载页面文件
        if ("--headless" in self.option.arguments):
            #获取下载文件的保存目录
            downdir = self.option.experimental_options["prefs"]["download.default_directory"]
            self.enable_download_in_headless_chrome(downdir)
        else:
            #如果不是无头浏览，不管配置里面设置的页面大小多少，都将页面最大化
            self.browser.maximize_window()
        return self.browser


    def enable_download_in_headless_chrome(self, download_dir):
        # add missing support for chrome "send_command"  to selenium webdriver
        self.browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        self.browser.execute("send_command", params)

    def __del__(self):
        self.browser.quit()

if __name__ == '__main__':
    browser = Chromebrowser().get_browser()
    browser.get("https://www.baidu.com")
    browser.find_element_by_id("ttt")


