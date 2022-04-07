import sys
import time
import cv2
#from __future__ import print_function
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
import time
import os

class QrDetectorSystem:

    def __init__(self):

        self.IP = socket.gethostbyname(socket.gethostname())
        #self.IP = "192.168.102.201"
        #self.IP = "192.168.100.168"
        self.PORT = 4455
        self.ADDR = (self.IP, self.PORT)
        self.FORMAT = "utf-8"
        self.SIZE = 2048
        self.error_message1 = 0
        self.error_message2 = 0
        self.error_message3 = 0
        self.error_message4 = 0
        self.error_message5 = 0
        self.error_message6 = 0
        self.error_message7 = 0
        self.t = 0
        self.hata = 0
        self.capture = 0
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.a = 0

    def Start_Webcam(self):

        # self.capture = cv2.VideoCapture('rtsp://192.168.102.77:554/ch01_sub.264')
        self.capture = cv2.VideoCapture(0)
        time.sleep(1)

        if not self.capture.isOpened():
            self.Send_Error(3)

        else:
            self.Update_Frame()
            # threading.Thread(target=self.Update_Frame).start()

    def decode(self, image):

        # Find barcodes and QR codes
        self.decodedObjects = pyzbar.decode(self.image)
        # Print results
        for self.obj in self.decodedObjects:
            print('Type : ', self.obj.type)
            print('Data : ', self.obj.data, '\n')
        return self.decodedObjects

    def Update_Frame(self):

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        try:

            if self.capture.isOpened() == True:

                while(self.capture.isOpened()):
                    # Capture frame-by-frame
                    ret, self.frame = self.capture.read()

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

                        print(x, y)

                        print('Type : ', self.decodedObject.type)
                        print('Data : ', self.decodedObject.data, '\n')

                        self.barCode = str(self.decodedObject.data)
                        cv2.putText(self.frame, self.barCode, (x, y-20),
                                    self.font, 1, (0, 255, 255), 2, cv2.LINE_AA)

                        self.decodedText = self.barCode[2:-1]

                        print(self.decodedText)

                        self.liste = list()
                        self.liste.append(self.decodedText)
                        print(self.liste[0])

                        if not len(self.liste) == 0:

                            self.capture.release()

                        # self.Send_Message()
                        # threading.Thread(target=self.Send_Message).start()

                        #self.frame = cv2.flip(self.frame, 1)

                        #self.frame = self.frame.rgbSwapped()

                    #cv2.imshow('video', self.frame)

                    key = cv2.waitKey(1)

            else:
                self.Send_Error(3)

        except:
            self.Send_Error(3)

    def Send_Message(self):

        self.t = str(datetime.datetime.now())

        # self.conn, self.ADDR = self.server.accept()

        try:

            if not len(self.liste) == 0:

                print("burada")

                self.veri = {

                "detectedQr" : self.liste[0],
                "zaman" : self.t,
                "error" : "Hata yok.",
                "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                }

                # #dumps the json object into an element
                # json_str = json.dumps(self.veri)
                #
                # #load the json to a string
                # resp = json.loads(json_str)
                #
                # #print the resp
                # print(resp)
                #
                # #extract an element in the response
                # print(resp['zaman'])

                # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                #
                # self.server.connect(self.ADDR)
                #
                # self.server.listen()
                # print(f"[LISTENING] Server is listening on {self.ADDR}")
                # # while True:
                # self.conn, self.ADDR = self.server.accept()

                self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                self.liste.pop(0)
                print(self.liste)

                # self.file = open("qrcode_result.txt", "r")
                # self.data = self.file.read()
                #
                # self.server.send("qrcode_result.txt".encode(self.FORMAT))
                # self.msg = self.server.recv(self.SIZE).decode(self.FORMAT)
                # print(f"[SERVER]: {self.msg}")
                #
                # self.server.send(self.data.encode(self.FORMAT))
                # self.msg = self.server.recv(self.SIZE).decode(self.FORMAT)
                # print(f"[SERVER]: {self.msg}")

                # self.server.close()
                os.execl(sys.executable, sys.executable, *sys.argv)

            else:

                self.veri = {

                "detectedQr" : "Qr okunmadı.",
                "zaman" : self.t,
                "error" : "Hata yok.",
                "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                }

                self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                self.server.close()
                os.execl(sys.executable, sys.executable, *sys.argv)

        except:
            self.Send_Error(7)

    def Send_Error(self, window):

        try:

            self.t = str(datetime.datetime.now())

            if window == 1:
                try:
                    #print("Geçersiz Resim")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Geçersiz Resim",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    #
                    # self.server.connect(self.ADDR)
                    # self.server.listen()
                    # print(f"[LISTENING] Server is listening on {self.ADDR}")
                    # # while True:
                    # self.conn, self.ADDR = self.server.accept()



                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    self.server.close()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 2:
                try:
                    #print("Geçersiz Video")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Geçersiz Video",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    #
                    # self.server.connect(self.ADDR)
                    # self.server.listen()
                    # print(f"[LISTENING] Server is listening on {self.ADDR}")
                    # # while True:
                    # self.conn, self.ADDR = self.server.accept()



                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    self.server.close()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 3:
                try:
                    #print("Webcam bağlı değil ya da Kamera arızalı, bağlantıları kontrol ediniz.")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Webcam bağlı değil ya da Kamera arızalı, bağlantıları kontrol ediniz.",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    #
                    # self.server.connect(self.ADDR)
                    # self.server.listen()
                    # # print(f"[LISTENING] Server is listening on {self.ADDR}")
                    # # while True:
                    # self.conn, self.ADDR = self.server.accept()



                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    self.server.close()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 4:
                try:
                    #print("Fotoğraf kaydedilirken bir sorunla karşılaşıldı veya uygun olmayan uygulama.")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Fotoğraf kaydedilirken bir sorunla karşılaşıldı veya uygun olmayan uygulama.",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    #
                    # self.server.connect(self.ADDR)
                    # self.server.listen()
                    # print(f"[LISTENING] Server is listening on {self.ADDR}")
                    # # while True:
                    # self.conn, self.ADDR = self.server.accept()



                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    self.server.close()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 5:
                try:
                    #print("Qr kod tespit edilemedi.")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Qr kod tespit edilemedi.",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    #
                    # self.server.connect(self.ADDR)
                    # self.server.listen()
                    # print(f"[LISTENING] Server is listening on {self.ADDR}")
                    # # while True:
                    # self.conn, self.ADDR = self.server.accept()



                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    self.server.close()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 6:
                try:
                    #print("Qr kod tespit edilemedi.")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Qr kod tespit edilemedi.",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    #
                    # self.server.connect(self.ADDR)
                    # self.server.listen()
                    # print(f"[LISTENING] Server is listening on {self.ADDR}")
                    # while True:
                    # self.conn, self.ADDR = self.server.accept()



                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    self.server.close()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 7:
                try:
                    #print("Ağ bağlantısı kurulamadı.")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Ağ bağlantısı kurulamadı.",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    #
                    # self.server.connect(self.ADDR)
                    # self.server.listen()
                    # print(f"[LISTENING] Server is listening on {self.ADDR}")
                    # # while True:
                    # self.conn, self.ADDR = self.server.accept()



                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    self.server.close()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 8:
                try:
                    #print("Bu işlem zaten yapıldı.")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Bu işlem zaten yapıldı.",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    #
                    # self.server.connect(self.ADDR)
                    # self.server.listen()
                    # print(f"[LISTENING] Server is listening on {self.ADDR}")
                    # # while True:
                    # self.conn, self.ADDR = self.server.accept()



                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    self.server.close()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 9:
                try:
                    #print("Video bitti/durduruldu.")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Video durduruldu.",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    #
                    # self.server.connect(self.ADDR)
                    # self.server.listen()
                    # print(f"[LISTENING] Server is listening on {self.ADDR}")
                    # # while True:
                    # self.conn, self.ADDR = self.server.accept()



                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    self.server.close()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 10:
                try:
                    #print("Program kapatıldı.")
                    self.veri = {

                    "detectedQr" : "Qr Kodu tespit edilemedi.",
                    "zaman" : self.t,
                    "error" : "Hata: Program kapatıldı",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    #
                    # self.server.connect(self.ADDR)
                    # self.server.listen()
                    # print(f"[LISTENING] Server is listening on {self.ADDR}")
                    # # while True:
                    # self.conn, self.ADDR = self.server.accept()



                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    self.server.close()
                    os.execl(sys.executable, sys.executable, *sys.argv)

                except:
                    self.Send_Error(11)

            if window == 11:
                #print("Program kapatıldı.")
                self.veri = {

                "detectedQr" : "JSON gönderim hatası",
                "zaman" : self.t,
                "error" : "Hata: Program kapatıldı",
                "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                }

                # self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                #
                # self.server.connect(self.ADDR)
                # self.server.listen()
                # print(f"[LISTENING] Server is listening on {self.ADDR}")
                # # while True:
                # self.conn, self.ADDR = self.server.accept()



                self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                self.server.close()
                os.execl(sys.executable, sys.executable, *sys.argv)

        except:
            self.Send_Error(7)

    def Server_Ol(self):

        try:

            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            """ Bind the IP and PORT to the server. """
            self.server.bind(self.ADDR)

            print("[STARTING] server is starting...")
            # self.start()
            # threading.Thread(target=self.start).start()

            self.server.listen()
            print(f"[LISTENING] Server is listening on {self.ADDR}")
            self.conn, self.ADDR = self.server.accept()

            # threading.Thread(target=self.handle_server, args=(self.conn, self.ADDR)).start()
        #     self.handle_server(self.conn, self.ADDR)
        #     # time.sleep(1)
        #
        # except:
        #     self.Send_Error(7)

    # def handle_server(self, conn, addr):

            self.t = str(datetime.datetime.now())

            # self.msg = self.conn.recv(2048).decode(self.FORMAT)
            # pprint(json.loads(self.msg))
            # for key in json.loads(self.msg):
            #     pprint(json.loads(self.msg)[key])

            # print(f"[NEW CONNECTION] {self.ADDR} connected.")

            # try:

            # self.connected = True
            # while self.connected:
                # print(f"[NEW CONNECTION] {self.ADDR} connected.")
                # msg_length = self.server.recv(1024).decode(self.FORMAT)
                # if msg_length:
                #     msg_length = int(msg_length)

                # self.msg = self.conn.recv(2048).decode(self.FORMAT)
                # pprint(json.loads(self.msg))
                # for key in json.loads(self.msg):
                #     pprint(json.loads(self.msg)[key])
                # if self.msg == self.DISCONNECT_MESSAGE:
                #     self.connected = False

            while True:

                if self.a == 0:

                    self.msg = self.conn.recv(2048).decode(self.FORMAT)
                    pprint(json.loads(self.msg))
                    for key in json.loads(self.msg):
                        pprint(json.loads(self.msg)[key])

                    self.veri = {

                    "durum" : "Bağlantı kuruldu.",
                    "zaman" : self.t,
                    "error" : "Hata: Program kapatıldı",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    # threading.Thread(target=self.handle_server, args=(self.conn, self.ADDR)).start()
                    # self.handle_server(self.conn, self.ADDR)
                    self.a = 1
                    # self.Server_Ol()

                    # time.sleep(1)

                if self.a == 1:

                    self.msg = self.conn.recv(2048).decode(self.FORMAT)
                    pprint(json.loads(self.msg))
                    for key in json.loads(self.msg):
                        pprint(json.loads(self.msg)[key])

                    self.veri = {

                    "durum" : "Kamera başlatıldı.",
                    "zaman" : self.t,
                    "error" : "Hata: Program kapatıldı",
                    "properties" : "MEPSAN Petrol Cihazları A.Ş. Akıllı Yazar Kasa Projesi için yazılmıştır."

                    }

                    self.conn.send(bytes(json.dumps(self.veri), 'UTF-8'))

                    self.a = 2

                    threading.Thread(target=self.Start_Webcam).start()

                    # threading.Thread(target=self.handle_server, args=(self.conn, self.ADDR)).start()
                    # threading.Thread(target=self.Server_Ol).start()
                    # self.Server_Ol()

                    # self.Start_Webcam()
                    # time.sleep(1)

                    # self.conn.close()

                if self.a == 2:

                    # self.conn, self.ADDR = self.server.accept()

                    while True:

                        self.msg = self.conn.recv(2048).decode(self.FORMAT)
                        self.message= json.loads(self.msg)
                        pprint(json.loads(self.msg))
                        for key in json.loads(self.msg):
                            pprint(json.loads(self.msg)[key])


                        # #dumps the json object into an element
                        # self.json_str = json.dumps(self.msg)
                        # print(self.json_str)
                        #
                        # #load the json to a string
                        # resp = json.loads(self.json_str)

                        # #print the resp
                        # resp = resp[0:]
                        #
                        # #extract an element in the response
                        #
                        if self.message["komut"] == "Okudun mu?":

                            threading.Thread(target=self.Send_Message).start()

                        # self.a == 2
                        # self.conn.close()
                        # os.execl(sys.executable, sys.executable, *sys.argv)
                        # break

        except:
            self.Send_Error(7)

        # def start(self):
        #
        #     self.server.listen()
        #     print(f"[LISTENING] Server is listening on {self.ADDR}")
        #     self.conn, self.ADDR = self.server.accept()
        #
        #     try:
        #
        #         threading.Thread(target=self.handle_server, args=(self.conn, self.ADDR)).start()
        #         # self.handle_server(self.conn, self.ADDR)
        #         time.sleep(1)
        #
        #     except:
        #         self.Send_Error(7)

if __name__ == '__main__':

    qr_detector = QrDetectorSystem()
    qr_detector.Server_Ol()
