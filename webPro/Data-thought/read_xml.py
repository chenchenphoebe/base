#-*- coding:utf-8 -*-
from xml.dom import minidom

dom = minidom.parse('info.xml')
root = dom.documentElement

print(root.nodeName)