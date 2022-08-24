from xml.sax.handler import DTDHandler
import pygame
import logging
from settings import *
from support import *
from timer import Timer


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # init setups
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # set the image to the status of the person
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # height axis or layer - so images will stack
        self.z = LAYERS['main']

        # movement attribute
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

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

    def use_tool(self):
        if (LOGGINGOPTS == 'DEBUG'):
            logging.debug(f'self.selected_tool: {self.selected_tool}')

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
        self.rect.centerx = self.pos.x
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.move(dt)
        self.animate(dt)
