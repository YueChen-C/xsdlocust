# -*-coding:utf-8 -*-
import ConfigParser

import logging
import time, os
from logging.handlers import TimedRotatingFileHandler
import redis
cf = ConfigParser.ConfigParser()
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


def exportTicket(num=1):
    '''
    :param num:获取登录凭证的数量（数量多，启动时间过长）
    :return:
    '''
    filecfg = os.path.dirname(os.path.realpath(__file__)) + '/config.cfg'
    rediscfg = cfg(filecfg, 'redis')
    pool = redis.Redis(host=rediscfg.query('host'), port=rediscfg.query('port'), db=rediscfg.query('db'),
                       password=rediscfg.query('password'),socket_timeout=1, socket_connect_timeout=1)
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
        "siteVersion": "1145",
        "ticket": None,
        "version": "1.0"
    }
}

liveHome = {
    "b": {
        "type": "娱乐生活",
        "pageNumber": "1",
        "pageSize": "16"
    },
    "h": {
        "appToken": "=",
        "device": "Xiaomi:Mi Note 2:23",
        "deviceId": "000000007f65e78f0000000000000000",
        "group": "liveHome",
        "method": "live_msg",
        "s": "1509437956159",
        "siteId": "1",
        "siteVersion": "235",
        "ticket": "",
        "version": "2.0"
    }
}
# 普通消息
PTdata = {
    'text': {
        'extra': '''{
        'isEnchantmentEffects':'false',
        'isBanSay':'false'}''',
        'text': '哈哈哈哈1',
        'barrage': '0'
    }, 'server': {
        'anchorLevel': '15',
        'wealthLevel': '39',
        'headImage': 'https://test3.txdsd.com/platform-rest/images/randomAvatar/ra_433.jpg',
        'liveId': 35413,
        'memberRole': 1,
        'imAccount': '1',
        'memberId': 36470,
        'nickName': "@一样",
        'roomId': '@ZBJ#186465'
    }}
