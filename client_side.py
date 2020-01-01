#from scapy.all import *
import socket, json, sys, select
from threading import Thread
from base64 import b64encode

"""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.1.107', 50001))

def intercept(pkt):
    global sock
    raw_pkt = str(pkt)
    encoded_data = base64.b64encode(raw_pkt)
    sock.send(encoded_data)
    print 'sent'
    

def main():
    sniff(filter = 'src host 192.168.1.107', prn = intercept)

if __name__ == '__main__':
    main() 
"""


MAX_BUFFER = 64 * 512
VPN_IP = '192.168.1.107'
VPN_PORT = 50002
class Packet(object):
    def __init__(self, data, token):
        self.pack = (b64encode(data), token)
    
    def __str__(self):
        return json.dumps(self.pack)
    
    
class Client():
    def __init__(self, addr, conn, token):
        self.token = token
        self.client_sock = conn
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #This should be an encrypted connection!!!!!
        try:
            self.server_sock.connect((VPN_IP, VPN_PORT))
        except socket.error:
            sys.exit('VPN server is not up now')
        
    
def run(sock):
    request = sock.client_sock.recv(MAX_BUFFER)
    packet = Packet(request, sock.token)
    sock.server_sock.sendall(str(packet))
    reply = sock.server_sock.recv(MAX_BUFFER,)
    sock.client_sock.send(reply)
    print reply
    sock.server_sock.setblocking(0)
    while 1:
        
        print '1'
        request = sock.client_sock.recv(MAX_BUFFER)
        packet = Packet(request, sock.token)
        sock.server_sock.sendall(str(packet))
        reply = sock.server_sock.recv(MAX_BUFFER)
        sock.client_sock.send(reply)
        print reply
        
            

def main(token):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Creating the main socket of the proxy.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('192.168.1.107', 50001))
    sock.listen(5)
    delay = 0.1
    inputs = [sock]
    proccesses = {}
    while True:
        
        """
        conn, addr = sock.accept()
        newthread = ClientThread(addr, conn, token)
        newthread.daemon = True
        newthread.start()
        """
        readables, _, _ = select.select(inputs, [], [], delay) 
        #Using 'select' for incoming inputs from other sockets.
        for s in readables:
            if s is sock:
                #Accepting new connections
                conn, addr = sock.accept()
                inputs.append(conn)
                proccesses[addr] = Client(addr, conn, token)
                print 'new connection with ', (conn, addr)
            else:
                if proccesses.get(addr):
                    run(proccesses[addr])
                    
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    
main(1)