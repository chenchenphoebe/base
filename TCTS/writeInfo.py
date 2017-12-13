#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import sys,os

input = []   
for arg in sys.argv:
    input.append(arg)
#[Login]
username = input[1]
password = input[2]
#[TestProject]
test_project = input[3]
vpm = input[4]
#[TestVersion]
maincode = input[5]
perso = input[6]
#[Tester]
tester = input[7]
#[TestScripts]
scripts_address = input[8]
module_address = input[9]
#[TestPC]
pc_name = input[10]
#[TestDevice]
MDevice = input[11]
SDevice = input[12]
Device1 = input[11]
Device2 = input[12]
Device3 = input[13]
Device4 = input[14]
Device5 = input[15]
Device6 = input[16]

config = ConfigParser.ConfigParser()
config.read(os.path.dirname(input[0]) +'\src\common\common.ini')

config.set("Login", "username", username)
config.set("Login", "password", password)
config.set("TestProject", "test_project", test_project)
config.set("TestProject", "vpm", vpm)
config.set("TestVersion", "maincode", maincode)
config.set("TestVersion", "perso",perso)
config.set("Tester", "tester", tester)
config.set("TestScripts", "scripts_address", scripts_address)
config.set("TestScripts", "module_address", module_address)
config.set("TestPC", "pc_name", pc_name)
config.set("TestDevice", "mdevice", MDevice)
config.set("TestDevice", "sdevice", SDevice)
config.set("TestDevice", "device1", Device1)
config.set("TestDevice", "device2", Device2)
config.set("TestDevice", "device3", Device3)
config.set("TestDevice", "device4", Device4)
config.set("TestDevice", "device5", Device5)
config.set("TestDevice", "device6", Device6)
config.write(open(os.path.dirname(input[0]) +'\src\common\common.ini', "r+"))
 