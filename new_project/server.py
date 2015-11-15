#coding=utf-8
import resolve_xml_ovs
import mongodb
import ip_distribution
import scheduler
import hashlib   
import time
import random
import traceback
import control


#获取随机id（16位）
def srand():
	rand=random.randint(0,15)
	src = str(time.time())
	m2 = hashlib.md5()
	m2.update(src)   
	str_rand=m2.hexdigest()[rand:rand+16]
	return str_rand


def demo_recover_ip():

	ip_start={
	"start":"10.0.0.0"
	}
	mongo=mongodb.mongo_opreate()
	mongo.del_tpl(ip_start,{})
	mongo.save_tpl_dic(ip_start,"ip_start")



#测试用例，返回task字典
def demo_create():


	#建立对象
	test=ip_distribution.ip_distribution()
	example=scheduler.scheduler()

	#获取列表
	list_ovs,list_relation=resolve_xml_ovs.get_xml_ovs()
	list_host=resolve_xml_ovs.get_xml_host_conf()
	list_ovs_new=test.distribution_ovs(list_ovs)
	operation,list_ovs_new_new,ovs_link=example.docker_scheduler(list_ovs_new,list_host,list_relation)

	#构建任务字典
	task_list={
		"id":srand(),
		"ovs_link":list_relation,
		"ovs_tube_link":ovs_link,
		"ovs_list":list_ovs_new_new,
		"host_list":list_host,
		"operate":operation,
		"state":""
	}
	return  task_list

def demo_exec():
	mongo=mongodb.mongo_opreate()
	list_exec=resolve_xml_ovs.get_xml_host_exec()
	execute_list=[]
	for exec_info in list_exec:
		docker_info=mongo.display_tpl_condition("docker_info",{"name":exec_info["docker_list"][0]})
		if docker_info==[]:
			print "找不到列表：",exec_info["docker_list"],"内的容器！"
			continue
		execute={
			"host":docker_info[0]["host_ip"],
			"version":docker_info[0]["version"],
			"docker_list":exec_info["docker_list"],     #待执行容器名
			"cmd":exec_info["command"],      #待执行命令
			"docker_num":exec_info["docker_num"]
		}
		execute_list.append(execute)
	task_list={
		"id":srand(),
		"operate":{
			"type":"execute",     #操作类型
			"operation":execute_list     #具体操作字典
		},
		"state":""
	}
	return task_list

def demo_del():
	mongo=mongodb.mongo_opreate()
	list_ovs=resolve_xml_ovs.get_xml_del()
	list_del=[]
	for ovs_del in list_ovs:
		docker=mongo.display_tpl_condition("docker_info",{"link_ovs":ovs_del})
		docker_list=[{"version":one["version"],"name":one["docker_id"],"host":one["host_ip"]} for one in docker]
		list_del.extend(docker_list)
	task_list={
		"id":srand(),
		"operate":{
			"type":"delete",     #操作类型
			"operation":{
				"ovs_list":list_ovs,
				"docker_list":list_del
			}
		},
		"state":""
	}
	return task_list





if __name__ == '__main__':

	###########测试前调用：恢复初始ip#############
	demo_recover_ip()

	##############创建测试#####################
	# data=demo_create()
	# print data
	# docker=control.docker_operate()
	# print docker.resolve(data)


	##############执行测试#####################
	# data=demo_exec()
	# print data
	# docker=control.docker_operate()
	# result=docker.resolve(data)
	# for res in result["return"]:
	# 	print res

	##############删除测试#####################
	data=demo_del()
	print data
	docker=control.docker_operate()
	print docker.resolve(data)


