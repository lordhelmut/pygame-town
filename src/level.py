from ast import Interactive
from typing import Collection
import pygame
import logging
from settings import *
from player import Player
from overlay import Overlay
from sprites import GenericSprites, WaterSprites, TreeSprites, WildFlowerSprites, InteractionSprites, ParticleEffects
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu import Menu


class Level:
    def __init__(self):
        logging.info('The level has started')
        # get the surface for the display
        self.display_surface = pygame.display.get_surface()

        # groups for the sprites
        self.all_sprites = CameraGroup()
        # keep track of things player can collide with
        self.collision_sprites = pygame.sprite.Group()

        # need to know where the trees are relative to player
        self.tree_sprites = pygame.sprite.Group()

        # interaction with objects
        self.interaction_sprites = pygame.sprite.Group()

        # populate soil properties
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)

        # start it up
        self.setup()
        self.overlay = Overlay(self.player)

        # new transition class
        self.transition = Transition(self.reset_scene, self.player)

        # sky
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        logging.info(f'is it raining? {self.raining}')
        self.sky = Sky()

        # shop
        self.menu = Menu(self.player, self.toggle_shop)
        self.shop_active = False

        # music
        success_path = ('audio/success.wav')
        self.success = pygame.mixer.Sound(success_path)
        self.success.set_volume(0.3)

        bgmusic_path = ('audio/music.mp3')
        self.bg_music = pygame.mixer.Sound(bgmusic_path)
        self.bg_music.set_volume(0.1)
        self.bg_music.play(loops=-1)

    def setup(self):

        # the map was created in "Tiled" software - mapeditor.org

        # load the map file
        map_file = 'data/map.tmx'
        tmx_data = load_pygame(map_file)

        # import a ton of different things ...

        # house layers need to be separate in pygame
        # bottom (floor) -> walls -> furniture bottom -> furniture top

        # bottom layer in house - order is important, make sure floor is drawn before bottom
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                GenericSprites((x * TILE_SIZE, y * TILE_SIZE), surf,
                               self.all_sprites, LAYERS['house bottom'])
                if (LOGGINGOPTS == 'DEBUG'):
                    logging.debug(f'layer: {layer} x: {x} y: {y}')

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                GenericSprites((x * TILE_SIZE, y * TILE_SIZE), surf,
                               self.all_sprites, LAYERS['main'])
                if (LOGGINGOPTS == 'DEBUG'):
                    logging.debug(f'layer: {layer} x: {x} y: {y}')

        # fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            GenericSprites((x * TILE_SIZE, y * TILE_SIZE), surf,
                           [self.all_sprites, self.collision_sprites], LAYERS['main'])
            if (LOGGINGOPTS == 'DEBUG'):
                logging.debug(f'layer: {layer} x: {x} y: {y}')

        # water
        water_folder = 'graphics/water'
        water_frames = import_folder(water_folder)
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            WaterSprites((x * TILE_SIZE, y * TILE_SIZE),
                         water_frames, self.all_sprites)
            if (LOGGINGOPTS == 'DEBUG'):
                logging.debug(f'frames: {water_frames} x: {x} y: {y}')

        # wildflowers
        # the image layer is slightly different as it was created differently in "Tiled" ...
        # ... but image placement logic is the same
        for obj in tmx_data.get_layer_by_name('Decoration'):
            WildFlowerSprites((obj.x, obj.y), obj.image, [
                              self.all_sprites, self.collision_sprites])
            if (LOGGINGOPTS == 'DEBUG'):
                logging.debug(f'decoration object: {obj} x: {x} y: {y}')

        # trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            TreeSprites(
                pos=(obj.x, obj.y),
                surf=obj.image,
                groups=[
                    self.all_sprites, self.collision_sprites, self.tree_sprites],
                name=obj.name,
                player_add=self.player_add)
            if (LOGGINGOPTS == 'DEBUG'):
                logging.debug(f'tree object: {obj.name} x: {x} y: {y}')

        # collision tiles - these are hard coded in the map layer, not by the objects
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            # this is not drawn or updated - just has a non-visible collision surface
            GenericSprites((x * TILE_SIZE, y * TILE_SIZE),
                           pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

        # player
        # check the map layer and place the player in the 'start' position
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos=(obj.x, obj.y),
                    group=self.all_sprites,
                    collision_sprites=self.collision_sprites,
                    tree_sprites=self.tree_sprites,
                    interaction=self.interaction_sprites,
                    soil_layer=self.soil_layer,
                    toggle_shop=self.toggle_shop)
            # check map layer and see if player is in 'bed' position
            if obj.name == 'Bed':
                InteractionSprites(
                    pos=(obj.x, obj.y),
                    size=(obj.width, obj.height),
                    groups=self.interaction_sprites,
                    name=obj.name)

            # trader
            if obj.name == 'Trader':
                InteractionSprites(
                    pos=(obj.x, obj.y),
                    size=(obj.width, obj.height),
                    groups=self.interaction_sprites,
                    name=obj.name)

        # create the floor
        floor_image = 'graphics/world/ground.png'
        GenericSprites(
            pos=(0, 0),
            surf=pygame.image.load(floor_image).convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground'])

    def toggle_shop(self):
        self.shop_active = not self.shop_active

    def player_add(self, item):
        self.player.item_inventory[item] += 1
        self.success.play()

        logging.info(f'inventory: {self.player.item_inventory}')

    def reset_scene(self):

        # plants
        self.soil_layer.update_plant_sprites()

        # soil
        self.soil_layer.remove_water_tiles()

        # rain
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        if self.raining:
            logging.info(f'is it raining? {self.raining}')
            self.soil_layer.water_all()

        # add apples on trees
        for tree in self.tree_sprites.sprites():
            # look for existing fruit
            for apple in tree.apple_sprites.sprites():
                # remove existing apples
                apple.kill()
            # purged all apples above, now re-add
            tree.create_fruit()

        # reset day/night
        self.sky.start_color = [255, 255, 255]

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    # 1 add inventory
                    # 2 remove plant
                    # 3 animations
                    # 4 reset grid attribute
                    self.player_add(plant.plant_type)
                    plant.kill()
                    ParticleEffects(plant.rect.topleft, plant.image,
                                    self.all_sprites, z=LAYERS['main'])
                    self.soil_layer.grid[plant.rect.centery //
                                         TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

    def run(self, dt):
        # remove previous screens and draw new one
        self.display_surface.fill('black')
        # call the new function for the camera group
        self.all_sprites.custom_draw(self.player)

        # updates
        if self.shop_active:
            self.menu.update()
        else:
            self.all_sprites.update(dt)
            self.plant_collision()

        # weather
        self.overlay.display()
        if self.raining and not self.shop_active:
            self.rain.update()

        # day time
        self.sky.display(dt)

        # check if need to change times
        if self.player.sleep:
            self.transition.play()


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
            # create a lambda function to sort lower value layers to be drawn below others based on 'y'
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    # changes the sprite's drawing in a position
                    self.display_surface.blit(sprite.image, offset_rect)
                    if (LOGGINGOPTS == 'DEBUG'):
                        logging.debug(f'layer is {sprite.z}')

                    # # find location of target hit
                    if (SPRITEDEBUG == 'DEBUG'):
                        if sprite == player:
                            pygame.draw.rect(
                                self.display_surface, 'red', offset_rect, 5)
                            hitbox_rect = player.hitbox.copy()
                            hitbox_rect.center = offset_rect.center
                            pygame.draw.rect(
                                self.display_surface, 'green', hitbox_rect, 5)
                            target_pos = offset_rect.center + \
                                PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
                            pygame.draw.circle(
                                self.display_surface, 'blue', target_pos, 5)
