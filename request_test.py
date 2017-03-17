# -*- coding: utf-8 -*-
import time
import datetime
import json

import arrow
#import requests
#from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from helper_device import Device
from helper_ping import *
from ini_conf import MyIni

class DeviceTest(object):
    def __init__(self):
        self.my_ini = MyIni()
        print self.my_ini.get_device()
        self.dev = Device(**self.my_ini.get_device())
    
    def test_get_device(self):
        """上传卡口数据"""
        #print self.dev.get_device_list()
        #print self.dev.get_device_list(type=2)
        #print self.dev.get_device_list(type=3)
        print self.dev.get_device_by_ip('127.0.0.1')
        print self.dev.get_device_check(num=20, type=2)
        print self.dev.get_device_check(num=10, type=3)
        #assert r['headers'] == 201

    def test_set_device(self):
        data = [
            {'ip': '127.0.0.1', 'status': True},
            {'ip': '127.0.0.2', 'status': False}
        ]
        r = self.dev.set_device(data)
        print r

class PingTest(object):
    def __init__(self):
        pass

    def test_ping(self):
        ping('192.168.1.123')


if __name__ == '__main__':  # pragma nocover
    dt = DeviceTest()
    dt.test_get_device()
    #dt.test_set_device()
    #pt = PingTest()
    #pt.test_ping()
