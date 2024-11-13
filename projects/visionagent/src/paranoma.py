from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor
import cv2
import numpy as np
import winsound
import sys

class Panorama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("파노라마 영상")
        self.setGeometry(200, 200, 1000, 200)

        collectButton = QPushButton("촬영", self)
        self.stitchButton = QPushButton("파노라마", self)
        self.textButton = QPushButton("글자 입력", self)
        self.drawButton = QPushButton("그리기", self)
        self.stopDrawButton = QPushButton("그리기 해제", self)
        self.colorButton = QPushButton("색 변경", self)
        self.undoButton = QPushButton("되돌리기", self)
        self.saveButton = QPushButton("저장", self)
        quitButton = QPushButton("나가기", self)
        self.label = QLabel("환영합니다!", self)

        collectButton.setGeometry(10, 25, 100, 30)
        self.stitchButton.setGeometry(110, 25, 100, 30)
        self.textButton.setGeometry(210, 25, 100, 30)
        self.drawButton.setGeometry(310, 25, 100, 30)
        self.stopDrawButton.setGeometry(410, 25, 100, 30)
        self.colorButton.setGeometry(510, 25, 100, 30)
        self.undoButton.setGeometry(610, 25, 100, 30)
        self.saveButton.setGeometry(710, 25, 100, 30)
        quitButton.setGeometry(810, 25, 100, 30)
        self.label.setGeometry(10, 70, 600, 170)

        self.stitchButton.setEnabled(False)
        self.textButton.setEnabled(False)
        self.drawButton.setEnabled(False)
        self.stopDrawButton.setEnabled(False)
        self.colorButton.setEnabled(False)
        self.undoButton.setEnabled(False)
        self.saveButton.setEnabled(False)

        collectButton.clicked.connect(self.collectFunction)
        self.stitchButton.clicked.connect(self.stitchFunction)
        self.textButton.clicked.connect(self.textFunction)
        self.drawButton.clicked.connect(self.drawFunction)
        self.stopDrawButton.clicked.connect(self.stopDrawingFunction)
        self.colorButton.clicked.connect(self.changeColorFunction)
        self.undoButton.clicked.connect(self.undoFunction)
        self.saveButton.clicked.connect(self.saveFunction)
        quitButton.clicked.connect(self.quitFunction)

        self.rect_start = None
        self.rect_end = None
        self.text_entered = False
        self.drawing = False
        self.brush_size = 5
        self.line_color = (255, 0, 0)
        self.history = []

    def collectFunction(self):
        self.stitchButton.setEnabled(False)
        self.textButton.setEnabled(False)
        self.drawButton.setEnabled(False)
        self.colorButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.label.setText("c를 여러 번 눌러 수집하고 끝나면 q를 눌러 비디오를 끕니다.")

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            sys.exit("카메라 연결 실패")

        self.imgs = []
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            cv2.imshow("video display", frame)

            key = cv2.waitKey(1)
            if key == ord("c"):
                self.imgs.append(frame)
            elif key == ord("q"):
                self.cap.release()
                cv2.destroyWindow("video display")
                break

        if len(self.imgs) >= 2:
            self.stitchButton.setEnabled(True)
            self.saveButton.setEnabled(True)

    def stitchFunction(self):
        stitcher = cv2.Stitcher_create()
        status, self.img_stitched = stitcher.stitch(self.imgs)
        if status == cv2.STITCHER_OK:
            self.img_display = self.img_stitched.copy()
            self.history.append(self.img_display.copy())  # Save to history
            cv2.imshow("Image stitched panorama", self.img_display)
            cv2.setMouseCallback("Image stitched panorama", self.draw)
            self.textButton.setEnabled(True)
            self.drawButton.setEnabled(True)
            self.colorButton.setEnabled(True)
            self.undoButton.setEnabled(True)
        else:
            winsound.Beep(3000, 500)
            self.label.setText("파노라마 제작에 실패했습니다. 다시 시도하세요.")

    def textFunction(self):
        if not self.rect_start or not self.rect_end:
            self.label.setText("사각형을 먼저 그려주세요")
            return

        rect_width = abs(self.rect_end[0] - self.rect_start[0])
        rect_height = abs(self.rect_end[1] - self.rect_start[1])
        rect_center_x = (self.rect_start[0] + self.rect_end[0]) // 2
        rect_center_y = (self.rect_start[1] + self.rect_end[1]) // 2

        text, ok = QInputDialog.getText(self, "글자 입력", "사각형에 넣을 글자를 입력하세요:")
        if ok and text:
            font_scale = 1
            while True:
                (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 2)
                if text_width > rect_width or text_height > rect_height:
                    font_scale -= 0.1
                    break
                font_scale += 0.1

            text_x = rect_center_x - text_width // 2
            text_y = rect_center_y + text_height // 2

            self.history.append(self.img_display.copy())  # Save to history before change
            cv2.putText(self.img_display, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, self.line_color, 2)
            cv2.putText(self.img_stitched, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, self.line_color, 2)
            cv2.imshow("Image stitched panorama", self.img_display)
            self.text_entered = True

    def drawFunction(self):
        self.drawing = True
        self.stopDrawButton.setEnabled(True)
        self.label.setText("왼쪽 버튼으로 그림을 그리세요.")
        self.history.append(self.img_display.copy())  # Save to history before drawing

        def painting(event, x, y, flags, param):
            if self.drawing and (event == cv2.EVENT_LBUTTONDOWN or (event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON)):
                cv2.circle(self.img_display, (x, y), self.brush_size, self.line_color, -1)
                cv2.circle(self.img_stitched, (x, y), self.brush_size, self.line_color, -1)
                cv2.imshow("Image stitched panorama", self.img_display)

        cv2.setMouseCallback("Image stitched panorama", painting)

    def stopDrawingFunction(self):
        self.drawing = False
        self.stopDrawButton.setEnabled(False)
        self.label.setText("그리기가 해제되었습니다. 사각형을 다시 그릴 수 있습니다.")
        cv2.setMouseCallback("Image stitched panorama", self.draw)

    def draw(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.rect_start = (x, y)
        elif event == cv2.EVENT_RBUTTONDOWN and self.rect_start:
            self.rect_end = (x, y)
            self.img_display = self.img_stitched.copy()
            cv2.rectangle(self.img_display, self.rect_start, self.rect_end, (0, 0, 255), 2)
            cv2.imshow("Image stitched panorama", self.img_display)
            self.text_entered = False

    def changeColorFunction(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.line_color = (color.blue(), color.green(), color.red())

    def undoFunction(self):
        if self.history:
            self.img_display = self.history.pop()
            self.img_stitched = self.img_display.copy()
            cv2.imshow("Image stitched panorama", self.img_display)

    def saveFunction(self):
        fname = QFileDialog.getSaveFileName(self, "파일 저장", "./data")
        if fname[0]:
            cv2.imwrite(fname[0], self.img_stitched)

    def quitFunction(self):
        if hasattr(self, 'cap'):
            self.cap.release()
        cv2.destroyAllWindows()
        self.close()

app = QApplication(sys.argv)
win = Panorama()
win.show()
app.exec()
