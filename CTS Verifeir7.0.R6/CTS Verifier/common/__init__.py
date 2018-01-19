#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python wrapper for Android uiautomator tool."""

import collections
from commands import getoutput as shell
from datetime import datetime
import hashlib
import itertools
import json
import os
from os.path import join, exists
import re
import socket
import subprocess
import sys
import time
import types


####################################
try:
    import cv2
except ImportError, e:
    print e
##################################




if 'localhost' not in os.environ.get('no_proxy', ''):
    os.environ['no_proxy'] = "localhost,%s" % os.environ.get('no_proxy', '')

try:
    import urllib2
except ImportError:
    import urllib.request as urllib2
try:
    from httplib import HTTPException
except:
    from http.client import HTTPException
try:
    if os.name == 'nt':
        import urllib3
except:  # to fix python setup error on Windows.
    pass

__version__ = "0.1.32"
__author__ = "youwei deng"
__all__ = ["device", "Device", "rect", "point", "Selector", "JsonRPCError"]

##########################################################################################
ANDROID_SERIAL = 'ANDROID_SERIAL'
DEFAULT_RIGHT_DIR_NAME = 'pics'
DEFAULT_REPORT_DIR_NAME = 'tmp'
WORKING_DIR_PATH = os.getcwd()
REPORT_DIR_PATH = join(WORKING_DIR_PATH, DEFAULT_REPORT_DIR_NAME)

##########################################################################################



def U(x):
    '''return Python major version '''
    if sys.version_info.major == 2:
        return x.decode('utf-8') if type(x) is str else x
    elif sys.version_info.major == 3:
        return x

#鍏冪�?()鍙傛暟锛歞ef function(*ARG)  
#瀛楀�?{}鍙傛暟锛歞ef function(**ARG)

def param_to_property(*props, **kwprops):
    '''鍙傛暟杞崲涓哄睘鎬�?'''
    if props and kwprops:
        raise SyntaxError("Can not set both props and kwprops at the same time.")

    class Wrapper(object):

        def __init__(self, func):
            self.func = func
            self.kwargs, self.args = {}, []

        def __getattr__(self, attr):
            if kwprops:
                for prop_name, prop_values in kwprops.items():
                    if attr in prop_values and prop_name not in self.kwargs:
                        self.kwargs[prop_name] = attr
                        return self
            elif attr in props:
                self.args.append(attr)
                return self
            raise AttributeError("%s parameter is duplicated or not allowed!" % attr)

        def __call__(self, *args, **kwargs):
            if kwprops:
                kwargs.update(self.kwargs)
                self.kwargs = {}
                return self.func(*args, **kwargs)
            else:
                new_args, self.args = self.args + list(args), []
                return self.func(*new_args, **kwargs)
    return Wrapper
