import sys, pygame
from pygame.color import Color

from render import screen
from entity import Player, Alien
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from space_map import Star
from particles import ParticlePrinciple
from backgrounds import Background

from debug import debug


class Engine():
    #player
    playerIcon = pygame.image.load('resources/spaceship.png')
    playerX = SCREEN_WIDTH/2 - playerIcon.get_width()/2
    playerY = 480
    player_speed = 10

    #Enemy
    alienIcon = pygame.transform.flip(pygame.image.load('resources/enemy.png'), False, True)
    alienX = SCREEN_WIDTH/2 - alienIcon.get_width()/2
    alienY = 100
    alien_speed = 1

    all_sprites = pygame.sprite.Group()
    alien_sprites = pygame.sprite.Group()

    def __init__(self):
        #self.bg_image = Background(screen)
        self.bg_color = Color(46, 79, 79)
        self.clock = pygame.time.Clock()
        self.particle1 = ParticlePrinciple(screen)
        self.PARTICLE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.PARTICLE_EVENT, 40)
        self.player_move = 0
        self.aliens = []
        self.player = Player(self, screen, self.playerIcon, self.player_speed, self.playerX, self.playerY)
        self.all_sprites.add(self.player)


    def make_aliens(self, num):
        for x in range(num):
            self.aliens.append(Alien(self, screen, self.alienIcon, self.alien_speed, 10, self.alienX, self.alienY-((x+1)*30)))
            self.all_sprites.add(self.aliens[x])
            self.alien_sprites.add(self.aliens[x])

    def run_game(self):
        self.make_aliens(4)

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.player_move = -self.player.speed
                    if event.key == pygame.K_RIGHT:
                        self.player.player_move = self.player.speed
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                        self.player.player_move = 0
                if event.type == self.PARTICLE_EVENT:
                    self.particle1.add_particles()

            # Draw / render
            screen.fill(self.bg_color)

            #self.bg_image.update()
            #self.bg_image.render()

            self.all_sprites.update()
            self.particle1.emit()

            self.clock.tick(30)

            #star_field.draw(screen)
            self.all_sprites.draw(screen)
            pygame.display.flip()
