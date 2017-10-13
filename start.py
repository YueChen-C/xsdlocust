#coding=utf8

import common
from Interface import *
from locust import HttpLocust, TaskSet, task
import random


class WebsiteTasks(TaskSet):

    def on_start(self):
        self.ticketlist=random.choice(self.locust.ticketlist)


    @task(3)
    def first(self):
        firstdata=random.choice(firstLevel)
        firstdata[1]['h']['appToken']=self.ticketlist[1]
        firstdata[1]['h']['ticket']=self.ticketlist[0]
        with self.client.post("/platform-rest/service.jws", json=firstdata[1],name=firstdata[0],catch_response = True) as response:
            if response.status_code==200:
                response.success()
            else:
                response.failure('request failure......')

    @task(2)
    def second(self):
        #直播间相关，需要liveId
        liveId=random.choice(self.locust.liveIdlist)
        seconddata=random.choice(secondLevel)
        seconddata[1]['h']['appToken']=self.ticketlist[1]
        seconddata[1]['h']['ticket']=self.ticketlist[0]
        seconddata[1]['b']['liveId']=liveId
        with self.client.post("/platform-rest/service.jws", json=seconddata[1],name=seconddata[0],catch_response = True) as response:
            if response.status_code==200:
                response.success()
            else:
                response.failure('request failure......')
    @task(1)
    def three(self):
        threedata=random.choice(threeLevel)
        threedata[1]['h']['appToken']=self.ticketlist[1]
        threedata[1]['h']['ticket']=self.ticketlist[0]
        with self.client.post("/platform-rest/service.jws", json=threedata[1],name=threedata[0],catch_response = True) as response:
            if response.status_code==200:
                response.success()
            else:
                response.failure('request failure......')

    def gift(self):
        giftd=giftdata
        liveId=random.choice(self.locust.liveIdlist)
        giftd[1]['h']['appToken']=self.ticketlist[1]
        giftd[1]['h']['ticket']=self.ticketlist[0]
        giftd[1]['b']['liveId']=liveId
        with self.client.post("/platform-rest/service.jws", json=giftd[1],name=giftd[0],catch_response = True) as response:
            if response.status_code==200:
                response.success()
            else:
                response.failure('request failure......')




class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "https://test3.txdsd.com"
    ticketlist=common.exportTicket(num=20)
    # liveIdlist=['34707']
    liveIdlist=common.checklive()
    min_wait = 1
    max_wait = 50










