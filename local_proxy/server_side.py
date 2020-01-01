import socket, base64
from scapy.all import *
import threading

PROXY_IP = '192.168.1.107'
PROXY_PORT = 80
IP_ADDR = '192.168.1.107'
PORT = 50001
client_count = 0


def main():
    global client_count
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP_ADDR, PORT))
    sock.listen(1000)
    print('listening')

    while 1:
        conn, addr = sock.accept()
        client_count += 1
        print('connected')
        reverse_address = (IP_ADDR, PORT + client_count)
        listenerHandle = FromProxyListener(reverse_address)
        client = ClientServe(conn, addr, reverse_address)
        client.start()
        listenerHandle.start()

class FromProxyListener(threading.Thread):
    def __init__(self, reverse_address):
        threading.Thread.__init__(self)
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(reverse_address)
        
    def run(self):
        self.listener.listen(1)
        conn, addr = self.listener.accept()
        while 1:
            data = conn.recv(100000)
            print data

class ClientServe(threading.Thread):
    def __init__(self, sock, addr, reverse_address):
        threading.Thread.__init__(self)
        self.sock = sock
        self.addr = addr
        self.reverse_address = reverse_address
        self.proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def run(self):
        while True:
            data = self.sock.recv(10000)
            decoded = base64.b64decode(data)
            pkt = Ether(decoded)
            print pkt.summary()
            if pkt.haslayer(TCP):
                pkt[IP].src = self.reverse_address[0] # IP
                pkt[IP].dst = PROXY_IP
                pkt[TCP].dport = PROXY_PORT
                pkt[TCP].sport = self.reverse_address[1] # PORT
                send(pkt)
        
        
main()