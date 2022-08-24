import pygame
import logging
from settings import *
from player import Player
from overlay import Overlay

# change from print to logs
logging.basicConfig(
    # filename='HISTORYlistener.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class Level:
    def __init__(self):
        logging.info('The game has started')
        # get the surface for the display
        self.display_surface = pygame.display.get_surface()

        # groups for the sprites
        self.all_sprites = pygame.sprite.Group()

        # start it up
        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        self.player = Player((640, 360), self.all_sprites)

    def run(self, dt):
        # remove previous screens and draw new one
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)

        # get the overlay from the overlay display function
        self.overlay.display()
