# If we receive a CONNECT request

import socket, threading, ssl

MAX_BUFFER = 64 * 512
class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.browser = clientsocket
        

    def run(self): 
        
        while True:
            request = self.browser.recv(MAX_BUFFER)
            # parse the first line
            
            
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            webserver, port = self.get_domain_port(request)
            if 'CONNECT' in request:
            # Connect to port 443
                print request
                try:
                    # If successful, send 200 code response
                    client.connect(( webserver, port ))
                    reply = "HTTP/1.0 200 Connection established\r\n"
                    reply += "Proxy-agent: FIMA\r\n"
                    reply += "\r\n"
                    self.browser.sendall( reply.encode() )
                except socket.error as err:
                    # If the connection could not be established, exit
                    # Should properly handle the exit with http error code here
                    break

                
                """
                self.ssl_browser = ssl.wrap_socket(self.browser, \
                                server_side=True, \
                                certfile='certificate.pem' ,\
                                keyfile='key.pem',\
                                do_handshake_on_connect = False)    
                
                self.ssl_browser.do_handshake()
                """
                self.ssl_browser = self.browser
                # Indiscriminately forward bytes
                self.ssl_browser.setblocking(0)
                client.setblocking(0)
                while True:
                    try:
                        request = self.ssl_browser.recv(MAX_BUFFER)
                        client.sendall( request )
                        
                    except socket.error as err:
                        pass
                    try:
                        reply = client.recv(MAX_BUFFER)
                        self.ssl_browser.sendall( reply )
                    except socket.error as err:
                        pass

                
            
        print ("Client at ", self.ssl_browser , " disconnected...")

    def get_domain_port(self, request):
        first_line = request.split('\n')[0]

        # get url
        url = first_line.split(' ')[1]

        http_pos = url.find("://") # find pos of ://
        if (http_pos==-1):
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
        if (port_pos==-1 or webserver_pos < port_pos): 

            # default port 
            port = 80 
            webserver = temp[:webserver_pos] 

        else: # specific port 
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos] 

        return webserver, port

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock = ssl.wrap_socket(sock, server_side=True, certfile='certificate.pem', keyfile='key.pem', do_handshake_on_connect=False)
    #sock.do_handshake()
    sock.bind(('192.168.1.107', 80))
    sock.listen(5)

    while True:
        conn, addr = sock.accept()
        #conn = ssl.wrap_socket(conn, server_side=True, certfile='certificate.pem', keyfile='key.pem')
        
        newthread = ClientThread(addr, conn)
        newthread.start()

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    

    

if __name__ == "__main__":
    main()