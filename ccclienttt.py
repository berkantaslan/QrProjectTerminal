from mainWinClient import Ui_MainWindow
import addMessage
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QDateTime
import sys
import time
import socket
import json
from pprint import pprint
import subprocess
import threading
from threading import Thread
import multiprocessing
import datetime
from matplotlib import pyplot as plt
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QTableWidgetItem, QFileDialog, QLabel, QDial
import os

class Main_App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Main_App, self).__init__(parent)
        self.Init_Ui()

    def Init_Ui(self):
        self.setupUi(self)
        self.show()
        self.pushButton.clicked.connect(self.QrDetector)
        self.pushButton_2.clicked.connect(self.QrDetectorWrite)
        self.actionProgram_Hakk_nda.triggered.connect(self.Hakkinda_Message)
        self.action_k.triggered.connect(self.Cikis)
        self.IP = socket.gethostbyname(socket.gethostname())
        #self.IP = "192.168.102.201"
        #self.IP = "192.168.100.168"
        self.PORT = 4455
        self.ADDR = (self.IP, self.PORT)
        self.FORMAT = "utf-8"
        self.SIZE = 2048
        self.t = 0

    def QrDetector(self):

        self.t = str(datetime.datetime.now())

        # try:
        self.veri = {

        "komut" : "Bağlantı kur.",
        "zaman" : self.t,
        "error" : "Hata yok.",
        "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

        }

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.client.connect(self.ADDR)

        self.client.send(bytes(json.dumps(self.veri), 'UTF-8'))

        # self.pushButton.setEnabled(False)
        # QTimer.singleShot(3000, lambda: self.pushButton.setDisabled(False))

        self.msg = self.client.recv(2048).decode(self.FORMAT)
        self.message= json.loads(self.msg)
        pprint(json.loads(self.msg))
        for key in json.loads(self.msg):
            pprint(json.loads(self.msg)[key])

        if self.message["durum"] == "Bağlantı kuruldu.":

            # threading.Thread(target=self.QrDetectorCam).start()
            self.QrDetectorCam()

        if self.message["durum"] == "Tekrar başlatılıyor.":

            # threading.Thread(target=self.QrDetector).start()
            self.QrDetector()

            # self.client.close()

        # except:
        #     print("Uygun olmayan istek")

    def QrDetectorCam(self):

        self.t = str(datetime.datetime.now())

        # try:

        self.veri = {

        "komut" : "Kamerayı başlat.",
        "zaman" : self.t,
        "error" : "Hata yok.",
        "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

        }

        self.client.send(bytes(json.dumps(self.veri), 'UTF-8'))

        self.msg = self.client.recv(2048).decode(self.FORMAT)
        pprint(json.loads(self.msg))
        for key in json.loads(self.msg):
            pprint(json.loads(self.msg)[key])

        # if self.pushButton.isChecked():
        #     # self.QrDetector()
        # threading.Thread(target=self.QrDetector).start()

        # self.client.close()

        # except:
        #     print("Uygun olmayan istek2")

    def QrDetectorWrite(self):

        self.t = str(datetime.datetime.now())

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.client.connect(self.ADDR)

        # try:
        self.veri = {

        "komut" : "Okudun mu?",
        "zaman" : self.t,
        "error" : "Hata yok.",
        "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

        }

        self.client.send(bytes(json.dumps(self.veri), 'UTF-8'))

        # self.QrDetectorWant()
        threading.Thread(target=self.QrDetectorWant).start()

        # except:
        #     print("Uygun olmayan istek3")

    def QrDetectorWant(self):

        try:
            while True:
                self.msg = self.client.recv(2048).decode(self.FORMAT)
                pprint(json.loads(self.msg))
                for key in json.loads(self.msg):
                    pprint(json.loads(self.msg)[key])

                os.execl(sys.executable, sys.executable, *sys.argv)

                self.client.close()

        except:
            print("Uygun olmayan istek4")

    def Cikis(self):
        result = QMessageBox.question(win, 'Message', 'Are you sure about exiting the program?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.NoButton)
        if result == QMessageBox.Yes:
            print("Programdan çıkış yapıldı.")
            win.close()
        else:
            win.show()

    def Hakkinda_Message(self):
        self.adding = Add_Message()
        self.adding.exec_()

class Add_Message(QDialog, addMessage.Ui_Dialog):
    def __init__(self, parent=None):
        super(Add_Message, self).__init__(parent)
        self.setupUi(self)

app = QApplication([])
win = Main_App()
app.exec_()
