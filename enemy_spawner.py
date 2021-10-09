import pygame
import copy


from debug import debug


class EnemySpawner(pygame.sprite.Sprite):
    def __init__(self, engine, icon, coords, enemy, delay, num_to_spawn = -1):
        pygame.sprite.Sprite.__init__(self)
        self.image = icon
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coords
        self.engine = engine
        self.enemy = enemy
        self.delay = delay
        self.num_to_spawn = num_to_spawn
        self.generator_iterator = self.spawn_enemy()

    def __next__(self):
        return next(self.generator_iterator)

    def spawn_enemy(self):
        current_timer = 0
        while self.num_to_spawn > 0 or self.num_to_spawn == -1:
            if current_timer == self.delay:
                current_timer = 0
                new_enemy = self.enemy.spawn((self.rect.x, self.rect.y))
                yield new_enemy
                if self.num_to_spawn != -1: self.num_to_spawn -= 1
            else:
                current_timer += 1
                yield None

    def update(self):
        enemy = next(self)
        if enemy != None:
            self.engine.alien_sprites.add(enemy)
            self.engine.all_sprites.add(enemy)
