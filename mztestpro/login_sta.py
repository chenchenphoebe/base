#-*- coding:utf-8 -*-
# from selenium import webdriver
# import time
#
# driver = webdriver.Firefox()
# driver.get("http://bbs.meizu.com")
# # driver.set_window_size(600,500)
# driver.maximize_window()
# # driver.find_element_by_xpath("//a/[@target='_blank']").click()
# driver.find_element_by_link_text(u"综合讨论").click()
# tit = driver.title
# print(tit)
#
# driver.quit()
# import sys ,os
# import os,sys
# project_path = os.path.dirname(sys.path[0])
# print project_path#C:\Users\xuchun.chen\PycharmProjects\base
# File = r'C:\Users\xuchun.chen\PycharmProjects\base\mztestpro\login_sta.py'
from selenium import webdriver
import time
#

driver = webdriver.Firefox()
driver.get("https://bbs.meizu.com")
# driver.set_window_size(600,500)
driver.maximize_window()
# driver.find_element_by_xpath("//a/[@target='_blank']").click()
# driver.find_element_by_xpath("//div[@class='scbar_wrap']/input[@name='srchtxt']").send_keys('selenium')
# driver.find_element_by_xpath("//div[@class='scbar_wrap']/button[@name='searchsubmit']").click()
# time.sleep(2)
# driver.find_element_by_xpath("//body[@id='nv_search']/div[@id='wp']/div[@class='cl w']/div[@class='mw']/div[@class='t1']/div[@class='mainbox threadlist']/table[@class='tsearch']/tbody/tr[1]/th[@colspan='6']").text
# driver.find_element_by_xpath("//*tr/th[contains(text(),’对不起，没有找到匹配结果。’)]")
driver.find_element_by_xpath("//div[@class='scbar_wrap']/input[@name='srchtxt']").clear()
driver.find_element_by_xpath("//div[@class='scbar_wrap']/input[@name='srchtxt']").send_keys('selenium')
driver.find_element_by_xpath("//div[@class='scbar_wrap']/button[@name='searchsubmit']").click()
# driver.find_element_by_xpath("//div[@id='wp']/div/div/div/div/div/table/thead/tr/th").text
# driver.find_element_by_link_text(u'首页').click()
# title = driver.find_element_by_xpath("//body/div[@id='hd']/div/div/div/ul/li[2]/a").click()
Text = driver.find_element_by_xpath("//*[@class='tsearch']/thead/tr/th").text
time.sleep(3)
print(Text)
driver.quit()
