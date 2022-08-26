import pygame
import logging

# create a class to reuse time duration functions
class Timer:
    def __init__(self, duration, func=None):
        self.duration = duration
        self.func = func
        self.start_time = 0
        self.active = False

    def activate(self):
        self.active = True
        # set the timer as a marker when it was instantiated
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            # if the function exists, instantiate it
            if self.func and self.start_time != 0:
                self.func()
            # duh - turn it off
            self.deactivate()
