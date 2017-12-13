# -*- coding: UTF-8 -*-

import sys
from ConfigParser import ConfigParser
from globalparameter import project_path


class GetConfigs(object):
    """Get a option value from a given section."""

    def __init__(self):
        self.commonconfig = ConfigParser()
        self.commonconfig.read(project_path + "\\src\\common\\common.ini")


    def getstr(self, section, option, filename, exc=None):
        """return an string value for the named option."""
        config = ConfigParser()
        try:
            config.read(project_path + "\\src\\common\\common.ini")
            return config.get(section,option)
        except:
            return exc

