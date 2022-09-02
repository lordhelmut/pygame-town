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
        self.padding = 8

        self.trader_options = list(
            self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

    def display_money(self):
        money_text_surf = self.font.render(
            f'${self.player.money}', False, 'Black')
        text_rect = money_text_surf.get_rect(
            midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))

        # add a small background
        pygame.draw.rect(self.display_surface, 'Hot pink',
                         text_rect.inflate(10, 10), 0, 4)
        self.display_surface.blit(money_text_surf, text_rect)

    def setup(self):
        self.text_surfs = []
        self.total_height = 0
        for item in self.trader_options:
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)

        # menu size calculations and padding
        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        # bounding box for main menu
        self.main_rect = pygame.Rect(
            SCREEN_WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

    def update(self):
        self.input()
        self.display_money()
        pygame.draw.rect(self.display_surface, 'red', self.main_rect)
        # use the item inventory as the menu options
        # for text_index, text_surf in enumerate(self.text_surfs):
        #     self.display_surface.blit(text_surf, (100, text_index*50))
