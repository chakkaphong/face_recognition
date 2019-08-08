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
from tqdm import tqdm
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

righ_eye_cascade = cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')
left_eye_cascade = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')




class MyApp(QMainWindow):
    def __init__(self, parent=None, camera_index=0, fps=30):
        super().__init__()
        #init camera
        self.capture = cv2.VideoCapture(camera_index)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 352)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.dimensions = self.capture.read()[1].shape[1::-1]
        ''' Connect Database'''
        global mydb
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="root", database="db_faces")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM tb_faces")
        global myresult
        myresult  = mycursor.fetchall()

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
        for x in tqdm(myresult):
            filepath = '../training/{}.jpg'.format(x[1])
            load_img = face_recognition.load_image_file(filepath)
            load_img_encoding = face_recognition.face_encodings(load_img)[0]
            known_face_encodings.append(load_img_encoding)
            known_face_names.append(x[2])
        print(known_face_encodings)
        print(known_face_names)
        state_process = True


    def face_detection(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            #print("Coodinate(xy,wh): ",faces)
            #print("w: ",faces[0,2])
            #print("h: ",faces[0,3])
            #print("found face: ",len(faces))
            eyes = eye_cascade.detectMultiScale(roi_gray)
            Reye = righ_eye_cascade.detectMultiScale(roi_gray)
            Leye = left_eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in Reye:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            for (ex,ey,ew,eh) in Leye:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            if(state_process == True):
                face_locations = face_recognition.face_locations(rgb)
                face_encodings = face_recognition.face_encodings(rgb, face_locations)
                for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    results = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(results)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        print(name)


            """
            for (ex,ey,ew,eh) in eyes:
                if(len(faces) == 1 and len(eyes) == 2):
                    cv2.imwrite('../IMG/captureimg4.jpg', cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            """

    def square(number):
        """The function squares whatever number it is provided."""
        unknow_img = face_recognition.load_image_file('../IMG/rapgod.jpg')
        unkow_ing_encoding = face_recognition.face_encodings(unknow_img)[0]

        for i in range(20):
            filepath = '../training/training{}.jpg'.format(number)
            load_img = face_recognition.load_image_file(filepath)
            load_img_encoding = face_recognition.face_encodings(load_img)[0]
            number+=1
            results = face_recognition.face_distance([load_img_encoding], unkow_ing_encoding)
            proc_id = os.getpid()
            process_name = current_process().name
            print(str(results) + str( proc_id) + str( process_name) + 'matching image: {}'.format(number-1))


    def display_webcame(self, frame):
        
        image = QImage(frame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.pixmapItem.setPixmap(pixmap)

        lbl = QtWidgets.QLabel(self.ui.imgWidgetShow)
        lbl.setPixmap(pixmap)
        lbl.show()


    def insertText(self):
        t = self.ui.label.text()
        #self.ui.lineEdit.setText("ยังโอมมอเทอฟักเกอร์")
        #self.setup_ui()
        #self.loadImage()
    def findFace(self):
        print("ok")

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
