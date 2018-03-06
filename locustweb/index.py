# coding=utf8
#!/usr/bin/python
import sys

import signal

reload(sys)
sys.setdefaultencoding('utf8')
import ConfigParser
import json
import os
import random
import threading
from time import sleep
import pymysql
import psutil
import redis
import requests
import subprocess
from flask import Flask, render_template, request, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from gevent import monkey
from gevent.pywsgi import WSGIServer

monkey.patch_all()

import common
import platform
import sqlite3
from rongcloud import RongCloud
import paramiko

global null
null = ''

app = Flask(__name__)
app.debug = True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

cf = ConfigParser.ConfigParser()
filecfg = os.path.dirname(os.path.realpath(__file__)) + '/config.cfg'
locustcfg = common.cfg(filecfg, 'locust')
rediscfg = common.cfg(filecfg, 'redis')
pool = redis.Redis(host=rediscfg.query('host'), port=rediscfg.query('port'), db=rediscfg.query('db'),
                   password=rediscfg.query('password'))

linuxcfg = common.cfg(filecfg, 'linux')
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=linuxcfg.query('hostname'), username=linuxcfg.query('username'),
            password=linuxcfg.query('password'), timeout=300,
            allow_agent=False, look_for_keys=False, port=22)

db = common.cfg(filecfg, 'mysql')
conn = pymysql.connect(host=db.query('host'), user=db.query('user'), passwd=db.query('passwd'),
                       db=db.query('db'), charset=db.query('charset'))


sqlite3conn = sqlite3.connect('locust.db', check_same_thread=False)
sqlite3conn.text_factory = str


def datalist():
    sqlite3cursors = sqlite3conn.cursor()
    text = sqlite3cursors.execute('SELECT * FROM Interface')
    list = []
    for row in text:
        postdata = eval(row[2])
        data = postdata['b']
        version = postdata['h']['version']
        key = [row[0], row[1], data, version, int(row[3])]
        list.append(key)
    sqlite3cursors.close()
    return list



class rongcloud():
    def __init__(self):
        rongcfg = common.cfg(filecfg, 'rongyun')
        app_key = rongcfg.query('app_key')
        app_secret = rongcfg.query('app_secret')
        self.rcloud = RongCloud(app_key, app_secret)

    def rongcheckOnline(self, useridlist):
        userlsit = []
        for userid in useridlist:
            r = self.rcloud.User.checkOnline(userId=userid)
            if r.get().get('status') == '1':
                userlsit.append(userid)
        return userlsit

    def rongpublishChatroom(self, textdata, time):
        global timer
        global kill
        content = {'content': {
            'content': '{0}'.format(json.dumps(textdata['text'], ensure_ascii=False)),
            'userAction': 1,
            'server': '{0}'.format(json.dumps(textdata['server'], ensure_ascii=False))
        }}
        r = self.rcloud.Message.publishChatroom(
                fromUserId=textdata['server']['imAccount'],
                toChatroomId={textdata['server']['roomId']},
                objectName='RC:TxtMsg',
                content="{0}".format(json.dumps(content, ensure_ascii=False)))
        print(r)
        if kill == True:
            timer = threading.Timer(1 / float(time), self.rongpublishChatroom, [textdata, time])
            timer.start()
        else:
            timer.cancel()
            timer = None
            kill = True

