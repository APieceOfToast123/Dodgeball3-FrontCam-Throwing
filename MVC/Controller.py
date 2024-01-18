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
        if self.model.add_button.CheckisClicked() == 'clicked':
            self.model.currentstate += 1
            self.evManager.Post(StateChangeEvent(self.model.currentstate))
        elif self.model.minus_button.CheckisClicked() == 'clicked':
            self.model.currentstate -= 1
            self.evManager.Post(StateChangeEvent(self.model.currentstate))

        self.model.input_event = pygame.event.get()    
        # Called for each game tick. We check our keyboard presses here.

        for event in self.model.input_event:

            # handle window manager closing our window
            if event.type == pygame.QUIT:
                self.graphics.quit_pygame()
                self.evManager.Post(QuitEvent())

            # handle key down events
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_ESCAPE:
            #         self.evManager.Post(StateChangeEvent(None))

                # # check key press for 1, 2, 3, 4, 5; if not same as current state, change state
                # elif event.key == pygame.K_1:
                #     self.evManager.Post(StateChangeEvent(1))

                # elif event.key == pygame.K_2:
                #     self.evManager.Post(StateChangeEvent(2))

                # elif event.key == pygame.K_3:
                #     self.evManager.Post(StateChangeEvent(3))

                # elif event.key == pygame.K_4:
                #     self.evManager.Post(StateChangeEvent(4))

                # elif event.key == pygame.K_5:
                #     self.evManager.Post(StateChangeEvent(5))


    def notify(self, event):
        """
        Receive events posted to the message queue. 
        """
        if isinstance(event, InitializeEvent):
            self.initialize()
        
       

        # if the state is changing, reset the pageinitilized flag
        elif isinstance(event, StateChangeEvent):
            self.pageinitilized = False
            print("State change event")

        elif isinstance(event, TickEvent):
            
            self.model.currentstate = self.model.state.peek()
            if self.pageinitilized == False:
                """
                Initialize new page
                """
                self.graphics.init_page()

                if self.model.CV2_class == None:
                    self.model.CV2_class = CV2_engine()
                self.model.FPS_class = FPS_engine()
                if self.model.currentstate == 3:
                    self.model.Mediapipe_pose_class = mediapipe_pose_engine()
                    self.start_time = time.time()
                    self.prev_time =self.start_time 
                    self.total_score = 0
                # elif self.model.currentstate == 3:
                #     self.model.Mediapipe_hand_class = mediapipe_hand_engine()
                # elif self.model.currentstate == 4:
                #     self.model.Mediapipe_FaceMesh_class = mediapipe_face_mesh_engine()
                # elif self.model.currentstate == 5:
                #     self.model.Mediapipe_Holistic_class = mediapipe_holistic_engine()
                print("New page initialized")
                # self.model.segmentation_class = segmentation_engine()
                
                self.pageinitilized = True
            
            """
            Handle all Business Logic
            """
            
            # Get camera image from CV2
            self.model.success, self.model.img = self.model.CV2_class.read_camera() # read camera
            
            if self.model.success:
                # Calculate FPS
                self.model.FPS_class.calculate_FPS()

                try:
                    # Mediapipe Pose
                    if self.model.currentstate == 3:
                        self.model.Mediapipe_pose_class.process_image(self.model.img)
                        self.model.Mediapipe_pose_class.expand_landmark()
                        self.model.Mediapipe_pose_class.handle_twist()
                        # self.model.Mediapipe_pose_class.expand_landmark()
                except Exception as e:
                    print(e)
                    import traceback
                    traceback.print_exc()

                
                
                # 判断是否到了3s
                
                self.model.elapsed_time = time.time() - self.model.prev_time
                if 0 <self.model.elapsed_time -3 < 1:
                    print(self.model.Mediapipe_pose_class.max_level)
                    if self.model.Mediapipe_pose_class != None:
                    #   time.sleep(1)
                    
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
                    #   self.direction =  self.model.Mediapipe_pose_class.generate_random_direction()
                      
                      self.model.prev_time = time.time()
                      
                    
                    #   print(time.time() - self.model.prev_time)
                    #   print("change the direction")
                
                    
                #判断60s是否结束
                self.model.total_left_time = time.time() - self.model.start_time
                if 0 <self.model.total_left_time - 80 < 1:
                # 如果结束，发送结束事件，转移状态，将pauseEvent g改为 StateChangeEvent
                    self.evManager.Post(PauseEvent())

                """
                Tell view to render after all Business Logic
                """
              
                self.graphics.render()
                
                # 归零
                

            self.input_event()
            
            
 



