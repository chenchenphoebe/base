#-*- coding:utf-8 -*-
# import sys
# sys.path.append("../..")
import os,sys
sys.path.append("../..")
project_path = os.path.dirname(sys.path[0])
print project_path#当前文件的父文件夹
print sys.path[0]#当前文件目录文件夹
project_path= r'C:\Users\xuchun.chen\PycharmProjects\base\mztestpro\bbs\test_case'
sys.path[0]=r'C:\Users\xuchun.chen\PycharmProjects\base\mztestpro\bbs\test_case\models'
log_path = project_path+"\\data\\mylog.log"
# dirs = os.path.join( os.path.dirname(__file__),'../..')
dirs = os.path.dirname(__file__)
print dirs#当前文件目录
dd = os.path.dirname(os.path.abspath(__file__))
print dd#C:\Users\xuchun.chen\PycharmProjects\base\mztestpro\bbs\test_case\models
print os.path.dirname(__file__)#C:\Users\xuchun.chen\PycharmProjects\base\mztestpro\bbs\test_case\models
file = os.path.abspath(__file__)#C:\Users\xuchun.chen\PycharmProjects\base\mztestpro\bbs\test_case\models\path.py
print(file)#当前文件的完整路径
back = sys.path.append("../..")#回到上上级目录
print(back)


