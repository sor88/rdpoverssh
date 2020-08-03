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
        # tex = self.ui.lineEdit.text()
        # print(tex)

    def connectionstart(self):
        """
        Функция подключается к керио передает введенную фамилию в качестве аргумента для поиска пользователя и ip адреса
        его компьютера в локальной сети. Далее kerio возвращает найденный ip адрес и передает в качестве аргумента для
        проброса порта на второй тоннель
        """
        import sshconnect
        sshconnect.login = self.ui.lineEdit.text()
        time.sleep(1)
        potok = threading.Thread(target=self.writelabelstatus, daemon=True)
        potok.start()
        # self.ui.label_4.setText(setstatust)
        # self.ui.label_4.addText("fsdgjdhfgsdfg")
        # self.ui.label_4.adjustSize()
        self.ui.statusbar.showMessage("Подключение.Пожалуйста подождите...")
        sshconnect.connecting()

    def writelabelstatus(self):
        import sshconnect
        while True:
            time.sleep(5)
            if sshconnect.setstatus is None:
                setstatust = "Старт"
                print(setstatust)
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