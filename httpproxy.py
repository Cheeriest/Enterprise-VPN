# If we receive a CONNECT request

import socket, threading, jwt, json, ssl
from base64 import b64decode

MAX_BUFFER = 64 * 512
class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.browser = clientsocket
        

    def run(self): 
        while True:
            #request = json.loads(self.browser.recv(MAX_BUFFER))
            #token = request[1]
            #request = b64decode(request[0])
            #print request
            data = json.loads(self.browser.recv(MAX_BUFFER))
            request = b64decode(data[0])
            token = data[1]
            # parse the first line
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            webserver, port = self.get_domain_port(request)

            if 'CONNECT' or 'GET' in request:
            # Connect to port 443
                if 'CONNECT' in request:
                    try:
                        # If successful, send 200 code response
                        client.connect(( webserver, port ))
                        reply = "HTTP/1.0 200 Connection established\r\n"
                        reply += "Proxy-agent: FIMA\r\n"
                        reply += "\r\n"
                        self.browser.sendall( reply.encode() )
                    except socket.error as err:
                        raise err
                        # If the connection could not be established, exit
                        # Should properly handle the exit with http error code here
                        break
                else:
                    client.connect(( webserver, port ))
                    client.send(request.encode())
                    self.browser.send(client.recv(MAX_BUFFER))

                # Indiscriminately forward bytes
                self.browser.setblocking(0)
                client.setblocking(0)
                while True:
                    try:
                        data = json.loads(self.browser.recv(MAX_BUFFER))
                        request = b64decode(data[0])
                        token = data[1]
                        #    token = request[1]
                        #    request = b64decode(request[0])
                        client.sendall(request)
                        
                    except socket.error as err:
                        pass
                    try:
                        reply = client.recv(MAX_BUFFER)
                        #print reply
                        self.browser.sendall( reply )
                    except socket.error as err:
                        pass

                
            
        print ("Client at ", self.browser , " disconnected...")

    def get_domain_port(self, request):
        first_line = request.split('\n')[0]
        # get url
        url = first_line.split(' ')[1]
        http_pos = url.find("://") # find pos of ://
        if (http_pos == -1):
            temp = url
        else:
            temp = url[(http_pos+3):] # get the rest of url
        port_pos = temp.find(":") # find the port pos (if any)
        # find end of web server
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if (port_pos == -1 or webserver_pos < port_pos): 
            # default port 
            port = 80 
            webserver = temp[:webserver_pos] 

        else: # specific port 
            port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos] 

        
        return webserver, port

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #Creating the main socket of the proxy.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('192.168.1.107', 50002))
    sock.listen(5)

    while True:
        conn, addr = sock.accept()
        conn = ssl.wrap_socket(conn,
                                server_side=True,
                                certfile="cert.pem",
                                keyfile="cert.pem")
        newthread = ClientThread(addr, conn)
        newthread.daemon = True
        print('new client', addr)
        newthread.start()

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    

    

if __name__ == "__main__":
    main()