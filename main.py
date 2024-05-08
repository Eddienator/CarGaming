import pygame
from random import randint, choice
import sys
from math import floor

# Functions
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

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Sprites/CarDuuuude.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (150,580))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 580:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= grass_rect.top + 10:
            self.rect.bottom = grass_rect.top + 10

    def update(self):
        self.player_input()
        self.apply_gravity()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == "cone":
            cone = pygame.image.load('Sprites/cone.png')
            self.frames = [cone]
            y_pos = grass_rect.top
        
        if type == "man":
            man1 = pygame.image.load('Sprites/ConstructorManBoy Parts/CoolMan1.png')
            man2 = pygame.image.load('Sprites/ConstructorManBoy Parts/CoolMan2.png')
            man3 = pygame.image.load('Sprites/ConstructorManBoy Parts/CoolMan3.png')
            man4 = pygame.image.load('Sprites/ConstructorManBoy Parts/CoolMan4.png')
            self.frames = [man1,man2,man3,man4]
            y_pos = grass_rect.top

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x < -100:
            self.kill() # Removes itself from the game

    def update(self):
        self.animation_state()
        self.destroy()

        self.rect.x -= 5

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Epic Game")
clock = pygame.time.Clock()
current_time = 0

# Surfaces, rects, and texts
fontObj = pygame.font.Font("Fonts/Cool.TTF",40)
starttime = 0

grass_surf = pygame.image.load('Sprites/roadbig.png').convert_alpha()
grass_rect = grass_surf.get_rect(topleft = (0,570))

day_surf = pygame.image.load('Sprites/Scrollable-export.png').convert()
day_rect = day_surf.get_rect(topleft = (0,0))

start_surf = pygame.image.load('Sprites/STARTSCREEN.png')

gameover_surf = pygame.image.load('Sprites/You Suck.png')

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1100)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

state = "START"
day_night = 1 # True means day, false means night

while True:
    # Event listener
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit("Program Stopped")
            
        if state == "START":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = "RUNNING"
                    starttime = pygame.time.get_ticks() / 1000
                if event.key == pygame.K_p:
                    write_score(0)

        if state == "RUNNING":
            if event.type == obstacle_timer: # Continously adds obstacles
                obstacle_group.add(Obstacle(choice(["cone","cone","cone","man"])))

        if state == "LOST":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    state = "RUNNING"
                    starttime = pygame.time.get_ticks() / 1000

    # Game loop

    if state == "START":
        screen.blit(start_surf,(0,0))
        player.draw(screen)
        highscore = read_score()
        highscore_surf = fontObj.render(f"{highscore}",False,(0,0,0))
        screen.blit(highscore_surf,(375,312))

    if state == "RUNNING":

        # Day/Night cycle

        screen.blit(day_surf, day_rect)

        screen.blit(grass_surf, grass_rect)

        # Obstacles
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Player
        player.draw(screen)
        player.update()

        # Collision Check
        if collision_check():
            state = "LOST"
        else:
            state = "RUNNING"

        # Score
        display_score()

    if state == "LOST":
        screen.blit(gameover_surf, (0,0))
        obstacle_group.empty()
        if int(current_time) > highscore:
            write_score(current_time) # Current_time is the score

    pygame.display.update()
    clock.tick(60) # 60 FPS Cap


