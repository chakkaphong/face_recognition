import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dialog import Ui_MainWindow
import cv2 as cv2
import numpy as np
import face_recognition
import threading
import mysql.connector

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

righ_eye_cascade = cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')
left_eye_cascade = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')


class MyApp(QMainWindow):
    def __init__(self, parent=None, camera_index=0, fps=30):
        super().__init__()
        #init camera
        global mydb
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="db_faces")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM tb_faces")
        global myresult
        myresult  = mycursor.fetchall()
        #QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Events
        #>pyuic5 MywindowClass.ui > dialog.py
        t1 = threading.Thread(target = self.loadImage , args = ())
        t1.start()
        self.ui.pushButton.clicked.connect(self.face_recog)

    
    def loadImage(self):
        global known_face_encodings 
        known_face_encodings = []
        global known_face_names 
        known_face_names = []
        for x in myresult:
            filepath = '../training/{}.jpg'.format(x[1])
            load_img = face_recognition.load_image_file(filepath)
            load_img_encoding = face_recognition.face_encodings(load_img)[0]
            known_face_encodings.append(load_img_encoding)
            known_face_names.append(x[2])
        print(known_face_encodings)
        print(known_face_names)
        
    
    def face_recog(self):
        matches = face_recognition.compare_faces(known_face_encodings, known_face_encodings[15])
        results = face_recognition.face_distance(known_face_encodings, known_face_encodings[15])
        best_match_index = np.argmin(results)
        print(results)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            print(name)
        




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    app.exec_()
