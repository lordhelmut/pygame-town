import logging
from re import T, X
import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from support import *


class SoilTileSprites(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']

class SoilLayer:
    def __init__(self, all_sprites) -> None:

        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        # graphics
        soil_surf_path = 'graphics/soil/o.png'
        self.soil_surf = pygame.image.load(soil_surf_path)
        # better soil animations
        soil_fol_path = 'graphics/soil/'
        self.soil_surfs = import_folder_dict(soil_fol_path)

        # instantiate the class methods
        self.create_soil_grid()
        self.create_hit_rects()

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

        # iterate through each list of lists
        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]

        # get the tmx data from the grid
        tmx_path = 'data/map.tmx'
        for x, y, _ in load_pygame(tmx_path).get_layer_by_name('Farmable').tiles():
            # get the y axis, then the x coordinates, then append 'F' as farmable
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    # understand the position of the soil hitbox
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)

    # check where the collision is hitting and if it's farmable
    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    logging.info(f'farmable')
                    # add attribute for farming - 'X'
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:
                    SoilTileSprites(
                        pos=(index_col * TILE_SIZE, index_row * TILE_SIZE),
                        surf=self.soil_surf,
                        groups=[self.all_sprites, self.soil_sprites]
                    )
