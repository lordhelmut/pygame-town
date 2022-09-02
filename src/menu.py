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

        # options
        self.width = 400
        self.space = 10  # between elements
        self.heading = 8

        self.trader_options = list(
            self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

    def setup(self):
        self.text_surfs = []
        for item in self.trader_options:
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

    def update(self):
        self.input()
        # use the item inventory as the menu options
        for text_index, text_surf in enumerate(self.text_surfs):
            self.display_surface.blit(text_surf, (100, text_index*50))
