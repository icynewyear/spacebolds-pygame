from __future__ import annotations

from typing import TYPE_CHECKING, Tuple, Iterator

import pygame

from debug import debug

class Flightpath():
    def __init__(self, speed: int = 1, timer: Tuple[int,int] = (0,0)):
        self.speed = speed
        self.timer = timer
        self.generator_iterator = self.step()

    def __next__(self) -> Tuple[int,int]:
        return next(self.generator_iterator)

    def step(self) -> Iterator[Tuple[int,int]]:
        current_timer, max_timer = self.timer

        x = -(self.speed)
        y = self.speed
        while True:
            yield (x,y)
            if current_timer < max_timer/2:
                x = -(self.speed)
            elif current_timer < max_timer:
                x = self.speed
            else:
                current_timer = 0
            current_timer += 1
