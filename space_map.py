from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, List
from enum import Enum, auto

if TYPE_CHECKING:
    from engine import Engine
    from entity import SpaceEntity

import pygame

from debug import debug

from colors import RED, BLUE
from settings import SCREEN_HEIGHT

class SpaceEvent(Enum):
    """Enums for events for building a space level script"""
    #Utility
    SET_BACKGROUND = auto()
    CHANGE_SPEED = auto()
    #Spawning
    SPAWN_ENEMY = auto()
    SPAWN_SPAWNER = auto()

class SpaceMap():
    """Handles the functions of a speace level map.  script list of Tuples (distancestamp_to_fire_event, event_type, int_var_for_event[-1 for none], entity_for_event[None for none])"""
    def __init__(self, engine: Engine, script, length: int = 0, scroll_speed: int = 1, pos: int = 0):
        self.engine = engine
        self.screen = engine.screen
        self.length = length
        self.scroll_speed = scroll_speed
        self.pos = pos
        self.last_pos = pos
        self.script = script
        self.script_init(self.script)

    def script_init(self, script):
        """Method to process any script commands with a distancestamp below 1"""
        init_events = [event for event in self.script if event[0] <= 0]
        print(init_events)
        if init_events: self.do_step(init_events)

    def step(self):
        """Compare internal position to script, do any events at this time step. iterate internal position"""
        events_to_fire = [event for event in self.script if event[0] == self.pos or (self.pos != self.last_pos and (event[0] < self.pos and event[0] > self.last_pos))]
        self.last_pos = self.pos
        if events_to_fire: self.do_step(events_to_fire)

    def do_step(self, events_to_fire):
        """Method to call appropriate methods when passed a list of SpaceEvents to process"""
        for event in events_to_fire:
            if event[1] == SpaceEvent.SET_BACKGROUND:
                self.set_background(event)
            elif event[1] == SpaceEvent.CHANGE_SPEED:
                self.set_speed(event)
            elif event[1] == SpaceEvent.SPAWN_SPAWNER or SpaceEvent.SPAWN_ENEMY:
                self.spawn(event[3],event[2], event[4])

    def update(self):
        """Method called to run the gamemap 1 tick"""
        self.renderProgessBar()
        self.pos += self.scroll_speed
        debug(self.scroll_speed)
        self.step()

    def set_background(self, event):
        """Method to process SET_BACKGROUND events"""
        pass

    def set_speed(self, event):
        self.scroll_speed = event[2]

    def spawn(self, entity, numeric_var, coords):
        """Method to process SPAWN_ events and spawn entities"""
        new_spawner = entity.spawn(coords)
        self.engine.alien_sprites.add(new_spawner)
        self.engine.all_sprites.add(new_spawner)

    def renderProgessBar(self):
        """Method to render a progress bar on the side of the screen"""
        progress_display = int((self.pos/self.length)*SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, RED, (0, 0, 5, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, BLUE, (0, SCREEN_HEIGHT-progress_display, 5, progress_display))
