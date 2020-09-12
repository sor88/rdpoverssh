# -*- coding: utf-8 -*-
import json
import urllib.request
import http.cookiejar
import ssl
import sys
#sys.path.insert(0, '/home/plus/hdd/tmp/deleop/rdpoverssh')

""" Cookie storage is necessary for session handling """
jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
urllib.request.install_opener(opener)
""" Hostname or ip address of your Kerio Control instance with protocol, port and credentials """
ipserver = "127.0.0.1"
server = "https://"+ipserver+":4081"
username = "kerio_admin_read_access_login"
password = "kerio_admin_read_admin_pass"
ssl._create_default_https_context = ssl._create_unverified_context  # Убирает ошибку сертификата SSL

def callMethod(method, params, token = None):
    """
    Remotely calls given method with given params.
    :param: method string with fully qualified method name
    :param: params dict with parameters of remotely called method
    :param: token CSRF token is always required except login method. Use method "Session.login" to obtain this token.
    """
    data =  {"method": method ,"id":1, "jsonrpc":"2.0", "params": params}

    req = urllib.request.Request(url = server + '/admin/api/jsonrpc/')
    req.add_header('Content-Type', 'application/json')
    if (token is not None):
        req.add_header('X-Token', token)

    httpResponse = urllib.request.urlopen(req, json.dumps(data).encode())

    if (httpResponse.status == 200):
        body = httpResponse.read().decode()
        return json.loads(body)

