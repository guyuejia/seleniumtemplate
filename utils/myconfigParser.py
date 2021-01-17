import configparser

#configparser默认是不区分大小写的，会把所有的大写英文字母转为小写，所以如果在大小写敏感的场合，需要自己重写一个类
class MyConfigParser(configparser.ConfigParser):
    def __init__(self,defaults=None):
        configparser.ConfigParser.__init__(self,defaults=None)
    def optionxform(self, optionstr):
        return optionstr