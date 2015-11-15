import socket
import sys

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(("127.0.0.1",10086))
while 1:
    data,addr=s.recvfrom(1024)
    print "from ",addr,"    message:",data