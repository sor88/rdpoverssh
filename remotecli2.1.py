from PyQt5 import QtWidgets, uic
from desing import Ui_MainWindow
import sys

class mywindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.connectionstart)
        self.ui.pushButton_2.clicked.connect(self.vihod)



    def connectionstart(self):
       self.ui.label_4.setText("Подключение к серверу авторизации")
       self.ui.label.adjustSize()
       import sshconnect
       import threading
       tun1 = threading.Thread(target=sshconnect.sshtunconnect, daemon=True)
       tun1.start()

    def vihod(self):
        """
        Выход
        """
        exit()

    def zaprosip():
        """
        Подключение к керио и поиск ip адреса для дальнейшего проброса порта и подклчюения к нему
        """
        pass
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