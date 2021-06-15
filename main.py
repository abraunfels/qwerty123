import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QTimer

import back
from errors import RegisterError, AccessError, AccessErrorType, OrdinaryError
import gen_pwd

def formatLabel(label, str):
    return "<html><head/><body><p align=\"center\">"+label+"</p>"+"<p align=\"center\">"+str+"</p>"+"</body></html>"

class Register(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('qwerty123: Регистрация')
        self.parent = parent
        font = QtGui.QFont()
        font.setFamily("Cocon-Regular")
        self.setFont(font)
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Button, QtGui.QColor(36, 43, 229))
        self.setPalette(pal)
        self.setMinimumWidth(500)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setAlignment(QtCore.Qt.AlignCenter)

        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignBottom)
        self.newLogin = QtWidgets.QLineEdit()
        self.newLogin.setMaxLength(15)
        self.newLogin.setMaximumWidth(500)
        self.newMasterKey = QtWidgets.QLineEdit()
        self.newMasterKey.setMaximumWidth(500)
        self.newMasterKey.setMaxLength(100)
        self.newMasterKey.setEchoMode(QtWidgets.QLineEdit.Password)
        self.repNewMasterKey = QtWidgets.QLineEdit()
        self.repNewMasterKey.setMaxLength(100)
        self.repNewMasterKey.setEchoMode(QtWidgets.QLineEdit.Password)
        self.repNewMasterKey.setMaximumWidth(500)
        self.denyBtm = QtWidgets.QPushButton()
        self.registerBtm = QtWidgets.QPushButton()

        self.label.setText("<html><head/><body><p align=\"center\">Регистрация</p></body></html>")
        self.newLogin.setPlaceholderText( "Логин")
        self.newMasterKey.setPlaceholderText("Пароль")
        self.repNewMasterKey.setPlaceholderText("Подтверждение пароля")

        self.horizonalLayout = QtWidgets.QHBoxLayout()

        self.denyBtm.setText("Отмена")
        self.registerBtm.setText("Регистрация")
        self.horizonalLayout.addWidget(self.denyBtm)
        self.horizonalLayout.addWidget(self.registerBtm)


        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.addWidget(self.newLogin)
        self.verticalLayout.addWidget(self.newMasterKey)
        self.verticalLayout.addWidget(self.repNewMasterKey)
        self.verticalLayout.addLayout(self.horizonalLayout)


        self.setLayout(self.verticalLayout)

        self.registerBtm.clicked.connect(self.click_registerBtn)
        self.denyBtm.clicked.connect(self.click_denyBtn)


    def click_registerBtn(self):
        username = self.newLogin.text()
        pwd = self.newMasterKey.text()
        rep_pwd = self.repNewMasterKey.text()

        if len(username)*len(pwd)*len(rep_pwd) != 0:
            if pwd == rep_pwd:
                self.register_user(username, pwd)
            else:
                self.label.setText(formatLabel("Регистрация","Пароли не совпдают"))

    def register_user(self, username, pwd):
        try:
            back.register(username, pwd)
            self.close()
            self.parent.setEnabled(True)
        except RegisterError as re:
            self.label.setText(formatLabel("Регистрация", str(re)))

    def click_denyBtn(self):
        self.closeEvent(QtGui.QCloseEvent)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.parent.setEnabled(True)
        self.close()

