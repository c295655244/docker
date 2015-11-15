#coding=utf-8
from docker import Client
import traceback
import socket
import simplejson
import mongodb
import ip_distribution


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
	"image":"ubuntu:14.04",    #选择镜像名称或id
	"start_ip":"10.0.0.1",
	"end_ip":"10.0.0.255",
	"link_ovs":0,
	"topo_id":0
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

	'''
	@功能：解析参数

	@格式：
		control={
		"type":"create",     #操作类型
		"operation":{具体操作}     #具体操作字典
		}
	'''
	def __init__(self):
		self.ip_solve=ip_distribution.ip_distribution()
		self.mongo=mongodb.mongo_opreate()

	#解析命令参数
	def resolve(self,task):
		control=task["operate"]
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
		try:
			self.host="tcp://"+operation["host"]+":2375"
			version=operation["version"]
			self.client = Client(base_url=self.host)
			contains_num=len(self.client.containers(all=True))			
			ip_num_int=self.ip_solve.ip2num(operation["start_ip"])+1
			docker_list=[]
			for num in range(operation["create_num"]):
				name=operation["name_pro"]+str(num+contains_num)
				container = self.client.create_container(
					image=operation["image"],
					name=name,
					stdin_open=True,
					host_config=self.client.create_host_config(network_mode='none',privileged=True,publish_all_ports=True)
					)
				self.client.start(container=container.get('Id'))


				#构建docker节点数据，存库
				docker_info={
					"docker_id":container.get('Id'),
					"ip":self.ip_solve.num2ip(ip_num_int),
					"broadcast":operation["end_ip"],
					"gateway":operation["start_ip"],
					"link_ovs":operation["link_ovs"],
				}				
				ip_num_int+=1
				docker_list.append(docker_info)
			docker_dic={
				"state":"no_ip",
				"docker_list":docker_list,
			}
			self.mongo.save_tpl(docker_list,"docker_info")
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
		return result["error"]


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


if __name__ == '__main__':
	create={
	"host":"127.0.0.1",
	"version":"1.7.1",
	"create_num":5,      #创建个数
	"name_pro":"docker",     #待创建容器前缀名
	"image":"ubuntu:14.04",    #选择镜像名称或id
	"start_ip":"10.0.0.1",
	"end_ip":"10.0.0.255",
	"ovs_id":"65d56asd656e5",
	"mask":27
	}
	display={
		"host":"127.0.0.1",
		"version":"1.7.1",
		"image":True,    #是否显示全部镜像
		"all_container":True    #是否显示全部容器，True为显示全部容器，False为显示正在运行的容器
	}
	control={
	"type":"create",     #操作类型
	"operation":create     #具体操作字典
	}
	control={
	"operate":control
	}
	docker=docker_operate()
	print docker.resolve(control)