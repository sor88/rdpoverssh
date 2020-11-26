from PyQt5 import QtWidgets
from first_form import Ui_MainWindow
from secondform import Ui_Form
import sys
import threading
import time
import sshconnect

class mywindow (QtWidgets.QMainWindow):

    def __init__(self):
        super (mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.connectionstart)
        sshconnect.read_settings()
        self.ui.statusBar.showMessage("Программа готова к работе")
  #      self.ui.label_2.clicked.connect(secondform.Ui_Form)

    def connectionstart(self):
        """
        Функция запускает в отдельном потоке функцию мониторинга состояния программы, для отображения его (состояния)
        в статус баре. Функция Проверяет заполненность полей Логина и пароля. Если одно из полей пустое, происходит
        возврат. Программа останавливается. Если все поля заполнены и статус программы " Программа готова к работе"
        происходит вызов фунции.
        """
        potok = threading.Thread(target=self.writelabelstatus, daemon=True)
        potok.start()
      #  import sshconnect
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
                self.starttun()

    def writelabelstatus(self):
        """
        Функция следит за состоянием выполнения кода и отображает в статус баре статус состояния программы. Работает в
        отдельном потоке ( не блокирует основной поток, форму приложения ).
        """
      #  import sshconnect
        while True:
            time.sleep(1)
            if sshconnect.setstatus == 'emptylogin':
                self.ui.statusBar.showMessage("Поле: 'Логин' не заполнено")
                time.sleep(3)
                self.ui.statusBar.showMessage("Программа готова к работе")
                sshconnect.setstatus = "ready"
                break
            if sshconnect.setstatus == 'emptypassword':
                self.ui.statusBar.showMessage("Поле: 'Пароль' не заполнено")
                time.sleep(3)
                self.ui.statusBar.showMessage("Программа готова к работе")
                sshconnect.setstatus = "ready"
                break
            if sshconnect.setstatus == "ip is found":
                self.ui.statusBar.showMessage('IP найден. Выполняется подключение.')
                time.sleep(10)
                self.ui.statusBar.clearMessage()
                self.ui.statusBar.showMessage("Программа готова к работе")
                sshconnect.setstatus = "ready"
                break
            if sshconnect.setstatus == "ipnotfound":
                self.ui.statusBar.showMessage('IP не найден. Обратитесь к администратору.')
                time.sleep(3)
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
                self.ui.statusBar.showMessage("Программа готова к работе")
                sshconnect.setstatus = "ready"
                break
            if sshconnect.setstatus == "Получение ip адреса":
                self.ui.statusBar.showMessage(sshconnect.setstatus)


    def starttun(self):
        """
        Функция вызывает функцию функцию установки ssh сессии в отдельном потоке.
        """
    #    import sshconnect
        tun1 = threading.Thread(target=sshconnect.connecttopc, daemon=True)
        sshconnect.setstatus == "connect"
        self.ui.statusBar.showMessage("Подключение. Пожалуйста подождите...")
        tun1.start()

    def update(self):
        """
        Запрос обновлений клиента
        """
        pass


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec())