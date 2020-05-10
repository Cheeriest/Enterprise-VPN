# If we receive a CONNECT request

import socket, threading, jwt, json, ssl
from base64 import b64decode, b64encode
import struct, datetime, requests

cached_tokens = []
MAX_BUFFER = 512 * 75
class ClientThread(threading.Thread):
    api_url = 'http://localhost:5000'
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.browser = clientsocket
        
    def run(self): 
        while True:
            #request = json.loads(self.browser.recv(MAX_BUFFER))
            #token = request[1]
            #request = b64decode(request[0])
            #print request
            data = self.get_msg(self.browser)
            data = json.loads(data)
            request = b64decode(data['data'])
            token = data['token']
            if not self.check_token(token):
                self.shutdown_connection()
                return
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
                        self.send_msg(self.browser, b64encode(reply))
                    except socket.error as err:
                        raise err
                        # If the connection could not be established, exitex
                        # Should properly handle the exit with http error code here
                        break
                else:
                    client.connect((webserver, port))
                    client.sendall(request.encode())
                    reply = client.recv(MAX_BUFFER)
                    if reply:
                        self.send_msg(self.browser, b64encode(reply))                    

                # Indiscriminately forward bytes
                self.browser.setblocking(0)
                client.setblocking(0)
                while True:
                    try:
                        data = self.get_msg(self.browser)
                        if data:
                            data = json.loads(data)
                            request = b64decode(data['data'])
                            token = data['token']
                            if self.check_token(token):
                                client.sendall(request)
                            else:
                                self.shutdown_connection()
                                return
                        
                    except socket.error as err:
                        pass
                    
                    try:
                        reply = client.recv(MAX_BUFFER)
                        #print reply
                        if reply:
                            self.send_msg(self.browser, b64encode(reply))
                            print len(b64encode(reply))
                            
                    except socket.error as err:
                        pass
     
        print ("Client at ", self.browser , " disconnected...")

    def check_token(self, token):
        tokens = cached_tokens
        if token in tokens:
            #check if the given token is in cache.
            headers = jwt.decode(token, verify = False)
            exp_time = headers.get('exp')
            #check for expiry date
            if exp_time:
                exp_time_obj = datetime.datetime.fromtimestamp(exp_time)
                now_time = datetime.datetime.now()
                if exp_time_obj < now_time:
                    #if the token has expired, then just get 
                    #rid of it.
                    cached_tokens.remove(token)
                    return False
                else:
                    return True
        else:
            #Check the api server if token is valid, if it is
            #just add it to cached tokens for further use.
            
            req = requests.post(ClientThread.api_url + '/check_token',
                                json = {'token' : token},
                                headers = {'Content-type': 'application/json'},
                                proxies = {'http' : ''})
            try:
                json_response = json.loads(req.text)
            except:
                print req.text
                import sys
                sys.exit(0)
            if str(json_response.get('Valid')) == "True":
                cached_tokens.append(token)
                return True
            else:
                return False
                

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
    

    def get_msg(self, s):
        count = struct.unpack('>I', self._get_block(s, 4))[0]
        return self._get_block(s, count)

    def send_msg(self, s, data):
        header = struct.pack('>I', len(data))
        self._send_block(s, header)
        self._send_block(s, data)
        
    def _get_block(self, s, count):
        if count <= 0:
            return ''
        buf = ''
        while len(buf) < count:
            recieve_amount = 0
            if count - len(buf) < MAX_BUFFER:
                recieve_amount = count - len(buf)
            else:
                recieve_amount = MAX_BUFFER
            buf2 = s.recv(recieve_amount)
            if not buf2:
                # error or just end of connection?
                if buf:
                    raise RuntimeError("underflow")
                else:
                    return ''
            buf += buf2
        return buf

    def _send_block(self, s, data):
        if data:
            s.sendall(data)
    
    def shutdown_connection(self):
        self.browser.shutdown(socket.SHUT_RDWR)
        self.browser.close()
        return
    

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
        #print('new client', addr)
        newthread.start()

    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    

    

if __name__ == "__main__":
    main()