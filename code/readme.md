安装最新版本docker


sudo apt-get install apt-transport-https  


# Add the Docker repository key to your local keychain  
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9  


# Add the Docker repository to your apt sources list.  
sudo sh -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"  


# update your sources list  
sudo apt-get update  

   
# 之后通过下面命令来安装最新版本的docker：  
apt-get install -y lxc-docker  


# 以后更新则：  
apt-get update -y lxc-docker  

  
ln -sf /usr/bin/docker /usr/local/bin/docker  



安装docker-machine
Digest: sha256:51a30269d3f3aaa04f744280e3c118aea032f6df85b49819aee29d379ac313b5
https://github.com/docker/machine/releases




安装docker-python

#sudo apt-get install python-pip
#sudo pip install docker-py
----------------------------
# wget https://github.com/docker/docker-py/archive/master.zip
# unzip master
# cd docker-py-master/
# sudo python setup.py install




需要设置下docker配置文件

vi /etc/default/docker.io 
或者
vi /etc/default/docker #追加下面一行
DOCKER_OPTS="-H tcp://0.0.0.0:2375 -H  unix://var/run/docker.sock"

sudo service docker restart
或者
sudo service docker.io restart



获取ubuntu镜像

sudo docker pull dl.dockerpool.com:5000/ubuntu:14.04
国内镜像站点：http://dockerpool.com/



创建容器：

create_container

注意：

1.除了不能使用-a 参数，其他均可用start()运行
2.mem_limit参数指限制的内存数，接受浮点数表示，例如： ('100000b', '1000k', '128m', '1g')，若没有单位，则指1字节
3.volumes_from和dns的参数不能用于v1.10版本以下，应使用host_config参数提供的字典格式


参数:

image (str): 运行镜像
command (str or list): 要运行的命令
hostname(主机名称) (str): Optional(可选择的) hostname for the container
user (str or int): Username or UID
detach(分离) (bool(弯曲件)): Detached mode: run container in the background and print new container Id
stdin_open (bool): 是否保持运行，默认为否
tty (bool): Allocate a pseudo-TTY
mem_limit (float or str): 内存限制 (格式: [number][optional unit], where unit = b, k, m, or g)
ports (list of ints): A list of port numbers
environment (dict or list): A dictionary or a list of strings in the following format ["PASSWORD=xxx"] or {"PASSWORD": "xxx"}.
dns (list): 容器所使用的dns服务器
volumes(量) (str or list):
volumes_from (str or list): List of container names or Ids to get volumes from. Optionally(可选择的) a single string joining container id's with commas
network_disabled (bool(弯曲件)): 禁用网络
name (str): 容器名
entrypoint(进入点) (str or list): An entrypoint
cpu_shares (int or float): cpu使用
working_dir (str): Path to the working directory
domainname(域名) (str or list): 设置默认域名列表
memswap_limit (int):
host_config (dict): A HostConfig dictionary
mac_address (str): mac地址
labels(标签) (dict or list): A dictionary of name-value labels (e.g. {"label1": "value1", "label2": "value2"}) or a list of names of labels to set with empty values (e.g. ["label1", "label2"])
volume(量)_driver (str): The name of a volume driver/plugin(插件).


Returns (dict): A dictionary with an image 'Id' key and a 'Warnings' key.


