#-*- coding:utf-8 -*-
import os

result_dir = r'C:\Users\xuchun.chen\PycharmProjects\base\webPro\test_project\report'
lists = os.listdir(result_dir)
lists.sort(key = lambda  fn :os.path.getmtime(result_dir+"\\"+fn))
print("最新的文件:" + lists[-1])
file = os.path.join(result_dir,lists[-1])
print(file)
