from sshtunnel import open_tunnel
from time import sleep
import threading
import time
import ssl
import sys

publicipadress = ('REMOTE_PUBLIC_IP', 3232)  # Публичный IP адрес и порт ssh сервера
setstatus = None
login = None
password = None
lock = threading.Lock()

def sshtunconnect(address):
    """
     Функция установки ssh соединения с найденным ip.
    """
     server = open_tunnel(
         publicipadress,
         ssh_username="LOGIN_SSH",
         ssh_password="PASSWORD_SSH",
#         ssh_pkey="srv.key", # можно использовать вместо пароля файл ключа
         remote_bind_address=address,
         local_bind_address=('localhost', 2222) #  адрес и порт откуда происходит проброс
     )
     server.start()
     print(server.local_bind_port)

             
def sshtungetip():
    """
    Функция получения ip адреса из Kerio Control
    """
      import kerio.kerio as kerio
      import kerio.keriofunction as kf
      from sshtunnel import SSHTunnelForwarder
      funame = None
      server = SSHTunnelForwarder(
          publicipadress,
          ssh_username="LOGIN_SSH",
          ssh_password="PASSWORD_SSH!",
          remote_bind_address=('IP_Kerio_FIREWALL', 4081), # ip адрес и порт kerio control
          local_bind_address=('127.0.0.1', 4081)
      )
      server.start()
      print(server.local_bind_port)
      time.sleep(3)
      global setstatus
      setstatus = "Получение ip адреса"
      print(setstatus)
      session = kerio.callMethod("Session.login", {"userName": kerio.username, "password": kerio.password,"application": {"vendor": "Kerio", "name": "Control Api Demo", "version": "8.4.0"}})
      token = session["result"]["token"]
      for funame, fip in kf.findinfo_connection(token, login):
          sleep(1)
      kf.keriologout()
      server.close()
      if funame is None:
            print("Имя пользователя не найдено среди активных подключений")
            fip = "IP не найден"
      return(fip)


def connecttopc():
    """
    Основная управляющая функция. получает ip и запускает функцию соединения.
    """
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
        sshtunconnect(address)
        rdpstart = threading.Thread(target=rdpdataconnection, daemon=True)
        rdpstart.start()




def rdpdataconnection():
    """
    Вызов  RDP с параметрами.
    """
    import subprocess
    global login, password
    subprocess.call(f"cmdkey /add:localhost /user:DOMAINMAIN\{login} /pass:{password}") # Если пользователи не доменные DOMAIN\ убрать
    time.sleep(3)
    subprocess.call("mstsc /v:localhost:2222")
    time.sleep(7)
    delkeyuser()
    
    
def delkeyuser():
    import subprocess
    subprocess.call("cmdkey /delete localhost")
    

