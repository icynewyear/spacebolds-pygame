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
    CHANGE_BACKGROUND = auto()
    CHANGE_SPEED = auto()
    CHANGE_POS = auto()

    #Spawning
    SPAWN_ENEMY = auto()
    SPAWN_SPAWNER = auto()

class SpaceMap():
    """Handles the functions of a space level map.  script list of Tuples (distancestamp_to_fire_event, event_type, int_var_for_event[-1 for none], entity_for_event[None for none])"""
    def __init__(self, engine: Engine, script, length: int = 0, scroll_speed: int = 1, pos: int = 0):
        self.engine = engine
        self.screen = engine.screen
        self.length = length
        self.scroll_speed = scroll_speed
        self.pos = pos
        self.last_pos = pos
        self.script = script
        self.last_bg = None
        self.script_init(self.script)

    def script_init(self, script) -> None:
        """Method to process any script commands with a distancestamp below 1"""
        init_events = [event for event in self.script if event[0] <= 0]
        if init_events: self.do_step(init_events)

    def step(self) -> None:
        """Compare internal position to script, do any events during that time step. sets last internal position"""
        events_to_fire = [event for event in self.script if event[0] == self.pos or (event[0] < self.pos and event[0] > self.last_pos)]
        self.last_pos = self.pos
        print(events_to_fire)
        if events_to_fire: self.do_step(events_to_fire)

    def do_step(self, events_to_fire) -> None:
        """Method to call appropriate methods when passed a list of SpaceEvents to process"""
        for event in events_to_fire:
            if event[1] == SpaceEvent.CHANGE_BACKGROUND:
                self.set_background(event)
            elif event[1] == SpaceEvent.CHANGE_SPEED:
                self.set_speed(event)
            elif event[1] == SpaceEvent.CHANGE_POS:
                self.set_pos(event)
            elif event[1] == SpaceEvent.SPAWN_SPAWNER or SpaceEvent.SPAWN_ENEMY:
                self.spawn(event[3], event[2], event[4])

    def update(self) -> None:
        """Method called to run the gamemap 1 tick"""
        self.pos += self.scroll_speed
        self.step()
        self.render()

    def set_background(self, event) -> None:
        """Method to process CHANGE_BACKGROUND events"""
        if self.last_bg != None: self.last_bg.stop()
        event[3].setup()
        self.last_bg = event[3]

    def set_speed(self, event) -> None:
        """Method to process CHANGE_SPEED events. Sets Scroll Speed to multiuse Var value"""
        self.scroll_speed = event[2]

    def set_pos(self, event) -> None:
        """Method to process CHANGE_POS events. Sets Position to multiuse Var value"""
        self.pos = event[2]

    def spawn(self, entity: SpaceEntity, multivar: int, coords: Tuple[int,int]) -> None:
        """Method to process SPAWN_ events and spawn entities. Passes multivar to spawn method of entity"""
        ### TODO: Perhaps collapse SPAWN_ENEMY and SPAWN_SPAWNER?
        new_entity = entity.spawn(coords, multivar)
        self.engine.alien_sprites.add(new_entity)
        self.engine.all_sprites.add(new_entity)

    def renderProgessBar(self) -> None:
        """Method to render a progress bar on the side of the screen"""
        progress_display = int((self.pos/self.length)*SCREEN_HEIGHT)
        pygame.draw.rect(self.screen, RED, (0, 0, 5, SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, BLUE, (0, SCREEN_HEIGHT-progress_display, 5, progress_display))

    def render(self) -> None:
        """Method to render gamemap elements to screen"""
        debug(self.pos)
        self.renderProgessBar()
