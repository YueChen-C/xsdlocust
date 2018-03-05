**locust性能测试脚本**
===================================
进入脚本目录下，在文件目录下运行

**1.单进程脚本**
-----------------------------------
命令行执行`locust -f start.py`

**2.开启执行多核多进程脚本**
-----------------------------------
先命令行`locust --master -f start.py`

后执行直接运行`openslave.py`脚本开启所有进程

开启多进程执行时需要修改文件路径/test.py要和master进程执行的文件相同。
`subprocess.call("locust --slave -f {0}/test.py --master-host=10.10.30.50".format(os.getcwd()),shell = True)`


直接启动GUI版本一键启动
-----------------------------------
进入 `DSDlocust/locustweb`目录

cmd运行`Python index.py runserver`

打开网页http://127.0.0.1:5000/index

