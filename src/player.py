from xml.sax.handler import DTDHandler
import pygame
import logging
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        # init setups
        self.image = pygame.Surface((32, 64))
        self.image.fill('green')
        self.rect = self.image.get_rect(center=pos)

        # movement attribute
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def input(self):
        # get the key presses
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            logging.debug('up arrow pressed')
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            logging.debug('down arrow pressed')
            self.direction.y = 1
        else:
            # this keeps the character from moving indefinitely
            self.direction.y = 0
        if keys[pygame.K_RIGHT]:
            logging.debug('right arrow pressed')
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            logging.debug('left arrow pressed')
            self.direction.x = -1
        else:
            # this keeps the character from moving indefinitely
            self.direction.x = 0

        logging.debug(f'direction: {self.direction}')

    def move(self, dt):
        # vector math, needs to be a positive number
        if self.direction.magnitude() > 0:
            # normalize the vector movement
            # otherwise player moves 1 right, plus 1 up, a^2 + b^2 = c^2 (approx 1.4)
            self.direction = self.direction.normalize()
        logging.debug(f'normalized: {self.direction}')

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def update(self, dt):
        self.input()
        self.move(dt)
