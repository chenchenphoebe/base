#-*- coding:utf-8 -*-
from selenium import webdriver
from time import sleep,ctime
from threading import Thread

#测试用例
def test_baidu(browser,search):
    print('start:%s'%ctime())
    print('browaser:%s'%browser)
    if browser == "ie":
        driver = webdriver.Ie()
    elif browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "ff":
        driver = webdriver.Firefox()
    else:
        print("输入信息有误")

    driver.get('http://www.baidu.com')
    driver.find_element_by_id('kw').send_keys(search)
    driver.find_element_by_id('su').click()
    sleep(2)
    driver.quit()

if __name__ == '__main__':
    lists = {'chrome': 'threading','ie':'webdriver','ff':'python'}
    threads =[]

    files = range(len(lists))
    #创建线程
    for broswer,search in lists.items():
        t = Thread(target=test_baidu,args=(broswer,search))
        threads.append(t)

    #启动线程
    for t in files:
        threads[t].start()
    for t in files:
        threads[t].join()

    print('end:%s'%ctime())









