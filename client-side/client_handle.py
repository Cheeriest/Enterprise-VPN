import requests, sys
import local_proxy
import registry_utils

def handle(jwt_token, auth_url):
    if __name__ != 'client_handle':
        sys.exit('Launched from an unverified location')
    
    services = ['Tunnel Connection - 1 ' , 'FTP Server - 2', 'DMZ - 3', 'Exit - 4']
    print 'Dear User, which service would you like to use?'
    print "\r\n".join(services)
    choice = raw_input('>>>> ')
    while choice not in ['1', '2', '3', '4']:
        print('Invalid')
        choice = raw_input('>>>> ')
        if choice == '1':
            connect_proxy(jwt_token, auth_url)
    
    
def connect_proxy(jwt_token, auth_url):
    get_proxy_url = auth_url + '/vpn'
    req = requests.get(get_proxy_url, headers = {'x-access-token':jwt_token}).json()
    PROXY_IP = req['ip']
    PROXY_PORT = req['port']
    registry_utils.connect(PROXY_IP, PROXY_PORT)
    
    
    