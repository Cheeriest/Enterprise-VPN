'''
import socket, ssl

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 5000))
sock.listen(5)
sock = ssl.wrap_socket(sock, keyfile='key.pem', certfile='certificate.pem')
conn, addr = sock.accept()

while 1:
    try:
        data = sock.recv(1024)
        if not data:
            break
        print data
        sock.send(data)

    except socket.error as err:
        print err
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

sock.shutdown(socket.SHUT_RDWR)
sock.close()
'''
#!/bin/usr/env python
import socket
import ssl
import pprint

#server
if __name__ == '__main__':

    HOST = '192.168.1.107'
    PORT = 1234

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)

    client, fromaddr = server_socket.accept()
    secure_sock = ssl.wrap_socket(client, server_side=True, ca_certs = "client.pem",\
                                certfile="server.pem", keyfile="key1.pem",\
                                cert_reqs=ssl.CERT_REQUIRED,\
                                ssl_version=ssl.PROTOCOL_TLSv1_2)

    '''
    print repr(secure_sock.getpeername())
    print secure_sock.cipher()
    print pprint.pformat(secure_sock.getpeercert())
    cert = secure_sock.getpeercert()
    print cert
    '''

    while 1:
        data = secure_sock.read(1024)
        secure_sock.write(data)
        print data

    