import pygame

from settings import SCREEN_HEIGHT

class BulletManager():
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.projectiles =[]

    def add_projectile(self, projectile):
        self.projectiles.append(projectile)

    def render(self):
        if self.projectiles:
            self.trim_projectiles()
            for projectile in self.projectiles:
                projectile.render()

    def update(self):
        if self.projectiles:
            for projectile in self.projectiles:
                projectile.update()

    def trim_projectiles(self):
        trimmed_projectiles = []
        if self.projectiles:
            for projectile in self.projectiles:
                if projectile.y > SCREEN_HEIGHT or projectile.y < 0:
                    projectile.remove()
                else:
                    trimmed_projectiles.append(projectile)
            self.projectiles = trimmed_projectiles

class Bullet(pygame.sprite.Sprite):
    def __init__(self, manager, x, y, direction, color):
        pygame.sprite.Sprite.__init__(self)
        self.manager = manager
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color

        self.image = pygame.Surface([3,3])
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()

    def render(self):
        pygame.draw.circle(self.manager.screen, self.color, [self.x,self.y], 5)

    def update(self):
        self.y += self.direction


    def remove(self):
        pass
