import sys, pygame
from pygame.color import Color


from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from entity import Player
from space_map import Star

pygame.init()

screen_title = "Koboldka"
icon = pygame.image.load('resources/goblin.png')

bg_color = Color(46, 79, 79)

#player
playerIcon = pygame.image.load('resources/spaceship.png')
playerX = SCREEN_WIDTH/2 - playerIcon.get_width()/2
#playerY = SCREEN_HEIGHT/2 - playerIcon.get_height()/2
playerY = 480
player_speed = 5
player_move = 0



#Set core display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(screen_title)
pygame.display.set_icon(icon)

#instantiate player


all_sprites = pygame.sprite.Group()
player = Player(playerIcon, player_speed, playerX, playerY)
all_sprites.add(player)

star_field = pygame.sprite.Group()
for s in range(100):
    star = Star()
    star_field.add(star)

clock = pygame.time.Clock()


#Core Game Loop
while 1:


    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_move = -player.speed
            if event.key == pygame.K_RIGHT:
                player_move = player.speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                player_move = 0

    player.move(player_move,0)

    all_sprites.update()
    star_field.update()

    # Draw / render
    screen.fill(bg_color)

    clock.tick(30)

    star_field.draw(screen)
    all_sprites.draw(screen)


    pygame.display.flip()
