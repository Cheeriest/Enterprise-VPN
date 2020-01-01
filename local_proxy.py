import socket, json, sys, select
from threading import Thread
from base64 import b64encode



MAX_BUFFER = 64 * 512
VPN_IP = '192.168.1.107'
VPN_PORT = 50002

class ClientThread(Thread):
    def __init__(self, addr, conn, token):
        Thread.__init__(self)
        self.client_socket = conn
        self.token = token
        
    def run(self):
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server_socket.connect((VPN_IP, VPN_PORT))
        except:
            sys.exit('error')
            
        data = self.client_socket.recv(MAX_BUFFER)
        self.server_socket.sendall(data)
        data = self.server_socket.recv(MAX_BUFFER)
        self.client_socket.sendall(data)
        
        self.client_socket.setblocking(0)
        self.server_socket.setblocking(0)
        
        while 1:
            try:
                data = self.client_socket.recv(MAX_BUFFER)
                self.server_socket.sendall(data)
            except:
                pass

            try:
                data = self.server_socket.recv(MAX_BUFFER)
                self.client_socket.sendall(data)
            except:
                pass
    

def main(token):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Creating the main socket of the proxy.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('192.168.1.107', 50001))
    sock.listen(1)
    while True:
        conn, addr = sock.accept()
        newthread = ClientThread(addr, conn, token)
        newthread.daemon = True
        newthread.start()
        
main('1')