import pygame
import logging
from settings import *
from timer import Timer


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

        # which item is selected in menu
        self.index = 0
        self.timer = Timer(200)

        # entries
        self.options = list(self.player.item_inventory.keys()) + \
            list(self.player.seed_inventory.keys())
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

        # set attributes for buying & selling text
        self.buy_text = self.font.render('BUY', False, 'White')
        self.sell_text = self.font.render('SELL', False, 'White')

    def input(self):
        keys = pygame.key.get_pressed()
        # update on every keypress
        self.timer.update()
        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()

            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:
                self.timer.activate()

                # get item
                current_item = self.options[self.index]

                # sell
                if self.index <= self.sell_border:
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]

                # buy
                else:
                    seed_price = PURCHASE_PRICES[current_item]
                    if self.player.money >= seed_price:
                        self.player.seed_inventory[current_item] += 1
                        self.player.money -= PURCHASE_PRICES[current_item]

        # roll the index over if hit top or bottom of menu
        if self.index < 0:
            self.index = len(self.options) - 1
        if self.index > len(self.options) - 1:
            self.index = 0

    def show_entry(self, text_surf, amount, top, selected):
        # background
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width,
                              text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'Hot pink', bg_rect, 0, 4)

        # text
        text_rect = text_surf.get_rect(
            midleft=(self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        # amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(
            midright=(self.main_rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        # selected entry
        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
            # sell
            if self.index <= self.sell_border:
                pos_rect = self.sell_text.get_rect(
                    midleft=(self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            # buy
            else:
                pos_rect = self.buy_text.get_rect(
                    midleft=(self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        self.input()
        self.display_money()
        # pygame.draw.rect(self.display_surface, 'Hot pink', self.main_rect)
        # use the item inventory as the menu options
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * \
                (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + \
                list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top, self.index == text_index)
            # self.display_surface.blit(text_surf, (100, text_index*50))
