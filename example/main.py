import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dialog import Ui_MainWindow
import cv2 as cv2
import numpy as np
import face_recognition
import threading
from multiprocessing import Process, current_process
import mysql.connector
from tqdm import tqdm, trange
import pickle
import datetime 
from sklearn import svm

eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

righ_eye_cascade = cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')
left_eye_cascade = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')



class MyApp(QMainWindow):
    def __init__(self, parent=None, camera_index=0, fps=30):
        super().__init__()
        global state_capture         
        state_capture = False
        global arr_employid
        self.arr_employid = None
        #init camera
        self.capture = cv2.VideoCapture(camera_index)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 352)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.dimensions = self.capture.read()[1].shape[1::-1]
        ''' Global id '''

        
        ''' Connect Database'''
        global mydb
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="db_nrod", port="3306")
        
 

        '''multi Threading'''
        t1 = threading.Thread(target = self.loadImage , args = ())
        t1.start()

        ''' Set VideoCapture'''
        scene = QGraphicsScene(self)
        pixmap = QPixmap(*self.dimensions)
        self.pixmapItem = scene.addPixmap(pixmap)
        timer = QTimer(self)
        timer.setInterval(int(1000/fps))
        timer.timeout.connect(self.get_frame)
        timer.start()

        #QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Events
        #>pyuic5 MywindowClass.ui > dialog.py
        self.ui.pushButton.clicked.connect(self.insertText)


    def get_frame(self):
        _, frame = self.capture.read()
        #face and eye detec

        self.face_detection(frame)
        #add camera to label
        self.display_webcame(frame)

    def loadImage(self):
        global known_face_encodings 
        known_face_encodings = []
        global known_face_names 
        known_face_names = []
        global state_process
        state_process = False



        pathKnownImg = "encodings.pickle"
        data = pickle.loads(open(pathKnownImg, "rb").read())
        known_face_encodings = data["encodings"]
        known_face_names = data["names"]
    
        #clf = svm.SVC(gamma='scale')
        #clf.fit(known_face_encodings,known_face_names)
        state_process = True


    #Machine Leaing wiht SVM
    def learnImage(self):
        clf = svm.SVC(gamma='scale')
        clf.fit(encodings,names)
        

    def updateProgressbar(self, n):
        con = int(n)
        print(con)
        if con >= 50:
            self.ui.progressBar.setValue(50)

    def face_detection(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if(state_process == True):
            face_locations = face_recognition.face_locations(rgb)
            temp = 0
            best_index = 0
            #cv2.imshow('ssss',face_encodings)
            if len(face_locations) == 1:
                face_encodings = face_recognition.face_encodings(rgb, face_locations)
            elif len(face_locations) >= 2:
                for i in range(len(face_locations)):
                    sum_of_face = face_locations[i][0] + face_locations[i][1] + face_locations[i][2] + face_locations[i][3]
                    #print('round:{} | sum:{}'.format(i, sum_of_face))
                    if sum_of_face > temp:
                        temp = sum_of_face
                        best_index = i
                #print(best_index)
                face_encodings = face_recognition.face_encodings(rgb, [face_locations[best_index]])
                temp = 0
                best_index = 0   
        try:
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                #pre_name = clf.predict(face_encoding)
                #print('Pre:{}'.format(pre_name))

                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.38)
                results = face_recognition.face_distance(known_face_encodings, face_encoding)
                print('{}'.format(face_locations))
                #print('Matching per: {}'.format(results))
                face_image = frame[top:bottom, left:right]
                cv2.imshow('hog',face_image)
                #name = "Unknown"
                if True in matches:
                    matchedIdxs = [i for (i,b) in enumerate(matches) if b]
                    counts = {}
                    for i in matchedIdxs:
                        name = known_face_names[i]
                        counts[name] = counts.get(name, 0) + 1
                        name = max(counts, key=counts.get)
                        #print(name)
                        id_spilt = name.split("_")
                        person_id = id_spilt[0]
                        self.GetEmpolyInfo(person_id)
                        self.checkName(person_id)        
                        #mycursor.execute("SELECT * FROM  tb_meeting_room WHERE meet_empID = {}".format(person_id))
                        #res = mycursor.fetchall()  
                        #print('Res:{}', res) 
                                
                   
                        

        except:
            print("Can't Found face in came")
    
    def checkName(self, person_id):
        a = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        mycursor = mydb.cursor()
        sql = "INSERT INTO tb_meeting_room (meet_id, meet_empID, meet_empTime) VALUES ({}, {}, '{}')".format(2, person_id, a)
        mycursor.execute(sql)
        mydb.commit()


    def GetEmpolyInfo(self, person_id):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM  nrod_emp WHERE emp_id = {}".format(person_id))
        global myresult
        myresult  = mycursor.fetchall()
        print(myresult)
        Spiltshot = myresult[0][2].split(" ")
        name_spilt = Spiltshot[0]
        lname_spilt = Spiltshot[1]
        self.ui.line_num.setText(myresult[0][1])
        self.ui.line_name.setText(name_spilt)
        self.ui.line_lname.setText(lname_spilt)
        self.ui.line_position.setText(myresult[0][4])
        self.ui.line_under.setText(myresult[0][5])


    def display_webcame(self, frame):
        image = QImage(frame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.pixmapItem.setPixmap(pixmap)


        lbl = QtWidgets.QLabel(self.ui.imgWidgetShow)
        lbl.setPixmap(pixmap)
        lbl.show()


    def insertText(self):
        t = self.ui.label.text()
        #self.ui.lineEdit.setText("")
        #self.setup_ui()
        #self.loadImage()


    def setup_ui(self):   
        src = cv2.imread('../IMG/my_1.jpg')
        src = src[:,:,::-1]
        h, w, ch = src.shape
        bytesPerLine = ch * w
        qImg = QtGui.QImage(src.data.tobytes(), w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
        pp = QtGui.QPixmap.fromImage(qImg)
        lbl = QtWidgets.QLabel(self.ui.imgWidgetShow)
        lbl.setPixmap(pp)
        lbl.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    app.exec_()
