import pygame, random
from colors import STAR_COLORS
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class Star(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([2,2])
        self.image.fill(random.choice(STAR_COLORS))
        self.rect = self.image.get_rect()
        self.speed = random.randint(1,3)
        self.rect.x = random.randint(0,SCREEN_WIDTH)
        self.rect.y = random.randint(0,SCREEN_HEIGHT)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0
