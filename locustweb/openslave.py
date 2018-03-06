# -*-coding:utf-8 -*-
import threading
import warnings,os
import sys,common

from multiprocessing import cpu_count

import subprocess
import platform


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
    try:
        import openpyxl
    except ImportError:
        warnings.warn('install the gevent python package')
        os.system('pip install openpyxl')

def ThreadStartone(method,retcode, num):
    Threads=[]
    # quene = Queue.Queue()
    for i in range(num):
        t = threading.Thread(target=method,args=(retcode,),name="进程："+str(i))
        t.setDaemon(True)
        Threads.append(t)
    for t in Threads:
        t.start()
        print >> sys.stderr,t
    for t in Threads:
        t.join()
        print >> sys.stderr,t

def opencpu(retcode):
    lcoustserver="locust --slave -f {0}/test.py --master-host={1}".format(os.path.dirname(os.path.realpath(__file__)),retcode)
    subprocess.call(lcoustserver,shell = True)


if __name__ == '__main__':
    if 'Windows' in platform.system():
        retcode = [a for a in os.popen('route print').readlines() if ' 0.0.0.0 ' in a][0].split()[-2].strip()
    else:
        retcode = subprocess.Popen('''ifconfig eth0 | grep "inet addr" | awk '{ print $2}' | awk -F: '{print $2}\'''', stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        retcode=retcode.stdout.readlines()[0].strip()

    # checkPacge()
    ThreadStartone(opencpu,retcode,cpu_count())






