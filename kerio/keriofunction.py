import json
import urllib.request
import http.cookiejar
import ssl
import sys
import time
import requests
# from mywebhook import send_message
import kerio as ker
# from kerio.kerio import callMethod
# from kerio.kerio import password
# from kerio.kerio import username


# from mywebhook import send_message
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
urllib.request.install_opener(opener)
ssl._create_default_https_context = ssl._create_unverified_context

def write_json(data, filename='otvetjs.json'):
    with open(filename, 'w') as f:
    	json.dump(data, f, indent=2, ensure_ascii=False)

def findinfo_connection(token, perem):
    usr = ker.callMethod("ActiveHosts.get", {"query":{}, "refresh": True}, token)
    resl = usr.get('result', usr.get('error')) 
    if 'error' in resl:
        funame = "Сервер недоступен, попробуйте позднее"
        return funame
    lsusr = resl.get('list')
    if lsusr is None:
        funame = "Сервер недоступен, попробуйте позднее"
        return funame
    else:
        lsusr = usr['result']['list']
    for finfo in lsusr:
        funame = finfo['user']['name']
        fip = finfo['ip']
        fmac = finfo['macAddress']
        fhostname = finfo['hostname']
        if perem in funame or perem in fip:
            yield funame, fip

def keriologout():
    session = ker.callMethod("Session.login", {"userName":ker.username, "password":ker.password, "application":{"vendor":"Kerio", "name":"Control Api Demo", "version":"8.4.0"}})
    token = session["result"]["token"]
    ker.callMethod("Session.logout",{}, token)

def keriofindquery():
    pass


def main():
    session = ker.callMethod("Session.login", {"userName":ker.username, "password":ker.password, "application":{"vendor":"Kerio", "name":"Control Api Demo", "version":"8.4.0"}})
    token = session["result"]["token"]

    # user_find(token, sys.argv[1])
    #findinfo_connection(token, sys.argv[1])
    for funame, fip, fmac, fhostname in findinfo_connection(token, sys.argv[1]):
        print(funame, fip, fmac, fhostname )
    keriologout()

if __name__ == '__main__':
    main()