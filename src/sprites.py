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
