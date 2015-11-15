from docker import Client

c = Client(base_url='unix:///var/run/docker.sock')

container=c.create_container(image="ubuntu:test",name="test1",command="/bin/bash",stdin_open=True,host_config=c.create_host_config(privileged=True,publish_all_ports=True))
c.start(container=container.get('Id'))

container=c.create_container(image="ubuntu:test",name="test2",command="/bin/bash",stdin_open=True,host_config=c.create_host_config(privileged=True,publish_all_ports=True))
c.start(container=container.get('Id'))

exec_container=c.exec_create(container="test1",cmd="python  /home/server.py")
response=c.exec_start(exec_id=exec_container.get('Id'),tty=True)