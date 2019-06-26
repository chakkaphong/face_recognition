import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dialog import Ui_MainWindow
import cv2 as cv2
import numpy as np
import face_recognition


class MyApp(QMainWindow):
    def __init__(self, parent=None, camera_index=0, fps=30):
        super().__init__()
        self.capture = cv2.VideoCapture(camera_index)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 511)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 281)
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
        obama_image = face_recognition.load_image_file("../IMG/obama_1.jpg")
        obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

        # Load a second sample picture and learn how to recognize it.
        biden_image = face_recognition.load_image_file("../IMG/my_1.jpg")
        biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

        # Create arrays of known face encodings and their names
        known_face_encodings = [
            obama_face_encoding,
            biden_face_encoding
        ]
        known_face_names = [
            "Barack Obama",
            "Joe Biden"
        ]
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


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
        self.loadImage()
    
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