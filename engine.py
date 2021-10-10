from __future__ import annotations

from typing import TYPE_CHECKING

import sys, pygame, random
from pygame.color import Color

from entity import Alien
from player import Player
from enemy_spawner import EnemySpawner
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from particles import ParticlePrinciple
from backgrounds import ParticleBackground, FlatColorBackgroud
from space_map import SpaceMap, SpaceEvent
from colors import *

from debug import debug


class Engine():
    #screen
    screen_title = "Koboldka"
    icon = pygame.image.load('resources/goblin.png')

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(screen_title)
    pygame.display.set_icon(icon)

    #player
    playerIcon = pygame.image.load('resources/spaceship.png')
    playerX = SCREEN_WIDTH/2 - playerIcon.get_width()/2
    playerY = 480
    player_speed = 10

    #Enemy
    alienIcon = pygame.transform.flip(pygame.image.load('resources/enemy.png'), False, True)
    alienX = int((SCREEN_WIDTH/2 - alienIcon.get_width()/2)-400)
    alienY = 100
    alien_speed = 10

    #Spawner
    spawnerIcon = pygame.image.load('resources/space-station.png')

    all_sprites = pygame.sprite.Group()
    alien_sprites = pygame.sprite.Group()

    def __init__(self):
        #self.bg_image = Background(screen)
        self.bg_color = Color(46, 79, 79)
        self.clock = pygame.time.Clock()
        self.particle1 = ParticlePrinciple(self)

        self.player_move = 0
        self.aliens = []
        self.player = Player(self, self.playerIcon, self.player_speed, self.playerX, self.playerY)
        self.all_sprites.add(self.player)

        self.alien = Alien(self, self.alienIcon, self.alien_speed, 10, self.alienX, self.alienY)
        self.spawner = EnemySpawner(self, self.spawnerIcon, (random.randint(0,800),random.randint(0,400)), self.alien, 100, 4, True)
        self.particle_bg = ParticleBackground(self)
        self.script = [
            (0, SpaceEvent.CHANGE_BACKGROUND, -1, self.particle_bg),
            (50, SpaceEvent.CHANGE_BACKGROUND, -1, FlatColorBackgroud(self, BLACK)),
            (0, SpaceEvent.CHANGE_SPEED, 1, None),
            (35, SpaceEvent.SPAWN_SPAWNER, -1, self.spawner, (400,80)),
            (36, SpaceEvent.SPAWN_SPAWNER, -1, self.spawner, (300,80)),
            (37, SpaceEvent.SPAWN_SPAWNER, -1, self.spawner, (500,80)),
            (300, SpaceEvent.PLAY_SOUND, -1, pygame.mixer.Sound('resources/burp.ogg')),
            (300, SpaceEvent.PLAY_MUSIC, 2, 'resources/galactictrek.wav'),
            (100, SpaceEvent.CHANGE_BACKGROUND, -1 , FlatColorBackgroud(self, (46, 79, 79))),
            (500, SpaceEvent.CHANGE_BACKGROUND, -1, self.particle_bg),
            (200, SpaceEvent.CHANGE_SPEED, 10, None),
            (300, SpaceEvent.SPAWN_SPAWNER, -1, self.spawner, (80,300)),
            #(400, SpaceEvent.CHANGE_POS, 100),
            (500, SpaceEvent.SPAWN_ENEMY, -1, self.alien, (640,0)),
            (500, SpaceEvent.SPAWN_ENEMY, -1, self.alien, (730,0)),
            ]
        self.map = SpaceMap(self, self.script, 2000, 5)

    def run_game(self) -> None:
        """Core Game Loop"""
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
            self.screen.fill(self.bg_color)

            #self.bg_image.update()
            #self.bg_image.render()

            self.all_sprites.update()
            self.particle1.emit()

            self.clock.tick(30)

            self.map.update()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
