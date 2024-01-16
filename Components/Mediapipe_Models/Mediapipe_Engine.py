import mediapipe
import cv2
import numpy as np
import pygame
class mediapipe_holistic_engine():
    def __init__(self):
        self.AI_model = mediapipe.solutions.holistic
        self.AI_model_initialized = self.AI_model.Holistic(
                                    model_complexity = 1,
                                    refine_face_landmarks = True,
                                    min_detection_confidence = 0.5, 
                                    min_tracking_confidence = 0.5,
                                    enable_segmentation = True,
                                    smooth_segmentation = True
                                    )
        self.mp_drawing = mediapipe.solutions.drawing_utils
        self.mp_drawing_styles = mediapipe.solutions.drawing_styles

    def process_image(self, img):
        self.results = self.AI_model_initialized.process(img)
        
        if self.results.pose_landmarks:
            self.pose_detected = True
            self.Pose_Pixel_Landmark_list = self.results.pose_landmarks
            self.Pose_Pixel_Landmark = self.results.pose_landmarks.landmark
            self.Pose_World_Landmark = self.results.pose_world_landmarks.landmark
        # else:
        #     self.pose_detected = False
        #     cv2.putText(img, "No pose detected", (10, 110), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        
        # if self.results.face_landmarks:
        #     self.face_detected = True
        #     self.Face_Pixel_Landmark = self.results.face_landmarks.landmark
        # else:
        #     self.face_detected = False
        #     cv2.putText(img, "No face detected", (10, 180), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        # if self.results.left_hand_landmarks:
        #     self.left_hand_detected = True
        #     self.Left_Hand_Pixel_Landmark = self.results.left_hand_landmarks.landmark
        # else:
        #     self.left_hand_detected = False
        #     cv2.putText(img, "No left hand detected", (10, 250), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
        
        # if self.results.right_hand_landmarks:
        #     self.right_hand_detected = True
        #     self.Right_Hand_Pixel_Landmark = self.results.right_hand_landmarks.landmark
        # else:
        #     self.right_hand_detected = False
        #     cv2.putText(img, "No right hand detected", (10, 320), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    def draw_all_landmark_drawing_utils(self, img):
        if self.pose_detected:
            self.mp_drawing.draw_landmarks(
                img,
                self.results.pose_landmarks[11,12],
                self.AI_model.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles
                .get_default_pose_landmarks_style())
    


