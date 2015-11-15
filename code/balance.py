#coding=utf-8
from docker import Client
import traceback
import socket
import copy
import simplejson
import crash_on_ipy


'''

host={
	
	"ip":"127.0.0.1",
	"docker_version":"1.7.1",
	"remain_mem":0,
	"cpu":0,
	"exist_docker":0,
	"run_docker":0
}

'''

class create_balance():
	def __init__(self,hosts_config):
		self.hosts=hosts_config

	def cul_min(self,hosts):
		min_id=0
		min_docker=1000000
		for num in xrange(0,len(hosts)):
			if hosts[num]["exist_docker"]<min_docker:
				min_docker=hosts[num]["exist_docker"]
				min_id=num

		return min_id


	def balance(self,create_operation):
		creates=[]
		hosts_docker= copy.deepcopy(self.hosts)
		for num in xrange(0,create_operation["create_num"]):
			min_host=self.cul_min(hosts_docker)
			hosts_docker[min_host]["exist_docker"]+=1

		for host_id in xrange(0,len(hosts_docker)):
			create_num=hosts_docker[host_id]["exist_docker"]-self.hosts[host_id]["exist_docker"]
			if create_num!=0:
				create={
					"host":self.hosts[host_id]["ip"],
					"version":self.hosts[host_id]["docker_version"],
					"create_num":create_num,      #创建个数
					"name_pro":create_operation["name_pro"],     #待创建容器前缀名
					"image":create_operation["image"]    #选择镜像名称或id
				}
				creates.append(create)

		return creates


if __name__ == '__main__':
	create={
	"host":"192.168.122.227",
	"version":"1.7.1",
	"create_num":10,      #创建个数
	"name_pro":"docker",     #待创建容器前缀名
	"image":"ubuntu:14.04"    #选择镜像名称或id
	}
	hosts=[
			{				
				"ip":"127.0.0.1",
				"docker_version":"1.7.1",
				"remain_mem":0,
				"cpu":0,
				"exist_docker":3,
				"run_docker":0,
				"max_limit_docker":100
			},
			{
				
				"ip":"127.0.0.1",
				"docker_version":"1.7.1",
				"remain_mem":0,
				"cpu":0,
				"exist_docker":0,
				"run_docker":0,
				"max_limit_docker":100
			}
		]

	example=create_balance(hosts)
	print example.balance(create)

		
