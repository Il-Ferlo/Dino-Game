import pygame 
import math
import random
import os

import functions_and_variables as fv
import player as pl
import BackGround as BK

pygame.init()

menu=[pygame.image.load(os.path.join("assest/Menu","PLAY.png")),
         pygame.image.load(os.path.join("assest/Menu","RECORD.png"))]

selected = 0

running=True

clock=pygame.time.Clock()

cloud=BK.Cloud()

game_speed = 14

scroll = 0 
image_with = fv.dirt.get_width()
tites = math.ceil(fv.screen_w/image_with)+1

def background():
    global scroll  # Per usare la variabile globale scroll
    y = 380
    image_width = fv.dirt.get_width()
    titles = math.ceil(fv.screen_w / image_width) + 1
    for i in range(0, titles):
        pl.screen.blit(fv.dirt, (i * image_width + scroll, y))

    scroll -= 15

    # Resetta scroll quando ha scorsi tutta l'immagine
    if abs(scroll) > image_width:
        scroll = 0



pygame.font.init()

       #Font(file_path=None, size=12) -> Font
font = pygame.font.Font('Pokemon GB.ttf',20)

text = 'click me'

points = 0

def score():
    global points, game_speed, font
    points+=1
  
    if points % 100==0:
        game_speed +=1

    #           render(       text,          antialias, color, background=None) -> Surface
    text = font.render("score: " + str(points), True, "black")

    textRect = text.get_rect()
    textRect.center = (1000,40)
    pl.screen.blit(text,textRect)

play_button = menu[0]

score_button = menu[1]

death=0

class Scene:
    def draw(self, screen: pygame.Surface):
        pass

    def handle_event(self, event):
        pass

class Play(Scene): 
    def __init__(self):
        self.player = pl.Dino()
        self.obstacles = []
        self.difficulty = 50/100
        self.frames = 0

    def draw(self, screen: pygame.Surface):
        self.frames += 1 
        
        screen.fill((255,255,255))
        userInpunt = pygame.key.get_pressed()

        background()

        cloud.draw(BK.screen)
        cloud.update()

        if random.random() < self.difficulty and self.frames%60==0:                      #ogni frame, 1% (1/100 = 0.01) di possibilità di ostacolo
            self.obstacles.append(random.choice([BK.Cactus(fv.cactus_list), BK.Bird()]))

        for obstacle in self.obstacles:
            obstacle.update()
            obstacle.draw(BK.screen)

            if obstacle.rect.x < -obstacle.rect.width:                                   #rimuovo ostacolo quando esce dallo schermo 
                self.obstacles.remove(obstacle)

            global selected
            if self.player.is_colliding(obstacle):
                self.player.game_over = True
                selected = 3

        score()
        self.player.update(userInpunt)
        self.player.draw(pl.screen)

        self.difficulty +=(50/100)/(100*30)

    def handle_event(self, event):
         global selected
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                selected = 0

class Menu(Scene):
    
    def __init__(self):
        super().__init__()

        self.image_play=play_button

        self.image_score=score_button

        self.screen_w = fv.screen_w 
        self.screen_h = fv.screen_h

        self.screen_rect = pl.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height

        self.image_play_rect=self.image_play.get_rect()
        self.image_score_rect=self.image_score.get_rect()

        self.offeset_x=150

        #self.offeset_y= (self.screen_h/3)

        self.image_play_rect.x=(self.screen_w/2) - (self.image_play_rect.width/2) - self.offeset_x
        self.image_score_rect.x=(self.screen_w/2) - (self.image_score_rect.width/2) + self.offeset_x

        self.image_play_rect.y=(self.screen_h/2)-(self.image_play_rect.height/2)
        self.image_score_rect.y=(self.screen_h/2)-(self.image_score_rect.height/2)
        

    def draw(self, screen: pygame.Surface):
        
        screen.fill((0x53,0x53,0x53)) 

        screen.blit(self.image_play, (self.image_play_rect.x, self.image_play_rect.y))
    
        screen.blit(self.image_score, (self.image_score_rect.x, self.image_score_rect.y))

    def handle_event(self, event):
        global selected, text
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event)
            
            #print(f"rect: {self.image_play_rect}, play: {self.image_play_rect.collidepoint(event.pos)}")
            #print(f"rext: {self.image_score_rect}, score: {self.image_score_rect.collidepoint(event.pos)}")

            if self.image_play_rect.collidepoint(event.pos):
                selected = 4
            
            elif self.image_score_rect.collidepoint(event.pos):
                selected = 2