@app.route('/', methods=['GET', 'POST'])
def index():
    louststatus = False
    status = False
    hobby = request.form.get('keydata')
    test = request.form.get('test')
    runserver = request.form.get('runlocust')
    killserver = request.form.get('killlocust')
    ticket = request.form.get('ticket')
    configdata = locustcfg.cfgdict()
    # if ticket:
    #     try:
    #         url = locustcfg.query('HOST') + "/platform-rest/service.jws"
    #         # 清理ticket
    #         keys = pool.keys('h-member-session*') + pool.keys('v-session-appToken*') + pool.keys('v-session-ticket*')
    #         if keys:
    #             pool.delete(*keys)
    #
    #         # 更新登录信息
    #         ticketnum = locustcfg.query('ticketnum')
    #         cursors = conn.cursor()
    #         cursors.execute(
    #                 "SELECT mobile_phone,login_password FROM member ORDER BY member_id  DESC  LIMIT {0}".format(
    #                         ticketnum))
    #         dbdata = cursors.fetchall()
    #         cursors.close()
    #         fail = {}
    #         for key in dbdata:
    #             login = common.logindata
    #             login['b']['loginName'] = key[0]
    #             login['b']['loginPassword'] = key[1]
    #             data = requests.post(url=url, json=login).json()
    #             if data['h']['code'] == '0':
    #                 pass
    #             else:
    #                 fail[key[0]] = (data['h']['message'])
    #         if fail:
    #             flash(u'警告：更新失败{0}'.format(json.dumps(fail, ensure_ascii=False)), 'danger')
    #         else:
    #             flash(u'提示：{}条ticket登录信息更新成功'.format(ticketnum), 'warning')
    #     except Exception as p:
    #         flash(u'警告：更新失败{0}'.format(p), 'danger')

    # 检查locust服务是否启动
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if 'locust' in proc.info['name']:
            louststatus = True

    # 启动locust服务
    if runserver:
        # try:
            htmldata = datalist()
            for proc in psutil.process_iter(attrs=['pid', 'name']):
                if 'locust' in proc.info['name']:
                    louststatus = True
                    flash(u'警告：locust服务已经启动，请停止后再启动！', 'danger')
                    return render_template('index.html', datalist=htmldata, configdata=configdata,
                                           louststatus=louststatus)
            if 'Windows' in platform.system():
                retcode = [a for a in os.popen('route print').readlines() if ' 0.0.0.0 ' in a][0].split()[-2].strip()
                lcoustserver = "locust --master -f {0}/test.py --web-host={1} --web-port=5001".format(
                    os.path.dirname(os.path.realpath(__file__)), retcode)
            else:
                retcode = subprocess.Popen('''ifconfig eth1 | grep "inet addr" | awk '{ print $2}' | awk -F: '{print $2}\'''',stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                retcode = retcode.stdout.readlines()[0].strip()
                lcoustserver = "locust --master -f {0}/test.py --web-host={1} --web-port=5001".format(
                    os.path.dirname(os.path.realpath(__file__)), retcode)


            subprocess.Popen(lcoustserver, shell=True)
            sleep(1)
            subprocess.Popen("python {0}/openslave.py ".format(os.path.dirname(os.path.realpath(__file__))), shell=True)
            sleep(2)
            louststatus = True
            status = retcode + ':5001'
            flash(u'成功：locust服务已经启动', 'success')
            return render_template('index.html', datalist=htmldata, configdata=configdata, louststatus=louststatus,
                                   status=status)
        # except Exception as E:
        #     flash(u'警告：locust启动失败 {0}'.format(E))

    # 停止locust服务
    if killserver:
        psutillist=psutil.process_iter(attrs=['pid', 'name'])
        for proc in psutillist:
             if 'locust' in proc.info['name'] :
                p = psutil.Process(proc.info['pid'])
                psutil.Process(p.children()[0].pid).terminate()
            # if 'locust' in proc.info['name']:
            #     # p = psutil.Process(proc.info['pid'])
            #     try:
            #         mProcess.terminate()
            #         break
            #         # psutil.Process(proc.info['pid']).terminate()
            #         # for child in p.children():
            #         #     psutil.Process(child.pid).terminate()
            #     except Exception:
            #         pass

        if len([proc for proc in psutil.process_iter(attrs=['pid', 'name']) if 'locust' in proc.info['name']])<1:
            louststatus = False
            flash(u'提示：locust服务已经关闭', 'warning')
        else:
            flash(u'提示：locust服务关闭失败请从尝试', 'danger')

    # 所选接口测试
    if test:
        try:
            faillist = {}
            ticketlist = common.exportTicket(num=10)
            if ticketlist:
                sqlite3cursors = sqlite3conn.cursor()
                sqlite3text = sqlite3cursors.execute('SELECT * FROM Interface')
                ticketdata = random.choice(ticketlist)
                for row in sqlite3text:
                    if row[3] == 1:
                        name = row[1]
                        postdata = eval(row[2])
                        postdata['h']['appToken'] = ticketdata[1]
                        postdata['h']['ticket'] = ticketdata[0]
                        url = locustcfg.query('HOST') + "/platform-rest/service.jws"
                        data = requests.post(url, json=postdata).json()
                        if data['h']['code'] == '0':
                            pass
                        else:
                            faillist[name] = data['h']['message']
                sqlite3cursors.close()
            else:
                htmldata = datalist()
                flash(u'警告：当前没有正在登录的用户，获取ticket失败', 'danger')
                return render_template('index.html', datalist=htmldata, configdata=configdata, louststatus=louststatus)

            if faillist:
                flash(u'警告：接口测试失败：{0}'.format(json.dumps(faillist, ensure_ascii=False, indent=2)), 'danger')
            else:
                flash(u'成功：所选接口测试通过', 'success')
        except Exception as a:
            flash(u'警告：{0}'.format(a), 'danger')

    # 保存修改数据
    if hobby:
        try:
            hobby = hobby.encode('unicode-escape').decode('string_escape')
            hobby = json.loads(hobby)
            for key, value in hobby.items():
                sqlite3cursors = sqlite3conn.cursor()
                sqlite3text = sqlite3cursors.execute('SELECT * FROM Interface WHERE id={0}'.format(key)).fetchall()
                postdata = eval(sqlite3text[0][2])
                postdata['b'] = eval(value[0].encode('unicode-escape'))
                postdata['h']['version'] = value[1].encode('unicode-escape')
                sqlite3cursors.execute('UPDATE Interface SET `postdata`=?,`type`=? WHERE id=? ',
                                       (str(postdata), value[2], int(key)))
                sqlite3conn.commit()
                sqlite3cursors.close()
            flash(u'成功：保存成功', 'success')
        except Exception, E:
            flash(u'警告：保存失败{0}'.format(E), 'danger')
    htmldata = datalist()
    return render_template('index.html', datalist=htmldata, configdata=configdata, louststatus=louststatus)


@app.route('/Deleteinterface', methods=['GET', 'POST'])
def Deleteinterface():
    data = request.form.getlist('interface[]')
    try:
        sqlite3cursors = sqlite3conn.cursor()
        sqlite3cursors.execute("DELETE FROM Interface WHERE id IN ({0});".format(','.join([i for i in data])))
        sqlite3conn.commit()
        sqlite3cursors.close()
        code = {'code': 0, 'message': '删除成功'}
    except Exception as E:
        code = {'code': 101, 'message': '删除失败:{0}'.format(E)}
    return jsonify(code)


@app.route('/AddInterface', methods=['GET', 'POST'])
def Addinterface():
    try:
        sqlite3cursors = sqlite3conn.cursor()
        data = eval(request.form.get('AddInterface'))
        sqlite3cursors.execute('INSERT INTO Interface(`name`,`postdata`,`type`) VALUES (?,?,?)',
                               (data['Interfacename'].encode('utf-8'), data['Interfacjson'], 1))
        sqlite3conn.commit()
        sqlite3cursors.close()
        code = {'code': 0, 'message': '添加成功'}
    except Exception as E:
        code = {'code': 101, 'message': '添加失败:{0}'.format(E)}

    return jsonify(code)


@app.route('/Interfacedetails', methods=['GET', 'POST'])
def Interfacedetails():
    try:
        data = request.form.get('Interfacedetails')
        sqlite3cursors = sqlite3conn.cursor()
        sqlite3text = sqlite3cursors.execute('SELECT * FROM Interface WHERE `name` LIKE ?',
                                             (data.encode('utf-8'),)).fetchall()
        sqlite3conn.commit()
        sqlite3cursors.close()
        return jsonify(json.dumps(sqlite3text[0], ensure_ascii=False))
    except Exception as E:
        code = {'code': 101, 'message': '添加失败:{0}'.format(E)}
        return jsonify(code)


@app.route('/Saveinterface', methods=['GET', 'POST'])
def Saveinterface():
    try:
        data = eval(request.form.get('Saveinterface'))
        sqlite3cursors = sqlite3conn.cursor()
        sqlite3cursors.execute('UPDATE Interface SET `postdata`=?,`name`=? WHERE id=? ',
                               (str(data['Interfacjson']), data['Interfacename'].encode('utf-8'), data['Interfaceid']))
        sqlite3conn.commit()
        sqlite3cursors.close()
        code = {'code': 0, 'message': '保存成功'}
    except Exception as E:
        code = {'code': 101, 'message': '保存失败:{0}'.format(E)}
    return jsonify(code)


timer = None
kill = True


@app.route('/zhibo', methods=['GET', 'POST'])
def zhibo():
    global timer
    peoplenum = []
    roomlist = []
    messagedata = request.form.get('data')
    rongc = rongcloud()
    try:
        locustcfg = common.cfg(filecfg, 'locust')
        url = locustcfg.query('HOST') + "/platform-rest/service.jws"
        home = common.liveHome
        data = requests.post(url=url, json=home).json()
        disport = data['b']['data']['liveList']

        for live in disport:
            if live['state'] == 1:
                roomlist.append([live['liveId'], live['title'], live['watchNumStr']])
        rongkeys = pool.keys('l-imAccount-map*')
        ronglist = []
        for rong in rongkeys:
            ronglist.append(rong.split(':')[1])
        peoplenum = rongc.rongcheckOnline(ronglist)
    except Exception as E:
        flash(u'警告：请求错误{0 }'.format(E), 'danger')
        return render_template('zhibo.html', roomlist=roomlist, peoplenum=len(peoplenum))

    if messagedata:
        messagedata = messagedata.encode('unicode-escape').decode('string_escape')
        messagedata = json.loads(messagedata)

        def killtimer():
            global kill
            kill = False

        if not messagedata.get('liveID'):
            flash(u'警告：请选择直播间', 'warning')
            return render_template('zhibo.html', roomlist=roomlist, peoplenum=len(peoplenum))

        if timer:
            flash(u'警告：正在执行任务请先结束当前任务', 'warning')
        else:
            timer = threading.Timer(0.1, rongc.rongpublishChatroom, [common.PTdata, messagedata['frequency']])
            timer.start()
            timer1 = threading.Timer(int(messagedata['time']), killtimer)
            timer1.start()
        return render_template('zhibo.html', roomlist=roomlist, peoplenum=len(peoplenum))

    kill = request.form.get('kill')
    if kill:
        if timer:
            print(timer, 'ceshi')
            timer.cancel()
            timer = None
            kill = True
        else:
            flash(u'警告：没有正在执行的任务', 'warning')

    # home['b']['type']='金融产业'
    # data=requests.post(url=url, json=home).json()
    # Finance=data['b']['data']['liveList']
    # for i in Finance:
    #     if i['state']==1:
    #         roomlist.append([i['liveId'],i['title']])

    return render_template('zhibo.html',
                           roomlist=roomlist,
                           peoplenum=len(peoplenum))


@app.route('/jiankong', methods=['GET', 'POST'])
def jiankong():
    system_information = {}

    system_command = [
        ["hostname", "hostname"],
        ["kernel", "cat /proc/version |cut -f1 -d'('"],
        ["cpuinfo", "cat /proc/cpuinfo |grep name |cut -f2 -d: \
            |uniq -c |sed -e 's/^[ \t]*//'"],
        ["meminfo",
         " cat /proc/meminfo |head -1|cut -f2- -d':'|sed -e 's/^[ \t]*//'"]]
    for i in xrange(len(system_command)):
        stdin, stdout, stderr = ssh.exec_command(system_command[i][1])
        system_information.setdefault(system_command[i][0], stdout.read())
    # ssh.close()
    return render_template('jiankong.html',
                           system_information=system_information)


@app.route('/getserver')
def server():
    mem = {}
    stdin, stdout, stderr = ssh.exec_command('cat /proc/meminfo')
    lines = stdout.readlines()
    for line in lines:
        if len(line) < 2:
            continue
        name = line.split(':')[0]
        var = line.split(':')[1].split()[0]
        mem[name] = float(var)
    mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']

    serverlist = {}
    # 记录内存使用率 已使用 总内存和缓存大小
    memory = {}
    memory['percent'] = str(round(mem['MemUsed'] / mem['MemTotal'] * 100)) + '%'
    memory['used'] = str(round(mem['MemUsed'] / (1024), 2)) + ' MB'
    memory['MemTotal'] = str(round(mem['MemTotal'] / (1024), 2)) + ' MB'
    memory['Buffers'] = str(round(mem['Buffers'] / (1024), 2)) + ' MB'

    # cpu负载
    loadavg = {}
    stdin, stdout, stderr = ssh.exec_command('cat /proc/loadavg')
    con = stdout.read().split()
    loadavg['lavg_1'] = con[0]
    loadavg['lavg_5'] = con[1]
    loadavg['lavg_15'] = con[2]
    loadavg['nr'] = con[3]

    # 网卡速度
    stdin, stdout, stderr = ssh.exec_command(' sar -n DEV  1 1')
    lines = stdout.readlines()
    Average = {}
    for line in lines:
        if 'Average' in line and 'IFACE' not in line:
            line1 = ' '.join(line.split()).split(" ")
            Average[line1[1]] = u'下载速度:' + str(line1[4]) + ' kb/s' + u'  上传速度:' + str(line1[5]) + ' kb/s'

    stdin, stdout, stderr = ssh.exec_command("netstat -n | awk '/^tcp/ {++S[$NF]} END {for(a in S) print a, S[a]}'")
    lines = stdout.readlines()
    netstat = {}
    netstat['ESTABLISHED'], netstat['CLOSE_WAIT'], netstat['TIME_WAIT'], netstat['SYN_RECV'], netstat['FIN_WAIT1'], \
    netstat['FIN_WAIT2'] = 0, 0, 0, 0, 0, 0
    for line in lines:
        line1 = line.split(" ")
        netstat[line1[0]] = line1[1]

    # 服务器连接数
    try:
        db = common.cfg(filecfg, 'mysql')
        conn = pymysql.connect(host=db.query('host'), user=db.query('user'), passwd=db.query('passwd'),
                               db=db.query('db'), charset=db.query('charset'))
        cursors = conn.cursor()
        cursors.execute('SHOW FULL PROCESSLIST')
        dbdata = cursors.fetchall()
        mysqlnum = len(dbdata)
    except Exception:
        mysqlnum = '数据库连接失败'

    try:
        reidinfo = pool.info()
        reidslsit = {}
        reidslsit['qps'] = reidinfo['instantaneous_ops_per_sec']
        reidslsit['keyspace_misses'] = reidinfo['keyspace_misses']
        reidslsit['used_memory'] = reidinfo['used_memory_human']
        reidslsit['blocked_clients'] = reidinfo['blocked_clients']
        reidslsit['connected_clients'] = reidinfo['connected_clients']
    except Exception:
        reidslsit = {}
        reidslsit['qps'] = 'redis连接失败'

    serverlist['reidslsit'] = reidslsit
    serverlist['netstat'] = netstat
    serverlist['Average'] = Average
    serverlist['memory'] = memory
    serverlist['loadavg'] = loadavg
    serverlist['mysqlnum'] = mysqlnum

    return jsonify(serverlist)


if __name__ == '__main__':
    manager.run()
