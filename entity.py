from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Union

if TYPE_CHECKING:
    from engine import Engine

import pygame, random

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from projectiles import Bullet, BulletManager
from colors import *
from flightpatterns import Flightpath


class SpaceEntity(pygame.sprite.Sprite):
    def __init__(self, engine: Engine):
        pygame.sprite.Sprite.__init__(self)
        self.engine = engine
        self.screen = engine.screen

class SpaceActor(SpaceEntity):
    def __init__(self, engine: Engine, icon, speed: int, x: int, y: int):
        SpaceEntity.__init__(self, engine)
        self.image = icon
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_move_amount = 0.0
        self.y_move_amount = 0.0
        self.bullet_manager = BulletManager(self.engine)

    def shoot(self) -> None:
        pass

    def update(self) -> None:
        self.bullet_manager.update()
        self.bullet_manager.render()

class Alien(SpaceActor):
    def __init__(self, engine: Engine, icon, speed: int, fire_rate: int, x: int, y: int):
        SpaceActor.__init__(self, engine, icon, speed, x, y)
        self.direction = random.randint(0,1)
        self.fire_rate = fire_rate
        self.timer = fire_rate
        self.y_timer = 0
        self.fp = Flightpath(1,(0,300))

    def shoot(self) -> None:
        if self.timer == self.fire_rate:
            self.timer = 0
            coords = (int(self.rect.x+(self.image.get_width()/2)), int(self.rect.y+self.image.get_height()))
            bullet = Bullet(self.bullet_manager, coords, 10, ALIEN_GUN)
            self.bullet_manager.add_projectile(bullet)
        else: self.timer+=1

    def spawn(self, coords: Tuple[int,int], multivar = -1) -> Alien:
        x, y = coords
        new_alien = Alien(self.engine, self.image, self.speed, self.fire_rate, x, y)
        return new_alien

    def move(self) -> Tuple[int,int]:
        move = next(self.fp)
        return move

    def do_movement(self, move: Tuple[int,int]) -> None:
        #X move
        x,y = move
        self.rect.x += x
        #Y move
        self.rect.y += y
        pass

    def check_hits(self) -> None:
            for bullet in self.bullet_manager.projectiles:
                if self.engine.player.rect.collidepoint((bullet.x,bullet.y)):
                    self.bullet_manager.projectiles.remove(bullet)
                    self.engine.player.hp -= 1

    def update(self) -> None:
        self.move()
        self.shoot()
        self.check_hits()
        self.do_movement(self.move())
        self.bullet_manager.update()
        self.bullet_manager.render()
