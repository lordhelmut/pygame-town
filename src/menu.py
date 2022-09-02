import pygame
import logging
from settings import *


class Menu:
    def __init__(self, player, toggle_menu) -> None:
        # general setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        font_path = 'font/LycheeSoda.ttf'
        self.font = pygame.font.Font(font_path, 30)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

    def update(self):
        self.input()
        self.display_surface.blit(pygame.Surface((1000,1000)),(0,0))