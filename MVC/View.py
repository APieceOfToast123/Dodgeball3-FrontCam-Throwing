from MVC.EventManager import *
from Scene.UI_1 import *
import pygame
from pygame.locals import *
import pygame.freetype
import cv2
from Components.Button.Button import button
from Components.Sprite_Engine.Sprite import sprite_engine
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

        pygame.display.set_caption('Test_Project')

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

    def init_page(self):
        self.model.add_button = button((100, 150), self.model.add_button_path, self.model, 2)
        self.model.minus_button = button((100, 250), self.model.minus_button_path, self.model, 2)
        
        self.model.bun_sprite = sprite_engine(self.model.bun_sprite_path, (100, 400), 6, self.model)

    def render(self):
        # Display FPS
        self.model.FPS_class.display_FPS(self.model.img)
        try:
            
            if self.model.currentstate == 1:
            # display the first page
                pass


            if self.model.currentstate == 2:
            # standardize page
                pass



            # Display Mediapipe Pose landmarks
            if self.model.currentstate == 3:
                
            
                
                
            # 显示图像
                
                # print(self.model.Mediapipe_pose_class.direction)
                # print("aaa")
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
             # 设置方框的位置和大小
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
                
            # display the twist direction
                text2 = "please twist {}".format(self.model.Mediapipe_pose_class.direction)
                box_size = (500,100 )
                box_position = (900, 50)
                text2_position = (box_position[0] + 50, box_position[1] + box_size[1] // 2)
                cv2.rectangle(self.model.img, box_position, (box_position[0] + box_size[0], box_position[1] + box_size[1]), box_color, -1)
                cv2.putText(self.model.img, text2, text2_position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)
                
            if self.model.currentstate == 3:
                # 报告游戏结果
                pass
                      
        except Exception as e:
            print(e)
            
       
            
        """
        Draw things on pygame
        """
        empty_color = pygame.Color(0, 0, 0, 0)
        self.model.screen.fill(empty_color)

        # Convert into RGB
        self.model.img = cv2.cvtColor(self.model.img, cv2.COLOR_BGR2RGB)

        # Convert the image into a format pygame can display
        self.model.img = pygame.image.frombuffer(self.model.img.tostring(), self.model.img.shape[1::-1], "RGB")

        # blit the image onto the screen
        self.model.screen.blit(self.model.img, (0, 0))
        
        # Draw button
        self.model.add_button.draw(self.model.screen)
        self.model.minus_button.draw(self.model.screen)

        # Draw sprite
        self.model.bun_sprite.draw(self.model.bun_sprite_time)
       
     


        '''
        Move this part to progress_bar component later
        '''

        
        # progress bar
        white = (255, 255, 255)
        green = (0, 255, 0)
        level = self.model.Mediapipe_pose_class.max_level
        pygame.draw.rect(self.model.screen, green, (50, 50, 100*level, 50))
        if 0 <self.model.elapsed_time -3 < 1:
            self.model.Mediapipe_pose_class.max_level_store = 0
      
   
        # Update the screen
        pygame.display.flip()

        # limit the redraw speed to 30 frames per second
        
        self.clock.tick(60)