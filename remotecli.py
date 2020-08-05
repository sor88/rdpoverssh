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
        self.ui.pushButton_2.clicked.connect(QCoreApplication.instance().quit)


    def connectionstart(self):
        """
        Функция подключается к керио передает введенную фамилию в качестве аргумента для поиска пользователя и ip адреса
        его компьютера в локальной сети. Далее kerio возвращает найденный ip адрес и передает в качестве аргумента для
        проброса порта на второй тоннель
        """
        potok = threading.Thread(target=self.writelabelstatus, daemon=True)
        potok.start()
        import sshconnect
        sshconnect.login = self.ui.lineEdit.text()
        if sshconnect.login == '':
            sshconnect.setstatus = "emptylogin"
            return
        sshconnect.password = self.ui.lineEdit_2.text()
        if sshconnect.password == '':
            sshconnect.setstatus = "emptypassword"
            return
        print(sshconnect.login)
        self.ui.statusbar.showMessage("Подключение. Пожалуйста подождите...")
        tun1 = threading.Thread(target=sshconnect.connecttopc, daemon=True)
        tun1.start()

    def writelabelstatus(self):
        import sshconnect
        while True:
            time.sleep(1)
            if sshconnect.setstatus == 'emptylogin':
                self.ui.statusbar.showMessage("Поле: 'Фамилия' не заполнено")
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