class Generator(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Generator, self).__init__()

        self.parent = parent

        font = QtGui.QFont()
        font.setFamily("Cocon-Regular")
        self.setFont(font)
        self.setWindowTitle("Генератор паролей")
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Button, QtGui.QColor(36, 43, 229))
        self.setPalette(pal)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignVCenter)

        self.lenHBox = QtWidgets.QHBoxLayout()

        self.lenHBox.addWidget(QtWidgets.QLabel('Длина'))
        self.lenline = QtWidgets.QLineEdit('15')
        self.lenline.setMaxLength(100)
        self.lenHBox.addWidget(self.lenline)

        self.verticalLayout.addLayout(self.lenHBox)

        self.pwd = QtWidgets.QLineEdit()
        self.verticalLayout.addWidget(self.pwd)

        self.bigCheck = QtWidgets.QCheckBox('a-z')
        self.smallCheck = QtWidgets.QCheckBox('A-Z')
        self.digitsCheck = QtWidgets.QCheckBox('0-9')
        self.symbolsCheck = QtWidgets.QCheckBox('@#$')

        self.verticalLayout.addWidget(self.bigCheck)
        self.verticalLayout.addWidget(self.smallCheck)
        self.verticalLayout.addWidget(self.digitsCheck)
        self.verticalLayout.addWidget(self.symbolsCheck)

        self.smallCheck.setChecked(True)
        self.bigCheck.setChecked(True)
        self.digitsCheck.setChecked(True)
        self.symbolsCheck.setChecked(True)

        self.generate()

        self.btnBox = QtWidgets.QDialogButtonBox()

        self.btnBox.addButton('Сохранить', QtWidgets.QDialogButtonBox.AcceptRole)
        self.btnBox.addButton('Отмена', QtWidgets.QDialogButtonBox.RejectRole)

        self.verticalLayout.addWidget(self.btnBox)

        self.setLayout(self.verticalLayout)

        self.lenline.returnPressed.connect(self.generate)
        self.smallCheck.stateChanged.connect(self.generate)
        self.bigCheck.stateChanged.connect(self.generate)
        self.digitsCheck.stateChanged.connect(self.generate)
        self.symbolsCheck.stateChanged.connect(self.generate)

        self.btnBox.rejected.connect(lambda : self.close())
        self.btnBox.accepted.connect(self._accept)

    def generate(self):
        BI, LO, NU, PS = self.get_check()
        len = self.lenline.text()
        pwd = gen_pwd.gen_pwd(len, BI, LO, NU, PS)
        self.pwd.setText(pwd)
        return pwd

    def get_check(self):
        return [self.smallCheck.isChecked(),
                self.bigCheck.isChecked(),
                self.digitsCheck.isChecked(),
                self.symbolsCheck.isChecked()]

    def _accept(self):
        self.parent.set_pwd(self.pwd.text())
        self.close()


def generate_label_package(name):
    label = QtWidgets.QLabel(name+':')
    line = QtWidgets.QLineEdit()
    line.setMaxLength(255)
    line.setMaximumWidth(500)

    return {'label': label,
        'line': line
            }

class Element(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Element, self).__init__(parent)
        self.parent = parent
        self.id = id

        font = QtGui.QFont()
        font.setFamily("Cocon-Regular")
        self.setFont(font)
        self.setWindowTitle("Редактирование")
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Button, QtGui.QColor(36, 43, 229))
        self.setPalette(pal)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setAlignment(QtCore.Qt.AlignHCenter)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignVCenter)

        full_dict = {'address':'Сайт',
                    'login':'Логин',
                    'password':'Пароль',
                    'comment':'Примечание'}

        self.package = {key: generate_label_package(full_dict[key]) for key in full_dict}

        self.package['password']['line'].setEchoMode(QtWidgets.QLineEdit.Password)

        for key in self.package.keys():
            self.verticalLayout.addWidget(self.package[key]['label'])
            if key == 'password':
                self.hPassBox = QtWidgets.QHBoxLayout()
                self.hPassBox.addWidget(self.package[key]['line'])
                self.openPwdBtn = QtWidgets.QToolButton()
                self.hPassBox.addWidget(self.openPwdBtn)
                self.genBtn = QtWidgets.QToolButton()
                self.hPassBox.addWidget(self.genBtn)
                self.verticalLayout.addLayout(self.hPassBox)
            else:
                self.verticalLayout.addWidget(self.package[key]['line'])

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.saveBtn = QtWidgets.QPushButton('Сохранить')
        self.denyBtn = QtWidgets.QPushButton('Отмена')

        self.horizontalLayout.addWidget(self.denyBtn)
        self.horizontalLayout.addWidget(self.saveBtn)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.setLayout(self.verticalLayout)

        self.denyBtn.clicked.connect(self.click_denyBtn)
        self.saveBtn.clicked.connect(self.click_saveBtn)

        self.genBtn.setIcon(QtGui.QIcon(QtGui.QPixmap("key-fill.svg")))
        self.genBtn.clicked.connect(self.gen_pass)

        self.openPwdBtn.setIcon(QtGui.QIcon(QtGui.QPixmap("eye.svg")))
        self.openPwdBtn.clicked.connect(self.open_pass)

    def gen_pass(self):
        generator = Generator(parent=self)
        generator.show()

    def open_pass(self):
        self.package['password']['line'].setEchoMode(QtWidgets.QLineEdit.Normal)
        self.openPwdBtn.clicked.connect(self.close_pass)

    def close_pass(self):
        self.package['password']['line'].setEchoMode(QtWidgets.QLineEdit.Password)
        self.openPwdBtn.clicked.connect(self.open_pass)


    def click_denyBtn(self):
        self.close()

    def set_pwd(self, new_pwd):
        self.package['password']['line'].setText(new_pwd)

