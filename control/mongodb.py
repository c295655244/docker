#coding=utf-8
from pymongo import MongoClient


class mongo_opreate():
	'''
	@功能：实现数据库操作
	'''
	def __init__(self,ip='172.26.253.3',port=27017):
		self.client = MongoClient(ip, port)



	'''
	@功能：存储操作
	'''	
	#存储ovs联系
	def save_ovs_link(self,list_relation):
		ovs_link=self.client.ovs.ovs_link
		post_id=ovs_link.insert_one(list_relation).inserted_id 
		return post_id

	#存储模板
	def save_tpl_list(self,data_list,table):
		data=self.client.ovs[table]
		post_id = [data.insert_one(post).inserted_id  for post in data_list] 
		return post_id

	def save_tpl_dic(self,data_dic,table):
		data=self.client.ovs[table]
		post_id = data.insert_one(data_dic).inserted_id 
		return post_id




	'''
	@功能：读取操作
	'''
	def display_tpl(self,table):
		data=self.client.ovs[table]
		return [post for post in data.find({})]



	def del_tpl(self,table,condition):
		data=self.client.ovs[table]
		data.delete_many(condition)

		

