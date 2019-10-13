'''
import socket, ssl
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5000))
sock = ssl.wrap_socket(sock, keyfile='key.pem')

while 1:
    data = raw_input('Enter Data: ')
    sock.send(data)
    data = sock.recv(1024)
    if not data:
        break
    print data
'''
import socket
import ssl

# client
if __name__ == '__main__':

    HOST = '192.168.1.107'
    PORT = 1234

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(1)
    sock.connect((HOST, PORT))

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile='server.pem')
    context.load_cert_chain(certfile="client.pem", keyfile="key2.pem")

    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_side=False, server_hostname=HOST)
    else:
        secure_sock = context.wrap_socket(sock, server_side=False)

    cert = secure_sock.getpeercert()
    print cert

    while 1:
        secure_sock.write('hello')
        secure_sock.read(1024)

    secure_sock.close()
    sock.close()