import pygame 
import os
import json

screen_h=600 #altezza
screen_w=1200 #larghezza 

#pygame.init()

running=[pygame.image.load(os.path.join("assest/Dino","DinoRun1.png")),
         pygame.image.load(os.path.join("assest/Dino","DinoRun2.png"))]

jumping=[pygame.image.load(os.path.join("assest/Dino","DinoJump.png"))]

ducking=[pygame.image.load(os.path.join("assest/Dino","DinoDuck1.png")),
         pygame.image.load(os.path.join("assest/Dino","DinoDuck2.png"))]

small_cactus=[pygame.image.load(os.path.join("assest/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("assest/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("assest/Cactus", "SmallCactus3.png"))]
large_cactus=[pygame.image.load(os.path.join("assest/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("assest/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("assest/Cactus", "LargeCactus3.png"))]

cloud = pygame.image.load(os.path.join("assest/Ambient","Cloud.png"))

dirt = pygame.image.load(os.path.join("assest/Ambient","Track.png"))

bird = [pygame.image.load(os.path.join("assest/Bird","Bird1.png")),
         pygame.image.load(os.path.join("assest/Bird","Bird2.png"))]

game_over = pygame.image.load(os.path.join("assest/Dino", "DinoDead.png"))



cactus_list=small_cactus + large_cactus #6 elemnti 
  
def register_point_and_names(number:int ,nome:str ):
    
    if not (os.path.exists("points.json")):
        with open("points.json", 'w') as file: 
            file.write("{}")
        
    score = load_points_and_names()
    score[nome] = number

    with open("points.json", "w") as file:
        json.dump(score, file)

def load_points_and_names():
    with open("points.json") as file:
        return json.load(file)

def score_max():
    score = load_points_and_names()

    names_points = list(score.items())
    point = list(score.values())

    index = point.index(max(point))

    name,number = names_points[index]

    return f"{name}: {number}"