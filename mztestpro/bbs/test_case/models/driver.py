#-*- coding:utf-8 -*-
from selenium.webdriver import Remote
#Remote相当于一种浏览器（firefox.chrome.ie等）
# from selenium import webdriver
# driver = webdriver.Firefox()
# driver.get(url)

#启动浏览器
def browser():
    # driver = webdriver.Firefox()
    # host = '127.0.0.1:4444' #运行主机：端口号
    # dc = {'browserName':'firefox'} #指定浏览器
    #需要在cmd窗口启动一个hub和两个node
    '''
    hub：java - jar. / driver / selenium - server - standalone - 3.7.1.jar -role -hub
    node1: java - jar. / driver / selenium - server - standalone - 3.7.1.jar -role -node -port 5555
    node2: java - jar. / driver / selenium - server - standalone - 3.7.1.jar -role -node -port 5556
    '''
    '''
    #定义主机和浏览器
    lists = {"http://127.0.0.1:4444/wd/hub":"chrome",
             "http://127.0.0.1:5555/wd/hub": "firefox",
             "http://127.0.0.1:5556/wd/hub": "internet explorer",
             }
    #通过不同的浏览器执行脚本：
    for host,browser in lists.items():
        driver = Remote(command_executor=host, desired_capabilities={
            'platform': 'ANY',
            'browserName': browser,
            # 'version':'',
            # 'javascriptEnabled':True
        })
    '''
    driver = Remote(command_executor="http://127.0.0.1:4444/wd/hub", desired_capabilities={
                    'platform':'ANY',
                    'browserName':'firefox',
                    # 'version':'',
                    # 'javascriptEnabled':True
                })
    return driver

if __name__ == "__main__":
    dr=browser()
    dr.get("http://www.baidu.com")
    dr.quit()