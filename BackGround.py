import pygame
import functions_and_variables as fv
import random

screen = pygame.display.set_mode((fv.screen_w,fv.screen_h))

game_speed = 14

class Cloud:
    global screen

    def __init__(self, minY=50, maxY=100):
        self.x = fv.screen_w + random.randint(800,1000) 
        self.y = random.randint(minY, maxY)

        self.image = fv.cloud
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed

        if self.x < -self.width:
            self.x = fv.screen_w + random.randint(2500,3000) 
            self.y = random.randint(50,100)

    def draw(self,screen=screen):
        
        screen.blit(self.image,(self.x,self.y))

class Obstacle: #Sottoclasse per gli ostacoli, tutte le sottoclassi di Obstacle, avranno la proprietà `self.rect`
    rect: pygame.Rect

class Bird(Obstacle):
    def __init__(self, minY=185, maxY=290):  
        self.range = (minY, maxY)
        self.step_index = 0
        self.images: list[pygame.Surface] = fv.bird
        self.rect = self.images[self.step_index // 5].get_rect()
        self.rect.x = fv.screen_w
        self.rect.y = random.randint(minY, maxY)


    def update(self):
        self.rect.x -= game_speed
        self.step_index += 1
        
        if self.step_index >= len(self.images) * 5:
            self.step_index=0 

        x, y = self.rect.x, self.rect.y
        
        self.rect = self.images[self.step_index // 5].get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self,screen=screen):
        screen.blit(self.images[self.step_index // 5], (self.rect.x,self.rect.y))

        # pygame.draw.rect(screen, "red", self.rect, width=1) # hit box


class Cactus(Obstacle):
    def __init__(self, list:list[pygame.Surface], variant: int=None):
        self.image_list = list         
        self.index = variant or random.randint(0, len(self.image_list) - 1)
        self.y1 = 325
        self.y2 = 300
        self.rect = self.image_list[self.index].get_rect()

        if self.index <=3:
            self.rect.y = self.y1
        elif self.index >3 and self.index<=5:
            self.rect.y = self.y2

        self.rect.x = fv.screen_w

    def update(self):
        self.rect.x -= game_speed
        #self.index = random.randint(0,5)
        
    def draw(self,screen=screen):
        if self.index <=3:
            screen.blit(self.image_list[self.index],(self.rect.x,self.y1))

        elif self.index >3 and self.index<=5:
            screen.blit(self.image_list[self.index],(self.rect.x,self.y2))

        #pygame.draw.rect(screen, "red", self.rect, width=1) # hit box