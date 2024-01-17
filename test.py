import cv2
import numpy as np

image_path = "C:/Users/16979/Desktop/CPS 4893 AI/Dodgeball3-FrontCam-Throwing/Program/Resources/Images/bg.jpg"
image = cv2.imread(image_path)

if image is None:
    print("Image not found")
else:
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) # open camer

    while True:
        ret, frame = cap.read()
    
        if not ret:
            break

        frame = cv2.resize(frame,(image.shape[1], image.shape[0]))

        overlay = image.copy()

        overlay[:, :image.shape[1] // 2 ] = frame[:, :image.shape[1] // 2 ]

        result = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)

        cv2.imshow("result", result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()