# coding=utf-8
import os
import random
import sqlite3
from locust import TaskSet, HttpLocust, task
import common


def postdata():
    sqlite3conn = sqlite3.connect('locust.db',check_same_thread=False)
    sqlite3cursors=sqlite3conn.cursor()
    data=sqlite3cursors.execute('SELECT * FROM Interface').fetchall()
    list = []
    for row in data:
        if row[3] == 0:
            key = [row[1], eval(row[2])]
            list.append(key)
    return list



class WebsiteTasks(TaskSet):
    def on_start(self):
        self.ticketlist = random.choice(self.locust.ticketlist)

    @task
    def first(self):
        data = random.choice(self.locust.postdata)
        data[1]['h']['appToken'] = self.ticketlist[1]
        data[1]['h']['ticket'] = self.ticketlist[0]
        with self.client.post("/platform-rest/service.jws", json=data[1], name=data[0],
                              catch_response=True) as response:
            if response.status_code == 200:
                try:
                    if response.json()['h']['code']=='0':
                        response.success()
                    else:
                        response.failure(response.text)
                except Exception as E:
                    response.failure('requests fail:{0}'.format(E))
            else:
                response.failure('requests fail:{0}'.format(response.status_code))


class WebsiteUser(HttpLocust):
    file = os.path.dirname(os.path.realpath(__file__)) + '/config.cfg'
    config = common.cfg(file, 'locust')
    task_set = WebsiteTasks
    host = config.query('host')
    ticketlist = common.exportTicket(num=int(config.query('ticketnum')))
    postdata = postdata()
    min_waittime = int(config.query('min_waittime'))
    max_waittime = int(config.query('max_waittime'))
