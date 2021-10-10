from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Iterator, Optional
if TYPE_CHECKING:
    from engine import Engine
    from entity import SpaceActor, Alien

import pygame
import copy


from debug import debug

pygame.init()

class EnemySpawner(pygame.sprite.Sprite):
    #num_to_spawn set to -1 for infinite. immediate to True to have the first enemy deploy on the first tick
    def __init__(self, engine: Engine, icon, coords: Tuple[int,int], enemy: Alien, delay: int, num_to_spawn: int = -1, immediate: bool = False):
        pygame.sprite.Sprite.__init__(self)
        self.image = icon
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
        self.engine = engine
        self.enemy = enemy
        self.delay = delay
        self.num_to_spawn = num_to_spawn
        self.immediate = immediate
        self.generator_iterator = self.spawn_enemy()

    def __next__(self) -> Optional[SpaceActor]:
        return next(self.generator_iterator)

    def spawn_enemy(self) -> Iterator[Optional[SpaceActor]]:
        current_timer = self.delay if self.immediate else 0
        while self.num_to_spawn >= 0 or self.num_to_spawn == -1:
            if current_timer == self.delay:
                current_timer = 0
                new_enemy = self.enemy.spawn((self.rect.x, self.rect.y))
                yield new_enemy
                if self.num_to_spawn == 1: current_timer = -1 #Lock out loop on last enemy
                if self.num_to_spawn != -1: self.num_to_spawn -= 1 #reduce number to spawn
            elif current_timer == -1: #Lock out timer and spawning
                yield None
            else:
                current_timer += 1 #iterate timer
                yield None

    def update(self) -> None:
        enemy = next(self)
        if enemy != None:
            self.engine.alien_sprites.add(enemy)
            self.engine.all_sprites.add(enemy)

    def spawn(self, coords):
        x, y = coords
        new_spawner = EnemySpawner(self.engine, self.image, (x,y), self.enemy, self.delay, self.num_to_spawn, self.immediate)
        return new_spawner
