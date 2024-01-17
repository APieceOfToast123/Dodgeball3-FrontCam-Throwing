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
            # For Main Page & Game Over Page, get the mouse position and check for input
            if self.model.currentstate == 1 or self.model.currentstate == 4:
                self.model.Mouse_Pos = pygame.mouse.get_pos()

                if self.model.currentstate == 1:
                    for button in [self.model.MainPage_PlayerButton, self.model.MainPage_OptionButton, self.model.MainPage_QuitButton]:
                        button.changeColor(self.model.Mouse_Pos)
                        button.update(self.model.screen)  

                if self.model.currentstate == 4:
                    for button in [self.model.EndPage_PlayerButton, self.model.EndPage_QuitButton]:
                        button.changeColor(self.model.Mouse_Pos)
                        button.update(self.model.screen)              

            # For Standardize Page & Game Page, get the camera image and display it
            if self.model.currentstate == 2 or self.model.currentstate == 3:               
                self.model.FPS_class.display_FPS(self.model.img)

                """
                Draw things on pygame
                """
                self.model.img = cv2.cvtColor(self.model.img, cv2.COLOR_BGR2RGB)
                self.model.img = pygame.image.frombuffer(self.model.img.tostring(), self.model.img.shape[1::-1], "RGB")

                # Standardize Page
                if self.model.currentstate == 2:
                    # Display the background
                    # self.model.Standardize_BG = pygame.transform.scale(pygame.image.load(self.model.Standardize_BG_path), (1280, 720))
                    self.model.screen.blit(self.model.img, (320, 0))
                    pygame.time.delay(int(1000 / 120))
                    self.model.Mediapipe_pose_class.expand_landmark()
                    
                # Game Page
                elif self.model.currentstate == 3:
                    self.model.screen.blit(self.model.img, (0, 0))
                    self.model.Mediapipe_pose_class.expand_landmark()
                    text_color = (0, 0, 0)

                    # display the count down
                    time_elapsed = time.time() - self.model.prev_time
                    time_left  = 3 - time_elapsed
                    font = pygame.font.Font(None, 36)
                    text_color = (0,255 , 0)
                    text = font.render(str(time_left), True, text_color)
                    text_rect = text.get_rect(center=(self.windowsize[0] // 2, self.windowsize[1] // 2))
                    self.model.screen.blit(text, text_rect)

                    # display the twist direction       
                    text2 = font.render("please twist {}".format(self.model.Mediapipe_pose_class.direction),True, text_color)
                    text_rect2 = text.get_rect(center=(self.windowsize[0] // 3, self.windowsize[1] // 3))
                    
                    self.model.Mediapipe_pose_class.expand_landmark()
                    # print(self.model.Mediapipe_pose_class.direction)
                    # print("aaa")
                    self.model.Mediapipe_pose_class.draw_shoulder_line (self.model.img)
                    
                    # self.model.Mediapipe_pose_class.draw_all_landmark_line(self.model.img)

                    '''
                    Move this part to progress_bar component later
                    '''

                    
                    # progress bar
                    white = (255, 255, 255)
                    green = (0, 255, 0)
                    pygame.draw.rect(self.model.screen, white, (50, 50, 300, 50)) 
                    if self.model.Mediapipe_pose_class.max_level == 1:
                        pygame.draw.rect(self.model.screen, green, (50, 50, 100, 50)) 
                    elif self.model.Mediapipe_pose_class.max_level == 2:
                        pygame.draw.rect(self.model.screen, green, (50, 50, 200, 50)) 
                    elif self.model.Mediapipe_pose_class.max_level == 3:
                        pygame.draw.rect(self.model.screen, green, (50, 50, 300, 50))

        except Exception as e:
            print(e)        
       
        pygame.display.flip()
        
        self.clock.tick(60)