import sys, pygame
from pygame.color import Color

from render import screen
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from space_map import Star
from particles import ParticlePrinciple

from entity_factory import all_sprites, alien_sprites, player, alien

pygame.init()

bg_color = Color(46, 79, 79)


#star_field = pygame.sprite.Group()
#for s in range(100):
#    star = Star()
#    star_field.add(star)

clock = pygame.time.Clock()

#Partile tests
particle1 = ParticlePrinciple(screen)

PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 40)
player_move = 0
#Core Game Loop
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.player_move = -player.speed
            if event.key == pygame.K_RIGHT:
                player.player_move = player.speed
            if event.key == pygame.K_SPACE:
                player.shoot()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                player.player_move = 0
        if event.type == PARTICLE_EVENT:
            particle1.add_particles()

    player.check_hits(alien_sprites)


    #star_field.update()

    # Draw / render
    screen.fill(bg_color)

    all_sprites.update()
    particle1.emit()

    clock.tick(30)

    #star_field.draw(screen)
    all_sprites.draw(screen)


    pygame.display.flip()
