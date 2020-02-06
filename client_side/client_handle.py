import requests, sys, time
import localproxy
import autoproxy
    
def connect_proxy(jwt_token, auth_url):
    get_proxy_url = auth_url + '/vpn'
    req = requests.get(get_proxy_url, headers = {'x-access-token':jwt_token}).json()
    print req
    VPN_IP = req['ip']
    VPN_PORT = req['port']
    autoproxy.on('localhost:8080')
    print 'Enabled local proxy traffic through localhost:8080'
    localproxy.main(jwt_token, VPN_IP, VPN_PORT)
    

def handle(jwt_token, auth_url):
    if __name__ != 'client_handle':
        sys.exit('Launched from an unverified location')
    services = ['Tunnel Connection - 1 ' , 'FTP Server - 2', 'DMZ - 3', 'Exit - 4']
    print 'Dear User, which service would you like to use?'
    print "\r\n".join(services)
    while True:
        choice = raw_input('>>>> ')
        if choice == '1':
            connect_proxy(jwt_token, auth_url)
            break
        else:
            print 'Invalid Option'
            continue
        
    

    
    
    