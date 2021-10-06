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
player_bullets = pygame.sprite.Group()

player = Player(screen, playerIcon, player_speed, playerX, playerY)
alien = Alien(screen, alienIcon, alien_speed, alienX, alienY)

all_sprites.add(player)
all_sprites.add(alien)
alien_sprites.add(alien)
