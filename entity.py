import pygame, random

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from projectiles import Bullet, BulletManager
from colors import *


class SpaceEntity(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen

class SpaceActor(SpaceEntity):
    def __init__(self, screen, icon, speed, x, y):
        SpaceEntity.__init__(self, screen)
        self.image = icon
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_move_amount = 0.0
        self.y_move_amount = 0.0
        self.bullet_manager = BulletManager(self.screen)

    def move(self, x_amount, y_amount):
        self.x_move_amount = x_amount
        self.y_move_amount = y_amount

    def do_movement(self):
        #X move
        self.rect.x += self.x_move_amount
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH-self.image.get_width():
            self.rect.x = SCREEN_WIDTH-self.image.get_width()

        #Y move
        self.rect.y += self.y_move_amount
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > SCREEN_HEIGHT-self.image.get_height():
            self.rect.y = SCREEN_HEIGHT-self.image.get_height()

    def shoot(self):
        pass

    def update(self):
        self.do_movement()
        self.bullet_manager.update()
        self.bullet_manager.render()

class Alien(SpaceActor):
    def __init__(self, screen, icon, speed, x, y):
        SpaceActor.__init__(self, screen, icon, speed, x, y)
        self.direction = random.randint(0,1)

    def shoot(self):
        bullet = Bullet(self.bullet_manager, self.rect.x+(self.image.get_width()/2), self.rect.y+self.image.get_height(), 10, ALIEN_GUN)
        self.bullet_manager.add_projectile(bullet)

    def move(self):
        if self.direction == 1:
            self.x_move_amount += self.speed
            if self.rect.x >= SCREEN_WIDTH-self.image.get_width(): self.direction = 0
        elif self.direction == 0:
            self.x_move_amount -= self.speed
            if self.rect.x <= 0: self.direction = 1
        self.y_move_amount = random.randint(-self.speed*3,self.speed*3)

    def update(self):
        self.move()
        self.shoot()
        super().update()


class Player(SpaceActor):
    def __init__(self, screen, icon, speed, x, y):
        SpaceActor.__init__(self, screen, icon, speed, x, y)
        self.player_move = 0

    def shoot(self):
        bullet = Bullet(self.bullet_manager, self.rect.x+(self.image.get_width()/2), self.rect.y, -10, PLAYER_GUN)
        self.bullet_manager.add_projectile(bullet)

    def check_hits(self, alien_sprites):
        for asprite in alien_sprites:
            for bullet in self.bullet_manager.projectiles:
                if bullet.rect.colliderect(asprite.rect):
                    print(asprite)

    def update(self):
        self.move(self.player_move,0)
        super().update()
