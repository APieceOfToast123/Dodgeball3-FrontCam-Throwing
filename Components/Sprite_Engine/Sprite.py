import pygame
import time

class sprite_engine():
    def __init__(self, path, pos, amount, model):
        
        self.model = model
        self.amount = amount
        self.imgList = []
        self.pos = pos
        self.current_sprite = 0
        
        # loop all images in the folder
        for i in range(1, self.amount+1):
            img = pygame.image.load(path + str(i) + ".png").convert_alpha()
            self.imgList.append(img)

        self.img = self.imgList[self.current_sprite]

        self.starting_time = time.time()
    
    def draw(self, speed):
        self.model.screen.blit(self.img, self.pos)
        current_time = time.time()
        remaining_time = current_time - self.starting_time
        self.current_sprite = remaining_time / speed * self.amount
        self.actucal_sprite = int(self.current_sprite)
        if current_time - self.starting_time >= speed:
            self.starting_time = current_time
            self.current_sprite = 0
            self.actucal_sprite = 0
        self.img = self.imgList[self.actucal_sprite]



