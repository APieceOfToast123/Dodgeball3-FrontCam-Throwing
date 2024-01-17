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
                if self.model.MainPage_PlayerButton.checkForInput(self.model.Mouse_Pos):
                    self.model.currentstate = 2
                    self.evManager.Post(StateChangeEvent(self.model.currentstate))
                if self.model.MainPage_OptionButton.checkForInput(self.model.Mouse_Pos):
                    self.model.currentstate = 4
                    self.evManager.Post(StateChangeEvent(self.model.currentstate))
                if self.model.MainPage_QuitButton.checkForInput(self.model.Mouse_Pos):
                    self.graphics.quit_pygame()
                    self.evManager.Post(QuitEvent())
                else:
                    pass

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

                else:
                    pass       

                self.graphics.init_page()
                print("New page initialized")

                self.pageinitilized = True

            """
            Handle all Business Logic
            """
            if self.model.currentstate == 2 or self.model.currentstate == 3:

                # Get camera image from CV2
                self.model.success, self.model.img = self.model.CV2_class.read_camera() # read camera
                
                if self.model.success:
                    # Calculate FPS
                    self.model.FPS_class.calculate_FPS()


                    # Mediapipe Pose
                    self.model.Mediapipe_pose_class.process_image(self.model.img)
                    # self.model.Mediapipe_pose_class.expand_landmark()
                    if self.model.currentstate == 3:
                        if time.time() - self.model.prev_time == 3:
                            self.model.MediaPipe_pose_class.generate_direction()
                            self.model.prev_time = time.time()
                            
                        if time.time() - self.mdoel.start_time == 60:
                            self.evManager.Post(PauseEvent())
           
            
            """
            Tell view to render after all Business Logic
            """
            self.graphics.render()

            self.input_event()
            
            
 



