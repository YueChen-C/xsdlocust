#coding=utf8
import ConfigParser
import json
import os
import random
from time import sleep

import openpyxl
import psutil
import requests
import subprocess
from flask import Flask, render_template,request, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from multiprocessing import cpu_count

import common
from openslave import checkPacge, ThreadStartone, opencpu

global null
null=''


app = Flask(__name__)
app.debug=True
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


cf = ConfigParser.ConfigParser()
filecfg=os.path.dirname(os.path.realpath(__file__))+'/config.cfg'
filexlsx=os.path.dirname(os.path.realpath(__file__))+'/interface.xlsx'
def datalist():
    readpath = filexlsx
    inwb = openpyxl.load_workbook(readpath)
    work_name= inwb.get_sheet_by_name('Sheet1')
    list=[]
    for row in range(1,work_name.max_row+1):
        k1=work_name.cell(row = row,column = 1).value
        k2=work_name.cell(row = row,column = 2).value
        postdata=eval(work_name.cell(row = row,column = 3).value)
        k3=postdata['b']
        k4=postdata['h']['version']
        k5=work_name.cell(row = row,column = 5).value
        key=[k1,k2,k3,k4,k5]
        list.append(key)
    return list



class cfg():
    def __init__(self,file):
        self.file=file

    def query(self,name,key):
        cf.read(self.file)
        content=cf.get(name,key)
        return content

    def cfgdict(self,name):
        cf.read(self.file)
        configdict={}
        for i in cf.items(name):
            configdict[i[0]]=i[1]
        return configdict

    def write(self,name,key,content):
        '''
        :param content: 写入内容
        :return:
        '''
        cf.set(name,key,content)
        cf.write(open(self.file,"w"))
        cf.read(self.file)
        text=cf.get(name,key)
        assert text==str(content)#检查是否写入成功







@app.route('/index',methods=['GET', 'POST'])
def index():
    louststatus=False
    status=False
    hobby = request.form.get('keydata')
    test=request.form.get('test')
    runserver=request.form.get('runlocust')
    killserver=request.form.get('killlocust')
    #检查locust服务是否启动
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if proc.info['name']=='locust.exe':
            louststatus=True

    if runserver:
        data=datalist()
        config=cfg(filecfg)
        configdata=config.cfgdict('locust')
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if proc.info['name']=='locust.exe':
                louststatus=True
                flash(u'locust服务已经启动，请停止后再启动！')
                return render_template('index.html',datalist=data,configdata=configdata,louststatus=louststatus)
        subprocess.Popen("locust --master -f {0}/test.py ".format(os.path.dirname(os.path.realpath(__file__))))
        sleep(2)
        subprocess.Popen("python {0}/openslave.py ".format(os.path.dirname(os.path.realpath(__file__))))
        louststatus=True
        status=True
        flash(u'locust服务已经启动','success')
        return render_template('index.html',datalist=data,configdata=configdata,louststatus=louststatus,status=status)

    if killserver:
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if proc.info['name']=='locust.exe':
                p=psutil.Process(proc.info['pid'])
                psutil.Process(p.children()[0].pid).terminate()
                louststatus=False
        flash(u'locust服务已经关闭','warning')



    if test:
        readpath = filexlsx
        inwb = openpyxl.load_workbook(readpath)
        work_name= inwb.get_sheet_by_name('Sheet1')
        faillist={}
        for row in range(1,work_name.max_row+1):
            if work_name.cell(row = row,column = 5).value==1:
                name=work_name.cell(row = row,column = 2).value
                postdata=eval(work_name.cell(row = row,column = 3).value)
                ticketlist=random.choice(common.exportTicket(num=10))
                postdata['h']['appToken']=ticketlist[1]
                postdata['h']['ticket']=ticketlist[0]
                data=requests.post('https://test3.txdsd.com/platform-rest/service.jws',json=postdata).json()
                if data['h']['code']=='0':
                    pass
                else:

                    faillist[name]=data['h']['message']
        if faillist:
            flash(u'接口测试失败：{0}'.format(json.dumps(faillist, ensure_ascii=False, indent=2)),'danger')
        else:
            flash(u'所选接口测试通过','success')

    if hobby:
        try:
            readpath = filexlsx
            inwb = openpyxl.load_workbook(readpath)
            work_name= inwb.get_sheet_by_name('Sheet1')
            hobby=hobby.encode('unicode-escape').decode('string_escape')
            hobby=json.loads(hobby)
            for key,value in hobby.items():
                postdata=eval(work_name.cell(row = int(key),column = 3).value)
                postdata['b']=eval(value[0].encode('unicode-escape'))
                postdata['h']['version']=value[1].encode('unicode-escape')
                work_name.cell(row = int(key),column = 3).value=str(postdata)
                work_name.cell(row = int(key),column = 5).value=value[2]
            inwb.save(readpath)
            flash(u'保存成功','success')
        except Exception,E:
            flash(u'保存失败{0}'.format(E),'danger')
    data=datalist()
    config=cfg(filecfg)
    configdata=config.cfgdict('locust')
    return render_template('index.html',datalist=data,configdata=configdata,louststatus=louststatus)




if __name__ == '__main__':
    manager.run()