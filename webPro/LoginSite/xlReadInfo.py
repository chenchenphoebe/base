#-*- coding:utf-8 -*-
import xlrd
import codecs

class ReadInfo():

    def readFile(path):
        # pc = open('info.text','rb')
        # content = pc.readlines()
        # for lin in content:
        #     # for i in range(num):
        #         str = lin.split(';')
        #         name = str[0].split('=')[1]
        #         pad =  str[1].split('=')[1]
        #         print(str[0].split('=')[1])
        #         print(str[1].split('=')[1])
        #         return name,pad
        # 返回的是一个列表，怎么返回一个字典呢？
        # ！！！思路：将返回的用户名和密码放入列表中，再dict(list),但是操作太麻烦
        config = codecs.open(path, 'r', 'utf-8')
        user_info = []
        for lin in config:
            # print(lin.strip())
            user_dict = {}
            result = [ele.strip() for ele in lin.split(';')]
            # result=[u'account=aizi_test@139.com', u'pwd=abc123456']
            for r in result:
                account = [ele.strip() for ele in r.split('=')]
                # print(r.split('='))
                user_dict.update(dict([account]))
            user_info.append(user_dict)
        print(user_info)
        return user_info

    def get_webinfo(path):
        web_info = {}
        config = codecs.open(path, 'r', 'utf-8')
        for line in config:
            result = [ele.strip() for ele in line.split('=')]
            print(result)
            #result=[account,password]列表中只能有两个值
            #dict([result])----->返回一个字典
            #dict的update方法，将字典值更新到字典
            web_info.update(dict([result]))
        # print(web_info)
        return web_info

    def get_read(file):
        pc = open(file, 'rb')
        # print(pc.readlines())输出一个列表
        # print(pc.read(10))读取字符
        # print(pc.readline())读取整行
        for lin in pc.readlines():
            print(lin)

class xlUserInfo(object):
    def __init__(self,path=''):
        self.xl = xlrd.open_workbook(path)

    def floattoStr(self,val):
        if isinstance(val,float):
            val = str(int(float))
        return val

    def get_sheet_info(self):
        listkey = ['account', 'pwd']
        infolist = []
        #range(1,self.sheet.nrows),从第一行开始读取数据(0行为列名称)
        for raw in range(1,self.sheet.nrows):
            #列表解析
            info = [self.floattoStr(val) for val in self.sheet.row_values(raw)]
            #zip():将列表转换成[('account',val),('pwd',val1)]
            tmp = zip(listkey,info)
            #list():将[('account',val),('pwd',val1)]----->{'account':val,'pwd':val1}
            infolist.append(dict(tmp))
        return infolist

    def get_sheetinfo_by_name(self,name):
        self.sheet = self.xl.sheet_by_name(name)
        return self.get_sheet_info()

    def get_sheetinfo_by_index(self,index):
        #index=0表示excel中的sheet1
        self.sheet = self.xl.sheet_by_index(index)
        return self.get_sheet_info()

if __name__ == "__main__":
    # info = ReadInfo()
    # info.readFile(r'C:\Users\xuchun.chen\PycharmProjects\base\webPro\LoginSite\info.text')
    xinfo = xlUserInfo(r'C:\Users\xuchun.chen\PycharmProjects\base\webPro\LoginSite\info.xlsx')
    info = xinfo.get_sheetinfo_by_index(0)
    print(info)



