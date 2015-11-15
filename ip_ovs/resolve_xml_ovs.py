# -*- coding:utf-8 -*-

from  xml.dom import  minidom



def get_attrvalue(node, attrname):
     return node.getAttribute(attrname) if node else ''

def get_nodevalue(node, index = 0):
    return node.childNodes[index].nodeValue if node else ''

def get_xmlnode(node,name):
    return node.getElementsByTagName(name) if node else []

def xml_to_string(filename='ovs.xml'):
    doc = minidom.parse(filename)
    return doc.toxml('UTF-8')


def get_xml_ovs(filename='ovs.xml'):
    doc = minidom.parse(filename) 
    root = doc.documentElement

    list_ovs=[]
    list_relation=[]
    list_relations={}
    ovs_nodes = get_xmlnode(root,'ovs_define')
    for node in ovs_nodes: 
        ovs_id = int(get_attrvalue(node,'ovs_id') )
        node_name = get_xmlnode(node,'ovs_name')
        num = get_xmlnode(node,'docker_num')
        ovs_name= get_nodevalue(node_name[0]).encode('utf-8','ignore')
        docker_num=int(get_nodevalue(num[0]).encode('utf-8','ignore'))
        data={
            "ovs_id":ovs_id,
            "ovs_name":ovs_name,
            "docker_num":docker_num
            }
        list_ovs.append(data)

    relations=get_xmlnode(root,'ovs-ovs')
    for node in relations: 
        node1 = get_xmlnode(node,'point1')
        node2 = get_xmlnode(node,'point2')
        point1= int(get_nodevalue(node1[0]).encode('utf-8','ignore'))
        point2=int(get_nodevalue(node2[0]).encode('utf-8','ignore'))
        point=[point1,point2]
        list_relation.append(point)

    list_relations={
    "list_relation":list_relation
    }
    return list_ovs,list_relations
        


if __name__ == "__main__":
    print get_xml_ovs()
    