##############################################################
def cmd_line(cmdline):
             return subprocess.Popen(cmdline, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
       
def forward_list():
        '''adb forward --list'''
         
        lines = cmd_line("adb forward --list").decode("utf-8").strip().splitlines()
        return [line.strip().split() for line in lines]
def screenshot_common():
        
        #if SK version <= 16
        #Capture the screenshot via adb and store it in the specified location.
         
     
        #print 'device.serial:'+str(AutomatorServer().adb.device_serial() )
        #print 'device.serial2:'+str(device.get_device_serial() )
        for s, lp, rp in   forward_list():
                    print "serail:"+s
                    #if s ==  device.server.adb.device_serial() :
                    #    print "serail:"+s
                    #    break
                    mtime=datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
                    filename =  "./"+s+"_Error_" +mtime+".png" 
                    png = os.path.basename(filename)
                    print "error : save screen shot at  "+png
                    print cmd_line("adb -s "+str(s)+"shell screencap /data/local/tmp/error.png")
                    #time.sleep(1)
                    print cmd_line("adb -s "+str(s)+"  pull data/local/tmp/error.png %s" +png)
                    cmd_line('adb -s %s shell screencap /sdcard/%s' % (s, png))
                    cmd_line('adb -s %s pull /sdcard/%s %s' % (s, png, filename))


        #print cmd_line("adb -s "+str(AutomatorDevice.get_device_serial())+"shell screencap /data/local/tmp/error.png")
        #print cmd_line("adb -s "+str(AutomatorDevice.get_device_serial())+"  pull data/local/tmp/error.png %s" + png)
        
  
##########################################################################
class JsonRPCError(Exception):
    '''jsonrpc 寮傚父鎵撳嵃'''
    def __init__(self, code, message):
        self.code = int(code)
        self.message = message

    def __str__(self):
        '''##################################################'''
        #screenshot_common("Error_"+self.adb.device_serial()+"_"+datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+".png")
        return "JsonRPC Error code: %d, Message: %s" % (self.code, self.message)
 
 
class JsonRPCMethod(object):
    '''jsonrpc 鏂规�?'''
    if os.name == 'nt':
        pool = urllib3.PoolManager()

    def __init__(self, url, method, timeout=30):
        self.url, self.method, self.timeout = url, method, timeout

    def __call__(self, *args, **kwargs):
        if args and kwargs:
            raise SyntaxError("Could not accept both *args and **kwargs as JSONRPC parameters.")
        data = {"jsonrpc": "2.0", "method": self.method, "id": self.id()}
        if args:
            data["params"] = args
        elif kwargs:
            data["params"] = kwargs
        if os.name == "nt":
            res = self.pool.urlopen("POST",
                                    self.url,
                                    headers={"Content-Type": "application/json"},
                                    body=json.dumps(data).encode("utf-8"),
                                    timeout=self.timeout)
            jsonresult = json.loads(res.data.decode("utf-8"))
        else:
            result = None
            try:
                req = urllib2.Request(self.url,
                                      json.dumps(data).encode("utf-8"),
                                      {"Content-type": "application/json"})
                result = urllib2.urlopen(req, timeout=self.timeout)
                jsonresult = json.loads(result.read().decode("utf-8"))
            finally:
                if result is not None:
                    result.close()
        if "error" in jsonresult and jsonresult["error"]:
            #raise JsonRPCError(jsonresult["error"]["code"], jsonresult["error"]["message"])
            #mtime=datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            #print "error : save screen shot at "+"./Error_" +mtime+".png"
            #print device.get_device_brand()
            #screenshot_common("./Error_" +mtime+".png")
            #screenshot_common("./Error_" +mtime+".png") 
            #screenshot_common()              
            raise JsonRPCError(
                jsonresult["error"]["code"],
                "%s: %s" % (jsonresult["error"]["data"]["exceptionTypeName"], jsonresult["error"]["message"])
            )
        return jsonresult["result"]

    def id(self):
        m = hashlib.md5()
        m.update(("%s at %f" % (self.method, time.time())).encode("utf-8"))
        return m.hexdigest()##鍔犲瘑鍚庣殑缁撴灉锛�?敤鍗佸叚杩涘埗�?�楃涓茶�?�绀恒��?


class JsonRPCClient(object):

    def __init__(self, url, timeout=30, method_class=JsonRPCMethod):
        self.url = url
        self.timeout = timeout
        self.method_class = method_class

    def __getattr__(self, method):
        return self.method_class(self.url, method, timeout=self.timeout)


class Selector(dict):

    """The class is to build parameters for UiSelector passed to Android device.
    """
    __fields = {
        "text": (0x01, None),  # MASK_TEXT,
        "textContains": (0x02, None),  # MASK_TEXTCONTAINS,
        "textMatches": (0x04, None),  # MASK_TEXTMATCHES,
        "textStartsWith": (0x08, None),  # MASK_TEXTSTARTSWITH,
        "className": (0x10, None),  # MASK_CLASSNAME
        "classNameMatches": (0x20, None),  # MASK_CLASSNAMEMATCHES
        "description": (0x40, None),  # MASK_DESCRIPTION
        "descriptionContains": (0x80, None),  # MASK_DESCRIPTIONCONTAINS
        "descriptionMatches": (0x0100, None),  # MASK_DESCRIPTIONMATCHES
        "descriptionStartsWith": (0x0200, None),  # MASK_DESCRIPTIONSTARTSWITH
        "checkable": (0x0400, False),  # MASK_CHECKABLE
        "checked": (0x0800, False),  # MASK_CHECKED
        "clickable": (0x1000, False),  # MASK_CLICKABLE
        "longClickable": (0x2000, False),  # MASK_LONGCLICKABLE,
        "scrollable": (0x4000, False),  # MASK_SCROLLABLE,
        "enabled": (0x8000, False),  # MASK_ENABLED,
        "focusable": (0x010000, False),  # MASK_FOCUSABLE,
        "focused": (0x020000, False),  # MASK_FOCUSED,
        "selected": (0x040000, False),  # MASK_SELECTED,
        "packageName": (0x080000, None),  # MASK_PACKAGENAME,
        "packageNameMatches": (0x100000, None),  # MASK_PACKAGENAMEMATCHES,
        "resourceId": (0x200000, None),  # MASK_RESOURCEID,
        "resourceIdMatches": (0x400000, None),  # MASK_RESOURCEIDMATCHES,
        "index": (0x800000, 0),  # MASK_INDEX,
        "instance": (0x01000000, 0)  # MASK_INSTANCE,
    }
    __mask, __childOrSibling, __childOrSiblingSelector = "mask", "childOrSibling", "childOrSiblingSelector"

    def __init__(self, **kwargs):
        super(Selector, self).__setitem__(self.__mask, 0)
        super(Selector, self).__setitem__(self.__childOrSibling, [])
        super(Selector, self).__setitem__(self.__childOrSiblingSelector, [])
        for k in kwargs:
            self[k] = kwargs[k]

    def __setitem__(self, k, v):
        if k in self.__fields:
            super(Selector, self).__setitem__(U(k), U(v))
            super(Selector, self).__setitem__(self.__mask, self[self.__mask] | self.__fields[k][0])
        else:
            raise ReferenceError("%s is not allowed." % k)

    def __delitem__(self, k):
        if k in self.__fields:
            super(Selector, self).__delitem__(k)
            super(Selector, self).__setitem__(self.__mask, self[self.__mask] & ~self.__fields[k][0])

    def clone(self):
        kwargs = dict((k, self[k]) for k in self
                      if k not in [self.__mask, self.__childOrSibling, self.__childOrSiblingSelector])
        selector = Selector(**kwargs)
        for v in self[self.__childOrSibling]:
            selector[self.__childOrSibling].append(v)
        for s in self[self.__childOrSiblingSelector]:
            selector[self.__childOrSiblingSelector].append(s.clone())
        return selector

    def child(self, **kwargs):
        self[self.__childOrSibling].append("child")
        self[self.__childOrSiblingSelector].append(Selector(**kwargs))

    def sibling(self, **kwargs):
        self[self.__childOrSibling].append("sibling")
        self[self.__childOrSiblingSelector].append(Selector(**kwargs))

    child_selector, from_parent = child, sibling


def rect(top=0, left=0, bottom=100, right=100):
    return {"top": top, "left": left, "bottom": bottom, "right": right}


def intersect(rect1, rect2):
    top = rect1["top"] if rect1["top"] > rect2["top"] else rect2["top"]
    bottom = rect1["bottom"] if rect1["bottom"] < rect2["bottom"] else rect2["bottom"]
    left = rect1["left"] if rect1["left"] > rect2["left"] else rect2["left"]
    right = rect1["right"] if rect1["right"] < rect2["right"] else rect2["right"]
    return left, top, right, bottom


def point(x=0, y=0):
    return {"x": x, "y": y}


class Adb(object):

    def __init__(self, serial=None):
        self.__adb_cmd = None
        self.default_serial = serial if serial else os.environ.get("ANDROID_SERIAL", None)

    def adb(self):
        if self.__adb_cmd is None:
            if "ANDROID_HOME" in os.environ:
                filename = "adb.exe" if os.name == 'nt' else "adb"
                adb_cmd = os.path.join(os.environ["ANDROID_HOME"], "platform-tools", filename)
                if not os.path.exists(adb_cmd):
                    raise EnvironmentError(
                        "Adb not found in $ANDROID_HOME path: %s." % os.environ["ANDROID_HOME"])
            else:
                import distutils
                if "spawn" not in dir(distutils):
                    import distutils.spawn
                adb_cmd = distutils.spawn.find_executable("adb")
                if adb_cmd:
                    adb_cmd = os.path.realpath(adb_cmd)
                else:
                    raise EnvironmentError("$ANDROID_HOME environment not set.")
            self.__adb_cmd = adb_cmd
        return self.__adb_cmd

    def cmd(self, *args):
        '''adb command, add -s serial by default. return the subprocess.Popen object.'''
        #cmd_line = ["-s", self.device_serial()] + list(args)
        #cmd_line = ["-s", "'%s'" % self.device_serial()] + list(args)
        serial = self.device_serial()
        if serial.find(" ") > 0:  # TODO how to include special chars on command line
            serial = "'%s'" % serial
        cmd_line = ["-s", serial] + list(args)
        return self.raw_cmd(*cmd_line)

    def raw_cmd(self, *args):
        '''adb command. return the subprocess.Popen object.'''
        cmd_line = [self.adb()] + list(args)
        if os.name != "nt":
            cmd_line = [" ".join(cmd_line)]
        return subprocess.Popen(cmd_line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def devices(self):
        '''get a dict of attached devices. key is the device serial, value is device name.'''
        out = self.raw_cmd("devices").communicate()[0].decode("utf-8")
        match = "List of devices attached"
        index = out.find(match)
        if index < 0:
            raise EnvironmentError("adb is not working.")
        return dict([s.split() for s in out[index + len(match):].strip().splitlines() if s.strip()])
        #return dict([s.split("\t") for s in out[index + len(match):].strip().splitlines() if s.strip()])

    def device_serial(self):
        devices = self.devices()
        if not devices:
            raise EnvironmentError("Device not attached.")

        if self.default_serial:
            if self.default_serial not in devices:
                raise EnvironmentError("Device %s not connected!" % self.default_serial)
        elif len(devices) == 1:
            self.default_serial = list(devices.keys())[0]
        else:            
            raise EnvironmentError("Multiple devices attached but default android serial not set.")
        return self.default_serial


    def forward(self, local_port, device_port):
        '''adb port forward. return 0 if success, else non-zero.'''
        return self.cmd("forward", "tcp:%d" % local_port, "tcp:%d" % device_port).wait()
    
    def version(self):
        '''adb version'''
        match = re.search(r"(\d+)\.(\d+)\.(\d+)", self.raw_cmd("version").communicate()[0].decode("utf-8"))
        return [match.group(i) for i in range(4)]

    def forward_list(self):
        '''adb forward --list'''
        version = self.version()
        if int(version[1]) <= 1 and int(version[2]) <= 0 and int(version[3]) < 31:
            raise EnvironmentError("Low adb version.")
        lines = self.raw_cmd("forward", "--list").communicate()[0].decode("utf-8").strip().splitlines()
        return [line.strip().split() for line in lines]

    


_init_local_port = 9007


def next_local_port():
    def is_port_listening(port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex(('127.0.0.1', port))
        s.close()
        return result == 0
    global _init_local_port
    _init_local_port = _init_local_port + 1 if _init_local_port < 32764 else 9008
    while is_port_listening(_init_local_port):
        _init_local_port += 1
    return _init_local_port


class NotFoundHandler(object):

    '''
    Handler for UI Object Not Found exception.
    It's a replacement of UiAutomator watcher on device side.
    '''

    def __init__(self):
        self.__handlers = collections.defaultdict(lambda: {'on': True, 'handlers': []})

    def __get__(self, instance, type):
        return self.__handlers[instance.adb.device_serial()]


class AutomatorServer(object):

    """start and quit rpc server on device.
    """
    __jar_files = {
        "bundle.jar": "libs/bundle.jar",
        "uiautomator-stub.jar": "libs/uiautomator-stub.jar",

    }
     ##########################################################################################
    __apk_files = { 
        "Service.apk": "libs\Service.apk" 
    }
    ##########################################################################################  
    handlers = NotFoundHandler()  # handler UI Not Found exception

    def __init__(self, serial=None, local_port=None):
        self.uiautomator_process = None
        self.adb = Adb(serial=serial)
        
        self.device_port = 9008
        if local_port:
            self.local_port = local_port
        else:
            try:  # first we will try to use the local port already adb forwarded
                for s, lp, rp in self.adb.forward_list():
                    if s == self.adb.device_serial() and rp == 'tcp:%d' % self.device_port:
                        
                        self.local_port = int(lp[4:])
                        break
                else:
                    self.local_port = next_local_port()
            except:
                self.local_port = next_local_port()

    def push(self):
        base_dir = os.path.dirname(__file__) #os.path.abspath(sys.argv[0])
        #print "base_dir:"+base_dir
        for jar, url in self.__jar_files.items():
            filename = os.path.join(base_dir, url)
            #print "filename:"+filename
            self.adb.cmd("push", filename, "/data/local/tmp/").wait()
        return list(self.__jar_files.keys())
    #########################################################################
    def installapk(self):
        base_dir = os.path.dirname(__file__) 
        filename=base_dir+"\libs\Service.apk" 
        self.adb.cmd(" install ", filename ).wait()
        #subprocess.call("adb -s "+self.adb.device_serial()+" install "+filename, shell=True)
        #print "install complete"
     
             
         
    #########################################################################

    def download(self, filename, url):
        with open(filename, 'wb') as file:
            res = None
            try:
                res = urllib2.urlopen(url)
                file.write(res.read())
            finally:
                if res is not None:
                    res.close()

    @property
    def jsonrpc(self):
        
        return self.jsonrpc_wrap(timeout=int(os.environ.get("jsonrpc_timeout", 90)))###

    def jsonrpc_wrap(self, timeout):###
        server = self###
        ERROR_CODE_BASE = -32000###
        def _JsonRPCMethod(url, method, timeout, restart=True):
            _method_obj = JsonRPCMethod(url, method, timeout)

            def wrapper(*args, **kwargs):
                URLError = urllib3.exceptions.HTTPError if os.name == "nt" else urllib2.URLError
                try:
                    return _method_obj(*args, **kwargs)
                except (URLError, socket.error, HTTPException) as e:
                    if restart:
                        server.stop()
                        server.start(timeout=30)
                        return _JsonRPCMethod(url, method, timeout, False)(*args, **kwargs)
                    else:
                        raise
                except JsonRPCError as e:
                    if e.code >= ERROR_CODE_BASE - 1:
                        server.stop()
                        server.start()
                        return _method_obj(*args, **kwargs)
                    elif e.code == ERROR_CODE_BASE - 2 and self.handlers['on']:  # Not Found
                        try:
                            self.handlers['on'] = False
                            # any handler returns True will break the left handlers
                            any(handler(self.handlers.get('device', None)) for handler in self.handlers['handlers'])
                        finally:
                            self.handlers['on'] = True
                        return _method_obj(*args, **kwargs)
                    raise
            return wrapper

        return JsonRPCClient(self.rpc_uri,
                             #timeout=int(os.environ.get("JSONRPC_TIMEOUT", 90)),
                             timeout=timeout,###
                             method_class=_JsonRPCMethod)

    def __jsonrpc(self):
        return JsonRPCClient(self.rpc_uri, timeout=int(os.environ.get("JSONRPC_TIMEOUT", 90)))

    def start(self, timeout=10):
        files = self.push()
        cmd = list(itertools.chain(["shell", "uiautomator", "runtest"],
                                   files,
                                   ["-c", "com.github.uiautomatorstub.Stub"]))
        self.uiautomator_process = self.adb.cmd(*cmd)
        #print "run uiautomator"
       
        #print "self.local_port:"+str(self.local_port)
        #print "self.device_port:"+str(self.device_port)
        #print "forward to RPC server"
        self.adb.forward(self.local_port, self.device_port)
        ###########################################################################################
        #print "forward to socket server"
        #self.adb.forward(19009,19008 )
        ############################################################################################# 
        #timeout = 10
        while not self.alive and timeout > 0:
            time.sleep(0.1)
            timeout -= 0.1
            
            
        if not self.alive:
               print "LOG: ls -l /data/local/tmp/"+self.adb.cmd("shell ls -l /data/local/tmp/").communicate()[0].decode("utf-8")
               print "LOG: forward --list"+self.adb.cmd("forward --list").communicate()[0].decode("utf-8")
               print "LOG curl:"+self.adb.cmd("curl -d '{\"jsonrpc\":\"2.0\",\"method\":\"deviceInfo\",\"id\":1}' ").communicate()[0].decode("utf-8")
               self.stop()
               files = self.push()
               cmd = list(itertools.chain(["shell", "uiautomator", "runtest"],
                                   files,
                                   ["-c", "com.github.uiautomatorstub.Stub"]))
               self.uiautomator_process = self.adb.cmd(*cmd)       
               self.adb.forward(self.local_port, self.device_port)        
               timeout = 20
               while not self.alive and timeout > 0:
                   time.sleep(0.1)
                   timeout -= 0.1
               if not self.alive: 
                      print "LOG: ls -l /data/local/tmp/ :"+self.adb.cmd("shell ls -l /data/local/tmp/").communicate()[0].decode("utf-8")
                      print cmd_line("forward --list")
                      #print "LOG: forward --list"+self.adb.cmd("forward --list").communicate()[0].decode("utf-8")
                      print cmd_line("curl -d '{\"jsonrpc\":\"2.0\",\"method\":\"deviceInfo\",\"id\":1}' ")
                      #print "LOG curl:"+self.adb.cmd("curl -d '{\"jsonrpc\":\"2.0\",\"method\":\"deviceInfo\",\"id\":1}' ").communicate()[0].decode("utf-8")
                      raise IOError("RPC server not started!")
         

    def ping(self):
        try:
            return self.__jsonrpc().ping()
        except:
            return None

    @property
    def alive(self):
        '''Check if the rpc server is alive.'''
        return self.ping() == "pong"

    def stop(self):
        '''Stop the rpc server.'''
        if self.uiautomator_process and self.uiautomator_process.poll() is None:
            res = None
            try:
                res = urllib2.urlopen(self.stop_uri)
                self.uiautomator_process.wait()
            except:
                self.uiautomator_process.kill()
            finally:
                if res is not None:
                    res.close()
                self.uiautomator_process = None
        try:
            out = self.adb.cmd("shell", "ps", "-C", "uiautomator").communicate()[0].decode("utf-8").strip().splitlines()
            if out:
                index = out[0].split().index("PID")
                for line in out[1:]:
                    if len(line.split()) > index:
                        self.adb.cmd("shell", "kill", "-9", line.split()[index]).wait()
        except:
            pass

    @property
    def stop_uri(self):
        return "http://localhost:%d/stop" % self.local_port

    @property
    def rpc_uri(self):
        return "http://localhost:%d/jsonrpc/0" % self.local_port

###########################################################################################====>
class ExpectException(AssertionError):
    '''A custom exception will be raised by AndroidDevice.'''
    def __init__(self, expect, current, msg):
        AssertionError.__init__(self)
        self.expect = expect
        self.current = current
        self.msg = msg

    def __str__(self):
        return repr(self.msg)
##############################################################################################====<
class AutomatorDevice(object):

    '''uiautomator wrapper of android device'''

    __orientation = (  # device orientation
        (0, "natural", "n", 0),
        (1, "left", "l", 90),
        (2, "upsidedown", "u", 180),
        (3, "right", "r", 270)
    )
    __alias = {
        "width": "displayWidth",
        "height": "displayHeight"
    }

    def __init__(self, serial=None, local_port=None):
        #print "object: "+str(object)
        self.server = AutomatorServer(serial=serial, local_port=local_port)
################################################################################################
        #print "serial:"+str(serial)
        self.serial = os.environ[ANDROID_SERIAL] if os.environ.has_key(ANDROID_SERIAL) else None
        #print "serial:"+str(serial)
        self.working_dir_path = WORKING_DIR_PATH
        self.report_dir_path = REPORT_DIR_PATH
        self.right_dir_path = WORKING_DIR_PATH
        


###############################################################################################
    def __call__(self, **kwargs):
        return AutomatorDeviceObject(self, Selector(**kwargs))

    def __getattr__(self, attr):
        '''alias of fields in info property.'''
        info = self.info
        
        if attr in info:
            return info[attr]
        elif attr in self.__alias:
            return info[self.__alias[attr]]
        else:
            raise AttributeError("%s attribute not found!" % attr)

    @property
    def info(self):
        '''Get the device info.'''
        return self.server.jsonrpc.deviceInfo()
    #############################################################################
    #add image comparison
    #############################################################################
    '''
    def screenshot_common(self, filename):
        
        #if SK version <= 16
        #Capture the screenshot via adb and store it in the specified location.
         
        png = os.path.basename(filename)
        if self.serial:
            shell('adb -s %s shell screencap /sdcard/%s' % (self.serial, png))
            shell('adb -s %s pull /sdcard/%s %s' % (self.serial, png, filename))
        else:
            shell('adb shell screencap /sdcard/%s' % png)
            shell('adb pull /sdcard/%s %s' % (png, filename))
        return True
    '''
    def adaptRotation(self,coord, size, rotation=0):
        if rotation == 0:
            return coord
        elif rotation == 90:
            height, width = size
            x_coord, y_coord = coord
            x = y_coord
            y = width - x_coord
            return (x, y)
        elif rotation == 180:
            height, width = size
            x_coord, y_coord = coord
            x = x_coord
            y = y_coord       
            return (x, y)
        elif rotation == 270:
            height, width = size
            x_coord, y_coord = coord
            x = height - y_coord
            y = x_coord
            return (x, y)
        else:
            return None
    
    def getMatchedCenterOffset(self,subPath, srcPath, threshold=0.03, rotation=0):
        '''
        get the coordinate of the mathced sub image center point.
        @type subPath: string
        @params subPath: the path of searched template. It must be not greater than the source image and have the same data type.
        @type srcPath: string
        @params srcPath: the path of the source image where the search is running.
        @type threshold: float
        @params threshold: the minixum value which used to increase or decrease the matching threshold. 0.01 means at most 1% difference.
                       default is 0.01.
        @type rotation: int
        @params rotation: the degree of rotation. default is closewise. must be oone of 0, 90, 180, 270
        @rtype: tuple
        @return: (x, y) the coordniate tuple of the matched sub image center point. return None if sub image not found or any exception.
        '''
        for img in [subPath, srcPath]: assert os.path.exists(img) , "No such image:  %s" % (img)
        method = cv2.cv.CV_TM_SQDIFF_NORMED #Parameter specifying the comparison method 
        try:
            subImg = cv2.imread(subPath) #Load the sub image
            srcImg = cv2.imread(srcPath) #Load the src image
            result = cv2.matchTemplate(subImg, srcImg, method) #comparision, 瓒婂皬鐨勬暟鍊间唬琛ㄦ洿楂樼殑鍖归厤缁撴�?
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result) #Get the minimum squared difference,minMaxLoc瀵绘壘鐭╅樀(涓�缁存暟缁勫綋浣滃悜閲�?,鐢∕at瀹氫�?) 涓渶灏忓�煎拰鏈�澶у�肩殑浣嶇�?. 
            if minVal <= threshold: #Compared with the expected similarity
                minLocXPoint, minLocYPoint = minLoc
                subImgRow, subImgColumn = subImg.shape[:2]
                centerPoint = (minLocXPoint + int(subImgRow/2), minLocYPoint + int(subImgColumn/2))
                #if image is binary format shape return (w, h) else return (w, h, d)
                (height, width) = srcImg.shape[:2]

                return self.adaptRotation(coord=centerPoint, size=(height, width), rotation=rotation)
            else:
                return None    
        except:
            return None
    
    
    def click_image(self, imagename, waittime=1, threshold=0.01, rotation=0):
        '''
            click  the subPath image exists in the current screen.
            @type imagename: string
            @params imagename: the name  of searched imagename.  
            @type waittime: int
            @params waittime:Delay execution for a given number of seconds after click.  
            @type threshold: float
            @params threshold: the minixum value which used to increase or decrease the matching threshold. 0.01 means at most 1% difference. default is 0.01. 
            @type rotation: int
            @params rotation: the degree of rotation. default is closewise. must be oone of 0, 90, 180, 270  
            @rtype: boolean
            @return: true if the sub image founded in the src image. return false if sub image not found or any exception.
        '''
        '''
        if the wanted image found on current screen click it.
        if the wanted image not found raise exception and set test to be failure.
        '''
        expect_image_path = None
        current_image_path = None
        if os.path.isabs(imagename):
            expect_image_path = imagename
            current_image_path = join(self.report_dir_path, os.path.basename(imagename))
        else:
            expect_image_path = join(self.right_dir_path, imagename)
            current_image_path = join(self.report_dir_path, imagename)       
        print "current_image_path:"+current_image_path

        assert os.path.exists(expect_image_path), 'the local expected image %s not found!' % expect_image_path

        #self.screenshot_common(current_image_path)#====================== 
        self.screenshot(current_image_path)#====================== 
        assert os.path.exists(current_image_path), 'fetch current screen shot image %s failed!' % imagename
        pos = self.getMatchedCenterOffset(subPath=expect_image_path, srcPath=current_image_path, threshold=0.03, rotation=rotation)
        if not pos:
            reason = 'Fail Reason: The wanted image \'%s\' not found on screen!' % imagename
            raise ExpectException(expect_image_path, current_image_path, reason)
        result =self.click(pos[0], pos[1])
        time.sleep(waittime)
        return result
    
    def isMatch(self,subPath, srcPath, threshold=0.03):
            '''
            check wether the subPath image exists in the srcPath image.
            @type subPath: string
            @params subPath: the path of searched template. It must be not greater than the source image and have the same data type.
            @type srcPath: string
            @params srcPath: the path of the source image where the search is running.
            @type threshold: float
            @params threshold: the minixum value which used to increase or decrease the matching threshold. 0.01 means at most 1% difference. default is 0.01. 
            @rtype: boolean
            @return: true if the sub image founded in the src image. return false if sub image not found or any exception.
            '''
            for img in [subPath, srcPath]: assert os.path.exists(img) , 'No such image:  %s' % (img)
            method = cv2.cv.CV_TM_SQDIFF_NORMED #Parameter specifying the comparison method 
            try:
                subImg = cv2.imread(subPath) #Load the sub image
                srcImg = cv2.imread(srcPath) #Load the src image
                result = cv2.matchTemplate(subImg, srcImg, method) #comparision
                minVal = cv2.minMaxLoc(result)[0] #Get the minimum squared difference
                if minVal <= threshold: #Compared with the expected similarity
                    return True
                else:
                    return False
            except:
                return False
    
    
    
    
    def find(self, imagename, interval=2, timeout=4, threshold=0.01):
        '''
            check wether the  image exists in the current scrren in a interval search time within a timeout.
            @type imagename: string
            @params imagename: the name  of searched imagename. 
            @type interval: int
            @params interval: the interval to search the image within the timeout.
            @type timeout: int
            @params timeout: the timeout to search the image. 
             @type threshold: float
            @params threshold: the minixum value which used to increase or decrease the matching threshold. 0.01 means at most 1% difference. default is 0.01. 
            @rtype: boolean
            @return: true if the sub image founded in the src image. return false if sub image not found or any exception.
        '''
        '''
        if the expected image found on current screen return true else return false
        '''
        expect_image_path = None
        current_image_path = None
        if os.path.isabs(imagename):
            expect_image_path = imagename
            current_image_path = join(self.report_dir_path, os.path.basename(imagename))
        else:
            expect_image_path = join(self.right_dir_path, imagename)
            current_image_path = join(self.report_dir_path, imagename)       

        assert os.path.exists(expect_image_path), 'the local expected image %s not found!' % expect_image_path

        begin = time.time()
        isExists = False
        while (time.time() - begin < timeout):
            time.sleep(interval)
            #self.screenshot_common(current_image_path)#=============
            self.screenshot(current_image_path)#====================== 
            isExists = self.isMatch(expect_image_path , current_image_path , threshold)
            if not isExists:
                time.sleep(interval)
                continue
        return isExists
   
    
    def expect(self, imagename, interval=2, timeout=4, threshold=0.01, msg=''):
        '''
            @type imagename: string
            @params imagename: the name  of searched imagename. 
            @type interval: int
            @params interval: the interval to search the image within the timeout.
            @type timeout: int
            @params timeout: the timeout to search the image. 
            @type threshold: float
            @params threshold: the minixum value which used to increase or decrease the matching threshold. 0.01 means at most 1% difference. default is 0.01. 
            @type msg: string
            @params msg: the exception message string to print 
            @rtype: boolean
            @return: true if the sub image founded in the src image. return false if sub image not found or any exception.
        '''
        '''
        if the expected image found on current screen return self 
        else raise exception. set test to be failure.
        '''
        expect_image_path = None
        current_image_path = None
        if os.path.isabs(imagename):
            expect_image_path = imagename
            current_image_path = join(self.report_dir_path, os.path.basename(imagename))
        else:
            expect_image_path = join(self.right_dir_path, imagename)
            current_image_path = join(self.report_dir_path, imagename)       

        assert os.path.exists(expect_image_path), 'the local expected image %s not found!' % expect_image_path
        begin = time.time()
        while (time.time() - begin < timeout):
            #self.screenshot_common(current_image_path)#####===============
            self.screenshot(current_image_path)#####===============
            if self.isMatch(expect_image_path , current_image_path , threshold):
                return self
            time.sleep(interval)
        reason = msg if msg else 'Fail Reason: Image \'%s\' not found on screen!' % imagename
        raise ExpectException(expect_image_path, current_image_path, reason)
    
    ############################################################################
    '''
    def sendcommand(self,command):
        stopservicecmd=" shell am broadcast -a NotifyServiceStop"
        startservicecmd=" shell am broadcast -a NotifyServiceStart"
        print "stop service"
        #subprocess.call("adb -s "+str(self.server.adb.device_serial())+stopservicecmd, shell=True)
        #time.sleep(3) 
        subprocess.call("adb -s "+str(self.server.adb.device_serial())+startservicecmd, shell=True)
        print "start service"
        #time.sleep(5) 
        print "forward to service server"        
        subprocess.call("adb -s "+str(self.server.adb.device_serial())+" forward tcp:19009 tcp;19008", shell=True)
        print "test socket"
        try: 
            clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = clientsocket.connect_ex(('127.0.0.1', 19009))
            print result
            clientsocket.sendall(command)
            data = clientsocket.recv(1024) 
            print 'Received', repr(data)
            clientsocket.close()
            print "close socket"
            return data
        except socket.error,e:
            print '  error creating socket:%s' %e
    '''    
    def get_device_phonenum1(self):    
        return self.server.jsonrpc.getDevicelinenum1()
        
        
    def get_device_serial(self):
        '''get adb devices serial number'''
        return self.server.adb.device_serial()
    
    #def get_pc_domain(self):
    #    '''get pc domain '''
    #    print socket.gethostbyname_ex(socket.gethostname())[0][-9:-4]
    #    return socket.gethostbyname_ex(socket.gethostname())[0][-9:-4]
    
    def get_device_brand(self):
        '''get device brand,result eg: [TCL]'''
        return self.server.jsonrpc.getDeviceBrand()
    
    def get_device_name(self):
        '''get device name,result eg:  [miata3G]'''
        return self.server.jsonrpc.getDeviceName()
    def get_device_manufacturer(self):
        '''get device manufactuer,result eg: [TCT]'''
        return self.server.jsonrpc.getDeviceManufacturer()
    def get_device_model(self):
        '''get device Model,result eg: [6016D]'''
        return self.server.jsonrpc.getDeviceModel()
    def get_current_lang(self):
        '''get current language name'''
        return subprocess.call("adb -s "+self.server.adb.device_serial()+" shell getprop persist.sys.country ", shell=True)

    def get_current_packagename(self):
        '''get Current Package Name,result eg:com.android.dialer'''
        return self.server.jsonrpc.getCurrentPackageName()
    
    def start_activity(self,packagename,activityname):
        '''
            @type packagename: string
            @params packagename: the package name. 
            @type activityname: string
            @params activityname: the activity name.            
            @rtype: string
            @return: the result of sucess or fail information .
        '''
        '''start app activity with packagename/activityname eg:com.android.dialer,com.android.dialer.DialtactsActivity'''
        subprocess.call("adb -s "+self.server.adb.device_serial()+" shell am start  "+packagename+"/"+activityname, shell=True)

    
    def call(self,phonenum):
        '''
            @type phonenum: string
            @params phonenum: the phone number to call.                    
            @rtype: string
            @return: the result of sucess or fail information .
        '''
        '''make mo call to specific phonenumber directly '''     
        subprocess.call("adb -s "+self.server.adb.device_serial()+" shell am start -a android.intent.action.CALL -d tel:"+phonenum, shell=True)
     
    def send_sms(self,phonenum,smsbody):
        '''
            @type phonenum: string
            @params phonenum: the phone number to send.     
            @type smsbody: string
            @params smsbody: the sms  content to send.                 
            @rtype: string
            @return: the result of sucess or fail information .
        '''   
        '''launch sms send screen with phone number and sms body''' 
        subprocess.call("adb -s "+self.server.adb.device_serial()+" shell am start -a android.intent.action.SENDTO -d smsto:"+phonenum+" -e \"sms_body\" "+smsbody, shell=True)
    #def send_mms(self,phonenum,smsbody,content):   
        '''launch mms send screen with phone number and mms body''' 
    #    subprocess.call("adb -s "+self.server.adb.device_serial()+" shell am start -a android.intent.action.SENDTO -d  mmsto:"+phonenum+" -e \"sms_body\" "+smsbody+" -eu android.intent.extra.STREAM "+content, shell=True)
    
    def load_url(self,url):
        '''
            @type url: string
            @params url: the url address to be launch in browser  
            @rtype: string
            @return: the result of sucess or fail information .
        '''   
        '''launch browser with url'''  
        subprocess.call("adb -s "+self.server.adb.device_serial()+" shell am start -a android.intent.action.VIEW -d "+url, shell=True)
    #def open_musicplayer(self,url):
    #    '''launch musicplayer with url''' 
    #    subprocess.call("adb -s "+self.server.adb.device_serial()+" shell am start -a android.intent.action.MUSIC_PLAYER", shell=True)
    def shell_adb(self,shellcmd):
        '''
            @type shellcmd: string
            @params shellcmd:  adb -s serial number+ shellcmd   
            @rtype: string
            @return: the result of sucess or fail information .
        '''  
        '''return adb -s serial number+ shell command string [devices]'''
        return subprocess.Popen("adb -s "+self.server.adb.device_serial()+" "+shellcmd, shell=True,stdout=subprocess.PIPE).communicate()[0]
    def shell_dos(self,shellcmd):
        '''
            @type shellcmd: string
            @params shellcmd: send pure dos command string   
            @rtype: string
            @return: the result of sucess or fail information .
        '''  
        '''return DOS shell command string [adb devices]'''
        return subprocess.Popen(shellcmd, shell=True,stdout=subprocess.PIPE).communicate()[0]
    def get_data_connected_status(self):
        """get the status of data connection.
        @return: "True","False"
        """
      
        status = self.shell_dos("adb -s "+self.server.adb.device_serial()+" shell "+"ifconfig rmnet0")
        returncode = re.search(r'rmnet0:\sip\s(?P<g1>.*)\smask.*\[up', status)
        if not returncode:
            #print ("Cannot connect data.")
            return False
        return True
    def get_data_service_state(self):
        """get data service state to judge whether attach the operator network.
        @return: "2G","3G","LTE","UNKNOWN"
        """
        #print("Check data service status.")
        data = self.shell_dos("adb -s "+self.server.adb.device_serial()+" shell "+"dumpsys telephony.registry")
        if not data:
            pass
            #return None    
        index = data.find("mServiceState")
        if index < 0:
            pass           
            #return None
        index2 = data.find("\n", index)
        assert index2 > 0        
        data = data[index:index2-1].lower()
        #print("Data service state is %s." % (data))   
        if (data.find("edge") > 0 or data.find ("gprs") > 0 or 
            data.find("1xrtt") > 0):
            return "2G"
        elif (data.find("evdo") > 0 or data.find("hsupa") > 0 or 
              data.find("hsdpa") > 0 or data.find("hspa") > 0):
            return "3G"
        elif data.find("lte") > 0:
            return "LTE"            
        else: 
            #print("Data service state is unknown.") 
            return "UNKNOWN"   
    def get_call_state(self):
        """get call service state to judge whether attach the operator network.
        @return:  "False","ringing","incall"
        """
         
        data = self.shell_dos("adb -s "+self.server.adb.device_serial()+" shell "+"dumpsys telephony.registry")
        if not data:
            pass
            #return None    
        index = data.find("mCallState")
        if index < 0:  
            pass         
            #return None
        index2 = data.find("\n", index)
        assert index2 > 0        
        data1 = data[index:index2-1].lower()
        #print("call state is %s." % (data1))
        index3 = data.find("mCallIncomingNumber")
        if index3 < 0:
            pass           
            #return None
        index4 = data.find("\n", index3)
        assert index4 > 0        
        data2 = data[index3+20:index4-1].lower()   
        if (data1.find("0") > 0 ):
            #print "no incoming call"
            return False
            
        elif (data1.find("1") > 0  ):
            #print  "there is an incoming call from:"+data2
            return  "ringing" 
        elif (data1.find("2") > 0  ):
            #print  "there is ongoing call from:"+data2
            return  "incall"                 
        else: 
            #print("call state is unknown.") 
            return "UNKNOWN"   
    def get_incomingcall_number(self):
        """get call service state to judge whether attach the operator network.
        @return:  "None",imcoming/outgoing call number,"UNKNOWN"
        """
         
        data = self.shell_dos("adb -s "+self.server.adb.device_serial()+" shell "+"dumpsys telephony.registry")
        if not data:
            pass
            #return None    
        index = data.find("mCallState")
        if index < 0: 
            pass          
            #return None
        index2 = data.find("\n", index)
        assert index2 > 0        
        data1 = data[index:index2-1].lower()
        #print("call state is %s." % (data1))
        index3 = data.find("mCallIncomingNumber")
        if index3 < 0:   
            pass        
            #return None
        index4 = data.find("\n", index3)
        assert index4 > 0        
        data2 = data[index3+20:index4-1].lower()   
        if (data1.find("0") > 0 ):
            # print "no incoming call"
            pass
            #return None            
        elif (data1.find("1") > 0  ):
            #print  "there is an incoming call from:"+data2
            return  data2 
        elif (data1.find("2") > 0  ):
            #print  "there is ongoing call from:"+data2
            return  data2                 
        else: 
            #print("call state is unknown.") 
            return "UNKNOWN" 
    def get_meminfo(self):
        '''get memory info'''
        return self.shell_dos("adb -s "+self.server.adb.device_serial()+" shell "+"dumpsys meminfo")
    def get_cpuinfo(self):
        '''get cpu info'''
        return self.shell_dos("adb -s "+self.server.adb.device_serial()+" shell "+"dumpsys cpuinfo")
    
    def delay(self,seconds):
        '''delay for seconds'''
        time.sleep(seconds)
    def press_call(self):
        '''Press KeyCODE_CALL button'''
        return self.server.jsonrpc.pressKeyCode(5)
    def press_endcall(self):
        '''press keycode_endcall button'''
        return self.server.jsonrpc.pressKeyCode(6)
    def get_qcom_log(self):
        '''get all qualcom log to current script path,same as QCOM_PULL_ALL_INFO.bat'''
        projectname=self.get_device_name()
        date=time.strftime('%Y-%m-%d-%H-%I-%M',time.localtime(time.time()))
        deviceid=self.server.adb.device_serial()
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" devices")
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /sdcard/TCTReport "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/")
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /sdcard1/TCTReport "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/TCTReport")
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /storage/sdcard0/ram_dump "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/ram_dump/sdcard0")
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /storage/sdcard1/ram_dump "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/ram_dump/sdcard1")
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull  /data/anr "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/anr")
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" shell ls /data/anr -l > "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/anr_date.txt") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" shell ls /data/ram_console -l > "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/ram_console_date.txt") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /data/jrdrecord "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/jrdrecord") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /sdcard/btsnoop_hci.log "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/btlog/btsnoop_hci.log") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /data/audio/ "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport//btlog/audio_sample") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /data/rtt_dump*  "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /data/aee_exp "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/data_aee_exp")
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /data/TCTReport "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/data_mobilelog")  
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /data/core "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/data_core") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /storage/sdcard0/batterylog "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/batterylog") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /storage/sdcard1/batterylog "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/batterylog") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /data/tombstones "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/tombstones") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" shell ls /data/tombstones -l > "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/tombstones_date.txt") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /data/ram_console   "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/ram_console") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" pull /mobile_info/   "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/mobile_info") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" ps -t   > "+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/ps.txt") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" top -t -m 5 -n 3  >"+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/top.txt") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" service list >"+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/serviceList.txt") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" cat /proc/meminfo >"+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/meminfo") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" procrank 鈥搒 >"+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/procrank.txt") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" cat /proc/zraminfo >"+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/zraminfo") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" cat /proc/bootprof >"+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/bootprof") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" dumpstate  >"+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/dumpstate.txt") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" cat proc/sched_debug  >"+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/sched_debug.txt") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" cat proc/interrupts  >"+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/interrupts.txt") 
        self.shell_dos("adb -s "+self.server.adb.device_serial()+" getprop   >"+projectname+"/"+deviceid+"/"+date+"/"+"TCTReport/android_prop.txt") 

        return "Done"
    
   
    
    #############################################################################

    def click(self, x, y):
        '''click at arbitrary coordinates.'''
        return self.server.jsonrpc.click(x, y)

    def long_click(self, x, y):
        '''long click at arbitrary coordinates.'''
        return self.swipe(x, y, x + 1, y + 1)

    def swipe(self, sx, sy, ex, ey, steps=100):
        '''Swipe from one point to another point.'''
        return self.server.jsonrpc.swipe(sx, sy, ex, ey, steps)

    def drag(self, sx, sy, ex, ey, steps=100):
        '''drag from one point to another point.'''
        return self.server.jsonrpc.drag(sx, sy, ex, ey, steps)

    def dump(self, filename=None, compressed=True):
        '''dump device window and pull to local file.'''
        content = self.server.jsonrpc.dumpWindowHierarchy(compressed, None)
        if filename:
            with open(filename, "wb") as f:
                f.write(content.encode("utf-8"))
        return content

    def screenshot(self, filename, scale=1.0, quality=100):
        '''take screenshot.'''
        device_file = self.server.jsonrpc.takeScreenshot("screenshot.png",
                                                         scale, quality)
        if not device_file:
            return None
        p = self.server.adb.cmd("pull", device_file, filename)
        p.wait()
        self.server.adb.cmd("shell", "rm", device_file).wait()
        return filename if p.returncode is 0 else None

    def freeze_rotation(self, freeze=True):
        '''freeze or unfreeze the device rotation in current status.'''
        self.server.jsonrpc.freezeRotation(freeze)

    @property
    def orientation(self):
        '''
        orienting the devie to left/right or natural.
        left/l:       rotation=90 , displayRotation=1
        right/r:      rotation=270, displayRotation=3
        natural/n:    rotation=0  , displayRotation=0
        upsidedown/u: rotation=180, displayRotation=2
        '''
        return self.__orientation[self.info["displayRotation"]][1]

    @orientation.setter
    def orientation(self, value):
        '''setter of orientation property.'''
        for values in self.__orientation:
            if value in values:
                # can not set upside-down until api level 18.
                self.server.jsonrpc.setOrientation(values[1])
                break
        else:
            raise ValueError("Invalid orientation.")

    @property
    def last_traversed_text(self):
        '''get last traversed text. used in webview for highlighted text.'''
        return self.server.jsonrpc.getLastTraversedText()

    def clear_traversed_text(self):
        '''clear the last traversed text.'''
        self.server.jsonrpc.clearLastTraversedText()

    @property
    def open(self):
        '''
        Open notification or quick settings.
        Usage:
        d.open.notification()
        d.open.quick_settings()
        '''
        @param_to_property(action=["notification", "quick_settings"])
        def _open(action):
            if action == "notification":
                return self.server.jsonrpc.openNotification()
            else:
                return self.server.jsonrpc.openQuickSettings()
        return _open

    @property
    def handlers(self):
        obj = self

        class Handlers(object):

            def on(self, fn):
                if fn not in obj.server.handlers['handlers']:
                    obj.server.handlers['handlers'].append(fn)
                obj.server.handlers['device'] = obj
                return fn

            def off(self, fn):
                if fn in obj.server.handlers['handlers']:
                    obj.server.handlers['handlers'].remove(fn)

        return Handlers()

    @property
    def watchers(self):
        obj = self

        class Watchers(list):

            def __init__(self):
                for watcher in obj.server.jsonrpc.getWatchers():
                    self.append(watcher)

            @property
            def triggered(self):
                return obj.server.jsonrpc.hasAnyWatcherTriggered()

            def remove(self, name=None):
                if name:
                    obj.server.jsonrpc.removeWatcher(name)
                else:
                    for name in self:
                        obj.server.jsonrpc.removeWatcher(name)

            def reset(self):
                obj.server.jsonrpc.resetWatcherTriggers()
                return self

            def run(self):
                obj.server.jsonrpc.runWatchers()
                return self
            
        return Watchers()

    def watcher(self, name):
        obj = self

        class Watcher(object):

            def __init__(self):
                self.__selectors = []

            @property
            def triggered(self):
                return obj.server.jsonrpc.hasWatcherTriggered(name)

            def remove(self):
                obj.server.jsonrpc.removeWatcher(name)

            def when(self, **kwargs):
                self.__selectors.append(Selector(**kwargs))
                return self

            def click(self, **kwargs):
                obj.server.jsonrpc.registerClickUiObjectWatcher(name, self.__selectors, Selector(**kwargs))

            @property
            def press(self):
                @param_to_property(
                    "home", "back", "left", "right", "up", "down", "center",
                    "search", "enter", "delete", "del", "recent", "volume_up",
                    "menu", "volume_down", "volume_mute", "camera", "power","call","end_call")
                def _press(*args):
                    obj.server.jsonrpc.registerPressKeyskWatcher(name, self.__selectors, args)
                return _press
        return Watcher()

    @property
    def press(self):
        '''
        press key via name or key code. Supported key name includes:
        home, back, left, right, up, down, center, menu, search, enter,
        delete(or del), recent(recent apps), volume_up, volume_down,
        volume_mute, camera, power.
        Usage:
        d.press.back()  # press back key
        d.press.menu()  # press home key
        d.press(89)     # press keycode
        '''
        @param_to_property(
            key=["home", "back", "left", "right", "up", "down", "center",
                 "menu", "search", "enter", "delete", "del", "recent",
                 "volume_up", "volume_down", "volume_mute", "camera", "power"]
        )
        def _press(key, meta=None):
            
            if isinstance(key, int):
                return self.server.jsonrpc.pressKeyCode(key, meta) if meta else self.server.jsonrpc.pressKeyCode(key)
            else:
                return self.server.jsonrpc.pressKey(str(key))
        return _press
      
    
    def wakeup(self):
        '''turn on screen in case of screen off.'''
        self.server.jsonrpc.wakeUp()

    def sleep(self):
        '''turn off screen in case of screen on.'''
        self.server.jsonrpc.sleep()

    @property
    def screen(self):
        '''
        Turn on/off screen.
        Usage:
        d.screen.on()
        d.screen.off()
        '''
        @param_to_property(action=["on", "off"])
        def _screen(action):
            return self.wakeup() if action == "on" else self.sleep()
        return _screen

    @property
    def wait(self):
        '''
        Waits for the current application to idle or window update event occurs(default 10 second).
        Usage:
        d.wait.idle(timeout=10000)
        d.wait.update(timeout=10000, package_name="com.android.settings")
        '''
        @param_to_property(action=["idle", "update"])
        def _wait(action, timeout=10000, package_name=None):
            if timeout/1000 + 5 > int(os.environ.get("JSONRPC_TIMEOUT", 90)):###
                 http_timeout = timeout/1000 + 5###
            else:###
                 http_timeout = int(os.environ.get("JSONRPC_TIMEOUT", 90))###
            if action == "idle":
                #return self.server.jsonrpc.waitForIdle(timeout)##
                return self.server.jsonrpc_wrap(timeout=http_timeout).waitForIdle(timeout)###
            elif action == "update":
                #return self.server.jsonrpc.waitForWindowUpdate(package_name, timeout)###
                return self.server.jsonrpc_wrap(timeout=http_timeout).waitForWindowUpdate(package_name, timeout)
        return _wait

    def exists(self, **kwargs):
        '''Check if the specified ui object by kwargs exists.'''
        return self(**kwargs).exists

