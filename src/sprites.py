from secrets import choice
import pygame
import logging
from settings import *
from timer import Timer
from random import randint, choice

class GenericSprites(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']) -> None:
        super().__init__(groups)
        # create the surface from the base image
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)

        # set the initial layer
        self.z = z

        # hitbox - the shinking of the size allows for player to ...
        # ... clip through more naturally looking rather than avoiding the object altogether
        self.hitbox = self.rect.copy().inflate(-self.rect.width *
                                               0.2, -self.rect.height * 0.75)


class WaterSprites(GenericSprites):
    def __init__(self, pos, frames, groups) -> None:

        # animation setup
        self.frames = frames
        self.frame_index = 0

        # sprite setup
        super().__init__(
            pos=pos,
            surf=self.frames[self.frame_index],
            groups=groups,
            z=LAYERS['water'])

    # animate the water
    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        if (LOGGINGOPTS == 'DEBUG'):
            logging.debug(f'water image animation: {self.image}')

    def update(self, dt):
        self.animate(dt)


class WildFlowerSprites(GenericSprites):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(pos, surf, groups)

        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

class TreeSprites(GenericSprites):
    def __init__(self, pos, surf, groups, name) -> None:
        super().__init__(pos, surf, groups)

        # hitbox - will inherit from GenericSprites

        # tree attributes
        self.health = 5  # hardcode to 5 hits per tree
        self.alive = True
        # what tree looks like when tree dies
        stump_path = f'graphics/stumps/{"small" if name == "small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()
        self.invul_timer = Timer(200)

        # apples
        appleimage_path = 'graphics/fruit/apple.png'
        self.apple_surf = pygame.image.load(appleimage_path)
        # possible positions for apple on the tree are in the settings
        # 'name' being passed in is either small or large
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

    def damage(self):
        self.health -= 1

        # remove an apple - such that the list has apples available
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            random_apple.kill()  # remove from sprite groups

    def check_death(self):
        if self.health <= 0:
            # change the image
            self.image = self.stump_surf
            # update the position of the new image to be the same position of previous
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            # update hitbox too
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            logging.info(f'tree died.  health: {self.health}')

    def update(self, dt):
        if self.alive:
            self.check_death()

    def create_fruit(self):
        for pos in self.apple_pos:
            appleluck = randint(0, 10)
            if appleluck < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                GenericSprites(
                    pos=(x, y),
                    surf=self.apple_surf,
                    groups=[self.apple_sprites, self.groups()[0]],
                    z=LAYERS['fruit'])
            if (LOGGINGOPTS == 'DEBUG'):
                logging.debug(f'appleluck: {appleluck}')
