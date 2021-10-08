import pygame

from debug import debug

class Flightpath():
    def __init__(self, timer = (0,0)):
        self.timer = timer
        self.generator_iterator = self.step()

    def __next__(self):
        return next(self.generator_iterator)

    def step(self):
        current_timer, max_timer = self.timer

        x = -1
        y = 1
        while True:
            yield (x,y)
            
            debug(current_timer)

            if current_timer < max_timer/2:
                x = -1
            elif current_timer < max_timer:
                x = 1
            else:
                current_timer = 0
            current_timer += 1
