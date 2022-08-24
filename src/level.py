import pygame
import logging
from settings import *
from player import Player
from overlay import Overlay
from sprites import GenericSprites

# change from print to logs
logging.basicConfig(
    # filename='HISTORYlistener.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


class Level:
    def __init__(self):
        logging.info('The level has started')
        # get the surface for the display
        self.display_surface = pygame.display.get_surface()

        # groups for the sprites
        self.all_sprites = CameraGroup()

        # start it up
        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        self.player = Player((640, 360), self.all_sprites)
        # create the floor
        floor_image = 'graphics/world/ground.png'
        GenericSprites(
            pos=(0, 0),
            surf=pygame.image.load(floor_image).convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground'])

    def run(self, dt):
        # remove previous screens and draw new one
        self.display_surface.fill('black')
        # call the new function for the camera group
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        # get the overlay from the overlay display function
        self.overlay.display()


class CameraGroup(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        logging.info('The CameraGroup has started')

        self.display_surface = pygame.display.get_surface()

        # needed to place the player relative to the layers
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # make the ground offset to the player from the camera pov
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in self.sprites():
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    # changes the sprite's drawing in a position
                    self.display_surface.blit(sprite.image, offset_rect)
                    if (LOGGINGOPTS == 'DEBUG'):
                        logging.debug(f'layer is {sprite.z}')
