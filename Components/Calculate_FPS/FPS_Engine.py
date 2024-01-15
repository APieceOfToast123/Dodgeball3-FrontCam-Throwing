import cv2
import time

class FPS_engine():
    def __init__(self):
        self.pTime = 0
        self.fps = 0

    def calculate_FPS(self):
        cTime = time.time()
        try:
            self.fps = 1/(cTime-self.pTime)
            self.pTime = cTime
        except:
            pass

    def display_FPS(self, img):
        cv2.putText(img, str(int(self.fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 255), 5)