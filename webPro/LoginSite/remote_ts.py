#-*- coding:utf-8 -*-
from selenium.webdriver import Remote
import time
#调用Remote方法,启动selenium server
driver = Remote(command_executor="http://127.0.0.1:4444/wd/hub",
                desired_capabilities={
                    'platform':'ANY',
                    'browserName':'firefox'
                    # 'version':'',
                    # 'javascriptEnabled':True
                })
driver.get("http://www.jd.com/")
time.sleep(2)
driver.find_element_by_id('key').send_keys('cloth')
driver.quit()

'''------运用hub和node运行脚本'''
'''
#在不同的浏览器上运行case：
#1.定义主机和浏览器
lists = {
    'http://127.0.0.1:4444/wd/hub':'chrome',
     'http://127.0.0.1:5555/wd/hub':'firefox',
     'http://127.0.0.1:5556/wd/hub':'internet explorer'
}
#2.通过不同的浏览器执行脚本
for host,browser in lists:
    driver = Remote(command_executor=host,
                    desired_capabilities={
                        'platform': 'ANY',
                        'browserName': browser,     
                        # 'version':'',
                        # 'javascriptEnabled':True
                    })
'''