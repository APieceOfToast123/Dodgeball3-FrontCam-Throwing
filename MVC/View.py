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
        self.model.Menu_Mouse_Pos = None
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
            self.model.StandardizedPage_BG = pygame.transform.scale(pygame.image.load(self.model.StandarizedPage_BG_path), (1280, 720))

            self.model.start_counting = False
            self.model.start_counting_time = None
            pygame.mixer.music.load(self.model.GamePage_StretchVoice_path)
            pygame.mixer.music.play()
            time.sleep(2)
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.model.StandarizedPage_BGM_path)
            pygame.mixer.music.play()


        # Game Page Init
        if self.model.currentstate == 3:
            self.model.GamePage_BG = pygame.transform.scale(pygame.image.load(self.model.GamePage_BG_path), (640, 720))
            self.model.Monster = pygame.image.load(self.model.Monster_path)

            self.model.icon_border = pygame.transform.scale(pygame.image.load(self.model.iconBorder_path), (130,130))
            self.model.center_bar = pygame.transform.scale(pygame.image.load(self.model.centerBar_path), (38, 74))
            self.model.right_bar = pygame.transform.scale(pygame.image.load(self.model.rightBar_path), (36, 74))

            self.model.leftEnergy = pygame.transform.scale(pygame.image.load(self.model.leftEnergy_path), (36, 74))
            self.model.reapetEnergy = pygame.transform.scale(pygame.image.load(self.model.reapetEnergy_path), (8.6, 74))
            self.model.rightEnergy = pygame.transform.scale(pygame.image.load(self.model.rightEnergy_path), (36, 74))

            self.model.timer = pygame.transform.scale(pygame.image.load(self.model.timer_path), (78, 80))
            self.model.magic = pygame.transform.scale(pygame.image.load(self.model.magic_path), (80, 85))
            self.model.xp = pygame.transform.scale(pygame.image.load(self.model.xp_path), (80, 47))

            self.model.bun_sprite = sprite_engine(self.model.bun_sprite_path, (780, 200), 13, self.model)

            # self.model.random_music()
            # pygame.mixer.music.load(self.model.GamePage_BGM_path)


        # Game Over Page Init
        if self.model.currentstate == 4:
            # Display the background
            self.model.EndPage_BG = pygame.transform.scale(pygame.image.load(self.model.EndPage_BG_path), (1280, 720))
            self.model.screen.blit(self.model.EndPage_BG, (0, 0))

            self.display_Title("Game Over", 100, "#F26448", 640, 180)
            self.display_Text("Score: {}".format(self.model.total_score) , 50, "#FFFFFF", 640, 280)

            if self.model.total_score < 10:
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
                self.model.screen.fill((255, 255, 255))

                # self.model.FPS_class.display_FPS(self.model.img)

                self.model.img = cv2.cvtColor(self.model.img, cv2.COLOR_BGR2RGB)
                self.model.img = pygame.image.frombuffer(self.model.img.tostring(), self.model.img.shape[1::-1], "RGB")

                # Standardize Page
                if self.model.currentstate == 2:
                    self.model.screen.blit(self.model.StandardizedPage_BG, (0, 0))
                    self.model.screen.blit(self.model.img, (320, 0))
                    self.display_Title("Strech Yout Arms!", 67, "#F26448", self.model.screen.get_width()//2, 80)

                    self.outline_origin = pygame.image.load(self.model.StandarizedPage_Outline_path)

                    self.model.outline = pygame.transform.scale(self.outline_origin, (self.model.img.get_width() - 6, self.outline_origin.get_height()/self.outline_origin.get_width() * self.model.img.get_width() - 30))
                    self.model.screen.blit(self.model.outline, ((self.model.screen.get_width() - self.model.img.get_width())//2 + 3, self.model.screen.get_height() - self.model.outline.get_height()))

                    self.model.Mediapipe_pose_class.expand_landmark()
                    if 330 < self.model.angle1 + self.model.angle2 < 350:
                        try:
                            if self.model.start_counting == False:
                                self.model.start_counting = True
                                self.model.start_counting_time = time.time()
                            elif self.model.start_counting: 
                                if time.time() - self.model.start_counting_time < 1.5:
                                        self.display_Title("Hold Still for 3 Seconds!", 50, "#FEB009", self.model.screen.get_width()//2, 120)
                                        print("Hold Still for 3 Seconds!")
                                elif 1.5 < (time.time() - self.model.start_counting_time) < 2.3:
                                        self.display_Title("Hold Still for 2 Seconds!", 50, "#FEB009", self.model.screen.get_width()//2, 120)
                                        print("Hold Still for 2 Seconds!")
                                elif 2.3< (time.time() - self.model.start_counting_time) < 3:
                                        self.display_Title("Hold Still for 1 Seconds!", 50, "#FEB009", self.model.screen.get_width()//2, 120)
                                        print("Hold Still for 1 Seconds!")
                                elif (time.time() - self.model.start_counting_time) > 3:
                                        self.model.currentstate = 3
                                        self.evManager.Post(StateChangeEvent(self.model.currentstate))
                                        self.model.start_counting_time = None
                                        self.model.start_counting = False
                            else:
                                self.display_Title("???!", 50, "#FEB009", self.model.screen.get_width()//2, 120)   
                        except Exception as e:
                            print(e)
                            from traceback import print_exc
                            print_exc()        
                    else:
                        self.model.start_counting_time = None
                        self.model.start_counting = False
                                    
                # Game Page
                if self.model.currentstate == 3:
                    self.model.screen.blit(self.model.img, (0, 0))

                    font = pygame.font.Font("Resources/Fonts/title_font.ttf", 35)
                    font_color = "#F26448" 
                    self.model.time_left = 3 - self.model.elapsed_time

                    self.model.Mediapipe_pose_class.draw_shoulder_line(self.model.screen, font)

                    # Progress bar
                    level = self.model.Mediapipe_pose_class.max_level                    
                    for i in range(self.model.borderLength):
                        self.model.screen.blit(self.model.center_bar, (self.model.icon_border.get_width()  + self.model.center_bar.get_width() * i, self.model.icon_border.get_height()//4 + 10))
                    self.model.screen.blit(self.model.right_bar, (self.model.icon_border.get_width()  + self.model.center_bar.get_width() * self.model.borderLength, self.model.icon_border.get_height()//4 + 10))
                    self.model.screen.blit(self.model.leftEnergy, (self.model.icon_border.get_width() +2, self.model.icon_border.get_height()//4 + 10))
                    
                    MovePaceLength = self.model.reapetEnergy.get_width()
                    for i in range(level):
                        for j in range(self.model.repeatLength * level ):
                            self.model.repeatImage = self.model.reapetEnergy.copy()
                            self.model.screen.blit(self.model.repeatImage, (self.model.icon_border.get_width() + self.model.leftEnergy.get_width() + MovePaceLength * j, self.model.icon_border.get_height()//4 + 10))
                    self.model.screen.blit(self.model.rightEnergy, (self.model.icon_border.get_width() + self.model.leftEnergy.get_width() + MovePaceLength * self.model.repeatLength * level , self.model.icon_border.get_height()//4 + 10))
                    
                    self.model.screen.blit(self.model.icon_border, (10, 10))

                    self.model.screen.blit(self.model.magic, (35, 35))

                    # Display the count down
                    box_size = (80, 80)
                    box_position = (0, 150)
                    text_position = (box_position[0] + 130, box_position[1] + box_size[1] // 3 + 20)
                    text_surface = font.render("{:.0f}".format(self.model.time_left), True, "#FEB009")
                    self.model.screen.blit(text_surface, text_position)
                    
                    self.model.screen.blit(self.model.timer, (box_position[0] + 25, box_position[1] + box_size[1] // 3))

                    # Display the twist direction hint
                    direction = "right " if self.model.Mediapipe_pose_class.direction == "left" else "left "
                    text2 = "Please twist  " + direction + "!"
                    box_size = (350, 100)
                    box_position = (self.model.img.get_width()-box_size[0]-5, 150)
                    text4_position = (box_position[0] - 50, box_position[1] + box_size[1] // 3 + 20)
                    text2_surface = font.render(text2, True, font_color)
                    self.model.screen.blit(text2_surface, text4_position)

                    # Display the wizard
                    self.model.screen.blit(self.model.GamePage_BG, (640, 0))
                    self.model.screen.blit(self.model.Monster, (750, 150))
                    # self.model.bun_sprite.draw(self.model.bun_sprite_time)

                    # Display the score
                    text3 = "Score:{}  {}".format(self.model.total_score, "Missed" if not self.model.hit_goal else "Hit")
                    box_size = (280, 100)
                    box_position = (self.model.screen.get_width()-box_size[0]-20, 30)
                    text3_position = (box_position[0] + 25, box_position[1] + box_size[1] // 3)
                    text3_surface = font.render(text3, True, font_color)
                    self.model.screen.blit(text3_surface, text3_position)

                    self.model.screen.blit(self.model.xp, (self.model.screen.get_width()-box_size[0]-90, 60))

                    if 0 < self.model.elapsed_time - 3 < 1:
                        self.model.Mediapipe_pose_class.max_level_store = 0

                      
        except Exception as e:
            print(e)
    
        pygame.display.flip()
        
        self.clock.tick(60)