Device = AutomatorDevice


class AutomatorDeviceUiObject(object):

    '''Represent a UiObject, on which user can perform actions, such as click, set text
    '''

    __alias = {'description': "contentDescription"}

    def __init__(self, device, selector):
        self.device = device
        self.jsonrpc = device.server.jsonrpc
        self.selector = selector

    @property
    def exists(self):
        '''check if the object exists in current window.'''
        return self.jsonrpc.exist(self.selector)

    def __getattr__(self, attr):
        '''alias of fields in info property.'''
        info = self.info
        if attr in info:
            return info[attr]
        elif attr in self.__alias:
            return info[self.__alias[attr]]
        else:
            raise AttributeError("%s attribute not found!" % attr)

    @property
    def info(self):
        '''ui object info.'''
        return self.jsonrpc.objInfo(self.selector)

    def set_text(self, text):
        '''set the text field.'''
        if text in [None, ""]:
            return self.jsonrpc.clearTextField(self.selector)  # TODO no return
        else:
            return self.jsonrpc.setText(self.selector, text)

    def clear_text(self):
        '''clear text. alias for set_text(None).'''
        self.set_text(None)
##############################################################add yw
    def get_text(self):
        '''get the text field of the object.'''
        
        return self.jsonrpc.getText(self.selector)
    
    def getChildCount(self):
        '''Counts the child views immediately under the present UiObject..'''
        
        return self.jsonrpc.getChildCount(self.selector)
    
    def getClassName(self):
        '''Retrieves the className property of the UI element.'''
        return self.jsonrpc.getClassName(self.selector)
    def getPackageName(self):
        '''Reads the view's package property'''
        return self.jsonrpc.getPackageName(self.selector)
    def getContentDescription(self):
        '''Reads the content_desc property of the UI element'''
        return self.jsonrpc.getContentDescription(self.selector)
    def isCheckable(self):
        '''Checks if the UI element's checkable property is currently true.'''
        return self.jsonrpc.isCheckable(self.selector)
    def isChecked(self):
        '''Check if the UI element's checked property is currently true'''
        return self.jsonrpc.isChecked(self.selector)
    def isClickable(self):
        '''Checks if the UI element's clickable property is currently true.'''
        return self.jsonrpc.isClickable(self.selector)
    def isEnabled(self):
        '''Checks if the UI element's enabled property is currently true.'''
        return self.jsonrpc.isEnabled(self.selector)   
    def isFocusable(self):
        '''Check if the UI element's focusable property is currently true'''
        return self.jsonrpc.isFocusable(self.selector) 
    def isFocused(self):
        '''Check if the UI element's focused property is currently true'''
        return self.jsonrpc.isFocused(self.selector) 
    def isLongClickable(self):
        '''Check if the view's long-clickable property is currently true'''
        return self.jsonrpc.isLongClickable(self.selector) 
    def isScrollable(self):
        '''Check if the view's scrollable property is currently true'''
        return self.jsonrpc.isScrollable(self.selector)
    def isSelected(self):
        '''Checks if the UI element's selected property is currently true.'''
        return self.jsonrpc.isSelected(self.selector)
