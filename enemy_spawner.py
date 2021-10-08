import pygame

class EnemySpawner(pygame.sprite.Sprite):
    def __init__(self, engine, enemy, delay, num_to_spawn = -1):
        pygame.sprite.Sprite.__init__(self)
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
            new_enemy = self.enemy
            if current_timer == self.delay:
                current_timer = 0
                yield new_enemy
                if self.num_to_spawn != -1: self.num_to_spawn -= 1
            else:
                current_timer += 1
