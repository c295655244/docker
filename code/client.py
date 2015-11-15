#coding=utf-8
#!/usr/bin/env python
import socket
import simplejson


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

json=simplejson.dumps(control)



#print control
port=8081
host='localhost'
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.sendto(json,(host,port))
json,addr=s.recvfrom(1024*8)
data=simplejson.loads(json)
print data["error"]