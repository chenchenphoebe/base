#-*- coding:utf-8 -*-
import time
import xlsxwriter
class MwriteLog(object):
    def __init__(self,path='./',mode='w'):
        fname = path + time.strftime('%Y-%m-%d-%H-%M-%S')
        self.file = open(path+fname+'.text',mode)

    def MwriteInfo(self,mag):
        self.file.write(mag)

    def MwriteClose(self):
        self.file.close()

class McreateLog(object):

    def __init__(self,path = '',mode = ''):
        fname = path + time.strftime('%Y-%m-%d-%H-%M-%S')
        self.row = 0
        self.xl = xlsxwriter.Workbook(path+fname+'.xls')
        self.style = self.xl.add_format({'bg_color':'red'})#背景变成红色

    def xl_write(self,*args):
        col = 0
        style = ''
        if 'Error' in args:
            style = self.style
        for val in args:
            self.sheet.write_string(self.row,col,val,style)
            col += 1
        self.row += 1

    def log_init(self,sheetname,*title):
        self.sheet = self.xl.add_worksheet(sheetname)
        self.sheet.set_column('A:E',30)
        self.xl_write(*title)

    def log_Write(self,*args):
        self.xl_write(*args)

    def log_close(self):
        self.xl.close()

if __name__ == "__main__":
    # log = MwriteLog()
    # log.MwriteInfo('test ok')
    # log.MwriteClose()
    xl = McreateLog()
    xl.log_init('sheet1','account','pwd','result','reason')
    xl.log_close()