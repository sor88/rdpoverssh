from PyQt5 import QtWidgets, uic
from desing import Ui_MainWindow
import sys
import threading
import time

setstatus = None

def writelabelstatus():
    import sshconnect
    if sshconnect.setstatus is None:
        global setstatust
        setstatust = "Старт"
        print(setstatust)
        return

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



      #  self.ui.label_4.setText("Подключение к серверу авторизации")
        import sshconnect

        sshconnect.login = self.ui.lineEdit.text()
        time.sleep(1)


        potok = threading.Thread(target=writelabelstatus, daemon=True)
        potok.start()
        # self.ui.label_4.setText(setstatust)
        # self.ui.label_4.addText("fsdgjdhfgsdfg")
        # self.ui.label_4.adjustSize()

        if 2 < 1:
            self.ui.statusbar.showMessage(setstatust)
        else:
            self.ui.statusbar.showMessage(setstatust)

       # self.ui.listWidget.showMessage(setstatus)
        # tun = threading.Thread(target=sshconnect.connecting)
        sshconnect.connecting()






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