import pygame, random

from colors import STAR_COLORS
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class ParticlePrinciple():
    def __init__(self,screen):
        self.screen = screen
        self.particles = []
        pygame.init()

    def emit(self):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                #move
                particle[0][1] += particle[2]
                #shrink
                particle[1] -= 0.05
                #Draw
                pygame.draw.circle(self.screen, particle[3], particle[0], int(particle[1]))

    def add_particles(self):
        pos_x = random.randint(0,SCREEN_WIDTH)
        pos_y = random.randint(0,SCREEN_HEIGHT/2)
        radius = 5
        direction = 4
        color = random.choice(STAR_COLORS)
        particle_cicle = [[pos_x,pos_y], radius, direction, color]
        self.particles.append(particle_cicle)

    def delete_particles(self):
        particle_copy = [particle for particle in self.particles if particle[1] > 0]
        self.particles = particle_copy