#################################################################
    @property
    def click(self):
        '''
        click on the ui object.
        Usage:
        d(text="Clock").click()  # click on the center of the ui object
        d(text="OK").click.wait(timeout=3000) # click and wait for the new window update
        d(text="John").click.topleft() # click on the topleft of the ui object
        d(text="John").click.bottomright() # click on the bottomright of the ui object
        '''
        @param_to_property(action=["tl", "topleft", "br", "bottomright", "wait"])
        def _click(action=None, timeout=3000):
            if action is None:
                return self.jsonrpc.click(self.selector)
            elif action in ["tl", "topleft", "br", "bottomright"]:
                return self.jsonrpc.click(self.selector, action)
            else:
                return self.jsonrpc.clickAndWaitForNewWindow(self.selector, timeout)
        return _click

    @property
    def long_click(self):
        '''
        Perform a long click action on the object.
        Usage:
        d(text="Image").long_click()  # long click on the center of the ui object
        d(text="Image").long_click.topleft()  # long click on the topleft of the ui object
        d(text="Image").long_click.bottomright()  # long click on the topleft of the ui object
        '''
        @param_to_property(corner=["tl", "topleft", "br", "bottomright"])
        def _long_click(corner=None):
            info = self.info
            if info["longClickable"]:
                if corner:
                    return self.jsonrpc.longClick(self.selector, corner)
                else:
                    return self.jsonrpc.longClick(self.selector)
            else:
                bounds = info.get("visibleBounds") or info.get("bounds")
                if corner in ["tl", "topleft"]:
                    x = (5*bounds["left"] + bounds["right"])/6
                    y = (5*bounds["top"] + bounds["bottom"])/6
                elif corner in ["br", "bottomright"]:
                    x = (bounds["left"] + 5*bounds["right"])/6
                    y = (bounds["top"] + 5*bounds["bottom"])/6
                else:
                    x = (bounds["left"] + bounds["right"])/2
                    y = (bounds["top"] + bounds["bottom"])/2
                return self.device.long_click(x, y)
        return _long_click

    @property
    def drag(self):
        '''
        Drag the ui object to other point or ui object.
        Usage:
        d(text="Clock").drag.to(x=100, y=100)  # drag to point (x,y)
        d(text="Clock").drag.to(text="Remove") # drag to another object
        '''
        def to(obj, *args, **kwargs):
            if len(args) >= 2 or "x" in kwargs or "y" in kwargs:
                drag_to = lambda x, y, steps=100: self.jsonrpc.dragTo(self.selector, x, y, steps)
            else:
                drag_to = lambda steps=100, **kwargs: self.jsonrpc.dragTo(self.selector, Selector(**kwargs), steps)
            return drag_to(*args, **kwargs)
        return type("Drag", (object,), {"to": to})()

    def gesture(self, start1, start2, *args, **kwargs):
        '''
        perform two point gesture.
        Usage:
        d().gesture(startPoint1, startPoint2).to(endPoint1, endPoint2, steps)
        d().gesture(startPoint1, startPoint2, endPoint1, endPoint2, steps)
        '''
        def to(obj_self, end1, end2, steps=100):
            ctp = lambda pt: point(*pt) if type(pt) == tuple else pt  # convert tuple to point
            s1, s2, e1, e2 = ctp(start1), ctp(start2), ctp(end1), ctp(end2)
            return self.jsonrpc.gesture(self.selector, s1, s2, e1, e2, steps)
        obj = type("Gesture", (object,), {"to": to})()
        return obj if len(args) == 0 else to(None, *args, **kwargs)

    @property
    def pinch(self):
        '''
        Perform two point gesture from edge to center(in) or center to edge(out).
        Usages:
        d().pinch.In(percent=100, steps=10)
        d().pinch.Out(percent=100, steps=100)
        '''
        @param_to_property(in_or_out=["In", "Out"])
        def _pinch(in_or_out="Out", percent=100, steps=50):
            if in_or_out in ["Out", "out"]:
                return self.jsonrpc.pinchOut(self.selector, percent, steps)
            elif in_or_out in ["In", "in"]:
                return self.jsonrpc.pinchIn(self.selector, percent, steps)
        return _pinch

    @property
    def swipe(self):
        '''
        Perform swipe action.
        Usages:
        d().swipe.right()
        d().swipe.left(steps=10)
        d().swipe.up(steps=10)
        d().swipe.down()
        d().swipe("right", steps=20)
        '''
        @param_to_property(direction=["up", "down", "right", "left"])
        def _swipe(direction="left", steps=10):
            return self.jsonrpc.swipe(self.selector, direction, steps)
        return _swipe

    @property
    def wait(self):
        '''
        Wait until the ui object gone or exist.
        Usage:
        d(text="Clock").wait.gone()  # wait until it's gone.
        d(text="Settings").wait.exists() # wait until it appears.
        '''
        @param_to_property(action=["exists", "gone"])
        def _wait(action, timeout=3000):
            #method = self.jsonrpc.waitUntilGone if action == "gone" else self.jsonrpc.waitForExists###
            if timeout/1000 + 5 > int(os.environ.get("JSONRPC_TIMEOUT", 90)):
                http_timeout = timeout/1000 + 5
            else:
                http_timeout = int(os.environ.get("JSONRPC_TIMEOUT", 90))
            method = self.device.server.jsonrpc_wrap(timeout=http_timeout).waitUntilGone if action == "gone" else self.device.server.jsonrpc_wrap(timeout=http_timeout).waitForExists
            return method(self.selector, timeout)
        return _wait


