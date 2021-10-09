import pygame, random

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from projectiles import Bullet, BulletManager
#from entity_factory import alien_sprites
from colors import *
from flightpatterns import Flightpath


class SpaceEntity(pygame.sprite.Sprite):
    def __init__(self, engine, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.engine = engine

class SpaceActor(SpaceEntity):
    def __init__(self, engine, screen, icon, speed, x, y):
        SpaceEntity.__init__(self, engine, screen)
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
        return (x_amount,y_amount)

    def do_movement(self, move):
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

    def shoot(self):
        pass

    def update(self):
        self.do_movement(self.move(self.x_move_amount, self.y_move_amount))
        self.bullet_manager.update()
        self.bullet_manager.render()

class Alien(SpaceActor):
    def __init__(self, engine, screen, icon, speed, fire_rate, x, y):
        SpaceActor.__init__(self, engine, screen, icon, speed, x, y)
        self.direction = random.randint(0,1)
        self.fire_rate = fire_rate
        self.timer = fire_rate
        self.y_timer = 0
        self.fp = Flightpath(1,(0,300))

    def shoot(self):
        if self.timer == self.fire_rate:
            self.timer = 0
            bullet = Bullet(self.bullet_manager, self.rect.x+(self.image.get_width()/2), self.rect.y+self.image.get_height(), 10, ALIEN_GUN)
            self.bullet_manager.add_projectile(bullet)
        else: self.timer+=1

    def spawn(self, coords):
        x, y = coords
        new_alien = Alien(self.engine, self.screen, self.image, self.speed, self.fire_rate, x, y)
        return new_alien

    # def move(self):
    #     x_amount = 0
    #     y_amount = 0
    #     if self.direction == 1:
    #         x_amount = self.speed
    #         if self.rect.x >= SCREEN_WIDTH-self.image.get_width(): self.direction = 0
    #     elif self.direction == 0:
    #         x_amount = -self.speed
    #         if self.rect.x <= 0: self.direction = 1
    #     if self.y_timer >= 25:
    #         y_amount = -5
    #     if self.y_timer < 25:
    #         y_amount = 5
    #     if self.y_timer == 50: self.y_timer = 0
    #     self.y_timer += 1
    #     return (x_amount,y_amount)

    def move(self):
        move = next(self.fp)
        return move

    def do_movement(self, move):
        #X move
        x,y = move
        self.rect.x += x
        #Y move
        self.rect.y += y
        pass

    def check_hits(self):
            for bullet in self.bullet_manager.projectiles:
                if self.engine.player.rect.collidepoint((bullet.x,bullet.y)):
                    self.bullet_manager.projectiles.remove(bullet)
                    self.engine.player.hp -= 1

    def update(self):
        self.move()
        self.shoot()
        self.check_hits()
        self.do_movement(self.move())
        self.bullet_manager.update()
        self.bullet_manager.render()


class Player(SpaceActor):
    def __init__(self, engine, screen, icon, speed, x, y):
        SpaceActor.__init__(self, engine, screen, icon, speed, x, y)
        self.player_move = 0
        self._hp = 10
        self.maxhp = 10
        self.dead = False

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, min(value, self.maxhp))
        if self._hp == 0:
            self.die()

    def die(self):
        if self.dead == False:
            gameover_sound = pygame.mixer.Sound('resources/gameover.ogg')
            gameover_sound.play()
            self.kill()
            self.dead = True

    def shoot(self):
        bullet = Bullet(self.bullet_manager, self.rect.x+(self.image.get_width()/2), self.rect.y, -10, PLAYER_GUN)
        self.bullet_manager.add_projectile(bullet)

    def check_hits(self):
        for asprite in self.engine.alien_sprites.sprites():
            for bullet in self.bullet_manager.projectiles:
                if asprite.rect.collidepoint((bullet.x,bullet.y)):
                    self.bullet_manager.projectiles.remove(bullet)
                    asprite.kill()

    def renderHP(self):
        pygame.draw.rect(self.screen, RED, (20,570,self.maxhp*20,20))
        pygame.draw.rect(self.screen, BLUE, (20,570,self.hp*20,20))


    def update(self):
        if self.dead == False:
            self.renderHP()
            self.move(self.player_move,0)
            self.check_hits()
            super().update()
