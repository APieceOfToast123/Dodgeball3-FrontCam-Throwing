import pygame
import time

# Button with different stages: Normal, Hovered, Clicked
class button():
    def __init__(self, pos, pathImg, model, scale=1):

        self.model = model

        img = pygame.image.load(pathImg).convert_alpha()

        self.width, self.height = img.get_size()
        img = pygame.transform.smoothscale(img, (int(self.width * scale), int(self.height * scale)))

        # Split image to get frame for each stage
        self.width, self.height = img.get_size()
        self.heightSingleFrame = int(self.height / 3)
        self.imgList = []

        for i in range(3):
            imgCrop = img.subsurface((0, i * self.heightSingleFrame, self.width, self.heightSingleFrame))
            self.imgList.append(imgCrop)

        self.img = self.imgList[0]
        self.rectImg = self.imgList[0].get_rect()
        self.pos = pos
        self.rectImg.center = self.pos
        self.control_time = 0.35
        self.button_control_time = time.time()

    def draw(self, surface):
        surface.blit(self.img, self.rectImg)

    def CheckisClicked(self):
        self.state = None
        # Get mouse position to check if inside button
        posMouse = pygame.mouse.get_pos()
        self.img = self.imgList[0]

        if self.rectImg.collidepoint(posMouse):
            if pygame.mouse.get_pressed()[0] and time.time() - self.button_control_time > self.control_time:
                self.img = self.imgList[2]  # Clicked
                
                if self.state != "clicked":

                    self.state = 'clicked'
                    self.button_control_time = time.time()
                    # clear all pygame.key.get_pressed() event
                    pygame.event.clear()
                else:
                    self.state = None
            else:    
                self.img = self.imgList[1]  # Hovered
                if self.state != "hover" and self.state != "clicked":

                    self.state = 'hover'
                else:
                    self.state = None
        else:
            self.state = None
            
        return self.state