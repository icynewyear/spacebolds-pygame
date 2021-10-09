from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, List

if TYPE_CHECKING:
    from engine import Engine

import pygame

from settings import SCREEN_HEIGHT

class BulletManager():
    def __init__(self, engine: Engine):
        pygame.init()
        self.screen = engine.screen
        self.projectiles = []

    def add_projectile(self, projectile: Bullet) -> None:
        self.projectiles.append(projectile)

    def render(self) -> None:
        if self.projectiles:
            self.trim_projectiles()
            for projectile in self.projectiles:
                projectile.render()

    def update(self) -> None:
        if self.projectiles:
            for projectile in self.projectiles:
                projectile.update()

    def trim_projectiles(self) -> None:
        trimmed_projectiles = []
        if self.projectiles:
            for projectile in self.projectiles:
                if projectile.y > SCREEN_HEIGHT or projectile.y < 0:
                    projectile.remove()
                else:
                    trimmed_projectiles.append(projectile)
            self.projectiles = trimmed_projectiles

class Bullet():
    def __init__(self, manager: BulletManager, coords: Tuple[int,int], direction: int, color: Tuple[int,int,int]):
        self.manager = manager
        self.x, self.y = coords
        self.direction = direction
        self.color = color

        self.image = pygame.Surface([3,3])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()

    def render(self) -> None:
        pygame.draw.circle(self.manager.screen, self.color, [self.x,self.y], 5)

    def update(self) -> None:
        self.y += self.direction

    def remove(self) -> None:
        pass
