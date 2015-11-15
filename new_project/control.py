# coding=utf-8
from docker import Client
import traceback
import socket
import simplejson
import mongodb
import ip_distribution


'''

控制包：

control={
	"type":"create",     #操作类型
	"operation":{具体操作}     #具体操作字典
}


创建：

create={
	"host":"192.168.122.227",
	"version":"1.7.1",
	"create_num":10,      #创建个数
	"name_pro":"docker",     #待创建容器前缀名
	"image":"ubuntu:14.04",    #选择镜像名称或id
	"start_ip":"10.0.0.1",
	"end_ip":"10.0.0.255",
	"link_ovs":0,
	"topo_id":0
}


执行：
execute={
	"host":"192.168.122.227",
	"version":"1.7.1",
	"id":"docker1",     #待执行容器名
	"cmd":"ping 127.0.0.1",      #待执行命令
}


删除：
delete={
	"host":"192.168.122.227",
	"version":"1.7.1",
	"del_all":True,       #是否全部删除
	"name":"docker"    #若不全部删除，则删除该名称容器
}


查看状态：
display={
	"host":"192.168.122.227",
	"version":"1.7.1",
	"image":True,    #是否显示全部镜像
	"all_container":True    #是否显示全部容器，True为显示全部容器，False为显示正在运行的容器
}

'''


class docker_operate:

    '''
    @功能：解析参数

    @格式：
            control={
            "type":"create",     #操作类型
            "operation":{具体操作}     #具体操作字典
            }
    '''

    def __init__(self):
        self.ip_solve = ip_distribution.ip_distribution(types=False)
        self.mongo = mongodb.mongo_opreate()

    # 解析命令参数
    def resolve(self, task):
        control = task["operate"]
        if control["type"] == "create":
            return self.create(task)

        if control["type"] == "execute":
            return self.execute(task)

        if control["type"] == "delete":
            return self.delete(task)

        if control["type"] == "display":
            return self.display(task)

    # 创建容器
    def create(self, task):
        operations = task["operate"]["operation"]
        try:
            for operation in operations:
                self.host = "tcp://"+operation["host"]+":2375"
                version = operation["version"]
                self.client = Client(base_url=self.host)
                contains_num = len(self.client.containers(all=True))
                ip_num_int = self.ip_solve.ip2num(operation["start_ip"])+1
                docker_list = []
                for num in range(operation["create_num"]):
                    name = operation["name_pro"]+str(num+contains_num)
                    container = self.client.create_container(
                        image=operation["image"],
                        name=name,
                        command="/bin/bash",
                        stdin_open=True,
                        host_config=self.client.create_host_config(
                            network_mode='none', privileged=True, publish_all_ports=True)
                    )
                    self.client.start(container=container.get('Id'))

                    docker_ip = self.ip_solve.num2ip(ip_num_int)

                    ip = docker_ip+"/"+str(operation["mask"])

                    # 此处分配ip 操作
                    print "已分配ip：", ip

                    # 构建docker节点数据，存库
                    docker_info = {
                        "image": operation["image"],
                        "docker_id": container.get('Id'),
                        "name": name,
                        "ip": docker_ip,
                        "broadcast": operation["end_ip"],
                        "gateway": operation["start_ip"],
                        "link_ovs": operation["ovs_id"],
                        "mask": operation["mask"],
                        "host_ip": operation["host"],
                        "version": operation["version"],
                        "state": "up"
                    }
                    ip_num_int += 1
                    docker_list.append(docker_info)
                docker_dic = {
                    "state": "no_ip",
                    "docker_list": docker_list,
                }
                self.mongo.save_tpl_list(docker_list, "docker_info")
            self.mongo.save_tpl_list(task["ovs_list"], "ovs_list", "OVS_ID")
            ovs_link = {
                "ovs_relation": task["ovs_link"]
            }
            self.mongo.save_tpl_dic(ovs_link, "ovs_link")
            result = {
                "operation": "create",
                "return": 0,
                "error": None
            }
        except:
            print traceback.format_exc()
            result = {
                "operation": "create",
                "return": -1,
                "error": str(traceback.format_exc())
            }
        return result["error"]

    # 执行命令
    def execute(self, task):
        operations = task["operate"]["operation"]
        try:
            returns = []
            for operation in operations:
                self.host = "tcp://"+operation["host"]+":2375"
                self.version = operation["version"]
                self.client = Client(base_url=self.host)
                for docker_id in operation["docker_list"]:
                    exec_container = self.client.exec_create(
                        container=docker_id,
                        cmd=operation["cmd"],
                    )
                    response = self.client.exec_start(
                        exec_id=exec_container.get('Id'), tty=True)
                    returns.append("来自"+docker_id+"的结果：\n"+str(response))

            result = {
                "operation": "execute",
                "return": returns,
                "error": None
            }

        except:
            print traceback.format_exc()
            result = {
                "operation": "execute",
                "return": -1,
                "error": str(traceback.format_exc())
            }
        return result

    # 删除容器
    def delete(self, task):
        operation = task["operate"]["operation"]
        host_ip = "127.0.0.1"
        self.host = "tcp://"+operation["docker_list"][0]["host"]+":2375"
        self.version = operation["docker_list"][0]["version"]
        self.client = Client(base_url=self.host)
        try:
            for docker in operation["docker_list"]:
                if docker["host"] != host_ip:
                    host_ip = docker["host"]
                    self.host = "tcp://"+docker["host"]+":2375"
                    self.version = docker["version"]
                    self.client = Client(base_url=self.host)
                try:
                    self.client.remove_container(
                        container=docker["name"], force=True)
                    self.mongo.del_tpl(
                        "docker_info", {"docker_id": docker["name"]})
                except:
                    print traceback.format_exc()
                    print "删除容器：", docker["name"], "错误！该容器可能不存在，或已经被删除！"
            result = {
                "operation": "delete",
                "return": 0,
                "error": None
            }

        except:
            print traceback.format_exc()
            result = {
                "operation": "delete",
                "return": -1,
                "error": str(traceback.format_exc())
            }
        return result

    # 查看容器
    def display(self, task):
        operations = task["operate"]["operation"]
        self.host = "tcp://"+operation["host"]+":2375"
        self.version = operation["version"]
        self.client = Client(base_url=self.host)
        try:
            if operation["image"] == True:
                images = self.client.images(all=True)
            else:
                images = []

            if operation["all_container"] == True:
                containers = self.client.containers(all=True)
            else:
                containers = self.client.containers()

            result = {
                "operation": "display",
                "return": {
                    "images": images,
                    "containers": containers
                },
                "error": None
            }

        except:
            print traceback.format_exc()
            result = {
                "operation": "display",
                "return": -1,
                "error": str(traceback.format_exc())
            }
        return result


