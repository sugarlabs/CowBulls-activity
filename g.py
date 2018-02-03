import pygame
import os

BG_COLOR = (220, 220, 220)
images = {}


def init():
    global screen, images
    for root, subdirs, files in os.walk('icons'):
        for file in files:
            load_image(os.path.join(root, file))

    screen = pygame.display.get_surface()
    pygame.display.set_caption('CowBulls')
    screen.fill(BG_COLOR)


def load_image(file_path):
    img = pygame.image.load(file_path)
    images[file_path] = img
