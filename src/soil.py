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

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                logging.info(f'soil tiled watered {soil_sprite}')

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'X' in cell:

                    # tile options - need to check adjacent cells
                    # to determine what graphics are used

                    # t = top, b = bottom, r = right, l = left
                    top = 'X' in self.grid[index_row - 1][index_col]
                    bottom = 'X' in self.grid[index_row + 1][index_col]
                    right = 'X' in row[index_col + 1]
                    left = 'X' in row[index_col - 1]

                    # 'o' is default tile
                    tile_type = 'o'

                    # all sides are adjacent
                    if all((top, bottom, right, top)):
                        tile_type = 'x'

                    # horizontal adjacent tiles
                    if left and not any((top, right, bottom)):
                        tile_type = 'r'
                    if right and not any((top, left, bottom)):
                        tile_type = 'l'
                    if left and right and not any((top, bottom)):
                        tile_type = 'lr'

                    # vertical adjacent tiles
                    if top and not any((right, left, bottom)):
                        tile_type = 'b'
                    if bottom and not any((top, left, right)):
                        tile_type = 't'
                    if bottom and top and not any((right, left)):
                        tile_type = 'tb'

                    # corners
                    if left and bottom and not any((top, right)):
                        tile_type = 'tr'
                    if right and bottom and not any((top, left)):
                        tile_type = 'tl'
                    if left and top and not any((bottom, right)):
                        tile_type = 'br'
                    if right and top and not any((bottom, left)):
                        tile_type = 'bl'

                    # T shapes
                    if all((top, bottom, right)) and not left:
                        tile_type = 'tbr'
                    if all((top, bottom, left)) and not right:
                        tile_type = 'tbl'
                    if all((left, right, top)) and not bottom:
                        tile_type = 'lrb'
                    if all((left, right, bottom)) and not top:
                        tile_type = 'lrt'

                    SoilTileSprites(
                        pos=(index_col * TILE_SIZE, index_row * TILE_SIZE),
                        surf=self.soil_surfs[tile_type],
                        groups=[self.all_sprites, self.soil_sprites]
                    )
