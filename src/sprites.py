import pygame
import logging
from settings import *


class GenericSprites(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']) -> None:
        super().__init__(groups)
        # create the surface from the base image
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

        # set the initial layer
        self.z = z


class WaterSprites(GenericSprites):
    def __init__(self, pos, frames, groups) -> None:

        # animation setup
        self.frames = frames
        self.frame_index = 0

        # sprite setup
        super().__init__(
            pos=pos,
            surf=self.frames[self.frame_index],
            groups=groups,
            z=LAYERS['water'])

    # animate the water
    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        if (LOGGINGOPTS == 'DEBUG'):
            logging.debug(f'water image animation: {self.image}')

    def update(self, dt):
        self.animate(dt)


class WildFlowerSprites(GenericSprites):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(pos, surf, groups)


class TreeSprites(GenericSprites):
    def __init__(self, pos, surf, groups, name) -> None:
        super().__init__(pos, surf, groups)
