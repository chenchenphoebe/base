# -*- coding: UTF-8 -*-

from ConfigParser import ConfigParser
import sys


class GetConfigs(object):
    """Get a option value from a given section."""
    
    def __init__(self, module):
        self.commonconfig = ConfigParser()
        self.commonconfig.read(sys.path[0] + "\\common\\common.ini")
        self.testtype = self.commonconfig.get("Default","TEST_TYPE").upper()
        self.networktype = self.commonconfig.get("Default","NETWORK_TYPE")
        self.module = module.capitalize()
        
    def getint(self, section, option, filename, exc=0):
        """return an integer value for the named option.
        return exc if no the option. 
        """
        config = ConfigParser()
        try:
            config.read(sys.path[0] + "\\common\\"+ filename + ".ini")
            return config.getint(section, option)
        except:
            return exc
        
    def getstr(self, section, option, filename, exc=None):
        """return an string value for the named option."""
        config = ConfigParser()
        try:
            config.read(sys.path[0] + "\\common\\"+filename + ".ini")
            return config.get(section,option)
        except:
            return exc
        
    def get_test_times(self):
        """return a dict with name:value for each option
        in the section.
        """
        config = ConfigParser()
        if self.testtype.find("STABILITY") > -1 :
            config.read(sys.path[0] + "\\common\\"+self.testtype+".ini")
        item = config.items(self.module)
        return dict(item)   
            
