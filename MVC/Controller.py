from MVC.EventManager import *
import MVC.View as view
from Components.Calculate_FPS.FPS_Engine import FPS_engine
from Components.CameraIO.CV2_Engine import CV2_engine
from Components.Mediapipe_Models.Mediapipe_Engine import *
from Components.Segmentation.Segmentation_Engine import segmentation_engine
import cv2
import pygame
import random
import time
class control(object):
    def __init__(self, evManager, model):
        self.evManager = evManager
        evManager.RegisterListener(self)
        self.model = model
        self.pageinitilized = False
        self.standardized = False
        self.model.CV2_class = None
        
    def initialize(self):
        """
        Initialize view.
        """
        self.graphics = view.UI_View(self.evManager, self.model)
        self.graphics.initialize()

    def input_event(self):
        self.model.input_event = pygame.event.get()    
        # Called for each game tick. We check our keyboard presses here.

        for event in self.model.input_event:
            # handle window manager closing our window
            if event.type == pygame.QUIT:
                self.graphics.quit_pygame()
                self.evManager.Post(QuitEvent())
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.graphics.ClickSound = pygame.mixer.Sound(self.model.ClickSound_path)
                self.graphics.ClickSound.set_volume(1)
                self.graphics.ClickSound.play()

                if self.model.currentstate == 1:
                    if self.model.MainPage_PlayerButton.checkForInput(self.model.Mouse_Pos):
                        self.model.currentstate = 2
                        self.evManager.Post(StateChangeEvent(self.model.currentstate))
                    if self.model.MainPage_OptionButton.checkForInput(self.model.Mouse_Pos):
                        self.model.currentstate = 5
                        self.evManager.Post(StateChangeEvent(self.model.currentstate))
                    if self.model.MainPage_QuitButton.checkForInput(self.model.Mouse_Pos):
                        self.graphics.quit_pygame()
                        self.evManager.Post(QuitEvent())
                        
                elif self.model.currentstate == 4:
                    if self.model.EndPage_PlayerButton.checkForInput(self.model.Mouse_Pos):
                        self.model.currentstate = 1
                        self.evManager.Post(StateChangeEvent(self.model.currentstate))
                    if self.model.EndPage_QuitButton.checkForInput(self.model.Mouse_Pos):
                        self.graphics.quit_pygame()
                        self.evManager.Post(QuitEvent())

                elif self.model.currentstate == 5:
                    if self.model.RankPage_BackButton.checkForInput(self.model.Mouse_Pos):
                        self.model.currentstate = 1
                        self.evManager.Post(StateChangeEvent(self.model.currentstate))
                else:
                    pass
    
    def calculate_angle(self,a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle
    

        
    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, InitializeEvent):
            self.initialize()     

        # if the state is changing, reset the pageinitilized flag
        elif isinstance(event, StateChangeEvent):
            self.pageinitilized = False
            self.graphics.state_change_pygame()
            print("State change event")

        elif isinstance(event, TickEvent):
            
            self.model.currentstate = self.model.state.peek()
            if self.pageinitilized == False:
                """
                Initialize new page
                """         
                if self.model.currentstate == 2 or self.model.currentstate == 3:
                    if self.model.CV2_class == None:
                        self.model.CV2_class = CV2_engine()
                    self.model.FPS_class = FPS_engine()
                    self.model.Mediapipe_pose_class = mediapipe_pose_engine()

                    if self.model.currentstate == 3:
                        self.model.start_time = time.time()
                        self.model.prev_time =self.model.start_time 
                        self.model.total_score = 0

                else:
                    pass       

                self.graphics.init_page()
                print("New page initialized")

                self.pageinitilized = True

            """
            Handle all Game Logic
            """
            if self.model.currentstate == 2 or self.model.currentstate == 3:
                # Get camera image from CV2
                self.model.success, self.model.img = self.model.CV2_class.read_camera() # read camera
                
                if self.model.success:
                    try: 
                        # Calculate FPS
                        # self.model.FPS_class.calculate_FPS()
                        self.model.Mediapipe_pose_class.process_image(self.model.img)
                        self.model.Mediapipe_pose_class.expand_landmark()

                        if self.model.currentstate == 2:
                            # Standardize the pose
                            try:
                                
                                left_shoulder = self.model.Mediapipe_pose_class.Left_Shoulder
                                right_shoulder = self.model.Mediapipe_pose_class.Right_Shoulder
                                left_elbow = self.model.Mediapipe_pose_class.Left_elbow
                                right_elbow = self.model.Mediapipe_pose_class.Right_elbow

                                self.model.angle1 = self.calculate_angle(left_shoulder, right_shoulder, right_elbow)
                                self.model.angle2 = self.calculate_angle(right_shoulder, left_shoulder, left_elbow)

                                
                            except:
                                pass

                        # Mediapipe Pose
                        if self.model.currentstate == 3:
                            self.model.Mediapipe_pose_class.handle_twist()
                            
                            self.model.elapsed_time = time.time() - self.model.prev_time

                            if time.time() - self.model.prev_time > 3:
                                self.model.guided = True

                            if 2 < self.model.elapsed_time < 2.1:
                                if self.model.guided == False:
                                    self.graphics.GamePage_guide = pygame.mixer.Sound(self.model.GamePage_guide_path)
                                    self.graphics.GamePage_guide.set_volume(1)
                                    self.graphics.GamePage_guide.play()
                                elif self.model.applaused == False and self.model.guided == True:
                                    if self.model.Mediapipe_pose_class != None:
                                        if self.model.Mediapipe_pose_class.max_level_store == 0:
                                            self.graphics.GamePage_level0 = pygame.mixer.Sound(self.model.GamePage_level0_path)
                                            self.graphics.GamePage_level0.set_volume(1)
                                            self.graphics.GamePage_level0.play()
                                        elif self.model.Mediapipe_pose_class.max_level_store == 1:
                                            self.graphics.GamePage_level1 = pygame.mixer.Sound(self.model.GamePage_level1_path)
                                            self.graphics.GamePage_level1.set_volume(1)
                                            self.graphics.GamePage_level1.play()
                                        elif self.model.Mediapipe_pose_class.max_level_store == 2:
                                            self.graphics.GamePage_level2 = pygame.mixer.Sound(self.model.GamePage_level2_path)
                                            self.graphics.GamePage_level2.set_volume(1)
                                            self.graphics.GamePage_level2.play()
                                        elif self.model.Mediapipe_pose_class.max_level_store == 3:
                                            self.graphics.GamePage_level3 = pygame.mixer.Sound(self.model.GamePage_level3_path)
                                            self.graphics.GamePage_level3.set_volume(1)
                                            self.graphics.GamePage_level3.play()
                                    self.model.applaused = True

                            # 判断是否到了3s
                            if 0 <self.model.elapsed_time -3 < 1:
                                if self.model.Mediapipe_pose_class != None:
                                    
                                    if self.model.Mediapipe_pose_class.max_level_store == 1:
                                        # if (random.uniform(0, 1) > 0.2):
                                            self.model.hit_goal = True 
                                            self.model.total_score += 50
                                        # else:
                                            # self.model.hit_goal = False
                                    elif self.model.Mediapipe_pose_class.max_level_store == 2:
                                        # if (random.uniform(0, 1) > 0.1):
                                            self.model.hit_goal = True  
                                            self.model.total_score += 50
                                        # else: 
                                            # self.model.hit_goal = False
                                    elif self.model.Mediapipe_pose_class.max_level_store == 3:
                                        self.model.hit_goal = True 
                                        self.model.total_score += 50
                                        print("打中了加分")
                                        
                                    #换一个新的方向
                                    self.model.direction =  self.model.Mediapipe_pose_class.generate_random_direction()                               

                                    if self.model.direction == "left":
                                        self.graphics.VoicePromptSound = pygame.mixer.Sound(self.model.GamePage_RightVoice_path)
                                    elif self.model.direction == "right":
                                        self.graphics.VoicePromptSound = pygame.mixer.Sound(self.model.GamePage_LeftVoice_path)
                                    self.graphics.VoicePromptSound.set_volume(1)
                                    self.graphics.VoicePromptSound.play()
                                
                                self.model.applaused = False 
                                self.model.prev_time = time.time()                               
                                
                                #   print(time.time() - self.model.prev_time)
                                #   print("change the direction")                            
                                
                            #判断60s是否结束
                            self.model.total_spend_time = time.time() - self.model.start_time
                            if 0 <self.model.total_spend_time - 60 < 1:
                            # 如果结束，发送结束事件，转移状态，将pauseEvent改为 StateChangeEvent
                                self.model.game_record.append({'score': self.model.total_score, 'timestamp': time.time()})
                                self.model.sorted_records = sorted(self.model.game_record, key=lambda x: x['score'], reverse=True)

                                self.model.currentstate = 4
                                self.evManager.Post(StateChangeEvent(self.model.currentstate))
                    
                    except Exception as e:
                        print(e)
                        import traceback
                        traceback.print_exc()              
                
            """
            Tell view to render after all Business Logic
            """
            self.graphics.render()

            self.input_event()
            
            
 



