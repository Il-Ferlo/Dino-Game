import pygame
import functions_and_variables as fv

import BackGround as BK

screen = pygame.display.set_mode((fv.screen_w,fv.screen_h))

class Dino:
    x_pos = 80
    y_pos = 310 

    pos_duck = 340 
    jump_y_val = 0.5

    gravity = 18

    def __init__(self):
        self.duck_img = fv.ducking
        self.run_img = fv.running
        self.jump_img = fv.jumping
        self.game_over_img = fv.game_over
        self.game_over=False

        self.animations = (self.run_img, self.duck_img, self.jump_img)
        self.state = 0    

        self.velocity_y = 0
        self.step_index = 0
        self.image: pygame.Surface = self.animations[self.state][(self.step_index // 5) % len(self.animations[self.state])]

        self.rect: pygame.Rect = self.image.get_rect()

    def run(self):
        self.state = 0
        self.image = self.animations[self.state][(self.step_index // 5) % len(self.animations[self.state])]

        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = 400 - self.rect.height 
        
     
    def duck(self):
        self.state = 1
        self.image = self.animations[self.state][(self.step_index // 5) % len(self.animations[self.state])]

        self.rect = self.image.get_rect()
        self.rect.x = self.x_pos
        self.rect.y = 400 - self.rect.height 
     
    def jump(self):
          self.state = 2
          self.image = self.animations[self.state][(self.step_index // 5) % len(self.animations[self.state])]

          self.rect = self.image.get_rect()
          self.rect.x = self.x_pos
          self.rect.y = 400 - self.rect.height

          self.velocity_y = 60 

    def draw(self, screen):
        if self.game_over: 
            self.image = self.game_over_img

        screen.blit(self.image,(self.rect.x,self.rect.y))

        #pygame.draw.rect(screen, "red", self.rect, width=1) # hit box


    def update(self, userInput): 
        self.step_index += 1  
        if self.step_index >= 10:
               self.step_index=0 


        self.rect.y -= self.velocity_y
        self.rect.y += Dino.gravity #gravità [pixels / frame]

        if self.rect.y + self.rect.height > 400:
            self.run()
            self.rect.y=400 + self.rect.height

        self.velocity_y *= 0.9
        if self.velocity_y <= 0.0001:
            self.velocity_y = 0   

        if userInput[pygame.K_UP] and self.state != 2:
            self.jump() 

        elif userInput[pygame.K_DOWN] and self.state != 2:
            self.duck()

        elif not (self.state == 2 or userInput[pygame.K_DOWN]):
            self.run()

        if self.game_over:
          y = self.rect.y
          self.rect = self.game_over_img.get_rect()

          self.rect.x = self.x_pos
          if self.state == 1: #ducking
               self.rect.y = 400 - self.rect.height
          else:
              self.rect.y = y

    def is_colliding(self, obstacle: BK.Obstacle):
        dyno_left = self.rect.x
        other_left = obstacle.rect.x

        dyno_right = self.rect.x + self.rect.width
        other_right = obstacle.rect.x + obstacle.rect.width

        dyno_top = self.rect.y
        other_top = obstacle.rect.y

        dyno_bottom = self.rect.y + self.rect.height
        other_bottom = obstacle.rect.y + obstacle.rect.height

        return not (dyno_right < other_left or dyno_left > other_right or dyno_top > other_bottom or dyno_bottom < other_top)