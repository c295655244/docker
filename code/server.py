#coding=utf-8
from docker import Client
client = Client(base_url="tcp://127.0.0.1:2375")
for x in range(1):
	client.create_container(
	image="ubuntu:14.04",
	detach=True,
	stdin_open=True
	)
