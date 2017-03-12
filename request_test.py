# -*- coding: utf-8 -*-
import time
import datetime
import json

import arrow
#import requests
#from requests.auth import HTTPBasicAuth, HTTPDigestAuth

from helper_device import Device
from ini_conf import MyIni

class DeviceTest(object):
    def __init__(self):
        self.my_ini = MyIni()
        print self.my_ini.get_device()
        self.dev = Device(**self.my_ini.get_device())
    
    def test_get_device(self):
        """上传卡口数据"""
        r = self.dev.get_device_list()
        print r
        r2 = self.dev.get_device_by_ip('127.0.0.1')
        print r2
        r3 = self.dev.get_device_check()
        print r3
        #assert r['headers'] == 201

    def test_set_device(self):
        data = [
                    {'ip': '127.0.0.1', 'status': True},
                    {'ip': '127.0.0.2', 'status': False}
                ]
        r = self.dev.set_device(data)
        print r

if __name__ == '__main__':  # pragma nocover
    dt = DeviceTest()
    dt.test_get_device()
    dt.test_set_device()
