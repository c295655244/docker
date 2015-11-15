#coding=utf-8
from pymongo import MongoClient



ip_start={
	"start":"10.0.0.0"
	}
key="ip"
client = MongoClient('172.26.253.3',27017)
data=client.ovs["docker_info"]
print  [post for post in data.find({"name":"165156"})]

#post_id=ovs_link.delete_many({})
#post_id=ovs_link.insert_one(ip_start).inserted_id 



# ip_remain={
# 	"start_ip":"20.0.0.1", 
# 	"end_ip":"20.0.0.32", 
# 	"mask":27
# }
# remain=client.ovs.ip_remain
# post_id=remain.insert_one(ip_remain).inserted_id 

# print post_id
