#-*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# smtpserver = "mail.sina.com"
# user = "13519149411@sina.cn"
    # password = "cxc02125053"
# sender = "13519149411@sina.cn"
# receiver = "xuchun.chen@tcl.com"
subject = "python email test"

#编写HTMl格式的邮件正文
msg = MIMEText('<html><h1>你好！</h1></html>','html','utf-8')
msg[subject] = Header(subject,'utf-8')

#连接发送邮件
smtp = smtplib.SMTP()
smtp.connect("smtp.126.com")
smtp.login("m18128866322@126.com", "cxc02125053")
smtp.sendmail("m18128866322@126.com", "xuchun.chen@tcl.com", msg.as_string())
smtp.quit()
print("email has send out")