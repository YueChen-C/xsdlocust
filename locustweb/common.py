# -*-coding:utf-8 -*-
import ConfigParser

import logging
import time, os
from logging.handlers import TimedRotatingFileHandler
import redis




def log(name, err):
    time1 = time.strftime('%Y%m%d', time.localtime(time.time()))
    file_name = os.getcwd() + "/" + time1 + "-" + name + ".log"
    log = logging.getLogger(name)
    logformatter = logging.Formatter('%(asctime)s %(filename)s:%(module)s %(levelname)s %(message)s')
    loghandle = TimedRotatingFileHandler(file_name, 'midnight', 1, 10)
    loghandle.setFormatter(logformatter)
    loghandle.suffix = '%Y%m%d'
    log.addHandler(loghandle)
    log.setLevel(logging.DEBUG)
    log.exception(err)
    log.removeHandler(loghandle)


def exportTicket(num=1):
    '''
    :param num:获取登录凭证的数量（数量多，启动时间过长）
    :return:
    '''
    host = "115.28.106.133"
    pool = redis.Redis(host=host, port='6379', db='3', password="123456")
    listkey = pool.keys('h-member-session*')
    ticket = []
    try:

        listTicket = map(lambda x: 'v-session-ticket:' + x, pool.mget(listkey[0:num]))
        for i in listTicket:
            try:
                key = pool.hscan(i)[1]
                ticket.append([key.keys()[0], eval(key.values()[0])['appToken']])
            except:
                pass
    except:
        pass
    return ticket



cf = ConfigParser.ConfigParser()


class cfg():
    def __init__(self, file, name):
        self.file = file
        self.name = name

    def query(self, key):
        cf.read(self.file)
        content = cf.get(self.name, key)
        return content

    def cfgdict(self):
        cf.read(self.file)
        configdict = {}
        for i in cf.items(self.name):
            configdict[i[0]] = i[1]
        return configdict

    def write(self, key, content):
        '''
        :param content: 写入内容
        :return:
        '''
        cf.set(self.name, key, content)
        cf.write(open(self.file, "w"))
        cf.read(self.file)
        text = cf.get(self.name, key)
        assert text == str(content)  # 检查是否写入成功


logindata = {
    "b": {
        "city": "",
        "latitude": "",
        "loginName": "loginName",
        "loginPassword": "loginPassword",
        "longitude": "",
        "province": "",
        "versionShow": "1.2.2"
    },
    "h": {
        "appToken": "NzU5YjE5NjZlYjY5M2MzMTAxMmNkMDlkMDc0ODg3MDI=",
        "device": "Xiaomi:Mi Note 2:23",
        "deviceId": "000000007f65e78fe6edc17d00000000",
        "group": "passport",
        "method": "login",
        "s": "1502420941493",
        "siteId": "1",
        "siteVersion": "1095",
        "ticket": None,
        "version": "1.0"
    }
}
