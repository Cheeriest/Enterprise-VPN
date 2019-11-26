# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_Main(object):
    def setupUi(self, Main):
        Main.setObjectName(_fromUtf8("Main"))
        Main.resize(388, 400)
        Main.setWindowTitle(_fromUtf8("VPiNhas"))
        self.centralwidget = QtGui.QWidget(Main)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 250, 171, 71))
        self.pushButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton.setStyleSheet(_fromUtf8("QPushButton {\n"
"    color: #333;\n"
"    border: 2px solid #555;\n"
"    border-radius: 20px;\n"
"    border-style: outset;\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
"        );\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:hover {\n"
"    background: qradialgradient(\n"
"        cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #bbb\n"
"        );\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"    background: qradialgradient(\n"
"        cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"        radius: 1.35, stop: 0 #fff, stop: 1 #ddd\n"
"        );\n"
"    }"))
        self.pushButton.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(112, 150, 161, 20))
        self.lineEdit.setStyleSheet(_fromUtf8("QLineEdit {\n"
" border: 2px solid gray;\n"
" border-radius: 10px;\n"
"}"))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(112, 210, 161, 20))
        self.lineEdit_2.setStyleSheet(_fromUtf8("QLineEdit {\n"
" border: 2px solid gray;\n"
" border-radius: 10px;\n"
"}"))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 0, 351, 121))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Rockwell"))
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 120, 71, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 190, 71, 20))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(0, 360, 411, 16))
        self.label_4.setAutoFillBackground(True)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        Main.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(Main)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        Main.setStatusBar(self.statusbar)

        self.retranslateUi(Main)
        QtCore.QMetaObject.connectSlotsByName(Main)

    def retranslateUi(self, Main):
        self.pushButton.setText(_translate("Main", "Disconnected", None))
        self.label.setText(_translate("Main", "<html><head/><body><p><span style=\" color:#fc0000;\">Please Insert Information </span></p><p><span style=\" color:#fc0000;\">regarding your VPN Server </span></p></body></html>", None))
        self.label_2.setText(_translate("Main", "<html><head/><body><p><span style=\" font-weight:600;\">Server IP:</span></p></body></html>", None))
        self.label_3.setText(_translate("Main", "<html><head/><body><p><span style=\" font-weight:600;\">Server Port:</span></p></body></html>", None))
        self.label_4.setText(_translate("Main", "<html><head/><body><p><span style=\" font-weight:600; font-style:italic;\">STATUS: </span></p></body></html>", None))

