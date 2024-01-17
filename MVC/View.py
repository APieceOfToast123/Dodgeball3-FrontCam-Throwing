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

    def init_page(self):
        self.alpha = 0
        if self.model.currentstate == 1:
            # Display the background
            self.model.MainPage_BG = pygame.transform.scale(pygame.image.load(self.model.MainPage_BG_path), (1280, 720))
            self.model.screen.blit(self.model.MainPage_BG, (0, 0))

            # Display the title
            self.model.Menu_Text = self.model.get_title_font(120).render("throw dodgeball", True, "#F26448")
            # Align the text
            self.model.Menu_Rect = self.model.Menu_Text.get_rect(center=(640, 180))
            # Display the text on the screen
            self.model.screen.blit(self.model.Menu_Text, self.model.Menu_Rect)

            self.model.MainPage_PlayerButton = Button(image=pygame.image.load(self.model.MainPage_PlayerButton_path), pos=(640, 360), 
                                text_input="PLAY", font=self.model.get_title_font(60), base_color="#FEB009", hovering_color="White")
            
            self.model.MainPage_OptionButton = Button(image=pygame.image.load(self.model.MainPage_OptionButton_path), pos=(640, 490), 
                                text_input="OPTIONS", font=self.model.get_title_font(60), base_color="#FEB009", hovering_color="White")
            
            self.model.MainPage_QuitButton = Button(image=pygame.image.load(self.model.MainPage_QuitButton_path), pos=(640, 620), 
                                text_input="QUIT", font=self.model.get_title_font(60), base_color="#FEB009", hovering_color="White")
            
            # Display background music
            pygame.mixer.music.load(self.model.MainPage_BGM_path)
            pygame.mixer.music.play(-1)

        if self.model.currentstate == 2:
            # Display background music
            pygame.mixer.music.load(self.model.StandarizedPage_BGM_path)
            pygame.mixer.music.play(-1)

        if self.model.currentstate == 3:
            # Display background music
            pygame.mixer.music.load(self.model.GamePage_BGM_path)
            pygame.mixer.music.play(-1)

    def render(self):
        try:
            if self.model.currentstate == 1:
                # Get the mouse position
                self.model.Menu_Mouse_Pos = pygame.mouse.get_pos()

                # If the mouse is hovering over the button, change the color
                for button in [self.model.MainPage_PlayerButton, self.model.MainPage_OptionButton, self.model.MainPage_QuitButton]:
                    button.changeColor(self.model.Menu_Mouse_Pos)
                    button.update(self.model.screen)                

            if self.model.currentstate == 2 or self.model.currentstate == 3:
            # standardize page
                # # Display the background
                # self.model.Standardize_BG = pygame.transform.scale(pygame.image.load(self.model.Standardize_BG_path), (1280, 720))

                # Display FPS
                self.model.FPS_class.display_FPS(self.model.img)

                """
                Draw things on pygame
                """
                # Convert into RGB
                self.model.img = cv2.cvtColor(self.model.img, cv2.COLOR_BGR2RGB)

                # Convert the image into a format pygame can display
                self.model.img = pygame.image.frombuffer(self.model.img.tostring(), self.model.img.shape[1::-1], "RGB")

                if self.model.currentstate == 2:
                    # blit the image onto the screen
                    self.model.screen.blit(self.model.img, (320, 0))
                    
                    # Expand Mediapipe Pose landmarks
                    self.model.Mediapipe_pose_class.expand_landmark()
                    
                elif self.model.currentstate == 3:
                    # blit the image onto the screen
                    self.model.screen.blit(self.model.img, (0, 0))
                    
                    # Expand Mediapipe Pose landmarks
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
       
        # Update the screen
        pygame.display.flip()

        # limit the redraw speed to 30 frames per second
        
        self.clock.tick(60)