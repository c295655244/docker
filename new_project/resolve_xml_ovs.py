# -*- coding:utf-8 -*-


'''
@作者：陈晨
@时间：2015.10.25
@功能：解析xml
'''


from xml.dom import minidom
import hashlib
import time
import random
import os

path=os.path.dirname(os.path.abspath("__file__"))+"/xml/"

# 生成16位随机id
def srand_str():
    rand = random.randint(0, 15)
    src = str(time.time())
    m2 = hashlib.md5()
    m2.update(src)
    str_rand = m2.hexdigest()[rand:rand+16]
    return str_rand


def get_attrvalue(node, attrname):
    return node.getAttribute(attrname) if node else ''


def get_nodevalue(node, index=0):
    return node.childNodes[index].nodeValue if node else ''


def get_xmlnode(node, name):
    return node.getElementsByTagName(name) if node else []


# 获取删除文件


def get_xml_del(filename=path+'del.xml'):
    doc = minidom.parse(filename)
    root = doc.documentElement
    ovs_list = [get_nodevalue(ovs_id).encode('utf-8', 'ignore') for ovs_id in get_xmlnode(root, 'ovs_id')]
    return ovs_list


# 获取操作指令文件
def get_xml_host_exec(filename=path+'exec.xml'):
    doc = minidom.parse(filename)
    root = doc.documentElement

    list_exec = []
    exec_nodes = get_xmlnode(root, 'exec_docker')
    for node in exec_nodes:
        command = get_xmlnode(node, 'command')
        docker_num = get_xmlnode(node, 'docker_num')
        docker_list = [get_nodevalue(docker_id).encode('utf-8', 'ignore') for docker_id in get_xmlnode(node, 'docker_id')]
        command = get_nodevalue(command[0]).encode('utf-8', 'ignore')
        docker_num = int(get_nodevalue(docker_num[0]).encode('utf-8', 'ignore'))
        exec_info = {
            "command": command,
            "docker_num": docker_num,
            "docker_list": docker_list,
        }
        list_exec.append(exec_info)
    return list_exec


# 获取物理机配置文件
def get_xml_host_conf(filename=path+'host_config.xml'):
    doc = minidom.parse(filename)
    root = doc.documentElement

    list_host = []
    host_nodes = get_xmlnode(root, 'host_config')
    for node in host_nodes:
        host_id = get_attrvalue(node, 'host_id')
        host_ip = get_xmlnode(node, 'host_ip')
        docker_version = get_xmlnode(node, 'docker_version')
        mem = get_xmlnode(node, 'mem')
        cpu = get_xmlnode(node, 'cpu')
        docker_max_num = get_xmlnode(node, 'docker_max_num')
        host_ip = get_nodevalue(host_ip[0]).encode('utf-8', 'ignore')
        docker_version = get_nodevalue(docker_version[0]).encode('utf-8', 'ignore')
        mem = get_nodevalue(mem[0]).encode('utf-8', 'ignore')
        cpu = get_nodevalue(cpu[0]).encode('utf-8', 'ignore')
        docker_max_num = int(get_nodevalue(docker_max_num[0]).encode('utf-8', 'ignore'))
        host_info = {
            "host_id": host_id,
            "ip": host_ip,
            "docker_version": docker_version,
            "mem": mem,
            "cpu": cpu,
            "docker_max_num":docker_max_num
        }
        list_host.append(host_info)
    return list_host


# 获取ovs配置文件
def get_xml_ovs(filename=path+'ovs.xml'):
    doc = minidom.parse(filename)
    root = doc.documentElement

    list_ovs = []
    list_relation = []
    list_relations = {}
    ovs_nodes = get_xmlnode(root, 'ovs_define')
    for node in ovs_nodes:
        ovs_id = get_attrvalue(node, 'ovs_id')
        node_name = get_xmlnode(node, 'ovs_name')
        num = get_xmlnode(node, 'docker_num')
        docker_image = get_xmlnode(node, 'docker_image')
        ovs_name = get_nodevalue(node_name[0]).encode('utf-8', 'ignore')
        docker_image = get_nodevalue(docker_image[0]).encode('utf-8', 'ignore')
        docker_num = int(get_nodevalue(num[0]).encode('utf-8', 'ignore'))

        ovs_info = {
            'OVS_ID': ovs_id,
            'OVS_Name': ovs_name,
            'OVS_IP': "",
            'OVS_HOST_IP': "",
            'OVS_Start_Ip': "",
            'OVS_End_Ip': "",
            'OVS_Docker_Num': docker_num,
            'OVS_Mask': "",
            'OVS_BroadCast': "",
            'OVS_DNS': ''"",
            'OVS_State': "",
            'OVS_Image': docker_image
        }
        list_ovs.append(ovs_info)

    relations = get_xmlnode(root, 'ovs-ovs')
    for node in relations:
        node1 = get_xmlnode(node, 'point1')
        node2 = get_xmlnode(node, 'point2')
        point1 = get_nodevalue(node1[0]).encode('utf-8', 'ignore')
        point2 = get_nodevalue(node2[0]).encode('utf-8', 'ignore')
        point = [point1, point2]
        list_relation.append(point)

    return list_ovs, list_relation


if __name__ == "__main__":

    # print get_xml_del()
    print get_xml_host_conf()
    # print get_xml_ovs()
    # print get_xml_host_exec()
