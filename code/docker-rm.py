from docker import Client

c = Client(base_url='unix:///var/run/docker.sock')


cons=c.containers(all=True)

for container in cons:

	c.remove_container(container=container["Id"],force=True)

