# -*-coding:utf-8 -*-
import threading
import warnings,os
import sys,common

from multiprocessing import cpu_count

import subprocess


def checkPacge():
    try:
        import locust
    except ImportError:
        warnings.warn('install the locust python package')
        os.system('pip install locustio')
    try:
        import zmq
    except ImportError:
        warnings.warn('install the zmqrpc python package')
        os.system('pip install pyzmq')
    try:
        import greenlet
    except ImportError:
        warnings.warn('install the greenlet python package')
        os.system('pip install greenlet')
    try:
        import requests
    except ImportError:
        warnings.warn('install the requests python package')
        os.system('pip install requests')
    try:
        import gevent
    except ImportError:
        warnings.warn('install the gevent python package')
        os.system('pip install gevent')

def ThreadStartone(method, num):
    Threads=[]
    # quene = Queue.Queue()
    for i in range(num):
        t = threading.Thread(target=method, name="进程："+str(i))
        t.setDaemon(True)
        Threads.append(t)
    for t in Threads:
        t.start()
        print >> sys.stderr,t
    for t in Threads:
        t.join()
        print >> sys.stderr,t
# print("locust --master -f {0}/start.py".format(os.getcwd()))
# os.system("locust --master -f {0}/start.py".format(os.getcwd()))

def opencpu():
        subprocess.call("locust --slave -f {0}/test.py --master-host=10.10.30.50".format(os.getcwd()),shell = True)


if __name__ == '__main__':
    checkPacge()
    # if common.checklive()==[]:
    #     print >> sys.stderr,u'没有正在直播的直播间，请开启直播间'
    # else:
    ThreadStartone(opencpu,cpu_count())






