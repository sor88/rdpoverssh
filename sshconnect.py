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
    Функция получения ip адреса из файла или базы данных подготовленных на сервере API керио или вручную.
    """
    from paramiko import SSHClient
    from paramiko import AutoAddPolicy
    getipsftp = SSHClient()
    getipsftp.load_system_host_keys()
    getipsftp.set_missing_host_key_policy(AutoAddPolicy())
    getipsftp.connect('IP_SSH/SFTP_SERVER', 'PORT', 'Login', 'password')
    sftp = getipsftp.open_sftp()
    import os
    file = sftp.file('ip-client.txt', 'r')
    file = file.read().decode("utf-8")
    getipsftp.close()
    fip = None
    for x in file.split("\n"):
        if login in x:
            a = x
            fip = a.split()[0]
    if fip == "Не" or fip is None:
        fip = "IP не найден"
    time.sleep(3)
    global setstatus
    setstatus = "Получение ip адреса"
    #print(setstatus)
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
    