class Score(Scene):
    def __init__(self):
        super().__init__()

        self.font = pygame.font.Font('Pokemon GB.ttf', 38)
        self.font2 = pygame.font.Font('Pokemon GB.ttf', 45)
        self.back_img = pygame.image.load(os.path.join("assest/Menu","Back.png"))
        self.rect=self.back_img.get_rect()

        self.pos=(10,10)

        self.text =  self.font.render(fv.score_max(),True, "white")
        self.text2 = self.font2.render("the best score",True, "white")
        
        self.text_rect = self.text.get_rect()
        self.text2_rect = self.text2.get_rect()

        self.screen_w = fv.screen_w 
        self.screen_h = fv.screen_h

        self.text_rect.x = (self.screen_w/2) - (self.text_rect.width/2)

        self.text2_rect.x = (self.screen_w/2) - (self.text2_rect.width/2)

        self.text_rect.y = (self.screen_h/2) - (self.text_rect.height/2) + 50

        self.text2_rect.y = (self.screen_h/2) - (self.text2_rect.height/2) - 100


    def draw(self,screen):
        screen.fill((0x53,0x53,0x53)) 

        screen.blit(self.text, ( self.text_rect.x,  self.text_rect.y))
        screen.blit(self.text2, ( self.text2_rect.x,  self.text2_rect.y))

        screen.blit(self.back_img,self.pos)

    def handle_event(self, event):
         global selected
         if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos): 
                selected = 0

    def reset(self):
         self.__init__()

class input_box(Scene):
    def __init__(self):
        self.input_box=pygame.Rect(100, 100, 140, 32)
        self.color_inactive = pygame.Color('red')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = True

        self.font = pygame.font.Font('Pokemon GB.ttf', 38)
        
        self.screen_w = fv.screen_w 
        self.screen_h = fv.screen_h

        self.screen_rect = pl.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height

        self.input_box.x=(self.screen_w/2) - (self.input_box.width/2)
        self.input_box.y=(self.screen_h/2)-(self.input_box.height/2)
        self.txt_surface = font.render("click me", True, self.color, "white")

    def handle_event(self, event):
        
        global text,selected

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Change the current color of the input box.
            self.color =self.color_active if self.active else self.color_inactive
           
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    if text != 'click me':
                        selected = 1
                    
                    #print(text) # for debuging
                elif event.key == pygame.K_BACKSPACE:
                        if text == 'click me':
                            text = ''
                        else:
                            text = text[:-1]
                else:
                    if text == 'click me':
                        text = ''
                    text += event.unicode 

        self.txt_surface = font.render(text, True, self.color, "white")

    def draw(self, screen:pygame.Surface):
        screen.fill((0x53,0x53,0x53)) 
        
        screen.blit(self.txt_surface, ( self.input_box.x,  self.input_box.y))

class GameOver(Scene):
    def __init__(self):
        super().__init__()

        self.screen_w = fv.screen_w 
        self.screen_h = fv.screen_h
            
        self.game_over_img = pygame.image.load(os.path.join("assest/GameEndInterface", "GameOver.png"))

        self.screen_rect = pl.screen.get_rect()
        self.screen_width = self.screen_rect.width
        self.screen_height = self.screen_rect.height

        self.game_over_img_rect=self.game_over_img.get_rect()

        self.game_over_img_rect.x=(self.screen_w/2) - (self.game_over_img_rect.width/2)
        self.game_over_img_rect.y=(self.screen_h/2)-(self.game_over_img_rect.height/2)-200+50

        self.coordinate = (self.game_over_img_rect.x,self.game_over_img_rect.y)

        self.title_end = font.render("press R to restart the game", True, 0x535353ff)  # color game over img = 0x535353ff

        self.text_rect = self.title_end.get_rect()
        self.text_rect.x=(self.screen_w/2) - (self.text_rect.width/2)

        self.restart_img = pygame.image.load(os.path.join("assest/GameEndInterface", "Reset.png"))
        self.restart_img_rect=self.restart_img.get_rect()
        self.restart_img_rect.x=(self.screen_w/2) - (self.restart_img_rect.width/2)
        self.restart_img_rect.y=(self.screen_h/2)-(self.restart_img_rect.height/2)-200+100
    def draw(self, screen: pygame.Surface):
        
        screen.blit(self.restart_img,(self.restart_img_rect.x,self.restart_img_rect.y))  
        screen.blit(self.title_end, (self.text_rect.x, self.game_over_img_rect.y + 125))
        screen.blit(self.game_over_img,self.coordinate)

    def handle_event(self, event):
        global selected, points

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            scenes[1] = Play()
            GameOver.data()
            points = 0
           
            selected = 1   

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if self.restart_img_rect.collidepoint(event.pos): 
                scenes[1] = Play()
                GameOver.data()
                points = 0
           
                selected = 1



    def data():
        global points, text
        fv.register_point_and_names(points,text)

#0 = Menu, 1 = Play, 2 = Score, 3 = GameOver
scenes: list[Scene] = [Menu(), Play(), Score(), GameOver(), input_box()]

while running:
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        scenes[selected].handle_event(event)
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                selected = 0
                text='click me'
                scenes[2].reset()

    scenes[selected].draw(pl.screen)

    clock.tick(30)
    
    pygame.display.update() 