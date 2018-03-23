
import subprocess,re 
import ConfigParser

def set_config(device, sx, sy, ci, ck):
    device_info = get_device()
    result = {
        "device": "",
        "sx": "",
        "sy": "",
        "client_id": "",
        "client_secret": "",
        "msg": "",
        "device_info": device_info,
    }
    cf = ConfigParser.ConfigParser()
    cf.read("server\\config.ini")
    if device == '' and sx=='' and sy == '':
        if len(cf.sections())<=0:
            return result
        try:
            result['sx']= cf.get('config', 'sx')
        except:
            pass
        try:
            result['sy'] = cf.get('config', 'sy')
        except:
            pass
        try:
            result['device'] = cf.get('config', 'device')
        except:
            pass
        try:
            result['client_id'] = cf.get('config', 'client_id')
        except:
            pass
        try:
            result['client_secret'] = cf.get('config', 'client_secret')
        except Exception as e:
            print e
        return result

    cf.add_section('config')
    cf.set('config', 'sx', sx)
    cf.set('config', 'sy', sy)
    cf.set('config', 'device', device)
    cf.set('config', 'client_id', ci)
    cf.set('config', 'client_secret', ck)
    cf.write(open("server\\config.ini", "w"))

    result = {
        "device": device,
        "sx": sx,
        "sy": sy,
        "client_id": ci,
        "client_secret": ck,
        "msg": "Config success!",
        "device_info": device_info,
    }
    return result

def get_config(name):
    cf = ConfigParser.ConfigParser()
    try:
        cf.read("server\\config.ini")
        return cf.get('config', name)
    except Exception as e:
        return ""

def get_file_data(path):
    f = file(path, 'r')
    b = f.read()
    f.close()
    return b

def get_pic(path):    
    cmd1 = "server\\bin\\adb.exe shell /system/bin/screencap -p /sdcard/screenshot.png"
    cmd2 = "server\\bin\\adb.exe  pull /sdcard/screenshot.png " + path
    device = ''
    try:
        device = get_config('device')
        if device != '':
            cmd1 = "server\\bin\\adb.exe -s %s shell /system/bin/screencap -p /sdcard/screenshot.png" % device
            cmd2 = "server\\bin\\adb.exe -s %s pull /sdcard/screenshot.png %s"  % (device, path)
    except:
        pass
    try:
        p = subprocess.Popen(cmd1, stderr=file("server\\bin\\log.txt", 'w'))
        p.wait()
        b = get_file_data("server\\bin\\log.txt")
        if len(b) > 0 and b.find('device') !=-1:
            return b
        p = subprocess.Popen(cmd2, stderr=file("server\\bin\\log.txt", 'w'))
        p.wait()
        b = get_file_data("server\\bin\\log.txt")
        if len(b) > 0 and b.find('device') !=-1:
            return b
        return True
    except Exception as e:
        return e

def get_device():
    cmd1 = "server\\bin\\adb.exe devices"
    try:
        p = subprocess.Popen(cmd1, stdout=file("server\\bin\\log.txt", 'w'))
        p.wait()
        b = get_file_data("server\\bin\\log.txt")
        b = b.split('\n')
        r = ''
        for bi in b:
            b1 = re.match(re.compile('(\d+).*device'), bi)
            if b1 != None:
                bi = bi + ' <<<<'
            r = r + bi + '\n'
        return r[:-2]
    except Exception as e:
        return e