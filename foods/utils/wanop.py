#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
@author: 刘红波
@license: ***
@contact: super_sponge@163.com
@see: https://github.com/super-sponge

@version: 0.0.1
@todo[0.0.2]: a new module

@note: a comment
@attention: please attention
@bug: a exist bug
@warning: warnings
'''

import urllib
import time
import re

def getWanIp():
    html = urllib.urlopen('http://www.whereismyip.com').read()
    ip = re.search('\d+.\d+.\d+.\d+', html)
    return ip.group(0)

if __name__ == '__main__':
    while True:
        urllib.urlopen("http://admin:admin@192.168.1.1/userRpm/StatusRpm.htm?Disconnect=%B6%CF%20%CF%DF&wan=1")
	time.sleep(5)
        urllib.urlopen("http://admin:admin@192.168.1.1/userRpm/StatusRpm.htm?Connect=%C1%AC%20%BD%D3&wan=1")
#        print time.ctime() + ' 公网IP地址为：' + getWanIp()
        time.sleep(300)


