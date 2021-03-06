# -*- coding: utf-8 -*-
import time
import json
import random
import multiprocessing as mul

import arrow

from helper_device import Device
from helper_ping import *
from my_yaml import MyYAML
from my_logger import *


debug_logging(u'logs/error.log')
logger = logging.getLogger('root')


class WatchDog(object):
    def __init__(self):
        # 配置文件
        ini = MyYAML()
        self.my_ini = ini.get_ini()
        # 设备状态实例
        self.dev = Device(**dict(self.my_ini['device']))
        # 进程池
        self.pool = mul.Pool(self.my_ini['pool'])
        # 循环检测次数
        self.loop = self.my_ini['loop']

    def __del__(self):
        pass

    def mul_ping(self, dev_list):
        """多进程ping"""
        # 确认结果列表
        dev_true_list = []
        # 不确认结果列表
        dev_false_list = []
        rel = self.pool.map(ping, [i['ip'] for i in dev_list])
        for i, j in zip(dev_list, rel):
            i['res'] = j
            # 结果为真 则写入确认结果列表
            if j is True:
                dev_true_list.append(i)
                continue
            # 结果为假并且最近一次记录为假 则写入确认结果列表
            if j is False and i['status'] is False:
                dev_true_list.append(i)
                continue
            # 其他情况则不确认
            dev_false_list.append(i)

        return dev_true_list, dev_false_list       

    def set_device_status(self, dev_list):
        """更新设备状态"""
        if len(dev_list) > 0:
            self.dev.set_device(dev_list)
            for i in dev_list:
                info = u'{0} {1} {2}'.format(
                    arrow.now('PRC').format('YYYY-MM-DD HH:mm:ss ZZ'),
                    i['ip'], i['status'])
                print info
                #logger.info(info)
    
    def device_status_check(self, type):
        """"设备状态检测"""
        dev_info_list = self.dev.get_device_check(num=20, type=type)['items']
        if len(dev_info_list) == 0:
            return
        for i in range(self.loop):
            dev_true_list, dev_false_list = self.mul_ping(dev_info_list)
            self.set_device_status(
                [{'id': i['id'], 'ip': i['ip'],
                  'status': i['res']} for i in dev_true_list])
            # 不确认结果列表为空则退出
            if len(dev_false_list) == 0:
                break
            dev_info_list = dev_false_list
        self.set_device_status(
            [{'id': i['id'], 'ip': i['ip'],
              'status': i['res']} for i in dev_false_list])

    def run(self):
        while 1:
            try:
                for i in [2, 3]:
                    self.device_status_check(i)
                time.sleep(1)
            except Exception as e:
                logger.error(e)
                time.sleep(10)
            finally:
                time.sleep(1)


if __name__ == "__main__":
    wd = WatchDog()
    #t1 = time.time()
    #wd.device_status_check()
    #t2 = time.time()
    #print t2 - t1
    #wd.device_status_check()
    wd.run()
    #wd.device_status_check()
