from PyQt5 import QtWidgets, uic
from desing import Ui_MainWindow
from PyQt5.QtCore import QCoreApplication
import sys
import threading
import time


class mywindow (QtWidgets.QMainWindow):

    def __init__(self):
        super (mywindow, self).__init__ ()
        self.ui = Ui_MainWindow ()
        self.ui.setupUi (self)
        self.ui.pushButton.clicked.connect (self.connectionstart)
        self.ui.statusbar.showMessage ("Программа готова к работе")

    def connectionstart(self):
        """
        Функция подключается к серверу СУБД  и передает введенную фамилию в качестве аргумента для поиска пользователя и ip адреса.
        """
        potok = threading.Thread (target=self.writelabelstatus, daemon=True)
        potok.start ()
        import sshconnect
        sshconnect.login = self.ui.lineEdit.text ()
        if sshconnect.login == '' or sshconnect.login is None:
            sshconnect.setstatus = "emptylogin"
            return
        sshconnect.password = self.ui.lineEdit_2.text ()
        if sshconnect.password == '' or sshconnect.password is None:
            sshconnect.setstatus = "emptypassword"
            return
        if sshconnect.login != "emptylogin" or sshconnect.local is not None and sshconnect.password != "emptypassword" or sshconnect.password is not None:
            if sshconnect.setstatus == "ready":
                tun1 = threading.Thread (target=sshconnect.connecttopc, daemon=True)
                sshconnect.setstatus == "connect"
                self.ui.statusbar.showMessage ("Подключение. Пожалуйста подождите...")
                tun1.start ()

    def writelabelstatus(self):
        """
        Функция выполняется следит за состоянием выполнения кода и изменяет сообщения в статус баре. Работает в отдельном потоке ( не блокирует основной поток, и форму приложения ).
        """
        import sshconnect
        while True:
            time.sleep (1)
            if sshconnect.setstatus == 'emptylogin':
                self.ui.statusbar.showMessage ("Поле: 'Логин' не заполнено")
                time.sleep (3)
                self.ui.statusbar.showMessage ("Программа готова к работе")
                sshconnect.setstatus = "ready"
                break
            if sshconnect.setstatus == 'emptypassword':
                self.ui.statusbar.showMessage ("Поле: 'Пароль' не заполнено")
                time.sleep (3)
                self.ui.statusbar.showMessage ("Программа готова к работе")
                sshconnect.setstatus = "ready"
                break
            if sshconnect.setstatus == "ip is found":
                self.ui.statusbar.showMessage ('IP найден. Выполняется подключение.')
                time.sleep (10)
                self.ui.statusbar.clearMessage ()
                self.ui.statusbar.showMessage ("Программа готова к работе")
                sshconnect.setstatus = "ready"
                break
            if sshconnect.setstatus == "ipnotfound":
                self.ui.statusbar.showMessage ('IP не найден. Обратитесь к администратору.')
                time.sleep (3)
                self.ui.lineEdit.clear ()
                self.ui.lineEdit_2.clear ()
                self.ui.statusbar.showMessage ("Программа готова к работе")
                sshconnect.setstatus = "ready"
                break
            if sshconnect.setstatus == "Получение ip адреса":
                self.ui.statusbar.showMessage (sshconnect.setstatus)

    def vihod(self):
        """
        Выход
        """
        sys.exit ()

    def update(self):
        """
        Запрос обновлений клиента
        """
        pass


app = QtWidgets.QApplication ([])
application = mywindow ()
application.show ()
sys.exit (app.exec ())