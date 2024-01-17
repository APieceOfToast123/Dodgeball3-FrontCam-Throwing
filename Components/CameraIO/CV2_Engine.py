import cv2

class CV2_engine():
    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # open camer
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G')) # set codec
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920) # set width
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # set height
        self.cap.set(cv2.CAP_PROP_FPS, 60) # set fps

    def read_camera(self):
        success, self.img = self.cap.read()
        return success, self.img[:,int(self.img.shape[1]*1/4):int(self.img.shape[1]*3/4)]
    
    def display_camera(self, img=None):
        if img is None:
            cv2.imshow("Image", self.img)
        else:
            cv2.imshow("Image", img)

    def check_exit(self):
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Image',cv2.WND_PROP_VISIBLE) < 1: # if press q
            return True
        else:
            return False    
    
    def release_camera(self):
        self.cap.release()
        cv2.destroyAllWindows()