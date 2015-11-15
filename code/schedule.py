#Copyright © 2015  All rights reserved.

#名称：子域名获取

#作者：陈晨

#时间：2015.10.1



#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import optparse
import Queue#python专有的队列结构
import sys
import dns.resolver
import threading
import time
import optparse
import MySQLdb
import traceback
import signal
import control
from lib.consle_width import getTerminalSize


class DNSBrute:
    #初始化
    def __init__(self,threads_num, output):
        self.thread_count = self.threads_num = threads_num#线程数
        self.lock = threading.Lock()
        self.task_queue = Queue.Queue()
        self.result_queue = Queue.Queue()




    #主查询函数
    def handle(self):
        thread_id = int( threading.currentThread().getName() )
        
        pass#进行操作

        while True: 
        if self.queue.qsize() > 0: 
            sub = self.queue.get(timeout=1.0)
            if self.exit_signal==True:
                break
            try:
                cur_sub_domain = sub + '.' + self.target
                answers = d.resolvers[thread_id].query(cur_sub_domain)#返回查询结果
                if answers:
                    for answer in answers:
                        self.lock.acquire()
                        if answer.address not in self.ip_dict:
                            self.ip_dict[answer.address] = 1
                        else:
                            self.ip_dict[answer.address] += 1
                        self.lock.release()
                        continue
                    self.lock.acquire()
                    for answer in answers:
                        self._out_to_mysql(cur_sub_domain,answer.address)
                        self.last_domain=self.target
                    self.lock.release()
                    for i in self.next_subs:
                        self.queue.put(i + '.' + sub)
            except Exception, e:
                pass
        self.lock.acquire()
        self.thread_count -= 1
        self.lock.release()

    #退出时运行的函数
    def _prepare_to_exit(self):
        self.outfile.write('\n----------'+time.strftime('%Y-%m-%d %H:%M:%S')+'--------------\n'+
            '结束时查询的域名： '+self.last_domain+ '\n本次共查询域名数量：'+str(self.finished_count)+
            '\n')
        print "日志文件已写入!"
        self.conn.close()
        self.cursor.close()
        sys.exit(0)

    #信号处理函数
    def signal_handler(self,sig,frame):
        self.exit_signal=True
        
        



    def send_control(self):
        port=8081
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind(('localhost',port))
        while 1:
            json,addr=s.recvfrom(1024)
            data=simplejson.loads(json)
            print "接受来自："+addr[0]+" 的命令"
            print "命令为: "+data["type"]
            json=simplejson.dumps(self.resolve(data))
            print "成功返回结果"
            s.sendto(json,addr)



    def recv_control(self):
        display={
        "host":"",
        "version":"1.7.1",
        "image":True,    #是否显示全部镜像
        "all_container":True    #是否显示全部容器，True为显示全部容器，False为显示正在运行的容器
        }
        control={
        "type":"display",     #操作类型
        "operation":display     #具体操作字典
        }
        self.queue.put(control)


    def thread_start(self,func):
        thread = threading.Thread(target=func, name=str(i))
        thread.setDaemon(True)#将线程声明为守护线程
        thread.start()

    def run(self):
        #控制退出信号
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)

        self.thread_start(func=self.recv_control)
        self.thread_start(func=self.send_control)


        while 1:          #进入无线循环查询

            for i in range(self.threads_num):#开启线程
                self.thread_start(func=self.handle)


            #当单条查询结束时退出循环
            while self.thread_count > 0:
                time.sleep(0.5)



            #接收到退出信号时退出程序
            if self.exit_signal==True:
                self._prepare_to_exit()
                break



if __name__ == '__main__':

    #解析参数
    parser = optparse.OptionParser('usage: %prog [options] the file of first domain  \n\nFor example:  python subDomainsBrute.py data.txt')
    parser.add_option('-t', '--threads', dest='threads_num',
              default=10, type='int',
              help='Number of threads. default = 10')
    parser.add_option('-f', '--file', dest='names_file', default='subnames.txt',
              type='string', help='Dict file used to brute sub names')
    parser.add_option('-o', '--output', dest='output', default="log.txt",
              type='string', help='Output file name. default is log.txt')

    (options, args) = parser.parse_args()


    if len(args) < 1:
        parser.print_help()
        sys.exit(0)

    d = DNSBrute(domains_file=args[0], names_file=options.names_file,
                 threads_num=options.threads_num,
                 output=options.output)
    d.run()


