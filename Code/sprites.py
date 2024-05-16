from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self,groups,scale):
        super().__init__(groups)
        
        self.animation_index = 0

        self.frames = []
        for i in range(1,3):
            car_image = pygame.image.load(join('Sprites','Player',f'CarDuuuude{i}.png')).convert_alpha()
            car_frame = pygame.transform.scale(car_image,Vector(car_image.get_size()) * scale)

            self.frames.append(car_frame)

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_frect(midbottom = (SCREEN_WIDTH / 8,toproad))
        self.gravity = 0

        self.mask = pygame.mask.from_surface(self.image)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= toproad:
            self.gravity = -12

    def apply_gravity(self,dt):
        self.gravity += 70 * dt  # All movement must include delta time!!
        self.rect.y += self.gravity
        if self.rect.bottom >= toproad:
            self.rect.bottom = toproad + 5

    def animation(self,dt):
        self.animation_index += 5 * dt
        if self.animation_index >= len(self.frames): self.animation_index = 0

        self.image = self.frames[int(self.animation_index)]

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,dt):
        self.player_input()
        self.apply_gravity(dt)
        self.animation(dt)

class Road(pygame.sprite.Sprite):
    def __init__(self,groups,scale):
        super().__init__(groups)

        road_image = pygame.image.load(join('Sprites','Road','roadbig.png')).convert()

        self.full_height = road_image.get_height() * scale
        self.full_width = road_image.get_width() * scale
        self.full_sz_image = pygame.transform.scale(road_image,(self.full_width,self.full_height))
        
        self.ypos = SCREEN_HEIGHT - self.full_sz_image.get_height()

        self.image = pygame.Surface((self.full_width * 2, self.full_height)) # * 2 because we are going to need the same picture twice for the background scroll.
        self.image.blit(self.full_sz_image,(0,0)) 
        self.image.blit(self.full_sz_image,(self.full_width,0))

        self.rect = self.image.get_frect(topleft = (0,self.ypos))  # Put the surface at the correct y-position.
        self.pos = Vector(self.rect.topleft)

        global toproad
        toproad = self.rect.top
    
    def update(self,dt):
        self.pos.x -= 650 * dt

        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,groups,type,scale):
        super().__init__(groups)

        self.animation_index = 0
        self.pos = Vector(SCREEN_WIDTH + randint(100,300), toproad)
        self.type = type

        self.frames = []

        # Load either cone or man frames depending on type.
        if self.type == "cone":
            cone_image = pygame.image.load(join('Sprites','Obstacles','cone.png'))
            cone_frame = pygame.transform.scale(cone_image,Vector(cone_image.get_size()) * scale)
            self.frames.append(cone_frame)

        if self.type == "man":

            for i in range(1,5):
                man_image = pygame.image.load(join('Sprites','ConstructorManBoy Parts',f'CoolMan{i}.png')).convert_alpha()
                man_image = pygame.transform.flip(man_image,flip_x=True,flip_y=False) # Makes the man face the correct direction
                man_frame = pygame.transform.scale(man_image,Vector(man_image.get_size()) * scale)
                self.frames.append(man_frame)  

        self.image = self.frames[self.animation_index]

    def animation(self,dt):

        self.animation_index += 5 * dt
        if self.animation_index >= len(self.frames): self.animation_index = 0

        self.image = self.frames[int(self.animation_index)]

        # Mask
        self.mask = pygame.mask.from_surface(self.image)

    def destroy(self):
        if self.pos.x <= -100:
            self.kill() # Removes itself from the game

    def move(self, dt):
        self.direction = -750 * dt
        self.pos.x += self.direction
        self.rect = self.image.get_frect(midbottom = self.pos)


    def update(self,dt):
        self.destroy()
        self.animation(dt)
        self.move(dt)

class BG(pygame.sprite.Sprite):
    def __init__(self,groups,scale):
        super().__init__(groups)

        bg_surf = pygame.image.load(join('Sprites','Background','Scrollable-export.png'))
        self.full_height = bg_surf.get_height() * scale
        self.full_width = bg_surf.get_width() * scale
        self.full_sz_image = pygame.transform.scale(bg_surf,(self.full_width,self.full_height))

        self.image = pygame.Surface((self.full_width * 2, self.full_height)) # * 2 because we are going to need the same picture twice for the background scroll.
        self.image.blit(self.full_sz_image,(0,0))
        self.image.blit(self.full_sz_image,(self.full_width,0))

        self.rect = self.image.get_frect(topleft = (0,0))  # Put the surface at the correct y-position.
        self.pos = Vector(self.rect.topleft)
    
    def animate(self,dt):
        self.pos.x -= 50 * dt

        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

    def update(self,dt):
        self.animate(dt)

class Coin(pygame.sprite.Sprite):
    def __init__(self,groups,scale):
        super().__init__(groups)

        self.pos = Vector(SCREEN_WIDTH + randint(100,300), toproad)
        self.image = pygame.image.load(join('Sprites','Teh Coin.png')).convert_alpha()
        self.frame = pygame.transform.scale(self.image,Vector(self.image.get_size()) * scale)

        self.mask = pygame.mask.from_surface(self.image)

    def move(self, dt):
        self.direction = -750 * dt
        self.pos.x += self.direction
        self.rect = self.image.get_frect(midbottom = self.pos)

    def destroy(self):
        if self.pos.x <= -100:
            self.kill() # Removes itself from the game

    def update(self,dt):
        self.move(dt)
        self.destroy()