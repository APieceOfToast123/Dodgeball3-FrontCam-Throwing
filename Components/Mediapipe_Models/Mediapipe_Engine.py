from MVC.EventManager import *
import mediapipe
import cv2
import numpy as np
import pygame
from pygame.locals import *
import random
class mediapipe_pose_engine():
    def __init__(self):
        self.AI_model = mediapipe.solutions.pose
        self.AI_model_initialized = self.AI_model.Pose(
                                    model_complexity = 1,
                                    min_detection_confidence = 0.6, 
                                    min_tracking_confidence = 0.6,
                                    enable_segmentation = False,
                                    smooth_segmentation = False
                                    )
        self.mp_drawing = mediapipe.solutions.drawing_utils
        self.mp_drawing_styles = mediapipe.solutions.drawing_styles
        self.hint =None
        self.shoulder_angle = 0
        self.prev_angle= 0
        self.max_level = 0
        self.direction = "right"
        self.accumulate = True
        self.max_level_store = 0

    def process_image(self, img):
        self.results = self.AI_model_initialized.process(img)
        
        if self.results.pose_landmarks:
            self.pose_detected = True
            self.Pixel_Landmark_list = self.results.pose_landmarks
            self.Pixel_Landmark = self.results.pose_landmarks.landmark
            self.World_Landmark = self.results.pose_world_landmarks.landmark
        else:
            self.pose_detected = False
            # cv2.putText(img, "No pose detected", (10, 110), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            
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
        
        self.Left_Shoulder_x, self.Left_Shoulder_y ,self.Left_Shoulder_z = self.Pixel_Landmark[11].x, self.Pixel_Landmark[11].y, self.Pixel_Landmark[11].z
        self.Right_Shoulder_x, self.Right_Shoulder_y ,self.Right_Shoulder_z = self.Pixel_Landmark[12].x, self.Pixel_Landmark[12].y, self.Pixel_Landmark[12].z
        self.Left_Shoulder = [self.Left_Shoulder_x, self.Left_Shoulder_y]
        self.Right_Shoulder = [self.Right_Shoulder_x, self.Right_Shoulder_y]
        self.Left_elbow  = [self.Pixel_Landmark[13].x, self.Pixel_Landmark[13].y]
        self.Right_elbow = [self.Pixel_Landmark[14].x, self.Pixel_Landmark[14].y]
        self.median_x_coor = (self.Left_Shoulder_x + self.Right_Shoulder_x) / 2
        self.median_z_coor = (self.Left_Shoulder_z + self.Right_Shoulder_z) / 2
        self.median_y_coor = (self.Left_Shoulder_y + self.Right_Shoulder_y) / 2


    def finger_pos(self):
        rect = (self.Right_Wrist_x, self.Right_Wrist_y, self.Right_Wrist_x, self.Right_Wrist_y)
        return rect
    
    def draw_all_landmark_circle(self, img):
        for id, lm in enumerate(self.Pixel_Landmark):
            cx, cy = int(lm.x * img.shape[1]), int(lm.y * img.shape[0])
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

       
    # def draw_shoulder_line(self, img):
        
    #     cv2.line(img, (int(self.Left_Shoulder_x * img.shape[1]), int(self.Left_Shoulder_y * img.shape[0])), 
                        # (int(self.Right_Shoulder_x * img.shape[1]), int(self.Right_Shoulder_y * img.shape[0])), (255, 0, 0), 3)    
    #     cv2.putText(img, self.hint, (int(self.median_x_coor * img.shape[1]), int(self.median_y_coor * img.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    def draw_shoulder_line(self, img, font):
        pygame.draw.line(img, (255, 0, 0), (int(self.Left_Shoulder_x * img.get_width() * 0.5), int(self.Left_Shoulder_y * img.get_height())),
                        (int(self.Right_Shoulder_x * img.get_width() * 0.5), int(self.Right_Shoulder_y * img.get_height())), 3)
        
        text_surface = font.render(self.hint, True, (255, 0, 0))
        text_position = (int(self.median_x_coor * img.get_width() * 0.5), int(self.median_y_coor * img.get_height()))
        img.blit(text_surface, text_position)

    def handle_twist(self):
        
        if self.direction == "right":
            self.right_ball()
           
        else:
            self.left_ball()
            
            
    def right_ball(self):
        
        x_diff = np.abs(self.Right_Shoulder_x - self.median_x_coor)
        z_diff = np.abs(self.Right_Shoulder_z - self.median_z_coor)
        
        self.right_twist = (self.Right_Shoulder_z - self.median_z_coor)>0
        
        self.shoulder_angle =  np.degrees(np.arctan2(z_diff,x_diff))
        self.accumulate = (self.shoulder_angle - self.prev_angle) >= 0.06
        
        if self.right_twist:
            # 5，20，40，60
                # print(self.accumulate)
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
                    # self.max_level = 0
                    # cv2.putText(self.model.img, self.hint, (int(self.median_x_coor * self.model.img.shape[1]), int(self.median_y_coor * self.model.img.shape[0])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
        else:
            
            self.hint = "twsit  wrong dirction"
            if self.max_level != 0 :
                self.went_back = True
                self.max_level_store = self.max_level
            self.max_level = 0
        
        # print(self.max_level)
        

        # self.angles.append(np.degrees(self.shoulder_angle))
        self.prev_angle = self.shoulder_angle
        # print( self.prev_angle)


    def left_ball(self):
        self.median_x_coor = (self.Left_Shoulder_x + self.Right_Shoulder_x) / 2
        self.median_z_coor = (self.Left_Shoulder_z + self.Right_Shoulder_z) / 2
        self.median_y_coor = (self.Left_Shoulder_y + self.Right_Shoulder_y) / 2
        x_diff = np.abs(self.Left_Shoulder_x - self.median_x_coor)
        z_diff = np.abs(self.Left_Shoulder_z - self.median_z_coor)
        
        self.left_twist = (self.Left_Shoulder_z - self.median_z_coor)>0
        
        self.shoulder_angle =  np.degrees(np.arctan2(z_diff,x_diff))
        self.accumulate = (self.shoulder_angle - self.prev_angle) >= 2
        
        if self.left_twist:
            # 5，20，40，60
                
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
                    # self.max_level = 0
         
        else:
            self.hint = "twsit  wrong dirction"
            if self.max_level != 0 :
                self.went_back = True
                self.max_level_store = self.max_level
            self.max_level = 0


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

    def generate_random_direction(self):
        random_float = random.uniform(0, 1)
        try:
            if random_float < 0.5:
                self.direction = "left"
                
            else:
                self.direction = "right"
            return self.direction
        except Exception as e:
            print(e)
            import traceback
            traceback.print_exc()