class AutomatorDeviceNamedUiObject(AutomatorDeviceUiObject):

    def __init__(self, device, name):
        super(AutomatorDeviceNamedUiObject, self).__init__(device, name)

    def child(self, **kwargs):
        return AutomatorDeviceNamedUiObject(
            self.device,
            self.jsonrpc.getChild(self.selector, Selector(**kwargs))
        )

    def sibling(self, **kwargs):
        return AutomatorDeviceNamedUiObject(
            self.device,
            self.jsonrpc.getFromParent(self.selector, Selector(**kwargs))
        )


class AutomatorDeviceObject(AutomatorDeviceUiObject):

    '''Represent a generic UiObject/UiScrollable/UiCollection,
    on which user can perform actions, such as click, set text
    '''

    def __init__(self, device, selector):
        super(AutomatorDeviceObject, self).__init__(device, selector)

    def child(self, **kwargs):
        '''set childSelector.'''
        self.selector.child(**kwargs)
        return self

    def sibling(self, **kwargs):
        '''set fromParent selector.'''
        self.selector.sibling(**kwargs)
        return self

    child_selector, from_parent = child, sibling

    def child_by_text(self, txt, **kwargs):
        if "allow_scroll_search" in kwargs:
            allow_scroll_search = kwargs.pop("allow_scroll_search")
            name = self.jsonrpc.childByText(
                self.selector,
                Selector(**kwargs),
                txt,
                allow_scroll_search
            )
        else:
            name = self.jsonrpc.childByText(
                self.selector,
                Selector(**kwargs),
                txt
            )
        return AutomatorDeviceNamedUiObject(self.device, name)

    def child_by_description(self, txt, **kwargs):
        if "allow_scroll_search" in kwargs:
            allow_scroll_search = kwargs.pop("allow_scroll_search")
            name = self.jsonrpc.childByDescription(
                self.selector,
                Selector(**kwargs),
                txt,
                allow_scroll_search
            )
        else:
            name = self.jsonrpc.childByDescription(
                self.selector,
                Selector(**kwargs),
                txt
            )
        return AutomatorDeviceNamedUiObject(self.device, name)

    def child_by_instance(self, inst, **kwargs):
        return AutomatorDeviceNamedUiObject(
            self.device,
            self.jsonrpc.childByInstance(self.selector, Selector(**kwargs), inst)
        )

    @property
    def count(self):
        return self.jsonrpc.count(self.selector)

    def __len__(self):
        return self.count

    def __getitem__(self, index):
        count = self.count
        if index >= count:
            raise IndexError()
        elif count == 1:
            return self
        else:
            selector = self.selector.clone()
            selector["instance"] = index
            return AutomatorDeviceObject(self.device, selector)

    def __iter__(self):
        obj, length = self, self.count

        class Iter(object):

            def __init__(self):
                self.index = -1

            def next(self):
                self.index += 1
                if self.index < length:
                    return obj[self.index]
                else:
                    raise StopIteration()
            __next__ = next

        return Iter()

    def right(self, **kwargs):
        def onrightof(rect1, rect2):
            left, top, right, bottom = intersect(rect1, rect2)
            return rect2["left"] - rect1["right"] if top < bottom else -1
        return self.__view_beside(onrightof, **kwargs)

    def left(self, **kwargs):
        def onleftof(rect1, rect2):
            left, top, right, bottom = intersect(rect1, rect2)
            return rect1["left"] - rect2["right"] if top < bottom else -1
        return self.__view_beside(onleftof, **kwargs)

    def up(self, **kwargs):
        def above(rect1, rect2):
            left, top, right, bottom = intersect(rect1, rect2)
            return rect1["top"] - rect2["bottom"] if left < right else -1
        return self.__view_beside(above, **kwargs)

    def down(self, **kwargs):
        def under(rect1, rect2):
            left, top, right, bottom = intersect(rect1, rect2)
            return rect2["top"] - rect1["bottom"] if left < right else -1
        return self.__view_beside(under, **kwargs)

    def __view_beside(self, onsideof, **kwargs):
        bounds = self.info["bounds"]
        min_dist, found = -1, None
        for ui in AutomatorDeviceObject(self.device, Selector(**kwargs)):
            dist = onsideof(bounds, ui.info["bounds"])
            if dist >= 0 and (min_dist < 0 or dist < min_dist):
                min_dist, found = dist, ui
        return found

    @property
    def fling(self):
        '''
        Perform fling action.
        Usage:
        d().fling()  # default vertically, forward
        d().fling.horiz.forward()
        d().fling.vert.backward()
        d().fling.toBeginning(max_swipes=100) # vertically
        d().fling.horiz.toEnd()
        '''
        @param_to_property(
            dimention=["vert", "vertically", "vertical", "horiz", "horizental", "horizentally"],
            action=["forward", "backward", "toBeginning", "toEnd"]
        )
        def _fling(dimention="vert", action="forward", max_swipes=1000):
            vertical = dimention in ["vert", "vertically", "vertical"]
            if action == "forward":
                return self.jsonrpc.flingForward(self.selector, vertical)
            elif action == "backward":
                return self.jsonrpc.flingBackward(self.selector, vertical)
            elif action == "toBeginning":
                return self.jsonrpc.flingToBeginning(self.selector, vertical, max_swipes)
            elif action == "toEnd":
                return self.jsonrpc.flingToEnd(self.selector, vertical, max_swipes)

        return _fling

    @property
    def scroll(self):
        '''
        Perfrom scroll action.
        Usage:
        d().scroll(steps=50) # default vertically and forward
        d().scroll.horiz.forward(steps=100)
        d().scroll.vert.backward(steps=100)
        d().scroll.horiz.toBeginning(steps=100, max_swipes=100)
        d().scroll.vert.toEnd(steps=100)
        d().scroll.horiz.to(text="Clock")
        '''
        def __scroll(vertical, forward, steps=100):
            method = self.jsonrpc.scrollForward if forward else self.jsonrpc.scrollBackward
            return method(self.selector, vertical, steps)

        def __scroll_to_beginning(vertical, steps=100, max_swipes=1000):
            return self.jsonrpc.scrollToBeginning(self.selector, vertical, max_swipes, steps)

        def __scroll_to_end(vertical, steps=100, max_swipes=1000):
            return self.jsonrpc.scrollToEnd(self.selector, vertical, max_swipes, steps)

        def __scroll_to(vertical, **kwargs):
            return self.jsonrpc.scrollTo(self.selector, Selector(**kwargs), vertical)

        @param_to_property(
            dimention=["vert", "vertically", "vertical", "horiz", "horizental", "horizentally"],
            action=["forward", "backward", "toBeginning", "toEnd", "to"])
        def _scroll(dimention="vert", action="forward", **kwargs):
            vertical = dimention in ["vert", "vertically", "vertical"]
            if action in ["forward", "backward"]:
                return __scroll(vertical, action == "forward", **kwargs)
            elif action == "toBeginning":
                return __scroll_to_beginning(vertical, **kwargs)
            elif action == "toEnd":
                return __scroll_to_end(vertical, **kwargs)
            elif action == "to":
                return __scroll_to(vertical, **kwargs)
        return _scroll

device = AutomatorDevice()
