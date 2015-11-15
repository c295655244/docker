# coding=utf-8
from docker import Client
import traceback
import os
import socket
import simplejson
import resolve_xml_ovs
import mongodb






def get_host_docker_info(host):
    base_url = "tcp://" + host["ip"] + ":2375"
    version = host["docker_version"]
    client = Client(base_url=base_url)
    containers = client.containers(all=True)
    up_docker=[ container  for container in containers   if  "Up" in container["Status"]]
    data={
            "host_ip":host["ip"],
            "num":len(containers),
            "running_num":len(up_docker),
    }
    return data










class docker_monitor:

    def __init__(self):
        self.list_host = resolve_xml_ovs.get_xml_host_conf()
        self.mongo=mongodb.mongo_opreate()



    # 查看容器
    def display(self):
        os.system('clear')
        for host in self.list_host:
            ovs_list=self.mongo.display_tpl_condition("ovs_list",{"OVS_HOST_IP":host["ip"]})
            base_url = "tcp://" + host["ip"] + ":2375"
            self.version = host["docker_version"]
            self.client = Client(base_url=base_url)
            containers = self.client.containers(all=True)
            up_docker=[ container  for container in containers   if  "Up" in container["Status"]]
            
            print "主机\t\tovs节点个数\t已创建docker数量\t运行docker数量"
            print host["ip"],"\t",len(ovs_list),"\t\t",len(containers),"\t\t\t",len(up_docker)










if __name__ == '__main__':
    demo=docker_monitor()
    demo.display()
    list_host = resolve_xml_ovs.get_xml_host_conf()
    print get_host_docker_info(list_host[0])

