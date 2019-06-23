import cv2
from PyQt5 import QtGui, QtWidgets

if __name__ == '__main__':
    import sys
    src = cv2.imread('alex-lacamoire.png')
    src = src[:,:,::-1]
    h, w, ch = src.shape
    bytesPerLine = ch * w
    qImg = QtGui.QImage(src.data.tobytes(), w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
    # Or
    # qImg = QtGui.QImage(bytes(src.data), w, h, bytesPerLine, QtGui.QImage.Format_RGB888)
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QLabel()
    w.setPixmap(QtGui.QPixmap.fromImage(qImg))
    w.show()
    sys.exit(app.exec_())