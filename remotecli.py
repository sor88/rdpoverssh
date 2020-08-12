from PyQt5 import QtWidgets, uic
from desing import Ui_MainWindow
from PyQt5.QtCore import QCoreApplication
import sys
import threading
import time


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.connectionstart)
        self.ui.statusbar.showMessage("Программа готова к работе")


    def connectionstart(self):
        """
        Функция подключается к керио передает введенную фамилию в качестве аргумента для поиска пользователя и ip адреса
        его компьютера в локальной сети. Далее kerio возвращает найденный ip адрес и передает в качестве аргумента для
        проброса порта на второй тоннель
        """
        potok = threading.Thread(target=self.writelabelstatus, daemon=True)
        potok.start()
       # import sshconnect

        from sshconnect import setstatus
        print(setstatus)
        from sshconnect import publicipadress
        if publicipadress[0] == "REMOTE_PUBLIC_IP":
            self.ui.statusbar.showMessage("Не задан IP адрес сервера SSH")
            return
        l = self.ui.lineEdit.text()
        if l == '':
            setstatus = "emptylogin"
            return
        p = self.ui.lineEdit_2.text()
        if p == '':
            setstatus = "emptypassword"
            return
     #   print(sshconnect.login)
        print(setstatus)
        self.ui.statusbar.showMessage("Подключение. Пожалуйста подождите...")
        if l != "emptylogin" and p != "emptypassword":
            import sshconnect
            sshconnect.login = l
            sshconnect.password = p
            tun1 = threading.Thread(target=sshconnect.connecttopc, daemon=True)
            tun1.start()

    def writelabelstatus(self):
        """
        Функция выполняется следит за состоянием выполнения кода и изменяет сообщения в статус баре. Работает в отдельном потоке ( не блокирует основной поток, и форму приложения ).
        """
        import sshconnect
        while True:
            time.sleep(1)
            if sshconnect.setstatus == 'emptylogin':
                self.ui.statusbar.showMessage("Поле: 'Логин' не заполнено")
                time.sleep(3)
                self.ui.statusbar.showMessage("Программа готова к работе")
                break
            if sshconnect.setstatus == 'emptypassword':
                self.ui.statusbar.showMessage("Поле: 'Пароль' не заполнено")
                time.sleep(3)
                self.ui.statusbar.showMessage("Программа готова к работе")
                break
            if sshconnect.setstatus == "ip is found":
                self.ui.statusbar.showMessage('IP найден. Выполняется подключение.')
                time.sleep(10)
                self.ui.statusbar.clearMessage()
                break
            if sshconnect.setstatus == "IP не найден":
                self.ui.statusbar.showMessage(sshconnect.setstatus)
                break
            
    def vihod(self):
        """
        Выход
        """
        sys.exit()

    def update(self):
        """
        Запрос обновлений клиента
        """
        pass


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit (app.exec ())