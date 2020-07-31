from sshtunnel import open_tunnel
from time import sleep
import threading
import time
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

def sshtunconnect2(ip_local):
      from sshtunnel import SSHTunnelForwarder
      server = SSHTunnelForwarder(
          ('90.150.80.113', 2222),
          ssh_username="itu",
          ssh_pkey="srv.key",
          remote_bind_address=(ip_local, 3389),
          local_bind_address=('127.0.0.1', 2222)
      )
      print(ip_local)
      server.start()
      print(server.local_bind_port)  # show assigned local port
      # work with `SECRET SERVICE` through `server.local_bind_port`.
      time.sleep(4)
      server.close()

def getip():
    ip_local = '172.16.1.55'
    tun1=threading.Thread(target=sshtunconnect2, daemon=True, args=(ip_local, ))
    tun1.start()
    print("Получение ip адреса")
    return(ip_local)


def connecttopc(ip_local):
    tun2 = threading.Thread(target=sshtunconnect, daemon=True, args=(ip_local, ))
    tun2.start()
    print("Подключение к ip 2")
    tun2.join()
    print("конец")