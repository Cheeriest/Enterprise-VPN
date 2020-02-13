import socket, json, sys, select, ssl
from threading import Thread
from base64 import b64encode



MAX_BUFFER = 64 * 512
VPN_IP = '192.168.1.107'
VPN_PORT = 50002

class ClientThread(Thread):
    def __init__(self, addr, conn, token, vpn_ip, vpn_port):
        Thread.__init__(self)
        self.client_socket = conn
        self.token = token
        self.vpn_ip = vpn_ip
        self.vpn_port = vpn_port
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket = ssl.wrap_socket(s, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)
        try:
            self.server_socket.connect((self.vpn_ip, self.vpn_port))
        except:
            sys.exit('Error on connecting to the vpn server')
        
            
        data = self.client_socket.recv(MAX_BUFFER)
        encoded_data = json.dumps([b64encode(data), self.token])
        self.server_socket.send(encoded_data)
        data = self.server_socket.recv(MAX_BUFFER)
        self.client_socket.sendall(data)
        self.post_sync()
    
    
    
    def post_sync(self):    
        self.client_socket.setblocking(0)
        self.server_socket.setblocking(0)
        
        while 1:
            try:
                data = self.client_socket.recv(MAX_BUFFER)
                encoded_data = json.dumps([b64encode(data), self.token])
                self.server_socket.send(encoded_data)
            except:
                pass

            try:
                data = self.server_socket.recv(MAX_BUFFER)
                self.client_socket.sendall(data)
            except:
                pass
    

def main(token, vpn_ip, vpn_port, self_ip, self_port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Creating the main socket of the proxy.
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self_ip, self_port))
        print 'listening on local callback proxy on %s %d' %(self_ip, self_port)
        sock.listen(1)
        while True:
            conn, addr = sock.accept()
            newthread = ClientThread(addr, conn, token, vpn_ip, vpn_port)
            newthread.daemon = True
            newthread.start()
    except IOError: 
        sys.exit(0)
        
#main('1')