if __name__ == '__main__':

    #############测试字典##########################
    create = {
        "host": "127.0.0.1",
        "version": "1.7.1",
        "create_num": 2,  # 创建个数
        "name_pro": "1",  # 待创建容器前缀名
        "image": "ubuntu:test",  # 选择镜像名称或id
        "start_ip": "10.0.0.1",
        "end_ip": "10.0.0.255",
        "ovs_id": "test_ovs",
        "mask": 27
    }
    display = {
        "host": "127.0.0.1",
        "version": "1.7.1",
        "image": True,  # 是否显示全部镜像
        "all_container": True  # 是否显示全部容器，True为显示全部容器，False为显示正在运行的容器
    }
    execute = {
        "host": "127.0.0.1",
        "version": "1.7.1",
        "docker_list": ["10", "11"],  # 待执行容器名
        "cmd": "ifconfig",  # 待执行命令
    }
    delete = {

        "docker_list": [{'host': '127.0.0.1', 'version': '1.7.1', 'name': '48'}, {'host': '127.0.0.1', 'version': '1.7.1', 'name': '49'}]
    }
    ####################执行测试####################################
    # control={
    # "type":"execute",     #操作类型
    # "operation":[execute]     #具体操作字典
    # }
    # controls={
    # "operate":control
    # }
    # docker=docker_operate()
    # result=docker.resolve(controls)
    # for res in result["return"]:
    # 	print res
    #####################创建测试#################################
    # control={
    # "type":"create",     #操作类型
    # "operation":[create]     #具体操作字典
    # }
    # controls={
    # "operate":control
    # }
    # docker=docker_operate()
    # print docker.resolve(controls)

    # 删除测试######################################.
    control = {
        "type": "delete",  # 操作类型
        "operation": delete  # 具体操作字典
    }
    controls = {
        "operate": control
    }
    docker = docker_operate()
    print docker.resolve(controls)["error"]
