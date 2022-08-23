from xml.sax.handler import DTDHandler
import pygame
import logging
from settings import *
from support import *


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

        # movement attribute
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

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

        if keys[pygame.K_UP]:
            self.direction.y = -1
            # set the correct animation surface
            self.status = 'up'
            if (LOGGINGOPTS == 'DEBUG'):
                logging.debug(f'up arrow pressed. self.status: {self.status}')
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
            if (LOGGINGOPTS == 'DEBUG'):
                logging.debug('down arrow pressed. self.status: {self.status}')
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
                logging.debug('left arrow pressed. self.status: {self.status}')
        else:
            # this keeps the character from moving indefinitely
            self.direction.x = 0
        if (LOGGINGOPTS == 'DEBUG'):
            logging.debug(
                f'direction: {self.direction}. self.status: {self.status}')

    def get_status(self):
        # if player is not moving, add "_idle" to status
        movement = self.direction.magnitude()
        if movement == 0:
            # split the string so that the first part
            # always returns the root file path
            # e.g. "up" such that "up_idle" will also return "up"
            self.status = self.status.split('_')[0] + '_idle'
        if (LOGGINGOPTS == 'DEBUG'):
            logging.debug(f'movement: {movement} self.status: {self.status}')

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
        self.move(dt)
        self.animate(dt)
