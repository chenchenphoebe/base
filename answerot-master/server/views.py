# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import time, sys, os, subprocess
import answerrot, adb
# Create your views here.
def index(request):
    #print os.getcwd()
    htmlpath = 'server/templates/server/result.html'
    if not os.path.exists(htmlpath):
        answerrot.write_html_file(htmlpath, '')

    if request.method == 'POST':
        return  render(request, 'server/index.html', {"result": "error", "time": ""})
    if not request.GET.has_key('submit'):
        return  render(request, 'server/index.html', {"result": ""})
    atype = '1'
    if not request.GET.has_key('type'):
        #return   render(request, 'server/index.html', {"result": "参数错误", "time": ""})
        pass
    else:
        atype = request.GET['type']
    search = '1'
    if request.GET.has_key('type'):
        search = request.GET['search']
        
    start = time.time()
    imgpath = os.path.join(os.getcwd(), 'server\\img\\1.jpg')
    
    e  = adb.get_pic(imgpath)
    if e != True:
        #return  render(reverse('server/config.html', {"result": "", "msg": e + ", Check device number"}))
        return HttpResponseRedirect('/config/?msg='+e + ", Check device number")  

    ci = adb.get_config("client_id")
    if ci == "":
        return HttpResponseRedirect('/config/?msg=Config client_id')  
    ck = adb.get_config("client_secret")
    if ck == "":
        return HttpResponseRedirect('/config/?msg=Config client_secret')

    sx = adb.get_config("sx")
    if sx == "":
        return HttpResponseRedirect('/config/?msg=Config screen width')  
    sy = adb.get_config("sy")
    if sy == "":
        return HttpResponseRedirect('/config/?msg=Config screen height')  

    res = answerrot.ocr(imgpath, htmlpath, int(atype), int(search), ci, ck, int(sx), int(sy))

    return  render(request, 'server/index.html', {"result": res, "time": time.time()-start})

def result(request):
    return  render(request, 'server/result.html')

def config(request):
    if request.method == 'POST':
        return  render(request, 'server/config.html', {"msg": "error"})

    device = ""
    screenx = ""
    screeny = ""
    ci = ""
    ck = ""
    msg = ''
    if request.GET.has_key('device'):
        device = request.GET['device']
    if request.GET.has_key('screenx'):
        screenx = request.GET['screenx']
    if request.GET.has_key('screeny'):
        screeny = request.GET['screeny']
    if request.GET.has_key('client_id'):
        ci = request.GET['client_id']
    if request.GET.has_key('client_secret'):
        ck = request.GET['client_secret']
    if request.GET.has_key('msg'):
        msg = request.GET['msg']

    ret = adb.set_config(device, screenx, screeny, ci, ck)
    if msg == '':
        msg = ret['msg']
    return render(request, 'server/config.html', {"result": ret, "msg":msg})