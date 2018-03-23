#! /usr/bin/env python
#coding=utf8

import urllib, urllib2, sys
import base64, ssl, time, re, os
import json
import access_token
from PIL import Image

def get_ocr(img, ci, ck):
    try:
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token.get_access_token(ci, ck)
        headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
        params = {
            'image': img,
            'language_type': 'CHN_ENG',
            'detect_language': 'false',
            'probability': 'false'
        }
        params = urllib.urlencode(params)
        request = urllib2.Request(url=url, data=params)
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        response = urllib2.urlopen(request)
        content = response.read()
        return [True, content]
    except Exception as e:
        return [False, e]

def get_img(path):
    f = file(path, 'rb')
    d = f.read()
    f.close()
    return base64.b64encode(d)

def crop_img(path, dst, atype, sx, sy):
    im = Image.open(path)
    img_size = im.size
    x = 0
    y = (200*sx)/1080
    if atype == 1 or atype == 3:
        y = (200*sx)/1080 #chongding # baidu
    elif atype == 2:
        y = (300*sx)/1080 #xigua # youku
    elif atype == 4:
        y = (400*sx)/1080
    w = img_size[0]
    h = img_size[1]/2
    region = im.crop((x, y, x+w, y+h))
    region.save(dst)

def write_html_file(path, data):
    f = file(path, 'w')
    f.write('<!DOCTYPE html>')
    f.write('<html>')
    f.write('<body>')
    data = data.replace('<', '&lt;')
    data = data.replace('<', '&gt;')
    f.write(data)
    f.write('</body>')
    f.write('</html>')
    f.close()

def write_file(path, data):
    f = file(path, 'w')
    f.write(data)
    f.close()

def ocr(path, htmlpath, atype, stype, ci, ck, sx, sy):
    if os.path.exists(htmlpath):
        os.remove(htmlpath)
    dst = os.path.join(os.path.dirname(path), 'r.jpg')
    crop_img(path, dst, atype, sx, sy)
    cont = get_ocr(get_img(dst), ci, ck)
    if cont[0] == False:
        write_html_file(htmlpath, str(cont[1]))
        return [cont[1], '请检查网络','','']
    cont1 = cont[1]
    cont = json.loads(cont1)
    
    if cont.has_key('words_result_num'):
        num = cont['words_result_num']
        if num >= 4:
            result = cont['words_result']
            question = ''
            for i in range(0, num-3):
                question = question + result[i]['words']
            ans1 = result[num-3]['words']
            ans2 = result[num-2]['words']
            ans3 = result[num-1]['words']
            question = re.sub(re.compile('^[\d\.]*'), '', question, count=1)
            return search(question, ans1, ans2, ans3, htmlpath, atype, stype)
    
    write_html_file(htmlpath, cont1)
    return ["识别图片失败", "请查看错误信息", "", ""]
        
def search(q, a1, a2, a3, path, atype, stype=1):
    if atype == 4: #youku
        a1 = a1[2:]
        a2 = a2[2:]
        a3 = a3[2:]
    q1 = q
    url = 'http://www.baidu.com/s?wd='+urllib.quote(q1.encode('gbk'))
    if stype == 1:
        url = 'http://www.baidu.com/s?wd='+urllib.quote(q1.encode('gbk'))
    elif stype == 2:
        url = 'https://m.baidu.com/s?word='+urllib.quote(q1.encode('gbk'))
    elif stype == 3:
        url = 'https://www.sogou.com/sgo?query='+urllib.quote(q1.encode('gbk'))
    elif stype == 4:
        url = 'https://www.google.com/search?q='+urllib.quote(q1.encode('gbk'))
    elif stype == 5:
        url = 'http://cn.bing.com/search?go=搜索&qs=ds&form=QBRE&q='+urllib.quote(q1.encode('utf8'))
    elif stype == 6:
        url = 'https://www.so.com/s?q='+urllib.quote(q1.encode('gbk'))
    
    content = ''
    try:
        request = urllib2.Request(url=url)
        response = urllib2.urlopen(request)
        content = response.read()
    except Exception as e:
        content = e

    #pattern = re.compile('<script.+?</script>', re.MULTILINE|re.DOTALL)
    #content = re.sub(pattern, '', content)
    content = content.replace('<em>', "<span style='font-size:22px;'><em>")
    content = content.replace('</em>', "</em></span>")
    content = content.replace(a1.encode('utf8'), "<span style='font-weight:bold;font-size:32px'><em>"+a1.encode('utf8')+"</em></span>")
    content = content.replace(a2.encode('utf8'), "<span style='font-weight:bold;font-size:32px'><em>"+a2.encode('utf8')+"</em></span>")
    content = content.replace(a3.encode('utf8'), "<span style='font-weight:bold;font-size:32px'><em>"+a3.encode('utf8')+"</em></span>")
    write_file(path, content)
    c1 = content.count(a1.encode('utf8'))
    c2 = content.count(a2.encode('utf8'))
    c3 = content.count(a3.encode('utf8'))

    return [q, a1 + ': ' + str(c1) , a2 + ': ' + str(c2), a3 + ': ' + str(c3) ]

if __name__ == '__main__':
    pass
    