import socket
import sys


port=10086
host=sys.argv[1]
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
while True:
	data="haha"
	s.sendto(data,(host,port))