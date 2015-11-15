#coding=utf-8
import resolve_xml_ovs



class ip_distribution:

	"""
	@功能：ip分配

	"""

	def __init__(self):
		pass

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

	def distribution_subnet(self,start_ip,docker_num):
		index=self.cul_index(docker_num)
		mask=32-index
		end_num=self.ip2num(start_ip)+2**index-1
		end_ip=self.num2ip(end_num)
		next_ip=self.num2ip(end_num+1)
		return start_ip,end_ip,mask,next_ip

	def distribution_docker(self,start_ip,end_ip,ovs_name):



	def distribution_ovs(self,start_ip,list_ovs):
		
		ip_start=start_ip
		list_result=[]
		for ovs in list_ovs:
			if ovs["docker_num"]!=0:
				start_ip_ovs,end_ip_ovs,mask_ovs,ip_start=self.distribution_subnet(ip_start,ovs["docker_num"])
				ovs_list={
					'OVS_ID':ovs["ovs_id"],
					'OVS_Name':ovs["ovs_name"],
					'OVS_IP':start_ip_ovs,
					'OVS_Start_Ip':start_ip_ovs,
					'OVS_End_Ip':end_ip_ovs,
					'OVS_Docker_Num':ovs["docker_num"],
					'OVS_Mask':mask_ovs,
					'OVS_BroadCast':end_ip_ovs,
					'OVS_DNS':''
				}
				list_result.append(ovs_list)
		return list_result


if __name__ == '__main__':
	test=ip_distribution()
	list_ovs,list_relation=resolve_xml_ovs.get_xml_ovs()
	print test.distribution_ovs("10.0.0.0",list_ovs)