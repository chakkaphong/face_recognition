import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from dialog import Ui_MainWindow
import cv2 as cv2
import face_recognition


class MyApp(QMainWindow):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Events
        #>pyuic5 MywindowClass.ui > dialog.py
        self.ui.pushButton.clicked.connect(self.insertText)
     
    def insertText(self):
        t = self.ui.label.text()
        #self.ui.lineEdit.setText("ยังโอมมอเทอฟักเกอร์")
        self.setup_ui()
        self.loadImage()
    
    def loadImage(self):
        self.pam_image = face_recognition.load_image_file("IMG/pam_1.jpg")
        self.obama_image = face_recognition.load_image_file("IMG/obama_1.jpg")
        self.na_kom_image = face_recognition.load_image_file("IMG/kom_1.jpg")
        self.unknown_image = face_recognition.load_image_file("IMG/obama_test.jpg")
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
        src = cv2.imread('alex-lacamoire.png')
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
