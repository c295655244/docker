#coding=utf-8

'''
@作者：陈晨
@时间：2015.10.25
@功能：ip分配
'''



import resolve_xml_ovs
import mongodb
import time
import traceback

class ip_distribution:

	"""
	@功能：ip分配

	"""

	def __init__(self,types=True):
		self.mongo=mongodb.mongo_opreate()
		if types==True:
			while True:
				try:
					self.start_ip=self.mongo.display_tpl("ip_start")[0]['start']
					break
				except:
					print traceback.format_exc()  
					time.sleep(0.5)
					print "无法获取初始ip！"
			self.mongo.del_tpl("ip_start",{})

	def cul_index(self,num):
		'''
		@功能：计算最小指数
		'''
		number=num+2
		index=0
		accumulate=1
		while True:
			if number<=accumulate:
				return index

			else:
				index+=1
				accumulate*=2


	def ip2num(self,ip):

		ip=[int(x) for x in ip.split('.')]
		return ip[0] <<24 | ip[1]<<16 | ip[2]<<8 |ip[3]


	def num2ip(self,num):
		return '%s.%s.%s.%s' %( (num & 0xff000000) >>24,
			(num & 0x00ff0000) >>16,
			(num & 0x0000ff00) >>8,
			num & 0x000000ff )



	#分配ip
	def distribution_subnet(self,start_ip_init,docker_num):
		index=self.cul_index(docker_num)
		mask=32-index
		start_ip_func,end_ip=self.ip_get_remain(mask)
		if start_ip_func=="":
			start_ip_func=start_ip_init
			end_num=self.ip2num(start_ip_init)+2**index-1
			end_ip=self.num2ip(end_num)
			next_ip=self.num2ip(end_num+1)
		else:
			next_ip=self.num2ip(self.ip2num(start_ip_init)+1)
		return start_ip_func,end_ip,mask,next_ip


	#判断是否有已回收ip池可用
	def ip_get_remain(self,mask):
		ip_remain=self.mongo.display_tpl("ip_remain")
		if len(ip_remain)>0:
			for ip_pool in ip_remain:
				if mask>=ip_pool["mask"]:
					ip_start_pool=ip_pool["start_ip"]
					ip_end_pool=ip_pool["end_ip"]
					self.mongo.del_tpl("ip_remain",{'start_ip': ip_start_pool})
					return ip_start_pool,ip_end_pool

		return "",""

	def cul_docker_sum(self,list_ovs):
		list_num=[ovs["OVS_Docker_Num"] for ovs in list_ovs]
		return reduce(lambda x, y: x + y, list_num)


	def distribution_ovs(self,list_ovs):
		list_result=[]
		docker_sum=self.cul_docker_sum(list_ovs)
		next_ip=self.start_ip
		ip_start,ip_end,mask,next_ip=self.distribution_subnet(next_ip,docker_sum)
		start_ip_ovs=ip_start
		for ovs in list_ovs:
			ovs["OVS_IP"]=start_ip_ovs
			ovs["OVS_Start_Ip"]=start_ip_ovs
			ovs["OVS_End_Ip"]=self.num2ip(self.ip2num(start_ip_ovs)+ovs["OVS_Docker_Num"])
			ovs["OVS_Mask"]=mask
			ovs["OVS_BroadCast"]=ip_end
			list_result.append(ovs)
			start_ip_ovs=self.num2ip(self.ip2num(start_ip_ovs)+ovs["OVS_Docker_Num"]+1)
		
		ip_start_db={
		"start":start_ip_ovs
		}
		self.mongo.save_tpl_dic(ip_start_db,"ip_start_db")
		return list_result


	# def distribution_ovs(self,list_ovs):
		
	# 	next_ip=self.start_ip
	# 	list_result=[]


	# 	for ovs in list_ovs:
	# 		if ovs["OVS_Docker_Num"]!=0:
	# 			start_ip_ovs,end_ip_ovs,mask_ovs,next_ip=self.distribution_subnet(next_ip,ovs["OVS_Docker_Num"])
	# 			ovs["OVS_IP"]=start_ip_ovs
	# 			ovs["OVS_Start_Ip"]=start_ip_ovs
	# 			ovs["OVS_End_Ip"]=end_ip_ovs
	# 			ovs["OVS_Mask"]=mask_ovs
	# 			ovs["OVS_BroadCast"]=end_ip_ovs
	# 		else:
	# 			start_ip_ovs,end_ip_ovs,mask_ovs,next_ip=self.distribution_subnet(next_ip,10)
	# 			ovs["OVS_IP"]=start_ip_ovs
	# 			ovs["OVS_Start_Ip"]=start_ip_ovs
	# 			ovs["OVS_End_Ip"]=end_ip_ovs
	# 			ovs["OVS_Mask"]=mask_ovs
	# 			ovs["OVS_BroadCast"]=end_ip_ovs
	# 		list_result.append(ovs)
	# 	ip_start={
	# 	"start":next_ip
	# 	}
	# 	self.mongo.save_tpl_dic("ip_start",ip_start):
	# 	return list_result


if __name__ == '__main__':


	ip_start={
	"start":"10.0.0.0"
	}
	mongo=mongodb.mongo_opreate()
	mongo.save_tpl_dic(ip_start,"ip_start")


	test=ip_distribution()
	list_ovs,list_relation=resolve_xml_ovs.get_xml_ovs()
	print test.distribution_ovs(list_ovs)
