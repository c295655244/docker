#coding=utf-8
from pymongo import MongoClient
import ip_distribution
import resolve_xml_ovs


class mongo_opreate():
	'''
	@功能：实现数据库操作
	'''
	def __init__(self,ip='172.26.253.3',port=27017):
		self.client = MongoClient(ip, port)


	'''
	@功能：存储操作
	'''	
	def save_ovs_info(self,list_ovs):
		ovs_info=self.client.ovs.ovs_info
		post_id = [ovs_info.insert_one(post).inserted_id  for post in list_ovs] 
		return post_id

	def save_ovs_link(self,list_relation):
		ovs_link=self.client.ovs.ovs_link
		post_id=ovs_link.insert_one(list_relation).inserted_id 
		return post_id

	def save_docker_info(self,docker_info):
		docker_info=self.client.ovs.docker_info
		post_id = [docker_info.insert_one(post).inserted_id  for post in docker_info] 
		return post_id



	'''
	@功能：读取操作
	'''
	def display_ovs_info(self,table):
		data=self.client.ovs[table]
		return [post for post in data.find({})]

		

if __name__ == '__main__':
	mongo=mongo_opreate()
	list_ovs,list_relation=resolve_xml_ovs.get_xml_ovs()
	test=ip_distribution.ip_distribution()
	lists=test.distribution_ovs("10.0.0.0",list_ovs)
	print mongo.save_ovs_link(list_relation)
