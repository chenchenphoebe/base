#-*- coding:utf-8 -*-
from HTMLTestRunner import HTMLTestRunner
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import unittest
import time
import os

def send_mail(file_new):
    f = open(file_new,"r")
    mail_body = f.read()
    f.close()

    msg = MIMEText(mail_body,'HTML','utf-8')
    msg['Subject'] = Header("自动化测试报告",'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect("smtp.126.com")
    smtp.login("m18128866322@126.com", "cxc02125053")
    smtp.sendmail("m18128866322@126.com", "993372246@qq.com", msg.as_string())
    smtp.quit()
    print("email has send out")

    #----查找测试报告找到最新的测试报告---
def new_report(testreport):
    lists = os.listdir(testreport)
    #按照每个文件修改的时间，从小到大排列
    lists.sort(key=lambda fn:os.path.getmtime(testreport + "\\" + fn))
    file_new = os.path.join(testreport,lists[-1])
    print(file_new)
    return file_new

if __name__ == "__main__":
    test_dir = r'C:\Users\xuchun.chen\PycharmProjects\base\mztestpro\bbs\test_case'
    test_dir1 = './'
    # C:\Users\xuchun.chen\PycharmProjects\base\mztestpro\hello_sta.py
    now = time.strftime("%Y-%m-%d-%H-%M-%S")
    filename = "./bbs/report/"+now+'result.html'
    #fp = open("./bbs/report/"+now+'result.html',"wb")
    fp = open(filename,"wb")
    runner = HTMLTestRunner(stream=fp,title="魅族自动化测试报告",description="环境：windows 7 浏览器：Firefox")
    discover = unittest.defaultTestLoader.discover(test_dir, pattern='search_sta.py')
    runner.run(discover)
    print(time.time())
    fp.close()
    file_path = new_report('./bbs/report/')
    # send_mail(file_path)

