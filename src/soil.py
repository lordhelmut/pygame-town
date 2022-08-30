import logging
import pygame
from settings import *


class SoilLayer:
    def __init__(self, all_sprites) -> None:

        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # graphics
        soil_surf_path = 'graphics/soil/o.png'
        self.soil_surf = pygame.image.load(soil_surf_path)

        self.create_soil_grid()

    def create_soil_grid(self):

        # for every tile, we need to check a few things
        # 1 - if area is farmable
        # 2 - if soil has been watered
        # 3 - if soil currently has a plant

        # need place the ground at the very bottom in relation to others
        # and need to know the size of the grid
        ground_path = 'graphics/world/ground.png'
        ground = pygame.image.load(ground_path)
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE
        logging.info(f'h_tiles: {h_tiles} v_tiles: {v_tiles}')

        self.grid = []
