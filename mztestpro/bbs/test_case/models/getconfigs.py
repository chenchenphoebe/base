# -*- coding: UTF-8 -*-

from ConfigParser import ConfigParser
# from globalparameter import project_path
import os,sys
# bbs_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))#C:\Users\xuchun.chen\PycharmProjects\base\mztestpro\bbs
# project_path = os.path.dirname(sys.path[0])#C:\Users\xuchun.chen\PycharmProjects\base\mztestpro\bbs\test_case
class GetConfigs(object):
    """Get a option value from a given section."""
    ####对于其他函数引用当前函数的路径问题,需要一个确定的完整路径，否则引用函数会出错如注释一

    bbs_path = r'C:\Users\xuchun.chen\PycharmProjects\base\mztestpro\bbs'
    def __init__(self):
        self.commonconfig = ConfigParser()
        self.commonconfig.read(self.bbs_path + "\\data\\common.ini")


    def getstr(self, section, option, filename, exc=None):
        """return an string value for the named option."""
        config = ConfigParser()
        try:
            config.read(self.bbs_path + "\\data\\common.ini")
            # print('--------ok1---------')
            print(config.get(section,option))
            # print('--------ok2---------')
            return config.get(section,option)

        except:
            return exc


if __name__ == "__main__":
    project_path = os.path.dirname(sys.path[0])
    print(project_path)
    bbs_path = os.path.abspath(os.path.join(os.getcwd(), "../.."))
    print(bbs_path)
