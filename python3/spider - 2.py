# import urllib2
# import urllib
#
# values = {}
# values['username'] = "8396854@qq.com"
# values['password'] = "wwww"
# data = urllib.urlencode(values)
# url = 'http://www.baidu.com'
# try:
#     request = urllib2.Request(url, data)
#     response = urllib2.urlopen(request)
# except urllib2.URLError, e:
#     print e.reason
#
# print response.read()