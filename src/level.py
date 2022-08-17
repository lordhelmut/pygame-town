import pygame
from settings import *
import logging

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


    def run(self, dt):
        # print('The game is running')
        logging.debug('The game is running')

        # remove previous screens and draw new one
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update()
