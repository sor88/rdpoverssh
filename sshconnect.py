from sshtunnel import open_tunnel
from time import sleep
import threading
import time

ip = None

def sshtunconnect(ip_local):
     with open_tunnel(
         ('90.150.80.113', 2222),
         ssh_username="itu",
         ssh_pkey="srv.key",
         remote_bind_address=(ip_local, 3389),
         local_bind_address=('localhost', 2222)
     ) as server:
         print(server.local_bind_port)
         while True:
             # press Ctrl-C for stopping
             sleep(1)

def sshtungetip():
      import kerio.kerio as ker
      import kerio.keriofunction as funker
      from sshtunnel import SSHTunnelForwarder
      print(ker.ipserver)
      server = SSHTunnelForwarder(
          ('90.150.80.113', 2222),
          ssh_username="itu",
          ssh_pkey="srv.key",
          remote_bind_address=(ker.ipserver, 4081),
          local_bind_address=('127.0.0.1', 4081)
      )
      server.start()
      print(server.local_bind_port)  # show assigned local port
      # work with `SECRET SERVICE` through `server.local_bind_port`.
      time.sleep(4)
      l = 'Потапов'
      print("Получение ip адреса")
      session = ker.callMethod("Session.login", {"userName": ker.username, "password": ker.password, "application": {"vendor": "Kerio", "name": "Control Api Demo", "version": "8.4.0"}})
      token = session["result"]["token"]
      for funame, fip in findinfo_connection(token, sys.argv[1]):
          print(funame, fip)
      funker.keriologout()


      userinfo = funker.main(l)
      print(userinfo)
      server.close()
      return (ip_local)


def connecttopc(ip_local):
    tun2 = threading.Thread(target=sshtunconnect, daemon=True, args=(ip_local, ))
    tun2.start()
    print("Подключение к ip 2")
    tun2.join()
    print("конец")

def connecting():
    tun = (
        threading.Thread (target=sshtungetip, daemon=True),
        threading.Thread (target=connecttopc, daemon=True)
    )
    for thread in tun:
        thread.start()
