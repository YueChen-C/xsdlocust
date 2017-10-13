# #coding=utf8
#一级优先接口配置
firstLevel=[
    ['直播首页',{
                "h":    {
                  "appToken": "M2I2Mzc1ZWVjNTQ1ZTc3ODNlOGIwMzNjMTlhN2RhNjc=",
                  "version": "2.0",
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
                }}],
    ['APP首页',{
                "h": {
                        "appToken": "NzU5YjE5NjZlYjY5M2MzMTAxMmNkMDlkMDc0ODg3MDI=",
                        "device": "Xiaomi:Mi Note 2:23",
                        "deviceId": "000000007f65e78fe6edc17d00000000",
                        "group": "home",
                        "method": "index",
                        "s": "1505187626308",
                        "siteId": "1",
                        "siteVersion": "1115",
                        "ticket": "n3Pr93P3VMc=",
                        "version": "1.0"
                    },
                "b":    {
                }}],
    ['直播首页热门',{
                "h":    {
                  "appToken": "M2I2Mzc1ZWVjNTQ1ZTc3ODNlOGIwMzNjMTlhN2RhNjc=",
                  "version": "2.0",
                  "group": "liveHome",
                  "deviceId": "62e83ba9adea62b770ee297809662af66",
                  "device": "iPhone9,1",
                  "siteId": "0",
                  "ticket": "i+M1P0Y6CFk=",
                  "siteVersion": "1115",
                  "method": "hot_rank"
                },
                "b":{
                }}]]

#直播间相关二级优先

secondLevel=[['观众加入房间',{
                "h":    {
                  "appToken": "M2I2Mzc1ZWVjNTQ1ZTc3ODNlOGIwMzNjMTlhN2RhNjc=",
                  "version": "1.0",
                  "group": "living",
                  "deviceId": "62e83ba9adea62b770ee297809662af66",
                  "device": "iPhone9,1",
                  "siteId": "0",
                  "ticket": "i+M1P0Y6CFk=",
                  "siteVersion": "1115",
                  "method": "join_live"
                },
                "b":    {
                  "liveId": '',
                }}],
           ['获取观众信息',{
                "h":    {
                  "appToken": "M2I2Mzc1ZWVjNTQ1ZTc3ODNlOGIwMzNjMTlhN2RhNjc=",
                  "version": "1.0",
                  "group": "living",
                  "deviceId": "62e83ba9adea62b770ee297809662af66",
                  "device": "iPhone9,1",
                  "siteId": "0",
                  "ticket": "i+M1P0Y6CFk=",
                  "siteVersion": "1115",
                  "method": "info"
                },
                "b":    {
                  "liveId": '',
                }}],
           ['发言接口',              {
                "h":    {
                  "appToken": "YmM4ODdjYmU0N2VhZTYzZGNmZDJmNmQ4ZTQ5ODc3ZjQ=",
                  "version": "1.0",
                  "group": "living",
                  "deviceId": "62e83ba9adea62b770ee297809662af66",
                  "device": "iPhone9,1",
                  "siteId": "0",
                  "ticket": "RqVidstG31U=",
                  "siteVersion": "1115",
                  "method": "is_bansay"
                },
                "b":    {
                  "anchorId": "27660"
                }}],
           ['直播间点赞接口',{
                "h":    {
                  "appToken": "YmM4ODdjYmU0N2VhZTYzZGNmZDJmNmQ4ZTQ5ODc3ZjQ=",
                  "version": "1.0",
                  "group": "living",
                  "deviceId": "62e83ba9adea62b770ee297809662af66",
                  "device": "iPhone9,1",
                  "siteId": "0",
                  "ticket": "RqVidstG31U=",
                  "siteVersion": "1115",
                  "method": "praise"
                },
                "b":    {
                    "anchorId": "27660",
                  "liveId": "34944"
                }}]
             ]

threeLevel=[['我的信息接口',{
                "h":    {
                  "appToken": "M2I2Mzc1ZWVjNTQ1ZTc3ODNlOGIwMzNjMTlhN2RhNjc=",
                  "version": "1.0",
                  "group": "member",
                  "deviceId": "62e83ba9adea62b770ee297809662af66",
                  "device": "iPhone9,1",
                  "siteId": "0",
                  "ticket": "i+M1P0Y6CFk=",
                  "siteVersion": "1115",
                  "method": "info/home"
                },
                "b":    {
                }}],
            ['项目列表',{
                "h":    {
                  "appToken": "M2I2Mzc1ZWVjNTQ1ZTc3ODNlOGIwMzNjMTlhN2RhNjc=",
                  "version": "1.0",
                  "group": "project",
                  "deviceId": "62e83ba9adea62b770ee297809662af66",
                  "device": "iPhone9,1",
                  "siteId": "0",
                  "ticket": "i+M1P0Y6CFk=",
                  "siteVersion": "1115",
                  "method": "project_list"
                },
                "b": {
                    "area": '',
                    "financeMoney": '',
                    "industry": '',
                    "name": '',
                    "pageCount": 15,
                    "pageNum": 1,
                    "projectStage": '',
                    "projectState": '',
                    "sort": "hot"
                }}],
            ['机构列表',{
                "h":    {
                  "appToken": "M2I2Mzc1ZWVjNTQ1ZTc3ODNlOGIwMzNjMTlhN2RhNjc=",
                  "version": "1.0",
                  "group": "finance_org",
                  "deviceId": "62e83ba9adea62b770ee297809662af66",
                  "device": "iPhone9,1",
                  "siteId": "0",
                  "ticket": "i+M1P0Y6CFk=",
                  "siteVersion": "1115",
                  "method": "list"
                },
                "b":    {
                }}],
            ['产品列表',{
                "h":    {
                  "appToken": "M2I2Mzc1ZWVjNTQ1ZTc3ODNlOGIwMzNjMTlhN2RhNjc=",
                  "version": "1.0",
                  "group": "product",
                  "deviceId": "62e83ba9adea62b770ee297809662af66",
                  "device": "iPhone9,1",
                  "siteId": "0",
                  "ticket": "i+M1P0Y6CFk=",
                  "siteVersion": "1115",
                  "method": "list"
                },
                "b":    {
                }}],
            ['资讯列表',{
                "h":    {
                  "appToken": "M2I2Mzc1ZWVjNTQ1ZTc3ODNlOGIwMzNjMTlhN2RhNjc=",
                  "version": "1.0",
                  "group": "help",
                  "deviceId": "62e83ba9adea62b770ee297809662af66",
                  "device": "iPhone9,1",
                  "siteId": "0",
                  "ticket": "i+M1P0Y6CFk=",
                  "siteVersion": "1115",
                  "method": "find"
                },
                "b":    {
                }}]]



giftdata= ['发送礼物接口',{
                "b": {
                    "uniqueId": "9a51ed5e-e844-407b-be6b-4b4f93b08318",
                    "giftCode": "1",
                    "liveId": "34921",
                    "giftNum": "1"
                },
                "h": {
                    "appToken": "NzU5YjE5NjZlYjY5M2MzMTAxMmNkMDlkMDc0ODg3MDI=",
                    "device": "Xiaomi:Mi Note 2:23",
                    "deviceId": "000000007f65e78fe6edc17d00000000",
                    "group": "gift",
                    "method": "send",
                    "s": "1506065435010",
                    "siteId": "1",
                    "siteVersion": "1125",
                    "ticket": "sHw+cuiafvM=",
                    "version": "1.4"
                }}]