class NewElement(Element):
    def __init__(self, parent=None):
        super(NewElement, self).__init__(parent)

    def click_saveBtn(self):
        address, login, password, comment = [value['line'].text() for value in self.package.values()]
        if len(address)*len(login)*len(password) != 0:
            id = back.new_element(self.parent.username, address, login, password, comment)
            self.parent.parent.list_add(id, address, login, comment)
            self.close()

class EditElement(Element):
    def __init__(self, id, parent=None):
        super(EditElement, self).__init__(parent)
        self.id = id
        element = back.get_element(self.parent.username, self.id)
        for key in element.keys():
            self.package[key]['line'].setText(element[key])

    def click_saveBtn(self):
        address, login, password, comment = [value['line'].text() for value in self.package.values()]
        if len(address) * len(login) * len(password) != 0:
            back.edit_element(self.parent.username, self.id, address, login, password, comment)
            self.parent.parent.list_update()
            self.close()

class ItemWidget(QtWidgets.QWidget):
    def __init__(self, address, login, comment, parent=None):
        super(ItemWidget, self).__init__()
        self.parent = parent

        self.username = parent.username
        self.address = address
        self.login = login

        self.row = QtWidgets.QHBoxLayout()

        self.addressLabel = QtWidgets.QLabel(address)
        self.loginLabel = QtWidgets.QLabel(login)
        self.commentLabel = QtWidgets.QLabel(comment)
        self.toolBtn = QtWidgets.QToolButton()

        self.row.addWidget(self.addressLabel)
        self.row.addWidget(self.loginLabel)
        self.row.addWidget(self.commentLabel)
        self.row.addWidget(self.toolBtn)

        self.setLayout(self.row)

class HeaderItem(ItemWidget):
    def __init__(self, address, login, comment, parent=None):
        super(HeaderItem, self).__init__(address, login, comment, parent)
        self.toolBtn.setIcon(QtGui.QIcon(QtGui.QPixmap("plus.svg")))
        self.toolBtn.clicked.connect(self.add_element)

    def add_element(self):
        self.el = NewElement(parent=self)
        self.el.show()



class RowItem(ItemWidget):
    def __init__(self, id, address, login, comment, parent=None):
        super(RowItem, self).__init__(address, login, comment, parent)
        self.id = id

        self.toolBtn.setIcon(QtGui.QIcon(QtGui.QPixmap("chevron-right.svg")))
        self.delBtn = QtWidgets.QToolButton()
        self.delBtn.setIcon(QtGui.QIcon(QtGui.QPixmap("x.svg")))
        self.row.addWidget(self.delBtn)

        self.delBtn.clicked.connect(self.del_element)
        self.toolBtn.clicked.connect(self.edit_element)

    def del_element(self):
        back.del_element(self.parent.username, self.id)
        self.parent.list_update()

    def edit_element(self):
        self.el = EditElement(self.id, parent=self)
        self.el.show()


class QwertyMain(QtWidgets.QMainWindow):
    def __init__(self, username, parent=None):
        super(QwertyMain, self).__init__(parent)
        self.parent = parent

        self.username = username

        self.setMinimumWidth(500)

        font = QtGui.QFont()
        font.setFamily("Cocon-Regular")
        self.setFont(font)
        self.setWindowTitle("qwerty123")
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Button, QtGui.QColor(36, 43, 229))
        self.setPalette(pal)

        self.init_row = HeaderItem('Сайт', 'Логин', 'Примечание', self)


    def list_display(self):
        data = back.get_elements(self.username)
        for key in data.keys():
            row = RowItem(key, data[key]['address'], data[key]['login'], data[key]['comment'], self)
            self.verticalLayout.addWidget(row)

        #self.setLayout(self.verticalLayout)

    def list_add(self, id, address, login, comment):
        row = RowItem(id, address, login, comment, self)
        self.verticalLayout.addWidget(row)
        self.setLayout(self.verticalLayout)

    def list_update(self):
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)

        self.verticalLayout.addWidget(self.init_row)
        self.list_display()
        #self.setLayout(self.verticalLayout)
        self.centralWidget = QtWidgets.QWidget()
        self.centralWidget.setLayout(self.verticalLayout)
        self.setCentralWidget(self.centralWidget)


