import cv2 as cv
import numpy as np
from PyQt6.QtWidgets import *
import sys

class VideoSpecialEffect(QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QLabel("환영합니다!", self)
        self.setWindowTitle('비디오 특수 효과')
        self.saveButton = QPushButton("저장", self)
        self.setGeometry(200, 200, 400, 100)
        self.saveButton.setGeometry(280, 50, 100, 30)
        self.saveButton.setEnabled(False)
        self.saveButton.clicked.connect(self.saveFunction)
        self.label.setGeometry(10, 70, 600, 170)

        videoButton = QPushButton('비디오 시작', self)
        self.pickCombo = QComboBox(self)
        self.pickCombo.addItems(['기본', '엠보싱', '카툰', '연필 스케치(명암)', '연필 스케치(컬러)', '유화'])
        quitButton = QPushButton('나가기', self)

        videoButton.setGeometry(10, 10, 140, 30)
        self.pickCombo.setGeometry(150, 10, 110, 30)
        quitButton.setGeometry(280, 10, 100, 30)

        videoButton.clicked.connect(self.videoSpecialEffectFunction)
        quitButton.clicked.connect(self.quitFunction)
        
        self.rectangles = []  # List to store drawn rectangles
        self.stack = None
        
    def videoSpecialEffectFunction(self):
        self.saveButton.setEnabled(False)
        self.label.setText("c를 여러 번 눌러 수집하고 끝나면 q를 눌러 비디오를 끕니다.")
        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        if not self.cap.isOpened(): 
            sys.exit('카메라 연결 실패')

        cv.namedWindow('Special effect')
        cv.setMouseCallback('Special effect', self.draw)

        self.imgs = []
        while True:
            ret, frame = self.cap.read()
            if not ret: 
                break

            pick_effect = self.pickCombo.currentIndex()
            special_img = frame.copy()  # Start with the original frame

            for rect in self.rectangles:
                x1, y1 = rect[0]
                x2, y2 = rect[1]
                roi = frame[y1:y2, x1:x2]

                # Apply the selected effect on the ROI
                if pick_effect == 1:  # 엠보싱
                    femboss = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
                    gray = cv.cvtColor(roi, cv.COLOR_BGR2GRAY)
                    gray16 = np.int16(gray)
                    effect_roi = np.uint8(np.clip(cv.filter2D(gray16, -1, femboss) + 128, 0, 255))
                    effect_roi = cv.cvtColor(effect_roi, cv.COLOR_GRAY2BGR)
                elif pick_effect == 2:  # 카툰
                    effect_roi = cv.stylization(roi, sigma_s=60, sigma_r=0.45)
                elif pick_effect == 3:  # 연필 스케치(명암)
                    effect_roi, _ = cv.pencilSketch(roi, sigma_s=60, sigma_r=0.07, shade_factor=0.02)
                elif pick_effect == 4:  # 연필 스케치(컬러)
                    _, effect_roi = cv.pencilSketch(roi, sigma_s=60, sigma_r=0.07, shade_factor=0.02)
                elif pick_effect == 5:  # 유화
                    effect_roi = cv.xphoto.oilPainting(roi, 10, 1, cv.COLOR_BGR2Lab)
                else:
                    effect_roi = roi

                special_img[y1:y2, x1:x2] = effect_roi

            for rect in self.rectangles:
                cv.rectangle(special_img, rect[0], rect[1], rect[2], 2)

            cv.imshow('Special effect', special_img)
            key = cv.waitKey(1)
            if key == ord("c"):
                self.imgs.append(cv.resize(special_img, dsize=(400, 300)))  # Resize for consistent dimensions
                if len(self.imgs) == 1:
                    self.stack = self.imgs[0]
                else:
                    self.stack = np.hstack(self.imgs) if len(self.imgs) > 1 else self.stack
                cv.imshow("Image collection", self.stack)
            elif key == ord("q"):
                self.cap.release()
                cv.destroyWindow("Special effect")
                break
        if self.stack is not None:
            self.saveButton.setEnabled(True)

    def draw(self, event, x, y, flags, param):
        if event == cv.EVENT_LBUTTONDOWN:
            self.rectangles.append(((x, y), (x + 200, y + 200), (0, 0, 255)))
        elif event == cv.EVENT_RBUTTONDOWN:
            self.rectangles.append(((x, y), (x + 200, y + 200), (255, 0, 0)))

    def saveFunction(self):
        fname, _ = QFileDialog.getSaveFileName(self, "파일 저장", "./data")
        if fname and self.stack is not None:
            cv.imwrite(fname, self.stack)

    def quitFunction(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        cv.destroyAllWindows()
        self.close()

app = QApplication(sys.argv)
win = VideoSpecialEffect()
win.show()
app.exec()
