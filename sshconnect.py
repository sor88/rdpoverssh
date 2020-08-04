from sshtunnel import open_tunnel
from time import sleep
import threading
import time
import ssl
import sys

publicipadress = ('194.247.184.169', 3232)
setstatus = None
login = None
password = None
lock = threading.Lock()

def sshtunconnect(address):
     with open_tunnel(
         publicipadress,
         ssh_username="dgh",
         ssh_pkey="srv.key",
         remote_bind_address=address,
         local_bind_address=('localhost', 2222)
     ) as server:
         print(server.local_bind_port)
         while True:
             # press Ctrl-C for stopping
             sleep(5)

def sshtungetip():
      import kerio.kerio as kerio
      import kerio.keriofunction as kf
      from sshtunnel import SSHTunnelForwarder
      funame = None
      server = SSHTunnelForwarder(
          publicipadress,
          ssh_username="dgh",
          ssh_pkey="srv.key",
          remote_bind_address=('192.168.41.1', 4081),
          local_bind_address=('127.0.0.1', 4081)
      )
      server.start()
      print(server.local_bind_port)
      time.sleep(3)
      print(login)
      global setstatus
      setstatus = "Получение ip адреса"
      print(setstatus)
      session = kerio.callMethod("Session.login", {"userName": kerio.username, "password": kerio.password,"application": {"vendor": "Kerio", "name": "Control Api Demo", "version": "8.4.0"}})
      token = session["result"]["token"]
      for funame, fip in kf.findinfo_connection(token, login):
          sleep(1)
      kf.keriologout()
      server.close()
      print("перед if")
      if funame is None:
            print("Имя пользователя не найдено среди активных подключений")
            fip = "IP не найден"
      return(fip)


def connecttopc():
    fip = sshtungetip()
    global setstatus
    if fip == "IP не найден":
        print(fip)
        setstatus = "IP не найден"
        return
    if fip:
        print('Ip получен')
        setstatus = "ip is found"
        address = (fip, 3389)
        sshtunconnect (address)
    if fname == "Не найдено":
            n += 5
            sleep(n)
            return


def connecting():

    # if login is None:
    #     print('Поле логин не может быть пустым')
    tun1 = threading.Thread(target=connecttopc, daemon=True)
    tun1.start()

