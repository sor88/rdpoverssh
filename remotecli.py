from PyQt5 import QtWidgets, uic
from desing import Ui_MainWindow
import sys
import threading
import time


class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.connectionstart)
        self.ui.statusbar.showMessage("Программа готова для работы")
        self.ui.pushButton_2.clicked.connect(self.vihod)


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
        #tex = self.ui.lineEdit.text()
        print(sshconnect.login)
        self.ui.statusbar.showMessage("Подключение.Пожалуйста подождите...")
        sshconnect.connecting()

    def writelabelstatus(self):
        import sshconnect
        while True:
            time.sleep(1)
            if sshconnect.setstatus == 'emptylogin':
                self.ui.statusbar.showMessage("Поле Фамилия не заполнено")
                break
            if sshconnect.setstatus == 'emptypassword':
                self.ui.statusbar.showMessage("Поле пароль не заполнено")
                break
            if sshconnect.setstatus == "ip is found":
                self.ui.statusbar.showMessage('IP найден, выполняется проброс порта.')
            if sshconnect.setstatus == "IP не найден":
                self.ui.statusbar.showMessage(sshconnect.setstatus)
                break

    def vihod(self):
        """
        Выход
        """
        self.ui.label_4.setText ("Выход")
        exit()

    def update(self):
        """
        Запрос обновлений клиента
        """
        pass


app = QtWidgets.QApplication([])
application = mywindow()
application.show()

#win = uic.loadUi ("untitled.ui")  # расположение вашего файла .ui

#win.show ()
sys.exit (app.exec ())