#coding=utf-8
from docker import Client
import traceback
import socket
import simplejson


'''

控制包：

control={
	"type":"create",     #操作类型
	"operation":{具体操作}     #具体操作字典
}


创建：

create={
	"host":"192.168.122.227",
	"version":"1.7.1",
	"create_num":10,      #创建个数
	"name_pro":"docker",     #待创建容器前缀名
	"image":"ubuntu:14.04"    #选择镜像名称或id
}


执行：
execute={
	"host":"192.168.122.227",
	"version":"1.7.1",
	"name":"docker1",     #待执行容器名
	"cmd":"ping 127.0.0.1",      #待执行命令
	"all_exec":False,    #是否全部容器执行
	"delete":False     #运行完成后是否删除容器
}


删除：
delete={
	"host":"192.168.122.227",
	"version":"1.7.1",
	"del_all":True,       #是否全部删除
	"name":"docker"    #若不全部删除，则删除该名称容器
}


查看状态：
display={
	"host":"192.168.122.227",
	"version":"1.7.1",
	"image":True,    #是否显示全部镜像
	"all_container":True    #是否显示全部容器，True为显示全部容器，False为显示正在运行的容器
}

'''


class docker_operate:  

	# def __init__(self):  
	# 	self.client = Client(base_url='unix:///var/run/docker.sock')
	# 	self.client = Client(base_url='tcp://192.168.122.227:2375',version="1.7.1")

	'''
	@功能：解析参数

	@格式：
		control={
		"type":"create",     #操作类型
		"operation":{具体操作}     #具体操作字典
		}
	'''

	#解析命令参数
	def resolve(self,control):
		if control["type"]=="create":
			return self.create(control["operation"])

		if control["type"]=="execute":
			return self.execute(control["operation"])

		if control["type"]=="delete":
			return self.delete(control["operation"])

		if control["type"]=="display":
			return self.display(control["operation"])



	#创建容器
	def create(self,operation):
		self.host="tcp://"+operation["host"]+":2375"
		self.version=operation["version"]
		self.client = Client(base_url=self.host)

		contains_num=len(self.client.containers(all=True))
		try:
			for num in range(operation["create_num"]):
				name=operation["name_pro"]+str(num+contains_num)
				container = self.client.create_container(
					image=operation["image"],
					name=name,
					stdin_open=True,
					host_config=c.create_host_config(network_mode='none',privileged=True,publish_all_ports=True)
					)
				self.client.start(container=container.get('Id'))
			result={
				"operation":"create",
				"return":0,
				"error":None
			}
		except:
			result={
				"operation":"create",
				"return":-1,
				"error":str(traceback.format_exc())
			}
		return result


	#执行命令
	def execute(self,operation):
		self.host="tcp://"+operation["host"]+":2375"
		self.version=operation["version"]
		self.client = Client(base_url=self.host)
		try:
			if operation["all_exec"]==True:
				all_containers=self.client.containers(all=True)
				for container in all_containers:
					exec_container=self.client.exec_create(
						container=container["Id"],
						cmd=operation["cmd"],
						)
					response=self.client.exec_start(exec_id=exec_container.get('Id'),tty=True)
					returns.append(str(response))					

					if operation["delete"]==True:
						self.client.remove_container(container=exec_container.get('Id'),force=True)
				result={
					"operation":"execute",
					"return":returns,
					"error":None
				}
			else:
				exec_container=self.client.exec_create(
					container=operation["name"],
					cmd=operation["cmd"],
					)
				response=self.client.exec_start(exec_id=exec_container.get('Id'),tty=True)
				returns.append(str(response))
				if operation["delete"]==True:
					self.client.remove_container(container=exec_container.get('Id'),force=True)

				result={
				"operation":"execute",
				"return":returns,
				"error":None
				}

		except:
			result={
				"operation":"execute",
				"return":-1,
				"error":str(traceback.format_exc())
			}
		return result





	#删除容器
	def delete(self,operation):
		self.host="tcp://"+operation["host"]+":2375"
		self.version=operation["version"]
		self.client = Client(base_url=self.host)
		try:
			if operation["del_all"]==True:
				all_containers=self.client.containers(all=True)
				for container in all_containers:
					self.client.remove_container(container=container["Id"],force=True)
			else:
				self.client.remove_container(container=operation["name"],force=True)

			result={
				"operation":"delete",
				"return":0,
				"error":None
			}

		except:
			result={
				"operation":"delete",
				"return":-1,
				"error":str(traceback.format_exc())
			}
		return result



	#查看容器
	def display(self,operation):
		self.host="tcp://"+operation["host"]+":2375"
		self.version=operation["version"]
		self.client = Client(base_url=self.host)
		try:
			if operation["image"]==True:
				images=self.client.images(all=True)
			else:
				images=[]

			if operation["all_container"]==True:
				containers=self.client.containers(all=True)
			else:
				containers=self.client.containers()

			result={
				"operation":"display",
				"return":{
					"images":images,
					"containers":containers
					},
				"error":None
			}

		except:
			result={
				"operation":"display",
				"return":-1,
				"error":str(traceback.format_exc())
			}
		return result

	#建立控制方连接
	def socket_message(self):
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

if __name__ == '__main__':

	docker=docker_operate()
	docker.socket_message()