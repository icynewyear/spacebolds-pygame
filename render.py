import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

#Set core display

screen_title = "Koboldka"
icon = pygame.image.load('resources/goblin.png')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(screen_title)
pygame.display.set_icon(icon)
