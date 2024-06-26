from settings import *
from sprites import Obstacle, Road, BG, Player, Coin, FloatingRoad
from math import floor

def write_score(score):
    with open("highscore.txt", 'w') as file:
        file.write(str(floor(score)))

def read_score():
    with open("highscore.txt", 'r') as file:
        return int(file.read())


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption("Epic Game")
        self.clock = pygame.time.Clock()

        self.state = "START"

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.floatingroad = pygame.sprite.Group()

        # Scale factor
        bg_height = pygame.image.load('Sprites/Background/Scrollable-export.png').get_height()
        self.scale_factor = SCREEN_HEIGHT / bg_height     

        # Sprite setup
        self.obstacletypes = ["cone","cone","cone","man"]
        
        BG(self.all_sprites,self.scale_factor)
        Road(self.all_sprites,self.scale_factor)
        self.player = Player(self.all_sprites,self.scale_factor)

        # Score setup
        self.score = 0
        self.font = pygame.font.Font(join('Fonts','Cool.TTF'))
        self.highscorefont = pygame.font.Font(join('Fonts','Cool.TTF'),35)
        self.startoffset = 0

        self.obtainedcoins = []


        # User event
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer,800)


    def run(self):
        last_time = time.time()
        while True:

            # Delta time
            dt = time.time() - last_time
            last_time = time.time()

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit("Game Stopped by Player")
                

                if self.state == "START":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.startoffset = pygame.time.get_ticks()  # Startoffset counts the current time, so the score timer can subtract from it and start at  0.
                            self.state = "RUNNING"                    
                
                if self.state == "RUNNING":
                    if event.type == self.obstacle_timer:  # Adds new obstacles or coins
                        if randint(1,100) > 10:
                            Obstacle([self.collision_sprites,self.all_sprites],choice(self.obstacletypes),self.scale_factor)
                        else:
                            Coin([self.coins,self.all_sprites],self.scale_factor)

                        for i in range(1,randint(2,4)):
                            FloatingRoad([self.all_sprites,self.floatingroad],self.scale_factor, i)
                if self.state == "LOST":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            
                            self.newgame = Game()
                            self.newgame.run() 
                            pygame.quit() 
                        """                             # Restarts if the player presses SPACE.

                            BG(self.all_sprites,self.scale_factor)
                            Road(self.all_sprites,self.scale_factor)
                            self.player = Player(self.all_sprites,self.scale_factor)
                            self.startoffset = pygame.time.get_ticks()
                            self.state = "RUNNING" """

            if self.state == "START":
                self.startscreen_surf = pygame.image.load(join('Sprites','StartandGameOver','STARTSCREEN.png'))
                self.startscreenimage = pygame.transform.scale(self.startscreen_surf,Vector(self.startscreen_surf.get_height()) * self.scale_factor)
                self.screen.blit(self.startscreenimage, (0,0))

                # Print highscore
                self.high_score = read_score()
                highscore_surf = self.highscorefont.render(str(self.high_score),False,(0,0,0),)
                highscore_surf = pygame.transform.scale(highscore_surf,Vector(highscore_surf.get_size()) * self.scale_factor)
                highscore_rect = highscore_surf.get_frect(center = (SCREEN_WIDTH / 1.5, SCREEN_HEIGHT / 1.8))
                self.screen.blit(highscore_surf, highscore_rect)
            
            if self.state == "RUNNING":
                self.screen.fill('black')

                self.all_sprites.update(dt)
                self.all_sprites.draw(self.screen)
                self.scorecounter()

                self.check_collisions() 


            if self.state == "LOST":
                self.all_sprites.empty()
                self.collision_sprites.empty()

                # Game Over Screen
                self.gameoverscreen_surf = pygame.image.load(join('Sprites','StartandGameOver','You Suck.png'))
                self.gameoverimage = pygame.transform.scale(self.gameoverscreen_surf,Vector(self.gameoverscreen_surf.get_height()) * self.scale_factor)
                self.screen.blit(self.gameoverimage, (0,0))

                # Write highscore?
                current_highscore = read_score()
                total_score = self.score
                if total_score > current_highscore:
                    write_score(total_score)
                self.score = 0
                self.obtainedcoins.clear()

            pygame.display.update()
            self.clock.tick(FRAMERATE)

    def check_collisions(self):
        if pygame.sprite.spritecollide(self.player,self.collision_sprites,False,pygame.sprite.collide_mask):
            self.state = "LOST"
        if pygame.sprite.spritecollide(self.player,self.coins,True,pygame.sprite.collide_mask):
            self.obtainedcoins.append(1)
        if pygame.sprite.spritecollide(self.player,self.floatingroad,False,pygame.sprite.collide_mask):
            if self.player.gravity > 0:
                self.player.rect.bottom = 625
                self.player.gravity = 0  
                self.player.isGrounded = True
            else:
                self.player.rect.bottom = 700
                self.player.gravity = 1
            

    def scorecounter(self):
        self.score = int(((pygame.time.get_ticks() - self.startoffset) / 1000)+len(self.obtainedcoins) * 10)
        score_surf = self.font.render(str(self.score),False,(0,0,0))
        score_surf = pygame.transform.scale(score_surf,Vector(score_surf.get_size()) * self.scale_factor)
        score_rect = score_surf.get_frect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 10))
        self.screen.blit(score_surf, score_rect) 


if __name__ == '__main__':
    game = Game()
    game.run()

