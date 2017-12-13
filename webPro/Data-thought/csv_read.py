#-*- coding:utf-8 -*-
import csv

date = csv.reader(open("csv_read.csv","r"))
for user in date:
    print(user[1])