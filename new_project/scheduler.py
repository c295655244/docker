# coding=utf-8
'''
@作者：陈晨
@时间：2015.10.25
@功能：docker创建调度
'''
import copy
import monitor
from FastNewman import *

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


class scheduler():

    def __init__(self):
        pass


    #计算当前宿主机存在的docker数量
    def cal_now_docker(self,host_list):
        for host in host_list:
            host["now_docker_num"]=host["docker_max_num"]-monitor.get_host_docker_info(host)["num"]



    #检查创建docker数量是否大于宿主机限制
    def check(self,ovs_list, host_list):
        ovs_num_list = [ovs["OVS_Docker_Num"] for ovs in ovs_list]
        sum_ovs_docker = sum(ovs_num_list)
        host_now_docker = [host["now_docker_num"] for host in host_list]
        sum_host_docker= sum(host_now_docker)
        if sum_ovs_docker>sum_host_docker:
            return False
        else:
            return True


    #负载均衡算法分配方式
    def balance_divide(self, ovs_list, host_list, list_relation):
        ovs_name_list = [ovs["OVS_ID"] for ovs in ovs_list]
        ovs_num_list = [ovs["OVS_Docker_Num"] for ovs in ovs_list]
        sum_docker = sum(ovs_num_list)
        ovs_num = len(ovs_list)
        host_num = len(host_list)

        #获取ovs的关联关系，以list_id为标志
        List = [[ovs_name_list.index(item) for item in relation] for relation in list_relation]

        #进行fastnewman算法分割
        divide_result,divide_index,club_link=fast_newman(ovs_name_list,List, len(ovs_name_list), host_num)

        #统计已被分割开的联系
        club_link=[[ovs_name_list[i] for i in item] for item in club_link]

        divide_ovs=[]
        for item in divide_index:
            dic={
                "relation":item,
                "docker_num":sum([ovs_num_list[i] for i in item])
            }
            divide_ovs.append(dic)
        divide_ovs.sort(key=lambda x:x["docker_num"])
        host_list.sort(key=lambda x:x["now_docker_num"])

        create_list = []
        ovs_lists = []
        balance_flag=True#标志是否成功分配
        for count in xrange(len(host_list)):
            if divide_ovs[count]["docker_num"]<=host_list[count]["now_docker_num"]:

                host=host_list[count]
                for index in divide_ovs[count]["relation"]:
                    ovs=ovs_list[index]
                    create = {
                        "host": host["ip"],
                        "version": host["docker_version"],
                        "create_num": ovs["OVS_Docker_Num"],  # 创建个数
                        'start_ip': ovs["OVS_Start_Ip"],
                        'end_ip': ovs["OVS_End_Ip"],
                        'mask': ovs["OVS_Mask"],
                        "name_pro": ovs["OVS_ID"],  # 待创建容器前缀名
                        "image": ovs["OVS_Image"],  # 选择镜像名称或id
                        "ovs_id": ovs["OVS_ID"],
                    }
                    ovs['OVS_HOST_IP'] = host["ip"]
                    create_list.append(create)
                    ovs_lists.append(ovs)
            else:
                break
                balance_flag=False

        if balance_flag==True:
            operation = {
                "type": "create",
                "operation": create_list
            }
            return operation, ovs_lists, club_link
        else:
            return False




    #单主机分配方式
    def single_divide(self, ovs_list, host_list, list_relation):
        ovs_name_list = [ovs["OVS_ID"] for ovs in ovs_list]
        ovs_num_list = [ovs["OVS_Docker_Num"] for ovs in ovs_list]
        sum_docker = sum(ovs_num_list)
        ovs_num = len(ovs_list)
        host_num = len(host_list)

        
        for host in host_list:
            #判断是否有虚拟机可容纳全部拓扑图
            if sum_docker <= host["now_docker_num"]:
                create_list = []
                ovs_lists = []
                for ovs in ovs_list:
                    create = {
                        "host": host["ip"],
                        "version": host["docker_version"],
                        "create_num": ovs["OVS_Docker_Num"],  # 创建个数
                        'start_ip': ovs["OVS_Start_Ip"],
                        'end_ip': ovs["OVS_End_Ip"],
                        'mask': ovs["OVS_Mask"],
                        "name_pro": ovs["OVS_ID"],  # 待创建容器前缀名
                        "image": ovs["OVS_Image"],  # 选择镜像名称或id
                        "ovs_id": ovs["OVS_ID"],
                    }
                    ovs['OVS_HOST_IP'] = host["ip"]
                    create_list.append(create)
                    ovs_lists.append(ovs)
                operation = {
                    "type": "create",
                    "operation": create_list
                }
                return operation, ovs_lists, []
        return False





    #背包算法分配方式
    def packing_divide(self, ovs_list, host_list, list_relation):
        ovs_name_list = [ovs["OVS_ID"] for ovs in ovs_list]
        ovs_num_list = [ovs["OVS_Docker_Num"] for ovs in ovs_list]
        sum_docker = sum(ovs_num_list)
        ovs_num = len(ovs_list)
        host_num = len(host_list)
        index=0
        create_list = []
        ovs_lists = []
        for host in host_list:
            while ovs_list[index]["OVS_Docker_Num"] <= host["now_docker_num"]: 
                ovs=ovs_list[index]         
                create = {
                    "host": host["ip"],
                    "version": host["docker_version"],
                    "create_num": ovs["OVS_Docker_Num"],  # 创建个数
                    'start_ip': ovs["OVS_Start_Ip"],
                    'end_ip': ovs["OVS_End_Ip"],
                    'mask': ovs["OVS_Mask"],
                    "name_pro": ovs["OVS_ID"],  # 待创建容器前缀名
                    "image": ovs["OVS_Image"],  # 选择镜像名称或id
                    "ovs_id": ovs["OVS_ID"],
                }
                ovs['OVS_HOST_IP'] = host["ip"]
                create_list.append(create)
                ovs_lists.append(ovs)                
                index+=1
                if index>=ovs_num:
                    break
            if index>=ovs_num:
                break

        #获取ovs的关联关系，以list_id为标志
        List = [[ovs_name_list.index(item) for item in relation] for relation in list_relation]
        club_link=[]
        for item in List:
            if ovs_list[item[0]]['OVS_HOST_IP'] !=ovs_list[item[1]]['OVS_HOST_IP']:
                club_link.append([ovs_list[item[0]]["OVS_ID"],ovs_list[item[1]]["OVS_ID"]])

        operation = {
            "type": "create",
            "operation": create_list
        }
        return operation, ovs_lists, club_link   




    #docker分配调度
    def docker_scheduler(self, ovs_list, host_list, list_relation):

        #计算当前目前存在的docker数量
        self.cal_now_docker(host_list)


        #检查是否符合分配条件
        if self.check(ovs_list, host_list)==False:
            print "创建的docker数量已超过宿主机限制！请修改后重试"
            return False

        #单主机分配      
        result_single=self.single_divide(ovs_list, host_list, list_relation)
        if result_single!=False:
            return result_single

        #负载均衡算法分配
        result_balance=self.balance_divide(ovs_list, host_list, list_relation)
        if result_balance!=False:
            return result_balance

        #背包算法分配
        return self.packing_divide(ovs_list, host_list, list_relation)
        

        

if __name__ == '__main__':
    import resolve_xml_ovs
    example = scheduler()
    list_ovs, list_relation = resolve_xml_ovs.get_xml_ovs()
    list_host = resolve_xml_ovs.get_xml_host_conf()
    for x in example.docker_scheduler(list_ovs, list_host, list_relation):
        print x
