"""
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
"""
from twisted.protocols.ftp  import FTPFactory, FTPRealm
from twisted.cred.portal    import Portal
from twisted.cred.checkers  import AllowAnonymousAccess, FilePasswordDB
from twisted.internet       import reactor
from twisted.protocols      import ftp
black_list = ['sex']
#pass.dat looks like this:
# jeff:bozo
# grimmtooth:bozo2
class DmzFTP(ftp.FTP):
    def ftp_RETR(self, path):
        if not self.check_balcklist(path):
            return super(DmzFTP, self).ftp_RETR('nope.txt')
        d = super(DmzFTP, self).ftp_RETR(path)
        
        return d

    def check_balcklist(self, path):
        with open(path, 'rb') as w:
            for i in black_list:
                for line in w:
                    if i in line.rstrip():
                        print 'yoyoyoy'
                        return False
        return True
        # XXX your code here
def run_ftp_server():  
    p = Portal(FTPRealm('./'), (AllowAnonymousAccess(), FilePasswordDB("pass.dat")))
    f = FTPFactory(p)
    f.protocol = DmzFTP
    reactor.listenTCP(21, f)
    reactor.run()

    
if __name__ == "__main__":
    run_ftp_server()
        