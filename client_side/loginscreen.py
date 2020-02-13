# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import requests, json, sys
from mw import Ui_MainWindow

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def __init__(self):
        self.TOKEN = ""
        self.AUTH_IP = 'localhost'
        self.AUTH_PORT = 5000
        
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowTitle(_fromUtf8("Fima VPN - Abstract Security "))
        Dialog.resize(400, 480)
        Dialog.setMinimumSize(QtCore.QSize(400, 480))
        Dialog.setMaximumSize(QtCore.QSize(400, 480))
        Dialog.setAutoFillBackground(True)
        Dialog.setStyleSheet(_fromUtf8("background-image: url(mainbg.jpg);"))
        self.user_label = QtGui.QLabel(Dialog)
        self.user_label.setGeometry(QtCore.QRect(170, 110, 61, 41))
        self.user_label.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.user_label.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.user_label.setObjectName(_fromUtf8("user_label"))
        self.user_textedit_2 = QtGui.QTextEdit(Dialog)
        self.user_textedit_2.setGeometry(QtCore.QRect(60, 240, 281, 31))
        self.user_textedit_2.setStyleSheet(_fromUtf8("background-color: gray;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    "))
        self.user_textedit_2.setObjectName(_fromUtf8("user_textedit_2"))
        self.user_textedit_3 = QtGui.QTextEdit(Dialog)
        self.user_textedit_3.setGeometry(QtCore.QRect(60, 150, 281, 31))
        self.user_textedit_3.setStyleSheet(_fromUtf8("background-color: gray;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    "))
        self.user_textedit_3.setObjectName(_fromUtf8("user_textedit_3"))
        self.user_label_2 = QtGui.QLabel(Dialog)
        self.user_label_2.setGeometry(QtCore.QRect(140, 190, 141, 41))
        self.user_label_2.setCursor(QtGui.QCursor(QtCore.Qt.UpArrowCursor))
        self.user_label_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.user_label_2.setObjectName(_fromUtf8("user_label_2"))
        self.login_button = QtGui.QPushButton(Dialog)
        self.login_button.clicked.connect(lambda : self.login_callback(Dialog))
        self.login_button.setGeometry(QtCore.QRect(80, 310, 241, 41))
        self.login_button.setStyleSheet(_fromUtf8("background-color: orange;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;"))
        self.login_button.setObjectName(_fromUtf8("login_button"))
        self.signup_button = QtGui.QPushButton(Dialog)
        self.signup_button.setGeometry(QtCore.QRect(110, 370, 186, 41))
        self.signup_button.setStyleSheet(_fromUtf8("background-color: orange;\n"
"    border-style: outset;\n"
"    border-width: 2px;\n"
"    border-radius: 10px;\n"
"    border-color: beige;\n"
"    font: bold 14px;\n"
"    min-width: 10em;\n"
"    padding: 6px;"))
        self.signup_button.setObjectName(_fromUtf8("signup_button"))
        self.retranslateUi(Dialog)
        self.login_button.raise_()
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        
        
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Fima VPN - Abstract Security", "Fima VPN - Abstract Security", None))
        self.login_button.setText(_translate("Dialog", "Login", None))
        self.signup_button.setText(_translate("Dialog", "Sign Up", None))
        self.user_label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">User</span></p></body></html>", None))
        self.user_label_2.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600;\">Password</span></p></body></html>", None))

    def login_callback(self, Dialog):
        url = 'http://' + self.AUTH_IP + ':' + str(self.AUTH_PORT)
        login_url = url + '/login'
        username = str(self.user_textedit_3.toPlainText())
        password = str(self.user_textedit_2.toPlainText()) 
        print username, password
        data_json = { 'name':username, 'password':password }
        headers = { 'Content-type': 'application/json' }
        try:
            req = requests.post(login_url, json=data_json, headers=headers)
            if json.loads(req.text).get('token'):
                self.TOKEN = json.loads(req.text)['token']
                Dialog.accept()
        except requests.exceptions.ConnectionError:
            return
        except ValueError:
            print 'Wrong Credentials'
        
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    if Dialog.exec_() == QtGui.QDialog.Accepted:
        window = Ui_MainWindow(ui.TOKEN)
        MainWindow = QtGui.QMainWindow()
        window.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())


