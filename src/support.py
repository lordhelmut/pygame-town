import logging
import pygame
from os import walk
from settings import *


def import_folder(path):
    surface_list = []

    # for folder_name, subfolder_name, image_files in walk(path):
    for _, __, img_files in walk(path):
        if (LOGGINGOPTS == 'DEBUG'):
            logging.debug(f'folder path import: {img_files}')
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
            if (LOGGINGOPTS == 'DEBUG'):
                logging.debug(f'image surf: {image_surf}')
                logging.debug(f'image full_path: {full_path}')

    return surface_list
