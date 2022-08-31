from xml.sax.handler import DTDHandler
import pygame
import logging
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer):
        super().__init__(group)

        # init setups
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # set the image to the status of the person
        self.image = self.animations[self.status][self.frame_index]

        # we don't want the player to be the same size as the hitbox
        # because in many cases the sprite is larger than the character
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy().inflate((-126, -70))

        # height axis or layer - so images will stack
        self.z = LAYERS['main']

        # movement attribute
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # collisions
        self.collision_sprites = collision_sprites

        # what time is it
        self.timers = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
        }

        # tool usages
        self.tools = ['axe', 'hoe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # seed usages
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        # inventory
        self.item_inventory = {
            'wood': 0,
            'apple': 0,
            'corn': 0,
            'tomato': 0
        }

        # interactive position relative to player
        self.tree_sprites = tree_sprites
        self.interaction = interaction

        # create & set attribute
        self.sleep = False

        self.soil_layer = soil_layer

    def use_tool(self):
        if self.selected_tool == 'hoe':
            self.soil_layer.get_hit(self.target_pos)
        if self.selected_tool == 'axe':
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()
        if self.selected_tool == 'water':
            self.soil_layer.water(self.target_pos)
        if (LOGGINGOPTS == 'DEBUG'):
            logging.debug(f'self.selected_tool: {self.selected_tool}')

    def get_target_pos(self):
        # get the offsets from the settings to move the target pixel to the correct area
        self.target_pos = self.rect.center + \
            PLAYER_TOOL_OFFSET[self.status.split('_')[0]]
        if (LOGGINGOPTS == 'DEBUG'):
            logging.debug(
                f'self.status direction = {self.status.split("_")[0]}')

    def use_seed(self):
        if (LOGGINGOPTS == 'DEBUG'):
            logging.debug(f'self.selected_tool: {self.selected_seed}')

    def import_assets(self):
        logging.info('Loading assets')

        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}

        for animation in self.animations.keys():
            full_path = 'graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)
            if (LOGGINGOPTS == 'DEBUG'):
                logging.debug(f'self.animations: {self.animations}')

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]
        if (LOGGINGOPTS == 'DEBUG'):
            logging.debug(f'self image animation: {self.image}')

    def input(self):

        # get the key presses
        keys = pygame.key.get_pressed()

        if not self.timers['tool use'].active:
            # cardinal movements
            if keys[pygame.K_UP]:
                self.direction.y = -1
                # set the correct animation surface
                self.status = 'up'
                if (LOGGINGOPTS == 'DEBUG'):
                    logging.debug(
                        f'up arrow pressed. self.status: {self.status}')
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
                if (LOGGINGOPTS == 'DEBUG'):
                    logging.debug(
                        'down arrow pressed. self.status: {self.status}')
            else:
                # this keeps the character from moving indefinitely
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
                if (LOGGINGOPTS == 'DEBUG'):
                    logging.debug(
                        'right arrow pressed. self.status: {self.status}')
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
                if (LOGGINGOPTS == 'DEBUG'):
                    logging.debug(
                        'left arrow pressed. self.status: {self.status}')
            else:
                # this keeps the character from moving indefinitely
                self.direction.x = 0
            if (LOGGINGOPTS == 'DEBUG'):
                logging.debug(
                    f'direction: {self.direction}. self.status: {self.status}')

            # tool used
            if keys[pygame.K_SPACE]:
                # timer for tool usage
                self.timers['tool use'].activate()
                # this halts the player while using a tool
                self.direction = pygame.math.Vector2()
                # this resets the frame and plays 0 animation (plays the animation from the start)
                self.frame_index = 0
                if (LOGGINGOPTS == 'DEBUG'):
                    logging.debug(f'self.timers: {self.timers}')

            # change tool
            if keys[pygame.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()
                self.tool_index += 1
                # make sure the tool is less than the length of the index
                self.tool_index = self.tool_index if self.tool_index < len(
                    self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]
                logging.info(f'selected tool: {self.selected_tool}')

            # seed used
            if keys[pygame.K_LCTRL]:
                # timer for seed usage
                self.timers['seed use'].activate()
                # this halts the player while using a seed
                self.direction = pygame.math.Vector2()
                # this resets the frame and plays 0 animation (plays the animation from the start)
                self.frame_index = 0
                if (LOGGINGOPTS == 'DEBUG'):
                    logging.debug(f'seed activated')

            # change seed
            if keys[pygame.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()
                self.seed_index += 1
                # make sure the seed is less than the length of the index
                self.seed_index = self.seed_index if self.seed_index < len(
                    self.seeds) else 0
                self.selected_seed = self.seeds[self.seed_index]
                logging.info(f'selected seed: {self.selected_seed}')

            if keys[pygame.K_RETURN]:
                collided_interaction_sprite = pygame.sprite.spritecollide(
                    self, self.interaction, False)
                # check if sprite has collided with the  location
                if collided_interaction_sprite:
                    logging.info(
                        f'You have reached a collision with : {collided_interaction_sprite[0].name}')
                    if collided_interaction_sprite[0].name == 'Trader':
                        pass
                    else:
                        # point the character after the collision to make it looking at bed
                        self.status = 'left_idle'
                        # now sleep
                        self.sleep = True

            if keys[pygame.K_i]:
                # debug whats in the inventory for now
                logging.info(f'inventory: {self.item_inventory}')


    def get_status(self):
        # if player is not moving, add "_idle" to status
        movement = self.direction.magnitude()
        if movement == 0:
            # split the string so that the first part
            # always returns the root file path
            # e.g. "up" such that "up_idle" will also return "up"
            self.status = self.status.split('_')[0] + '_idle'

        # tool usage
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

        if (LOGGINGOPTS == 'DEBUG'):
            logging.debug(f'movement: {movement} self.status: {self.status}')

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            # quick check if this is needed
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0:  # moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction.y > 0:  # moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery
                    if (LOGGINGOPTS == 'DEBUG'):
                        logging.debug(
                            f'sprite: {sprite} has hitbox:', hasattr(sprite, 'hitbox'))

    def move(self, dt):
        # vector math, needs to be a positive number
        if self.direction.magnitude() > 0:
            # normalize the vector movement
            # otherwise player moves 1 right, plus 1 up, a^2 + b^2 = c^2 (approx 1.4)
            self.direction = self.direction.normalize()
        if (LOGGINGOPTS == 'DEBUG'):
            logging.debug(f'normalized: {self.direction}')

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        # also move the hitbox when moving
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()

        self.move(dt)
        self.animate(dt)
