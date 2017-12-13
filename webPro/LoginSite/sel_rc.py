#-*- coding:utf-8 -*-
#selenium 这个类找不到
from selenium import selenium

sel = selenium("localhost",4444,"*firefox","http://www.jd.com/")
sel.start()

sel.open('/')
sel.type('id=key','selenium_grid')
sel.stop()