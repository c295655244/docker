import BaseHTTPServer    
import urlparse    
import time  
from SocketServer import ThreadingMixIn  
import threading  
  
class WebRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):    
    def do_GET(self):  
        buf = "Receive the request!\n"  
        self.protocal_version = "HTTP/1.1"   

        self.send_response(200)  

        self.send_header("Welcome", "Contect")         

        self.end_headers()  

        self.wfile.write(buf)  
  
class ThreadingHttpServer( ThreadingMixIn, BaseHTTPServer.HTTPServer ):  
    pass  
  
if __name__ == '__main__':  
    server = ThreadingHttpServer(('0.0.0.0',8083), WebRequestHandler)    
    ip, port = server.server_address  
    server_thread = threading.Thread(target=server.serve_forever)  
    server_thread.setDaemon(True)  
    server_thread.start()  
    print "Server loop running in thread:", server_thread.getName()  
    while True:  
        pass  