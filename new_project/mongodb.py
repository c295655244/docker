#coding=utf-8
from pymongo import MongoClient
import ip_distribution
import resolve_xml_ovs


class mongo_opreate():
	'''
	@功能：实现数据库操作
	'''
	def __init__(self,ip='127.0.0.1',port=27017):
		self.client = MongoClient(ip, port)



	'''
	@功能：存储操作
	'''	

	#存储模板
	def save_tpl_list(self,data_list,table,key=""):			
		data=self.client.ovs[table]
		if key=="":
			post_id = [data.insert_one(post).inserted_id  for post in data_list] 
			return post_id
		else:
			for post in data_list:
				if data.count({key:post[key]}) ==0:
					data.insert_one(post).inserted_id  

			#post_id = [data.insert_one(post).inserted_id  if data.count({key:post[key]}) !=0  for post in data_list]
			return data_list



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

	def display_tpl_condition(self,table,condition):
		data=self.client.ovs[table]
		return [post for post in data.find(condition)]



	def del_tpl(self,table,condition):
		data=self.client.ovs[table]
		data.delete_many(condition)

		

if __name__ == '__main__':
	mongo=mongo_opreate()
	list_ovs,list_relation=resolve_xml_ovs.get_xml_ovs()
	test=ip_distribution.ip_distribution()
	lists=test.distribution_ovs("10.0.0.0",list_ovs)
	print mongo.save_ovs_link(list_relation)
