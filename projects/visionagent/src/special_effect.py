import cv2 as cv
import numpy as np
from PyQt6.QtWidgets import *
import sys

class VideoSpecialEffect(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('비디오 특수 효과')
        self.setGeometry(200, 200, 400, 100)

        videoButton = QPushButton('비디오 시작', self)
        self.pickCombo = QComboBox(self)
        # Added '기본' as the first option
        self.pickCombo.addItems(['기본', '엠보싱', '카툰', '연필 스케치(명암)', '연필 스케치(컬러)', '유화'])
        quitButton = QPushButton('나가기', self)

        videoButton.setGeometry(10, 10, 140, 30)
        self.pickCombo.setGeometry(150, 10, 110, 30)
        quitButton.setGeometry(280, 10, 100, 30)

        videoButton.clicked.connect(self.videoSpecialEffectFunction)
        quitButton.clicked.connect(self.quitFunction)
        
        self.rectangles = []  # List to store drawn rectangles

    def videoSpecialEffectFunction(self):
        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        if not self.cap.isOpened(): sys.exit('카메라 연결 실패')

        cv.namedWindow('Special effect')
        cv.setMouseCallback('Special effect', self.draw)

        while True:
            ret, frame = self.cap.read()
            if not ret: break

            pick_effect = self.pickCombo.currentIndex()
            if pick_effect == 1:  # 엠보싱
                femboss = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                gray16 = np.int16(gray)
                special_img = np.uint8(np.clip(cv.filter2D(gray16, -1, femboss) + 128, 0, 255))
            elif pick_effect == 2:  # 카툰
                special_img = cv.stylization(frame, sigma_s=60, sigma_r=0.45)
            elif pick_effect == 3:  # 연필 스케치(명암)
                special_img, _ = cv.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.02)
            elif pick_effect == 4:  # 연필 스케치(컬러)
                _, special_img = cv.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.02)
            elif pick_effect == 5:  # 유화
                special_img = cv.xphoto.oilPainting(frame, 10, 1, cv.COLOR_BGR2Lab)
            else:  # 기본 (No special effect)
                special_img = frame

            # Draw rectangles from the list
            for rect in self.rectangles:
                cv.rectangle(special_img, rect[0], rect[1], rect[2], 2)

            cv.imshow('Special effect', special_img)
            if cv.waitKey(1) == ord('q'):  # Press 'q' to exit
                break

    def draw(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            # Draw a red rectangle and store it in the list
            self.rectangles.append(((x, y), (x + 200, y + 200), (0, 0, 255)))
        elif event == cv.EVENT_RBUTTONDOWN:
            # Draw a blue rectangle and store it in the list
            self.rectangles.append(((x, y), (x + 200, y + 200), (255, 0, 0)))

    def quitFunction(self):
        self.cap.release()
        cv.destroyAllWindows()
        self.close()

app = QApplication(sys.argv)
win = VideoSpecialEffect()
win.show()
app.exec()
