from __future__ import print_function
import sys
import time
import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np
import socket
import json
from pprint import pprint
import subprocess
import threading
from threading import Thread
import multiprocessing
import datetime
from matplotlib import pyplot as plt
from PIL import Image
import os

class QrDetectorSystem:

    def __init__(self):

        self.IP = socket.gethostbyname(socket.gethostname())
        #self.IP = "192.168.102.201"
        #self.IP = "192.168.100.168"
        self.PORT = 3456
        self.ADDR = (self.IP, self.PORT)
        self.FORMAT = "utf-8"
        self.SIZE = 3096
        self.t = 0
        self.liste = list()
        self.a = 0
        self.b = 0

    def Start_Webcam(self):

        # self.capture = cv2.VideoCapture('rtsp://192.168.102.77:554/ch01_sub.264')
        self.capture = cv2.VideoCapture(0)
        #self.capture = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L)
        #self.capture = cv2.VideoCapture("/dev/video1", cv2.CAP_V4L)

        if not self.capture.isOpened():
            self.Send_Error(3)

        else:
            self.Update_Frame()

    def decode(self, image):

        # Find barcodes and QR codes
        self.decodedObjects = pyzbar.decode(self.image)
        # Print results
        #for self.obj in self.decodedObjects:
            #print('Type : ', self.obj.type)
            #print('Data : ', self.obj.data, '\n')
        return self.decodedObjects

    def Update_Frame(self):

        try:

            self.font = cv2.FONT_HERSHEY_SIMPLEX

            if self.capture.isOpened() == True:

                while(self.capture.isOpened()):

                    # Capture frame-by-frame
                    self.ret, self.frame = self.capture.read()

                    # Our operations on the frame come here
                    self.image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

                    self.decodedObjects = self.decode(self.image)
                    # self.decodedObjects = threating.Thread(target=self.decode, args=(self.image)).start()

                    for self.decodedObject in self.decodedObjects:

                        self.points = self.decodedObject.polygon

                        # If the points do not form a quad, find convex hull
                        if len(self.points) > 4:
                            self.hull = cv2.convexHull(
                                np.array([self.point for self.point in self.points], dtype=np.float32))
                            self.hull = list(map(tuple, np.squeeze(self.hull)))
                        else:
                            self.hull = self.points

                        # Number of points in the convex hull
                        n = len(self.hull)
                        # Draw the convext hull
                        for j in range(0, n):
                            cv2.line(self.image, self.hull[j],
                                     self.hull[(j+1) % n], (255, 0, 0), 1)

                        x = self.decodedObject.rect.left
                        y = self.decodedObject.rect.top

                        #print(x, y)

                        #print('Type : ', self.decodedObject.type)
                        #print('Data : ', self.decodedObject.data, '\n')

                        self.barCode = str(self.decodedObject.data)
                        cv2.putText(self.frame, self.barCode, (x, y-20),
                                    self.font, 1, (0, 255, 255), 2, cv2.LINE_AA)

                        self.decodedText = self.barCode[2:-1]

                        self.liste.append(self.decodedText)

                        if not len(self.liste) == 0:

                            self.capture.release()

                    #cv2.imshow('frame',self.frame)

                    key = cv2.waitKey(1)

            else:
                self.Send_Error(3)

        except:
            self.Send_Error(4)

    def Send_Message(self):

        #self.server.listen()

        #self.conn, self.ADDR = self.server.accept()

        self.t = str(datetime.datetime.now())

        try:

            self.capture.release()

            self.capture = cv2.VideoCapture(0)
            #self.capture = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L)
            #self.capture = cv2.VideoCapture("/dev/video1", cv2.CAP_V4L)

            if self.capture.isOpened() != True:
               self.Send_Error(3)

            else:

                self.capture.release()

                if not len(self.liste) == 0:

                    self.veri = {

                    "detectedQr" : self.liste[0],
                    "zaman" : self.t,
                    "error" : "Hata yok.",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    self.liste.pop(0)

                    #self.server.close()

                    #os.execl(sys.executable, sys.executable, *sys.argv)

                else:

                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata yok.",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    #self.server.close()

                    #os.execl(sys.executable, sys.executable, *sys.argv)

        except:
            self.Send_Error(4)

    def Send_Error(self, window):

        #self.server.listen()

        #self.conn, self.ADDR = self.server.accept()

        self.capture.release()

        try:

            self.t = str(datetime.datetime.now())

            if window == 3:

                try:
                    #print("Webcam bağlı değil ya da Kamera arızalı, ya da Ağ bağlantısı kurulamadı.")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Webcam bağlı değil ya da Kamera arızalı",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    # self.server.close()
                    #os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 4:

                try:
                    #print("Webcam bağlı değil ya da Kamera arızalı, ya da Ağ bağlantısı kurulamadı.")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Ağ bağlantısı kurulamadı.",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    # self.server.close()
                    #os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 10:

                try:
                    #print("Program kapatıldı.")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Program kapatıldı.",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    # self.server.close()
                    #os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 11:

                #print("Program kapatıldı.")
                self.veri = {

                "detectedQr" : "Qr Kodu tespit edilemedi.",
                "zaman" : self.t,
                "error" : "Hata: JSON gönderim hatası ile karşılaşıldı.",
                "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                }

                self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                # self.server.close()
                #os.execl(sys.executable, sys.executable, *sys.argv)

            else:
                self.Send_Error(4)

        except:
            self.Send_Error(4)

    def Server_Ol(self):

        try:

            if self.b == 1:

                self.t = str(datetime.datetime.now())

                self.server.listen()

                self.conn, self.ADDR = self.server.accept()

                if self.a == 0:

                    #self.capture.release()

                    # try:

                    self.a = 1

                    self.msg = self.conn.recv(3096).decode(self.FORMAT)
                    self.message= json.loads(self.msg)
                    pprint(json.loads(self.msg))
                    #for key in json.loads(self.msg):
                        #pprint(json.loads(self.msg)[key])

                    if self.message["komut"] == "Bağlantı kur.":

                        self.veri = {

                        "durum" : "Bağlantı kuruldu.",
                        "zaman" : self.t,
                        "error" : "Hata yok.",
                        "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                        }

                        self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                        # self.b = 1
                        #
                        # self.Server_Ol()

                    #     else:
                    #         self.Send_Error(4)
                    #
                    # except:
                    #     self.Send_Error(4)

                if self.a == 1:

                    #self.capture.release()

                    try:

                        self.server.listen()

                        self.conn, self.ADDR = self.server.accept()

                        self.capture = cv2.VideoCapture(0)
                        #self.capture = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L)

                        if not self.capture.isOpened():
                            self.Send_Error(3)

                        else:

                            self.a = 2

                            self.msg = self.conn.recv(3096).decode(self.FORMAT)
                            self.message= json.loads(self.msg)
                            pprint(json.loads(self.msg))
                            #for key in json.loads(self.msg):
                                #pprint(json.loads(self.msg)[key])

                            self.capture.release()

                            if self.message["komut"] == "Kamerayı başlat.":

                                self.veri = {

                                "durum" : "Kamera başlatıldı.",
                                "zaman" : self.t,
                                "error" : "Hata yok.",
                                "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                                }

                                self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                                threading.Thread(target=self.Start_Webcam).start()
                                #self.Start_Webcam()

                                # self.b = 1
                                #
                                # self.Server_Ol()

                            else:
                                self.Send_Error(4)

                    except:
                        self.Send_Error(4)

                if self.a == 2:

                    try:

                        self.server.listen()

                        self.conn, self.ADDR = self.server.accept()

                        #self.capture = cv2.VideoCapture(0)
                        #self.capture = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L)

                        # if not self.capture.isOpened():
                        #     self.Send_Error(3)
                        #
                        # else:

                            # while True:

                        self.msg = self.conn.recv(3096).decode(self.FORMAT)
                        self.message= json.loads(self.msg)
                        pprint(json.loads(self.msg))
                        #for key in json.loads(self.msg):
                            #pprint(json.loads(self.msg)[key])

                        self.capture.release()

                        if self.message["komut"] == "Okudun mu?":

                            #self.capture.release()

                            threading.Thread(target=self.Send_Message).start()

                            #self.server.close()

                            self.a = 0

                            self.b = 1

                            self.Server_Ol()

                        if self.message["komut"] == "Bağlantı kur.":

                            #self.capture.release()

                            self.veri = {

                            "durum" : "Tekrar başlatılıyor.",
                            "zaman" : self.t,
                            "error" : "Hata yok.",
                            "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                            }

                            self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                            #threading.Thread(target=self.Server_Ol).start()


                            self.a = 0

                            self.b = 1

                            self.Server_Ol()

                            # threading.Thread(target=self.Send_Message).start()

                            #os.execl(sys.executable, sys.executable, *sys.argv)

                            #self.server.close()

                    except:
                        self.Send_Error(4)

                else:
                    self.Send_Error(4)

            if self.b == 0:

                self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                """ Bind the IP and PORT to the server. """
                self.server.bind(self.ADDR)

                print("[STARTING] server is starting...")

                self.server.listen()
                print(f"[LISTENING] Server is listening on {self.ADDR}")
                self.conn, self.ADDR = self.server.accept()

                self.t = str(datetime.datetime.now())

                if self.a == 0:

                    try:

                        self.a = 1

                        self.msg = self.conn.recv(3096).decode(self.FORMAT)
                        self.message= json.loads(self.msg)
                        pprint(json.loads(self.msg))
                        #for key in json.loads(self.msg):
                            #pprint(json.loads(self.msg)[key])

                        if self.message["komut"] == "Bağlantı kur.":

                            self.veri = {

                            "durum" : "Bağlantı kuruldu.",
                            "zaman" : self.t,
                            "error" : "Hata yok.",
                            "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                            }

                            self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                            # self.Server_Ol()

                        # if self.message["komut"] == "Okudun mu?":
                        #
                        #     #self.capture.release()
                        #
                        #     threading.Thread(target=self.Send_Message).start()
                        #
                        #     self.a = 0
                        #
                        #     self.b = 1
                        #
                        #     self.Server_Ol()
                        #
                        #     #self.Send_Message()
                        #     #self.server.close()


                        # if self.message["komut"] == "Bağlantı kur.":
                        #
                        #     self.capture.release()
                        #
                        #     self.veri = {
                        #
                        #     "durum" : "Tekrar başlatılıyor.",
                        #     "zaman" : self.t,
                        #     "error" : "Hata yok.",
                        #     "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."
                        #
                        #     }
                        #
                        #     self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    except:
                        self.Send_Error(4)

                if self.a == 1:

                    try:

                        self.server.listen()

                        self.conn, self.ADDR = self.server.accept()

                        self.capture = cv2.VideoCapture(0)
                        #self.capture = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L)

                        if not self.capture.isOpened():
                            self.Send_Error(3)

                        else:

                            self.a = 2

                            self.msg = self.conn.recv(3096).decode(self.FORMAT)
                            self.message= json.loads(self.msg)
                            pprint(json.loads(self.msg))
                            #for key in json.loads(self.msg):
                                #pprint(json.loads(self.msg)[key])

                            self.capture.release()

                            if self.message["komut"] == "Kamerayı başlat.":

                                self.veri = {

                                "durum" : "Kamera başlatıldı.",
                                "zaman" : self.t,
                                "error" : "Hata yok.",
                                "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                                }

                                self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                                threading.Thread(target=self.Start_Webcam).start()
                                #self.Start_Webcam()

                                # self.Server_Ol()

                    except:
                        self.Send_Error(4)

                if self.a == 2:

                    try:

                        self.server.listen()

                        self.conn, self.ADDR = self.server.accept()

                        # while True:

                        self.msg = self.conn.recv(3096).decode(self.FORMAT)
                        self.message= json.loads(self.msg)
                        pprint(json.loads(self.msg))
                        #for key in json.loads(self.msg):
                            #pprint(json.loads(self.msg)[key])

                        #self.capture.release()

                        if self.message["komut"] == "Okudun mu?":

                            #self.capture.release()

                            threading.Thread(target=self.Send_Message).start()

                            self.a = 0

                            self.b = 1

                            self.Server_Ol()

                            #self.Send_Message()
                            #self.server.close()

                        if self.message["komut"] == "Bağlantı kur.":

                            #self.capture.release()

                            self.veri = {

                            "durum" : "Tekrar başlatılıyor.",
                            "zaman" : self.t,
                            "error" : "Hata yok.",
                            "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                            }

                            self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                            self.a = 0

                            self.b = 1

                            #threading.Thread(target=self.Server_Ol).start()

                            #self.server.close()

                            self.Server_Ol()

                            # threading.Thread(target=self.Send_Message).start()

                            #os.execl(sys.executable, sys.executable, *sys.argv)

                            #self.server.close()

                    except:
                        self.Send_Error(4)

                else:
                    self.Send_Error(4)

            else:
                self.Send_Error(4)

        except:
            self.Send_Error(3)

if __name__ == '__main__':

    qr_detector = QrDetectorSystem()
    qr_detector.Server_Ol()
