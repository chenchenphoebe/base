#-*- coding:utf-8 -*-
from HTMLTestRunner import HTMLTestRunner
from email.mime.text import  MIMEText
from email.header import Header
import smtplib
import unittest
import time
import os

#----定义发送邮件---
def send_mail(file_new):
    f = open(file_new,"wb")
    mail_body = f.read()
    f.close()

    msg = MIMEText(mail_body,"html","utf-8")
    msg['Subject']= Header("自动化测试报告","utf-8")

    smtp = smtplib.SMTP()
    smtp.connect("smtp.126.com")
    smtp.login("m18128866322@126.com","cxc02125053")
    smtp.sendmail("m18128866322@126.com","823974765@qq.com",msg.as_string())
    smtp.quit()
    print("email has send out")

#----查找最新的测试报告目录----
def new_report(testreport):
    lists = os.listdir(testreport)
    lists.sort(key=lambda fn:os.path.getmtime(testreport+"\\"+fn))
    file_new = os.path.join(testreport,lists[-1])
    print(file_new)
    return file_new

if __name__ == "__main__":
    test_dir = r'C:\Users\xuchun.chen\PycharmProjects\base\webPro\test_project\test_case'
    test_report = r'C:\Users\xuchun.chen\PycharmProjects\base\webPro\test_project\report'

    discover = unittest.defaultTestLoader.discover(test_dir,pattern="test_*.py")
    now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
    fp = open(r'C:\Users\xuchun.chen\PycharmProjects\base\webPro\test_project\report\result%s.html' % now, "wb")
    runner = HTMLTestRunner(stream=fp,title="测试报告",description="用例执行情况")
    runner.run(discover)
    fp.close()
    print(time.time())

    new_report = new_report(test_report)
    send_mail(new_report)


