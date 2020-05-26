import os, threading
from server_side import httpproxy
from server_side import ftpserver
vpn_thread = threading.Thread(target = httpproxy.main)
#ftp_thread = threading.Thread(target = ftpserver.run_ftp_server)
vpn_thread.start()
#ftp_thread.start()
os.system('python ./server_side/api.py')