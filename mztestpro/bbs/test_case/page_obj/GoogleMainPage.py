#-*- coding:utf-8 -*-
from BasePage import BasePage


class GoogleMainPage(BasePage):
    """description of class"""
    searchbox = ('ID', 'lst-ib')

    def __init__(self, browser='chrome'):
        BasePage.__init__(browser)

    def inputSearchContent(self, searchContent):
        searchBox = self.findElement(self.searchbox)
        self.type(searchBox, searchContent)
        self.enter(searchBox)