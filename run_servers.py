import os, threading
from server_side import httpproxy
vpn_thread = threading.Thread(target = httpproxy.main)
vpn_thread.start()
os.system('python ./server_side/api.py')