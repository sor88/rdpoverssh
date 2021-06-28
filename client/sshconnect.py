from sshtunnel import open_tunnel
from time import sleep
import threading
import time
import json
setstatus = "ready"
login = None
password = None
readsettings = None
def read_settings():
    """
    Функция чтения настроек из файла settings.json. При его наличие берутся параметры IP и Port ssh сервера по-умолчанию
    Если настройки указаны в форме программы, параметры settings.json игнорируются.
    """
    with open("settings.json", "r") as f:
        import json
        tmp = json.load(f)
    for x in tmp:
        ip_server = x["settings"]["ssh_server_ip"]
        ip_port = x["settings"]["ssh_port"]
        ssh_login = x["settings"]["ssh_login"]
    print(ip_server, ip_port, ssh_login)
    global readsettings
    if ip_port is not int:
        ip_port = "Заполнено неверно"
    else:
        ip_port == int(ip_port)
    readsettings = (ip_server, ip_port, ssh_login)
    return(readsettings)

readsettings = read_settings()
print(readsettings)
publicipadress = (readsettings[0], readsettings[1])

def sshtunconnect(address):
    """
     Устанавливает соединение с пробросом порта по заданному IP адресу ( который был найден из JSON объекта) ранее и
     передан в функцию в качестве параметра.
    """
    server = open_tunnel(
        publicipadress,
        ssh_username=readsettings[2],
        #       ssh_password="password",
        ssh_pkey="srv.key",  # можно использовать вместо пароля файл ключа
        remote_bind_address=address,
        local_bind_address=('localhost', 2222)  # адрес и порт куда происходит проброс
    )
    server.start()
    print(server.local_bind_port)


def sshtungetip():
    """
   Подключается по sftp к серверу получает данные JSON. Осуществляет поиск IP и возращает его в качестве параметра в
   место вызова.
    """
    global setstatus
    global login
    setstatus = "Получение ip адреса"
    from paramiko import SSHClient
    from paramiko import AutoAddPolicy
    from paramiko import RSAKey
    getipsftp = SSHClient()
    pk = RSAKey.from_private_key_file('srv.key')
    getipsftp.load_system_host_keys()
    getipsftp.set_missing_host_key_policy(AutoAddPolicy())
    getipsftp.connect(hostname=publicipadress[0], port=str(publicipadress[1]), username='sftp', pkey=pk)
    sftp = getipsftp.open_sftp()
    fip = None
    with sftp.file('ip-client.json', 'r') as f:
        dataip = json.load(f)
    getipsftp.close()
    for x in dataip:
        if login == x["User"]["login"] or login in x["User"]["FullName"]:
            fip = x["User"]["ipaddress"]["ip"][0]
            fullname = x["User"]["login"]
    if fip == "Не найдено" or fip is None:
        fip = "IP не найден"
    time.sleep(1)
    return(fip)


def connecttopc():
    """
    Основная управляющая функция. получает ip  из функции sshtungetip. Проверяет IP по заданной маске. Если IP не найден
    передает в статус бар сообщение о том что IP не найден. Если IP найден вызывает функцию ssh соединения функцию
    соединения.
    """
    fip = sshtungetip()
    print(fip)
    global setstatus
    if fip == "IP не найден":
        setstatus = "ipnotfound"
        print(setstatus)
        sleep(5)
        setstatus = "ready"
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
    if len(login.split()) > 0:
        login = login.split()[0]
        print(login)
    subprocess.call(
        f"cmdkey /add:localhost /user:DOMAIN\{login} /pass:{password}")  # Если пользователи не доменные DOMAIN\ убрать
    time.sleep(3)
    subprocess.call ("mstsc /v:localhost:2222")
    time.sleep(15)
    delkeyuser()


def delkeyuser():
    import subprocess
    subprocess.call("cmdkey /delete localhost")


