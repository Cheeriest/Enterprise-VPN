# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from random import randint
import requests, sys, time
import localproxy
import autoproxy
from threading import Thread
from ftpclient import *



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

class Ui_MainWindow(object):
    def __init__(self, TOKEN):
        self.vpn_on = False
        self.jwt_token = TOKEN
        self.AUTH_IP = 'localhost'
        self.AUTH_PORT = 5000
        self.auth_url = 'http://' + self.AUTH_IP + ':' + str(self.AUTH_PORT)
        self.local_proxy_ip = 'localhost'
        self.local_proxy_port = randint(5000, 10000) 
        self.local_proxy_thread = None
        
        
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        MainWindow.resize(500, 450)
        MainWindow.setWindowTitle(_fromUtf8("Fima VPN - Abstract Security "))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet(_fromUtf8("""background-image: url(mainbg.jpg);"""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.vpnButton = QtGui.QPushButton(self.centralwidget)
        self.vpnButton.setGeometry(QtCore.QRect(60, 60, 161, 131))
        self.vpnButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.vpnButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.vpnButton.setAutoFillBackground(False)
        self.vpnButton.setStyleSheet(_fromUtf8("border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"padding: 4px;\n"
"font-size:25px;\n"
"background-color: #A3C1DA; \n"
"color: red;"))
        self.vpnButton.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.vpnButton.setText(_fromUtf8("VPN: OFF"))
        self.vpnButton.setCheckable(False)
        self.vpnButton.setAutoDefault(False)
        self.vpnButton.setObjectName(_fromUtf8("vpnButton"))
        self.vpnButton.clicked.connect(lambda: self.handle_vpn(MainWindow))
        self.dmzButton = QtGui.QPushButton(self.centralwidget)
        self.dmzButton.setGeometry(QtCore.QRect(290, 60, 161, 131))
        self.dmzButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.dmzButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.dmzButton.setAutoFillBackground(False)
        self.dmzButton.setStyleSheet(_fromUtf8("border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"padding: 4px;\n"
"font-size:25px;\n"
"background-color: #A3C1DA; \n"
"color: red;"))
        self.dmzButton.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.dmzButton.setText(_fromUtf8("DMZ"))
        self.dmzButton.setCheckable(False)
        self.dmzButton.setAutoDefault(False)
        self.dmzButton.setObjectName(_fromUtf8("dmzButton"))
        self.comingSoonButton = QtGui.QPushButton(self.centralwidget)
        self.comingSoonButton.setGeometry(QtCore.QRect(290, 230, 161, 131))
        self.comingSoonButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.comingSoonButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comingSoonButton.setAutoFillBackground(False)
        self.comingSoonButton.setStyleSheet(_fromUtf8("border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"padding: 4px;\n"
"font-size:25px;\n"
"background-color: #A3C1DA; \n"
"color: yellow;\n"
""))
        self.comingSoonButton.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.comingSoonButton.setText(_fromUtf8("Coming soon"))
        self.comingSoonButton.setCheckable(False)
        self.comingSoonButton.setAutoDefault(False)
        self.comingSoonButton.setObjectName(_fromUtf8("comingSoonButton"))
        self.comingSoonButton.setEnabled(False)
        self.ftpButton = QtGui.QPushButton(self.centralwidget)
        self.ftpButton.setGeometry(QtCore.QRect(60, 230, 161, 131))
        self.ftpButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ftpButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.ftpButton.setAutoFillBackground(False)
        self.ftpButton.setStyleSheet(_fromUtf8("border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 15px;\n"
"border-color: black;\n"
"padding: 4px;\n"
"font-size:25px;\n"
"background-color: #A3C1DA; \n"
"color: red;\n"
""))
        self.ftpButton.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.ftpButton.setText(_fromUtf8("FTP"))
        self.ftpButton.setCheckable(False)
        self.ftpButton.setAutoDefault(False)
        self.ftpButton.setObjectName(_fromUtf8("ftpButton"))
        self.ftpButton.clicked.connect(lambda: self.handle_ftp())
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 400, 591, 31))
        self.label.setStyleSheet(_fromUtf8("background-color:#A3C1DA;\n"
"  border: 0px solid #32414B;\n"
"  padding: 2px;\n"
"  margin: 0px;\n"
"  color: rgb(0, 0, 0)"))
        self.label.setObjectName(_fromUtf8("label"))
        self.dmzButton.raise_()
        self.vpnButton.raise_()
        self.ftpButton.raise_()
        self.comingSoonButton.raise_()
        self.label.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
        self.menuInfo = QtGui.QMenu(self.menubar)
        self.menuInfo.setObjectName(_fromUtf8("menuInfo"))
        MainWindow.setMenuBar(self.menubar)
        self.actionVPN_Settings = QtGui.QAction(MainWindow)
        self.actionVPN_Settings.setObjectName(_fromUtf8("actionVPN_Settings"))
        self.actionFTP_Settings = QtGui.QAction(MainWindow)
        self.actionFTP_Settings.setObjectName(_fromUtf8("actionFTP_Settings"))
        self.actionDMZ_Settings = QtGui.QAction(MainWindow)
        self.actionDMZ_Settings.setObjectName(_fromUtf8("actionDMZ_Settings"))
        self.actionUse_Information = QtGui.QAction(MainWindow)
        self.actionUse_Information.setObjectName(_fromUtf8("actionUse_Information"))
        self.menuOptions.addAction(self.actionVPN_Settings)
        self.menuOptions.addAction(self.actionFTP_Settings)
        self.menuOptions.addAction(self.actionDMZ_Settings)
        self.menuInfo.addAction(self.actionUse_Information)
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.label.setText(_translate("MainWindow", "Current Information:", None))
        self.menuOptions.setTitle(_translate("MainWindow", "Options", None))
        self.menuInfo.setTitle(_translate("MainWindow", "Info", None))
        self.actionVPN_Settings.setText(_translate("MainWindow", "VPN Settings", None))
        self.actionFTP_Settings.setText(_translate("MainWindow", "FTP Settings", None))
        self.actionDMZ_Settings.setText(_translate("MainWindow", "DMZ Settings", None))
        self.actionUse_Information.setText(_translate("MainWindow", "Use Information", None))

    def handle_ftp(self):
        Ftp = FtpWindow()
        Ftp.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        Ftp.exec_()

    def handle_vpn(self, MainWindow):
        if not self.vpn_on:
            get_vpn_url = self.auth_url + '/vpn'
            req = requests.get(get_vpn_url, headers = {'x-access-token':self.jwt_token}).json()
            VPN_IP = req['ip']
            VPN_PORT = req['port']
            print self.local_proxy_ip + ":"+ str(self.local_proxy_port)
            autoproxy.on(self.local_proxy_ip + ":"+ str(self.local_proxy_port))
            self.local_proxy_thread = Thread(target = localproxy.main,\
                                             args = (self.jwt_token, VPN_IP, VPN_PORT, self.local_proxy_ip, self.local_proxy_port))
            self.local_proxy_thread.daemon = True
            self.local_proxy_thread.start()
            self.label.setText('Current Information: Enabled local proxy traffic')
            self.vpnButton.setStyleSheet(_fromUtf8("border-style: outset;\n"
    "border-width: 2px;\n"
    "border-radius: 15px;\n"
    "border-color: black;\n"
    "padding: 4px;\n"
    "font-size:25px;\n"
    "background-color: #A3C1DA; \n"
    "color: green;"))
            self.vpnButton.setText('VPN: ON')
            self.vpn_on = True
        else:
            autoproxy.off()
            self.vpnButton.setStyleSheet(_fromUtf8("border-style: outset;\n"
    "border-width: 2px;\n"
    "border-radius: 15px;\n"
    "border-color: black;\n"
    "padding: 4px;\n"
    "font-size:25px;\n"
    "background-color: #A3C1DA; \n"
    "color: red;"))
            self.vpnButton.setText('VPN: OFF')
            self.label.setText('Current Information: Disabled local proxy traffic')
            self.vpn_on = False