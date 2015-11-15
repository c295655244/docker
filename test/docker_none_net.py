from docker import Client
import docker

c = Client(base_url='unix:///var/run/docker.sock')


# cons=c.containers(all=True)
# for container in cons:

# 	c.remove_container(container=container["Id"],force=True)

container = c.create_container(
	image='ubuntu:http',
	name="test",
	stdin_open=True,
	command="python  /home/http_test.py",
	host_config=c.create_host_config(privileged=True,publish_all_ports=True)
	)
result=c.start(
	container=container.get('Id'),
	)
print result

exec_container=c.exec_create(
	container="test",
	cmd="ifconfig",
	)
response=c.exec_start(exec_id=exec_container.get('Id'),tty=True)

print response