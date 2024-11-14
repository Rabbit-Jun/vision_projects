import cv2 as cv2
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
        self.label.setGeometry(20, 50, 280, 30)

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
        self.rectangles = []
        self.saveButton.setEnabled(False)
        self.label.setText("원하는 영역을 click하여 필터를 적용하세요. \n c:캡쳐    q:종료")
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened(): 
            sys.exit('카메라 연결 실패')

        cv2.namedWindow('Special effect')
        cv2.setMouseCallback('Special effect', self.draw)

        self.imgs = []
        while True:
            ret, frame = self.cap.read()
            if not ret: 
                break

            frame = cv2.flip(frame, 1)  # 좌우 반전 처리
            pick_effect = self.pickCombo.currentIndex()
            special_img = frame.copy()  # 원본 프레임에서 시작

            for rect in self.rectangles:
                x1, y1 = rect[0]
                x2, y2 = rect[1]
                roi = frame[y1:y2, x1:x2]

                # 선택한 효과를 ROI에 적용
                if pick_effect == 1:  # 엠보싱
                    femboss = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
                    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                    gray16 = np.int16(gray)
                    effect_roi = np.uint8(np.clip(cv2.filter2D(gray16, -1, femboss) + 128, 0, 255))
                    effect_roi = cv2.cvtColor(effect_roi, cv2.COLOR_GRAY2BGR)
                elif pick_effect == 2:  # 카툰
                    effect_roi = cv2.stylization(roi, sigma_s=60, sigma_r=0.45)
                elif pick_effect == 3:  # 연필 스케치(명암)
                    _, effect_roi = cv2.pencilSketch(roi, sigma_s=60, sigma_r=0.07, shade_factor=0.02)
                    
                elif pick_effect == 4:  # 연필 스케치(컬러)
                    _, effect_roi = cv2.pencilSketch(roi, sigma_s=60, sigma_r=0.07, shade_factor=0.02)
                    
                elif pick_effect == 5:  # 유화
                    effect_roi = cv2.xphoto.oilPainting(roi, 10, 1, cv2.COLOR_BGR2Lab)
                else:
                    effect_roi = roi

                special_img[y1:y2, x1:x2] = effect_roi

            for rect in self.rectangles:
                cv2.rectangle(special_img, rect[0], rect[1], rect[2], 2)

            cv2.imshow('Special effect', special_img)
            key = cv2.waitKey(1)
            if key == ord("c"):
                self.imgs.append(cv2.resize(special_img, dsize=(400, 300)))  # 일관된 크기로 조정
                if len(self.imgs) == 1:
                    self.stack = self.imgs[0]
                else:
                    self.stack = np.hstack(self.imgs) if len(self.imgs) > 1 else self.stack
                cv2.imshow("Image collection", self.stack)
            elif key == ord("q"):
                self.cap.release()
                cv2.destroyWindow("Special effect")
                break
        if self.stack is not None:
            self.saveButton.setEnabled(True)


    def draw(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.rectangles.append(((x, y), (x + 200, y + 200), (0, 0, 255)))
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.rectangles.append(((x, y), (x + 200, y + 200), (255, 0, 0)))

    def saveFunction(self):
        fname, _ = QFileDialog.getSaveFileName(self, "파일 저장", "./", "Images (*.png *.jpg *.bmp)")
        if fname and self.stack is not None:
            cv2.imwrite(fname, self.stack)

    def quitFunction(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.close()

app = QApplication(sys.argv)
win = VideoSpecialEffect()
win.show()
app.exec()
