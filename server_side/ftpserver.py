from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
def run_ftp_server():
    authorizer = DummyAuthorizer()
    authorizer.add_user("root", "pass", "./") #The third paramater is root directory of ftp server
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer(("192.168.1.107", 21), handler)
    server.serve_forever()
