#-*- coding:utf-8 -*-
from selenium.webdriver import Remote

sel = Remote("localhost",4444,"*firefox","http://www.baidu.com")
sel.start()

sel.open('/')
sel.type("id = kw","selenium grid")
sel.click()
sel.wait_for_page_to_load("30000")

sel.stop()