class Auth(QtWidgets.QWidget):
    def __init__(self):
        super(Auth, self).__init__()
        font = QtGui.QFont()
        font.setFamily("Cocon-Regular")
        self.setFont(font)
        pal = QtGui.QPalette()
        pal.setColor(QtGui.QPalette.Button, QtGui.QColor(36, 43, 229))
        self.setPalette(pal)
        self.setMinimumWidth(500)

        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel()
        self.verticalLayout.addWidget(self.label)
        self.verticalLayout.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignCenter))

        self.login = QtWidgets.QLineEdit()
        self.login.setMaxLength(15)
        self.verticalLayout.addWidget(self.login)

        self.masterKey = QtWidgets.QLineEdit()
        self.masterKey.setMaxLength(100)
        self.masterKey.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verticalLayout.addWidget(self.masterKey)

        self.signBtm = QtWidgets.QPushButton()
        self.verticalLayout.addWidget(self.signBtm)

        self.label_2 = QtWidgets.QLabel()
        self.verticalLayout.addWidget(self.label_2)

        self.regBtm = QtWidgets.QPushButton()
        self.verticalLayout.addWidget(self.regBtm)

        self.setWindowTitle('qwerty123: Регистрация')
        self.label.setText("<html><head/><body><p align=\"center\">Вход в систему</p></body></html>")
        self.login.setPlaceholderText("Логин")
        self.masterKey.setPlaceholderText("Мастер-ключ")
        self.signBtm.setText("Вход")
        self.label_2.setText("<html><head/><body><p align=\"center\">Нет аккаунта?</p></body></html>")
        self.regBtm.setText("Регистрация")

        self.login.setMaximumWidth(500)
        self.masterKey.setMaximumWidth(500)
        self.signBtm.setMaximumWidth(500)
        self.regBtm.setMaximumWidth(500)

        self.label.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignBottom))
        self.label_2.setAlignment(QtCore.Qt.Alignment(QtCore.Qt.AlignBottom))

        self.setLayout(self.verticalLayout)

        self.signBtm.clicked.connect(self.click_signBtm)
        self.regBtm.clicked.connect(self.register)


    def click_signBtm(self):
        username = self.login.text()
        pwd = self.masterKey.text()

        if len(username) * len(pwd) != 0:
            self.sign_in(username, pwd)

    def sign_in(self, username, pwd):
        try:
            self.check_attempts(username)
            back.check_entrance(username, pwd)
            back.new_attempts(username, 0)
            self.close()
            inizialized(username)

        except AccessError as ae:
            self.label.setText(formatLabel("Вход в систему", str(ae)))
            if ae.type == AccessErrorType.PASSWORD_FASLE:
               back.new_attempts(username, 1)

    def register(self):
        self.reg = Register(self)
        self.reg.show()
        self.setEnabled(False)

    def check_attempts(self, username):
        attempts = back.check_attempts(username)
        if attempts > 2:
            back.new_attempts(username, -2)
            self.wait()

    def wait(self):
        self.signBtm.setEnabled(False)
        timer = QTimer(self)
        timer.timeout.connect(lambda :self.signBtm.setEnabled(True))
        timer.start(1000*15)

def inizialized(username):
    try:
        qwertyMain = QwertyMain(username)
        qwertyMain.list_update()
        qwertyMain.show()
    except OrdinaryError as er:
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(str(er))
        msg.exec_()  # this will show our messagebox


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    app.setStyle('Fusion')
    auth_window = Auth()  # Создаём объект класса App
    auth_window.show()  # Показываем окно

    app.exec_()  # и запускаем приложение


