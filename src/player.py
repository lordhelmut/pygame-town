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
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        self.input()
        self.move(dt)
