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
        self.ui.pushButton_2.clicked.connect(self.vihod)



    def connectionstart(self):
        """
        Функция подключается к керио передает введенную фамилию в качестве аргумента для поиска пользователя и ip адреса
        его компьютера в локальной сети. Далее kerio возвращает найденный ip адрес и передает в качестве аргумента для
        проброса порта на второй тоннель
        """
        self.ui.label_4.setText("Подключение к серверу авторизации")
        self.ui.label.adjustSize()

        import sshconnect
        sshconnect.connecting()


        while True:
             if sshconnect.setstatus:
                  self.ui.label_4.setText("Поиск ip адреса в локальной сети")
                  break

    def vihod(self):
        """
        Выход
        """
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