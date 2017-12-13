#-*- coding:utf-8 -*-
import codecs
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
            #返回的是一个列表，怎么返回一个字典呢？
        #！！！思路：将返回的用户名和密码放入列表中，再dict(list),但是操作太麻烦
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
    config = codecs.open(path,'r','utf-8')
    for line in config:
        result = [ele.strip() for ele in line.split('=')]
        print(result)
        web_info.update(dict([result]))
    # print(web_info)
    return web_info

def get_read():
    pc = open('info.text', 'rb')
    # print(pc.readlines())输出一个列表
    # print(pc.read(10))读取字符
    # print(pc.readline())读取整行
    for lin in pc.readlines():
        print(lin)



if __name__ == "__main__":
    # info = get_webinfo(r'C:\Users\xuchun.chen\PycharmProjects\base\webPro\LoginSite\info.text')
    # print(info)
    # for key in info:
    #     print(key,info[key])
    readFile(r'C:\Users\xuchun.chen\PycharmProjects\base\webPro\LoginSite\info.text')
    # get_read()
