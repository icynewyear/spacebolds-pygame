import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class SpaceEntity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class SpaceActor(SpaceEntity):
    def __init__(self, icon, speed, x, y):
        SpaceEntity.__init__(self)
        self.image = icon
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_move_amount = 0.0
        self.y_move_amount = 0.0

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

class Player(SpaceActor):
    def __init__(self, icon, speed, x, y):
        SpaceActor.__init__(self, icon, speed, x, y)
