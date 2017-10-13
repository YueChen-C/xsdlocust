#coding=utf-8
from locust import HttpLocust, TaskSet, task
class WebsiteTasks(TaskSet):


    @task
    def first(self):
        with self.client.post("/platform-rest/service.jws", json={
                "h":    {
                  "appToken": "M2I2Mzc1ZWVjNTQ1ZTc3ODNlOGIwMzNjMTlhN2RhNjc=",
                  "version": "1.4",
                  "group": "liveHome",
                  "deviceId": "62e83ba9adea62b770ee297809662af66",
                  "device": "iPhone9,1",
                  "siteId": "0",
                  "ticket": "i+M1P0Y6CFk=",
                  "siteVersion": "165",
                  "method": "live_msg"
                },
                "b":    {
                  "type": "",
                  "pageNumber": "1",
                  "pageSize": "15"
                }},name='首页',catch_response = True) as response:
            if response.status_code==200:
                response.success()
            else:
                response.failure('测试')



class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "https://test3.txdsd.com"
    min_wait = 1000
    max_wait = 3000



