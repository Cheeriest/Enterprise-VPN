import winreg, os, requests, argparse, json, sys
import client_handle

def login(username, password):
    TOKEN = ""
    AUTH_IP = 'localhost'
    AUTH_PORT = 5000
    PROXY_IP = ''
    PROXY_PORT = None

    url = 'http://' + AUTH_IP + ':' + str(AUTH_PORT)
    login_url = url + '/login'
    data_json = { 'name':username, 'password':password }
    headers = { 'Content-type': 'application/json' }
    
    while 1:
        req = requests.post(login_url, json=data_json, headers=headers)
        try:
            if json.loads(req.text)['token']:
                TOKEN = json.loads(req.text)['token']
                print 'Congragulations %s, you are now connected to our service' %username
                print 'Enjoy your use.'
                break
            else:
                continue
        except ValueError:
            if 'Could not verify' in req.text:
                sys.exit('Your credentials are wrong \r\nPlease try again')
    try:
        client_handle.handle(TOKEN, url)
    except KeyboardInterrupt:
        autoproxy.off()
        try:
            sys.exit(0)
        except:
            os._exit(0)


if __name__ == '__main__':
    #Parsing the client credentials and passing them to the login function.
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest = 'username',  required = True, help='Insert Client Username')
    parser.add_argument('-p', dest = 'password',  required = True, help='Insert Client Pass')
    args = parser.parse_args()
    login(args.username, args.password)