class mediapipe_pose_engine():
    def __init__(self):
        self.AI_model = mediapipe.solutions.pose
        self.AI_model_initialized = self.AI_model.Pose(
                                    model_complexity = 1,
                                    min_detection_confidence = 0.8, 
                                    min_tracking_confidence = 0.8,
                                    enable_segmentation = False,
                                    smooth_segmentation = False
                                    )
        self.mp_drawing = mediapipe.solutions.drawing_utils
        self.mp_drawing_styles = mediapipe.solutions.drawing_styles
        self.hint =None
        self.shoulder_angle = 0
        self.prev_angle= 0
        self.max_level = 0
    
    def process_image(self, img):
        try:
            results = self.AI_model_initialized.process(img)
            if results.pose_landmarks:
                self.Pixel_Landmark_list = results.pose_landmarks
                self.Pixel_Landmark = results.pose_landmarks.landmark
                self.World_Landmark = results.pose_world_landmarks.landmark
            else:
                cv2.putText(img, "No pose detected", (10, 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        except:
            pass
        """
        self.Pose_Landmark.landmark[0]
        x = self.Pose_Landmark.landmark[0].x
        Output Example of Pose_Landmark.landmark[0]:
            x = 0.5 (0.0 ~ 1.0)
            pixel_x = x * image_width (e.g 1920x1080)
            (pixel_x, pixel_y) = (960, 540)
        y = self.Pose_Landmark.landmark[0].y
        visibility = self.Pose_Landmark.landmark[0].visibility
        """
        
        """
        self.World_Landmark.landmark[0]
        x = self.World_Landmark.landmark[0].x
        Output Example of World_Landmark.landmark[0]:
            x = 0.5 (0.0 ~ 1.0)
            center_meters_x = x * 100 (e.g 100cm = 1m)
        y = self.World_Landmark.landmark[0].y
        z = self.World_Landmark.landmark[0].z
        visibility = self.World_Landmark.landmark[0].visibility
        """
    def expand_landmark(self):
        # self.Nose_x, self.Nose_y = self.Pixel_Landmark[0].x, self.Pixel_Landmark[0].y
        # self.Left_Eye_Inner_x, self.Left_Eye_Inner_y = self.Pixel_Landmark[1].x, self.Pixel_Landmark[1].y
        # self.Left_Eye_x, self.Left_Eye_y = self.Pixel_Landmark[2].x, self.Pixel_Landmark[2].y
        # self.Left_Eye_Outer_x, self.Left_Eye_Outer_y = self.Pixel_Landmark[3].x, self.Pixel_Landmark[3].y
        # self.Right_Eye_Inner_x, self.Right_Eye_Inner_y = self.Pixel_Landmark[4].x, self.Pixel_Landmark[4].y
        # self.Right_Eye_x, self.Right_Eye_y = self.Pixel_Landmark[5].x, self.Pixel_Landmark[5].y
        # self.Right_Eye_Outer_x, self.Right_Eye_Outer_y = self.Pixel_Landmark[6].x, self.Pixel_Landmark[6].y
        # self.Left_Ear_x, self.Left_Ear_y = self.Pixel_Landmark[7].x, self.Pixel_Landmark[7].y
        # self.Right_Ear_x, self.Right_Ear_y = self.Pixel_Landmark[8].x, self.Pixel_Landmark[8].y
        # self.Mouth_Left_x, self.Mouth_Left_y = self.Pixel_Landmark[9].x, self.Pixel_Landmark[9].y
        # self.Mouth_Right_x, self.Mouth_Right_y = self.Pixel_Landmark[10].x, self.Pixel_Landmark[10].y
        self.Left_Shoulder_x, self.Left_Shoulder_y ,self.Left_Shoulder_z = self.Pixel_Landmark[11].x, self.Pixel_Landmark[11].y, self.Pixel_Landmark[11].z
        self.Right_Shoulder_x, self.Right_Shoulder_y ,self.Right_Shoulder_z = self.Pixel_Landmark[12].x, self.Pixel_Landmark[12].y, self.Pixel_Landmark[12].z
        # self.Left_Elbow_x, self.Left_Elbow_y ,self.Left_Elbow_z= self.Pixel_Landmark[13].x, self.Pixel_Landmark[13].y,self.Pixel_Landmark[13].z
        # self.Right_Elbow_x, self.Right_Elbow_y = self.Pixel_Landmark[14].x, self.Pixel_Landmark[14].y
        # self.Left_Wrist_x, self.Left_Wrist_y = self.Pixel_Landmark[15].x, self.Pixel_Landmark[15].y
        # self.Right_Wrist_x, self.Right_Wrist_y = self.Pixel_Landmark[16].x, self.Pixel_Landmark[16].y
        # self.Left_Pinky_x, self.Left_Pinky_y = self.Pixel_Landmark[17].x, self.Pixel_Landmark[17].y
        # self.Right_Pinky_x, self.Right_Pinky_y = self.Pixel_Landmark[18].x, self.Pixel_Landmark[18].y
        # self.Left_Index_x, self.Left_Index_y = self.Pixel_Landmark[19].x, self.Pixel_Landmark[19].y
        # self.Right_Index_x, self.Right_Index_y = self.Pixel_Landmark[20].x, self.Pixel_Landmark[20].y
        # self.Left_Thumb_x, self.Left_Thumb_y = self.Pixel_Landmark[21].x, self.Pixel_Landmark[21].y
        # self.Right_Thumb_x, self.Right_Thumb_y = self.Pixel_Landmark[22].x, self.Pixel_Landmark[22].y
        # self.Left_Hip_x, self.Left_Hip_y = self.Pixel_Landmark[23].x, self.Pixel_Landmark[23].y
        # self.Right_Hip_x, self.Right_Hip_y = self.Pixel_Landmark[24].x, self.Pixel_Landmark[24].y
        # self.Left_Knee_x, self.Left_Knee_y = self.Pixel_Landmark[25].x, self.Pixel_Landmark[25].y
        # self.Right_Knee_x, self.Right_Knee_y = self.Pixel_Landmark[26].x, self.Pixel_Landmark[26].y
        # self.Left_Ankle_x, self.Left_Ankle_y = self.Pixel_Landmark[27].x, self.Pixel_Landmark[27].y
        # self.Right_Ankle_x, self.Right_Ankle_y = self.Pixel_Landmark[28].x, self.Pixel_Landmark[28].y
        # self.Left_Heel_x, self.Left_Heel_y = self.Pixel_Landmark[29].x, self.Pixel_Landmark[29].y
        # self.Right_Heel_x, self.Right_Heel_y = self.Pixel_Landmark[30].x, self.Pixel_Landmark[30].y
        # self.Left_Foot_Index_x, self.Left_Foot_Index_y = self.Pixel_Landmark[31].x, self.Pixel_Landmark[31].y
        # self.Right_Foot_Index_x, self.Right_Foot_Index_y = self.Pixel_Landmark[32].x, self.Pixel_Landmark[32].y

    def finger_pos(self):
        rect = (self.Right_Wrist_x, self.Right_Wrist_y, self.Right_Wrist_x, self.Right_Wrist_y)
        return rect
    
    def draw_all_landmark_circle(self, img):
        for id, lm in enumerate(self.Pixel_Landmark):
            cx, cy = int(lm.x * img.shape[1]), int(lm.y * img.shape[0])
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

       


    def draw_shoulder_line(self, img):
        self.median_x_coor = (self.Left_Shoulder_x + self.Right_Shoulder_x) / 2
        self.median_z_coor = (self.Left_Shoulder_z + self.Right_Shoulder_z) / 2
        self.median_y_coor = (self.Left_Shoulder_y + self.Right_Shoulder_y) / 2
        x_diff = np.abs(self.Right_Shoulder_x - self.median_x_coor)
        z_diff = np.abs(self.Right_Shoulder_z - self.median_z_coor)
        
        self.right_twist = (self.Right_Shoulder_z - self.median_z_coor)>0
        
        self.shoulder_angle =  np.degrees(np.arctan2(z_diff,x_diff))
        self.accumulate = (self.shoulder_angle - self.prev_angle) >= 2
        cv2.line(img, (int(self.Left_Shoulder_x * img.shape[1]), int(self.Left_Shoulder_y * img.shape[0])), (int(self.Right_Shoulder_x * img.shape[1]), int(self.Right_Shoulder_y * img.shape[0])), (255, 0, 0), 3)
        
        if self.right_twist:
            # 5，20，40，60
                print(self.accumulate)
                if 12< self.shoulder_angle < 28:
                    self.hint = "Level One"
                    if self.accumulate:
                        self.max_level = 1
                    
                elif 32< self.shoulder_angle < 50:
                    self.hint = "Level Two"
                    if self.accumulate:
                        self.max_level = 2
                    
                elif 50 <self.shoulder_angle:
                    self.hint = "Level Three"
                    if self.accumulate:
                        self.max_level = 3
                    
                elif self.shoulder_angle < 8:
                    self.hint = "No twisting"
                    self.max_level = 0
         
                    # cv2.putText(self.model.img, self.hint, (int(self.median_x_coor * self.model.img.shape[1]), int(self.median_y_coor * self.model.img.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        if self.shoulder_angle < 10:
            self.max_level = 0
        cv2.putText(img, self.hint, (int(self.median_x_coor * img.shape[1]), int(self.median_y_coor * img.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # self.angles.append(np.degrees(self.shoulder_angle))
        self.prev_angle = self.shoulder_angle




    def draw_all_landmark_drawing_utils(self, img):
        try:
            self.mp_drawing.draw_landmarks(
                    img,
                    self.Pixel_Landmark_list,
                    self.AI_model.POSE_CONNECTIONS, #this is the connection of the landmark
                    landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
                    )
        except:
            pass