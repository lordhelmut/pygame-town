import logging
import pygame
from settings import *
from support import import_folder
from sprites import GenericSprites
from random import randint, choice


class Sky:
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # use this to blend the sky
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)

    def display(self, dt):
        # blend the start -> end
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:
                self.start_color[index] -= 2 * dt

        self.full_surf.fill(self.start_color)
        self.display_surface.blit(
            self.full_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

class Drop(GenericSprites):
    def __init__(self, pos, moving, surf, groups, z) -> None:
        super().__init__(pos, surf, groups, z)

        # general setup
        self.lifetime = randint(400, 500)
        self.start_time = pygame.time.get_ticks()

        # move the particles
        self.moving = moving
        if self.moving:
            # basically anything in pygame requires position direction & speed
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(150, 225)

    def update(self, dt):
        # rain movement
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # rain timer
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()


class Rain:
    def __init__(self, all_sprites) -> None:
        self.all_sprites = all_sprites

        # graphics
        # rain drops folder
        raindrops_folder = 'graphics/rain/drops/'
        self.rain_drops = import_folder(raindrops_folder)
        # rain floor folders
        rainfloor_folder = 'graphics/rain/floor/'
        self.rain_floor = import_folder(rainfloor_folder)

        # need to determine size of floor to rain down upon
        self.floor_w, self.floor_h = pygame.image.load(
            'graphics/world/ground.png').get_size()

    def create_floor(self):
        Drop(
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            moving=False,
            surf=choice(self.rain_floor),
            groups=self.all_sprites,
            z=LAYERS['rain floor'])

    def create_drops(self):
        Drop(
            pos=(randint(0, self.floor_w), randint(0, self.floor_h)),
            moving=True,
            surf=choice(self.rain_drops),
            groups=self.all_sprites,
            z=LAYERS['rain drops'])

    def update(self):
        self.create_floor()
        self.create_drops()
