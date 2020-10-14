# -*- coding: utf-8 -*-
import urllib.request
import http.cookiejar
import ssl
import sys
import time
import requests
# from mywebhook import send_message
import kerio.kerio as ker # обратите внимание на то откуда запускается основной файл
# from kerio.kerio import callMethod
# from kerio.kerio import password
# from kerio.kerio import username


# from mywebhook import send_message
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
urllib.request.install_opener(opener)
ssl._create_default_https_context = ssl._create_unverified_context


def user_find(token):
    usr = ker.callMethod("Users.get", {"query":{}, "domainId":"local"}, token)
    lsusr = usr["result"]["list"]
    if len(lsusr) == 0:
        b = None
        c = None
        a =  "Не найдено"
        yield(a,b,c)
    for usser in lsusr:
        grepusr = usser['credentials']['userName']
        fullname = usser['fullName']
        ipaddr = usser['autoLogin']['addresses']['value']
        if len(ipaddr) == 0:
           ipaddr = ["Не найдено"]
        if len(ipaddr) > 0:
            listipaddr = []
            for x in ipaddr:
                listipaddr.append(x)
        yield(grepusr, fullname, (listipaddr or ipaddr))


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
    ########################## Парсер и запись в json
    import json
    listjson = []
    with open('ip-client.json', 'w', encoding="utf-8") as f:
        for a,b,c in user_find(token):
             to_json = {"User" : {'login':a, "FullName":b, "ipaddress": {"ip":c }}}
             if a == "Не найдено":
                 print("Не найдено")
                 break
             listjson.append(to_json)
        json.dump(listjson, f, ensure_ascii=False, sort_keys=False, indent=4)
    ##########################
    ker.callMethod("Session.logout",{}, token)


if __name__ == '__main__':
    main()