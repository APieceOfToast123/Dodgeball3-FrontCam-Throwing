from MVC.EventManager import *
from Scene.UI_1 import *
import pygame
from pygame.locals import *
import pygame.freetype
import cv2
from Components.Button.Button import Button
from Components.Sprite_Engine.Sprite import sprite_engine
import sys
# from Components.Mediapipe_Models.Mediapipe_Engine import mediapipe_pose_engine
# import numpy as np
import time


class UI_View(object):
    def __init__(self, evManager, model):
        self.evManager = evManager
        self.model = model

    def initialize(self):
        """
        Initialize the UI.
        """
        pygame.init()
        pygame.font.init()
        pygame.freetype.init()
        pygame.mixer.init()

        pygame.display.set_caption('Throw Dodgeball')

        # flags = FULLSCREEN | DOUBLEBUF
        flags = DOUBLEBUF

        if (pygame.display.get_num_displays() >= 2):
            screen_no = 1
        else:
            screen_no = 0
        self.windowsize =(1280, 720)
        self.model.screen = pygame.display.set_mode(self.windowsize, flags, 16, display = screen_no, vsync=1)

        self.clock = pygame.time.Clock()

        # speedup a little bit
        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

    def quit_pygame(self):
        # shut down the pygame graphics
        self.isinitialized = False
        self.model.Menu_Mouse_Pos = None
        pygame.quit()
        sys.exit()

    def state_change_pygame(self):
        pygame.mixer.music.stop()
        self.model.screen.fill((255, 255, 255))
        # self.alpha += 10
        # current_color = (255, 255, 255, self.alpha)

        # flash = pygame.Surface(self.windowsize, pygame.SRCALPHA)
        # pygame.draw.rect(flash, current_color, (0, 0, 1280, 720))

        # self.model.screen.blit(flash, (0, 0))

    def display_Title(self, text, size, color, x, y):
        self.model.Text = self.model.get_title_font(size).render(text, True, color)
        self.model.Rect = self.model.Text.get_rect(center=(x, y))
        self.model.screen.blit(self.model.Text, self.model.Rect)
    
    def display_Text(self, text, size, color, x, y):
        self.model.Text = self.model.get_font(size).render(text, True, color)
        self.model.Rect = self.model.Text.get_rect(center=(x, y))
        self.model.screen.blit(self.model.Text, self.model.Rect)

    """
    Every time state changes, the page will be reinitialized
    """
    def init_page(self):
        # self.alpha = 0

        # Main Page Init
        if self.model.currentstate == 1:
            # Display the background
            self.model.MainPage_BG = pygame.transform.scale(pygame.image.load(self.model.MainPage_BG_path), (1280, 720))
            self.model.screen.blit(self.model.MainPage_BG, (0, 0))

            self.display_Title("Throw DodgeBall", 110, "#F26448", 640, 170)

            self.model.MainPage_PlayerButton = Button(image=pygame.image.load(self.model.PlayerButton_path), pos=(640, 360), 
                                text_input="PLAY", font=self.model.get_title_font(60), base_color="#FEB009", hovering_color="White")
            
            self.model.MainPage_OptionButton = Button(image=pygame.image.load(self.model.OptionButton_path), pos=(640, 490), 
                                text_input="OPTIONS", font=self.model.get_title_font(60), base_color="#FEB009", hovering_color="White")
            
            self.model.MainPage_QuitButton = Button(image=pygame.image.load(self.model.QuitButton_path), pos=(640, 620), 
                                text_input="QUIT", font=self.model.get_title_font(60), base_color="#FEB009", hovering_color="White")
            

            pygame.mixer.music.load(self.model.MainPage_BGM_path)

        # Standardize Page Init
        if self.model.currentstate == 2:


            pygame.mixer.music.load(self.model.StandarizedPage_BGM_path)

        # Game Page Init
        if self.model.currentstate == 3:
            

            self.model.random_music()
            pygame.mixer.music.load(self.model.GamePage_BGM_path)

        # Game Over Page Init
        if self.model.currentstate == 4:
            # Display the background
            self.model.EndPage_BG = pygame.transform.scale(pygame.image.load(self.model.EndPage_BG_path), (1280, 720))
            self.model.screen.blit(self.model.EndPage_BG, (0, 0))

            self.display_Title("Game Over", 100, "#F26448", 640, 180)
            self.display_Text("Score: 1000", 50, "#FFFFFF", 640, 280)
            self.display_Title("Your Wrist Is Very Healthy!", 50, "#FEB009", 640, 365)

            self.model.EndPage_PlayerButton = Button(image=pygame.image.load(self.model.PlayerButton_path), pos=(640, 490), 
                                text_input="PLAY AGAIN", font=self.model.get_title_font(60), base_color="#FEB009", hovering_color="White")
            
            self.model.EndPage_QuitButton = Button(image=pygame.image.load(self.model.QuitButton_path), pos=(640, 620), 
                                text_input="QUIT", font=self.model.get_title_font(60), base_color="#FEB009", hovering_color="White")
            

            pygame.mixer.music.load(self.model.MainPage_BGM_path)
            
        pygame.mixer.music.play(-1)

    """
    This function will be called 60 times per second
    """
    def render(self):
        try:
            # Update the screen
            # For Main Page & Game Over Page, get the mouse position and check for input
            if self.model.currentstate == 1 or self.model.currentstate == 4:
                self.model.Mouse_Pos = pygame.mouse.get_pos()

                # Main Menu Page
                if self.model.currentstate == 1:
                    for button in [self.model.MainPage_PlayerButton, self.model.MainPage_OptionButton, self.model.MainPage_QuitButton]:
                        button.changeColor(self.model.Mouse_Pos)
                        button.update(self.model.screen)  

                # Game Page
                if self.model.currentstate == 4:
                    for button in [self.model.EndPage_PlayerButton, self.model.EndPage_QuitButton]:
                        button.changeColor(self.model.Mouse_Pos)
                        button.update(self.model.screen)              

            # For Standardize Page & Game Page, get the camera image and display it
            if self.model.currentstate == 2 or self.model.currentstate == 3:               
                self.model.FPS_class.display_FPS(self.model.img)

                self.model.img = cv2.cvtColor(self.model.img, cv2.COLOR_BGR2RGB)
                self.model.img = pygame.image.frombuffer(self.model.img.tostring(), self.model.img.shape[1::-1], "RGB")

                # Standardize Page
                if self.model.currentstate == 2:
                    self.model.screen.blit(self.model.img, (320, 0))
                    self.model.Mediapipe_pose_class.expand_landmark()

                # Game Page
                if self.model.currentstate == 3:
                    self.model.screen.blit(self.model.img, (0, 0))
                    self.model.Mediapipe_pose_class.draw_shoulder_line (self.model.img)
                    
                    # self.model.Mediapipe_pose_class.draw_all_landmark_line(self.model.img)
                    
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    font_scale = 1
                    font_thickness = 2
                    font_color = (255, 255, 255)  # 白色       
                    box_color = (0, 0, 255)  # 红色
                    image_height, image_width, _ = self.model.img.shape     
                    self.model.time_left  = 3 - self.model.elapsed_time
                    # display the count down
                    box_position = (400, 50)
                    box_size = (100, 100)
                    cv2.rectangle(self.model.img, box_position, (box_position[0] + box_size[0], box_position[1] + box_size[1]), box_color, -1)
                    text_position = (box_position[0] + 25, box_position[1] + box_size[1] // 2)
                    cv2.putText(self.model.img, "{:.0f}".format(self.model.time_left), text_position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

                
                    # display the score
                    text3 = "Score:{}  ".format(self.model.total_score)
                    text3 = text3+("Missed" if self.model.hit_goal == False else "Hit")
                    box_size = (300,100)
                    box_position = (900,400)
                    text3_position = (box_position[0] + 50, box_position[1] + box_size[1] // 2)
                    cv2.rectangle(self.model.img, box_position, (box_position[0] + box_size[0], box_position[1] + box_size[1]), box_color, -1)
                    cv2.putText(self.model.img, text3, text3_position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)
                    
                    # display the twist direction hint
                    text2 = "please twist {}".format(self.model.Mediapipe_pose_class.direction)
                    box_size = (500,100 )
                    box_position = (900, 50)
                    text2_position = (box_position[0] + 50, box_position[1] + box_size[1] // 2)
                    cv2.rectangle(self.model.img, box_position, (box_position[0] + box_size[0], box_position[1] + box_size[1]), box_color, -1)
                    cv2.putText(self.model.img, text2, text2_position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

                    # progress bar
                    white = (255, 255, 255)
                    green = (0, 255, 0)
                    level = self.model.Mediapipe_pose_class.max_level
                    pygame.draw.rect(self.model.screen, green, (50, 50, 100*level, 50))
                    if 0 <self.model.elapsed_time -3 < 1:
                        self.model.Mediapipe_pose_class.max_level_store = 0
                      
        except Exception as e:
            print(e)
            
       
            
        """
        Draw things on pygame
        """
 


        '''
        Move this part to progress_bar component later
        '''

        

   
        
           
                    
               
                   
                    
               

   
        pygame.display.flip()
        
        self.clock.tick(60)