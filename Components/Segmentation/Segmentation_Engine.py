import cv2
import numpy

class segmentation_engine():
    def __init__(self):
        # load the image
        self.bg_image = cv2.imread('Resources/Images/bg.jpg')

        # convert the image from BGR to RGB
        self.bg_image = cv2.cvtColor(self.bg_image, cv2.COLOR_BGR2RGB)

        # # resize the image to fit the webcam
        # self.bg_image = cv2.resize(self.bg_image, (640, 480))

    def calculate_segmentation(self, image_from_Webcam, result_from_mediapipe):
        # make the image transparent         
        condition = numpy.stack((result_from_mediapipe,) * 3, axis=-1) > 0.1
        final_result = numpy.where(condition, image_from_Webcam, self.bg_image)

        return final_result
