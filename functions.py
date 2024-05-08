import pygame
from random import randint, choice
from math import floor

def display_score():
    global current_time
    current_time = pygame.time.get_ticks() / 1000 - starttime
    score_surf = fontObj.render(f"Score: {int(current_time)}",False,(64,64,64))
    score_rect = score_surf.get_rect(center = (300,50))
    screen.blit(score_surf,score_rect)

def collision_check():

    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        return True # True if collision is detected
    else:
        return False

def write_score(score):
    with open("highscore.txt", 'w') as file:
        file.write(str(floor(score)))

def read_score():
    with open("highscore.txt", 'r') as file:
        return int(file.read())