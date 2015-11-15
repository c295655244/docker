#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#Copyright © 2015  All rights reserved.

#作者：陈晨

#时间：2015.10.1


import optparse
import Queue
import sys
import threading
import time
import traceback
import signal
import socket
import simplejson
reload(sys)   
sys.setdefaultencoding('utf8')  

class controls:
    #初始化
    def __init__(self,threads_num):
        self.thread_count = self.threads_num = threads_num#线程数
        self.task_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.exit_signal=False

    #退出时运行的函数
    def _prepare_to_exit(self):
        sys.exit(0)

    #信号处理函数
    def signal_handler(self,sig,frame):
        self.exit_signal=True
        pass

    def handle(self):
        try:        
            while True:

                if self.task_queue.qsize() > 0:
                    data=self.task_queue.get()
                    self.task_queue.put(data)

                if self.exit_signal==True:
                    break
        except:
            print traceback.format_exc()
        
    def send_control(self):
        execute={
        "host":"192.168.122.227",
        "version":"1.7.1",
        "name":"docker1",     #待执行容器名
        "cmd":"ps -ax",      #待执行命令
        "all_exec":False,    #是否全部容器执行
        "delete":False     #运行完成后是否删除容器
        }

        create={
        "host":"192.168.122.227",
        "version":"1.7.1",
        "create_num":2,      #创建个数
        "name_pro":"docker",     #待创建容器前缀名
        "image":"ubuntu:14.04"    #选择镜像名称或id
        }

        delete={
        "host":"192.168.122.227",
        "version":"1.7.1",
        "del_all":True,       #是否全部删除
        "name":"docker0"    #若不全部删除，则删除该名称容器
        }

        display={
        "host":"192.168.122.227",
        "version":"1.7.1",
        "image":True,    #是否显示全部镜像
        "all_container":True    #是否显示全部容器，True为显示全部容器，False为显示正在运行的容器
        }
        control={
        "type":"display",     #操作类型
        "operation":display     #具体操作字典
        }

        
        try:
            port=8081
            host='localhost'
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            while True:
                data = input("Please input:\n")
                json=simplejson.dumps(control)
                s.sendto(json,(host,port))
                if self.exit_signal==True:
                    break
        except:
            print traceback.format_exc()



    def recv_control(self):
        try:
            port=8082
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.bind(('localhost',port))
            while 1:
                json,addr=s.recvfrom(1024)
                data=simplejson.loads(json)
                print "接受来自："+addr[0]+" 的命令"
                print "命令为: "+str(data)
                if self.exit_signal==True:
                    break
        except:
            print traceback.format_exc()


    def thread_start(self,func):
        thread = threading.Thread(target=func)
        thread.setDaemon(True)#将线程声明为守护线程
        thread.start()

    def run(self):
        #控制退出信号
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

        self.thread_start(func=self.recv_control)
        self.thread_start(func=self.send_control)

        while True:
            time.sleep(5)
            if self.exit_signal==True:
                    break



if __name__ == '__main__':



    d = controls(1)
    d.run()


