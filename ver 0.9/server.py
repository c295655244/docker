#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#Copyright © 2015  All rights reserved.

#作者：陈晨

#时间：2015.10.1


import optparse
import Queue#python专有的队列结构
import sys
import threading
import time
import traceback
import signal
import socket
import simplejson
import control
reload(sys)   
sys.setdefaultencoding('utf8')  


class controls:
    #初始化
    def __init__(self,threads_num):
        self.thread_count = 0
        self.threads_num = threads_num#线程数
        self.task_queue = Queue.Queue()
        self.result_queue = Queue.Queue()
        self.exit_signal=False
        self.docker_operate=control.docker_operate()

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
                if self.task_queue.empty() == False:
                    print "收到"
                    data=self.task_queue.get()

                    '''
                    此处为docker操作函数
                    '''

                    result="服务器已收到！"
                    #result=self.docker_operate.resolve(data)

                    self.result_queue.put(result)

                if self.exit_signal==True:
                    break
        except:
            print traceback.format_exc()
        
    def send_control(self):
        try:
            port=8082
            host='localhost'
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            while True:
                if self.result_queue.empty() == False:
                    data =self.result_queue.get(timeout=1.0)
                    print "结果已发送"
                    json=simplejson.dumps(data)
                    s.sendto(json,(host,port))
                if self.exit_signal==True:
                    break
        except:
            print traceback.format_exc()



    def recv_control(self):
        try:
            port=8081
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.bind(('localhost',port))
            while 1:
                json,addr=s.recvfrom(1024)
                data=simplejson.loads(json)
                self.task_queue.put(data)
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

        for i in xrange(0,self.threads_num):
            self.thread_start(func=self.handle)

        while True:
            time.sleep(5)
            if self.exit_signal==True:
                    break



if __name__ == '__main__':

    d = controls(1)
    d.run()


