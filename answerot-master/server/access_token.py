#! /usr/bin/env python
#coding=utf-8

import urllib, urllib2, sys
import ssl
import json
    
    
def get_access_token(client_id, client_secret):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK    
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' % (client_id, client_secret)
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        k = json.loads(content)
        if k.has_key('access_token'):
            return k['access_token']
    return None    
