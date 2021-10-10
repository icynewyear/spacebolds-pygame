from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Union

if TYPE_CHECKING:
    from engine import Engine

import pygame, random

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from projectiles import Bullet, BulletManager
from entity import SpaceActor
from colors import *
from flightpatterns import Flightpath


class Player(SpaceActor):
    def __init__(self, engine: Engine, icon, speed: int, x: int, y: int):
        SpaceActor.__init__(self, engine, icon, speed, x, y)
        self.player_move = 0
        self._hp = 10
        self.maxhp = 10
        self.dead = False

    @property
    def hp(self) -> int:
        return self._hp

    @hp.setter
    def hp(self, value: int) -> None:
        self._hp = max(0, min(value, self.maxhp))
        if self._hp == 0:
            self.die()

    def die(self) -> None:
        if self.dead == False:
            gameover_sound = pygame.mixer.Sound('resources/gameover.ogg')
            gameover_sound.play()
            self.kill()
            self.dead = True

    def shoot(self) -> None:
        coords = (int(self.rect.x+(self.image.get_width()/2)), self.rect.y)
        bullet = Bullet(self.bullet_manager, coords, -10, PLAYER_GUN)
        self.bullet_manager.add_projectile(bullet)

    def check_hits(self) -> None:
        for asprite in self.engine.alien_sprites.sprites():
            for bullet in self.bullet_manager.projectiles:
                if asprite.rect.collidepoint((bullet.x,bullet.y)):
                    self.bullet_manager.projectiles.remove(bullet)
                    asprite.kill()

    def renderHP(self) -> None:
        pygame.draw.rect(self.screen, RED, (20,570,self.maxhp*20,20))
        pygame.draw.rect(self.screen, BLUE, (20,570,self.hp*20,20))

    def move(self, x_amount: float, y_amount: float) -> Tuple[float,float]:
        self.x_move_amount = x_amount
        self.y_move_amount = y_amount
        return (x_amount,y_amount)

    def do_movement(self, move: Tuple[float,float]) -> None:
        #X move
        x,y = move
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

    def update(self) -> None:
        if self.dead == False:
            self.do_movement(self.move(self.x_move_amount, self.y_move_amount))
            self.renderHP()
            self.move(self.player_move,0)
            self.check_hits()
            super().update()
