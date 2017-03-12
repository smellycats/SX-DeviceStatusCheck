#-*- encoding: utf-8 -*-
import ConfigParser

class MyIni(object):
    def __init__(self, confpath = 'my_ini.conf'):
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(confpath)

    def __del__(self):
        del self.cf

    def get_device(self):
        conf = {}
        section = 'DEVICE'
        conf['host'] = self.cf.get(section, 'host')
        conf['port'] = self.cf.getint(section, 'port')
        return conf



