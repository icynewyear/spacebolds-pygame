import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from entity import Player, Alien
from render import screen


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

player = Player(screen, playerIcon, player_speed, playerX, playerY)
alien = Alien(screen, alienIcon, alien_speed, alienX, alienY)
alien2 = Alien(screen, alienIcon, alien_speed, alienX+100, alienY-30)
alien3 = Alien(screen, alienIcon, alien_speed, alienX-100, alienY)

all_sprites.add(player)
all_sprites.add(alien)
all_sprites.add(alien2)
all_sprites.add(alien3)
alien_sprites.add(alien)
alien_sprites.add(alien2)
alien_sprites.add(alien3)
