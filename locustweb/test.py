#coding=utf8
import json

data = {"1":["None","1"],"2":["None","1"],"3":["None","1"],"4":["None","1"],"5":["None","1"],"6":["{\"anchorId\": \"27660\"}","1"],"7":["{\"anchorId\": \"27660\",\"liveId\": \"34944\"}","1"],"8":["None","1"],"9":["None","1"],"10":["None","1"],"11":["None","1"],"12":["None","1"],"13":["None","1"],"14":["None","1"]}
encode_json = json.dumps(data)


data=json.loads(encode_json)
print(type(data))
for i,k in data.items():
    print i,k