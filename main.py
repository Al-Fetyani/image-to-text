import cv2
from PyQt5.QtWidgets import QApplication, QFileDialog, QRubberBand
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import pytesseract
import os
import sys
from PyQt5 import uic
from PyQt5 import QtWidgets
import glob

language_path = 'C:\\Program Files\\Tesseract-OCR\\tessdata\\'
language_path_list = glob.glob(language_path + '*.traineddata')
language_list = [os.path.splitext(os.path.basename(path))[0] for path in language_path_list]




class APP(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi("gui.ui", self)
        self.image = None

        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

        self.pushButton.clicked.connect(self.open_image)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.ui.label_2.setMouseTracking(True)
        self.ui.label_2.installEventFilter(self)
        self.ui.label_2.setAlignment(Qt.AlignCenter)

        self.language = 'eng'
        self.comboBox.addItems(language_list)
        self.comboBox.currentIndexChanged['QString'].connect(self.language_change)
        self.comboBox.setCurrentIndex(language_list.index(self.language))

    def language_change(self, value):
        self.language = value

    def open_image(self):
        self.textEdit.clear()
        filename, _ = QFileDialog.getOpenFileName(self, 'Open file', './')
        if filename:
            self.image = cv2.imread(filename)
            self.display_image()
            self.perform_ocr()

    def display_image(self):
        if self.image is not None:
            frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            self.ui.label_2.setPixmap(QPixmap.fromImage(image))
        else:
            QtWidgets.QMessageBox.information(self, "Error", "Error loading image")

    def perform_ocr(self):
        text = pytesseract.image_to_string(self.image, lang=self.language)
        self.textEdit.setText(text)

       
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = APP()
    window.show()
    sys.exit(app.exec_())
