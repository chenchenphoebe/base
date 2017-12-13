# coding:utf-8

import smtplib
from email.mime.text import MIMEText
from email.header import Header



"""
请确保自己的邮箱的smtp协议开启，都则会出现认证的错误的，如ssh等
"""


sender = "m18128866322@163.com"
# 收件人，可以是多个
receivers = ['m18128866322@163.com']

# 三个参数：第一个为纯文本，第二个plain设置文本格式，第三个为编码格式
message = MIMEText('这里是发送的邮件的主要的内容。Pure Text Here!','plain','utf-8')
message['From'] = Header('来自Mark','utf-8')
message['To'] = Header('测试标题','utf-8')

subject = '哈哈哈哈哈哈，这是邮件的主题 '
message['Subject'] = Header(subject,'utf-8')


try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect('smtp.163.com',25)
    smtpObj.login(sender,'cl02125053')
    smtpObj.sendmail(sender,receivers,message.as_string())
    smtpObj.quit()
    print '邮件已成功发送了'
except smtplib.SMTPException, e:
    print e.message
