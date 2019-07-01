import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dialog import Ui_MainWindow
import cv2 as cv2
import numpy as np
import face_recognition

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

    def face_detection(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            print("Coodinate(xy,wh): ",faces)
            print("w: ",faces[0,2])
            print("h: ",faces[0,3])
            print("found face: ",len(faces))
            eyes = eye_cascade.detectMultiScale(roi_gray)
            Reye = righ_eye_cascade.detectMultiScale(roi_gray)
            Leye = left_eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in Reye:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            for (ex,ey,ew,eh) in Leye:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            """\
            for (ex,ey,ew,eh) in eyes:
                if(len(faces) == 1 and len(eyes) == 2):
                    cv2.imwrite('../IMG/captureimg4.jpg', cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR))
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            """


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

    
    def loadImage(self):
        self.pam_image = face_recognition.load_image_file("../IMG/pam_1.jpg")
        self.obama_image = face_recognition.load_image_file("../IMG/obama_1.jpg")
        self.na_kom_image = face_recognition.load_image_file("../IMG/kom_1.jpg")
        self.unknown_image = face_recognition.load_image_file("../IMG/obama_test.jpg")
        try:
            pam_face_encoding = face_recognition.face_encodings(self.pam_image)[0]
            obama_face_encoding = face_recognition.face_encodings(self.obama_image)[0]
            na_kom_encoding = face_recognition.face_encodings(self.na_kom_image)[0]
            unknown_face_encoding = face_recognition.face_encodings(self.unknown_image)[0]
        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
            quit()
        
        known_faces = [
            pam_face_encoding,
            obama_face_encoding,
            na_kom_encoding
        ]
        results = face_recognition.compare_faces(known_faces, unknown_face_encoding)
        print("Is the unknown face a picture of ป๋อมแป๋ม? {}".format(results[0]))
        print("Is the unknown face a picture of โอบาม่า? {}".format(results[1]))
        print("Is the unknown face a picture of น้าค่อม? {}".format(results[2]))
        print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
        self.ui.lineEdit.setText("ยังโอมมอเทอฟักเกอร์ {}".format(results[1]))


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