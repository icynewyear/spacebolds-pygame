from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from engine import Engine

import pygame

from colors import *

from particles import ParticlePrinciple

class Background():
    """May Remove"""
    def __init__(self, engine):
        self.engine = engine
        self.screen = engine.screen

    def setup(self):
        pass

    def stop(self):
        pass

class FlatColorBackgroud(Background):
    """Class to change background to a flat color"""
    def __init__(self, engine: Engine, color: Tuple[int,int,int]):
        self.engine = engine
        self.screen = engine.screen
        self.color = color

    def setup(self) -> None:
        """called by Spacemap to apply this background"""
        self.engine.bg_color = self.color

    def stop(self) -> None:
        pass

class ParticleBackground(Background):
    """Start of class to start and stop a particle based background"""
    def __init__(self, engine: Engine, particlegen = None, timer: int = 40):
        self.engine = engine
        self.screen = engine.screen
        self.particlegen = particlegen
        self.timer = timer

    def setup(self) -> None:
        """called by Spacemap to apply this background"""
        self.engine.PARTICLE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.engine.PARTICLE_EVENT, self.timer)
        if self.particlegen == None: self.particlegen = ParticlePrinciple(self.engine)

    def stop(self) -> None:
        """called by Spacemap to remove this background"""
        pygame.time.set_timer(self.engine.PARTICLE_EVENT, 0)


# class ScrollingImageBackground(Background):
#     def __init__(self):
#         self.bgimage = pygame.image.load('')
#         self.rectBGimg = self.bgimage.get_rect()
#
#         self.bgY1 = 0
#         self.bgX1 = 0
#
#         self.bgY2 = self.rectBGimg.height
#         self.bgX2 = 0
#
#         self.moving_speed = 5
#
#     def update(self):
#         self.bgY1 -= self.moving_speed
#         self.bgY2 -= self.moving_speed
#         if self.bgY1 <= -self.rectBGimg.height:
#             self.bgY1 = self.rectBGimg.height
#         if self.bgY2 <= -self.rectBGimg.height:
#             self.bgY2 = self.rectBGimg.height
#
#     def render(self):
#         self.screen.blit(self.bgimage, (self.bgX1, self.bgY1))
#         self.screen.blit(self.bgimage, (self.bgX2, self.bgY2))
