#coding=utf-8
from docker import Client
import traceback
import socket
import simplejson

class docker_monitor:  

	def __init__(self):
		pass

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
	pass