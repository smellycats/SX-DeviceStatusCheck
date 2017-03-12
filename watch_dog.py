# -*- coding: utf-8 -*-
import time
import json

import arrow

from helper_device import Device
from helper_ping import *
from ini_conf import MyIni
from my_logger import *


debug_logging(u'logs/error.log')
logger = logging.getLogger('root')


class WatchDog(object):
    def __init__(self):
        self.my_ini = MyIni()
        
        self.dev = Device(**self.my_ini.get_device())

    def __del__(self):
        pass

    def device_status_check(self):
        """"设备状态检测"""
        #沉睡时间
        t = 30
        dev = self.dev.get_device_check()
        status_list = []
        for i in dev['items']:
            r = ping(i['ip'])
            status_list.append({'ip': i['ip'], 'status': r})
            print '{0} {1} {2}'.format(str(arrow.now()), i['ip'], r)
            logger.info('{0} {1}'.format(i['ip'], r))
            if not r:
                t = 5
                break
        if len(status_list) == 0:
            return t
        self.dev.set_device(status_list)
        return t

    def run(self):
        while 1:
            try:
                r = self.device_status_check()
                time.sleep(r)
            except Exception as e:
                print e
                logger.exception(e)
                time.sleep(10)
            finally:
                time.sleep(1)


if __name__ == "__main__":
    wd = WatchDog()
    #wd.get_ip_list()
    wd.run()
    #wd.device_status_check()
