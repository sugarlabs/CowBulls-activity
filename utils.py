# utils.py
"""
    Copyright (C) 2018  Rahul Bothra

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""

import pygame
import g
import random

Numbers = {
    pygame.K_1: '1',
    pygame.K_2: '2',
    pygame.K_3: '3',
    pygame.K_4: '4',
    pygame.K_5: '5',
    pygame.K_6: '6',
    pygame.K_7: '7',
    pygame.K_8: '8',
    pygame.K_9: '9',
    pygame.K_0: '0',
    pygame.K_KP0: '0',
    pygame.K_KP1: '1',
    pygame.K_KP2: '2',
    pygame.K_KP3: '3',
    pygame.K_KP4: '4',
    pygame.K_KP5: '5',
    pygame.K_KP6: '6',
    pygame.K_KP7: '7',
    pygame.K_KP8: '8',
    pygame.K_KP9: '9',
}

levels = {
    2: (5, 0.5),
    3: (5, 0),
    4: (6, -0.5)
}


def get_input(key):
    if key in Numbers:
        return Numbers[key]
    else:
        return None


def blit_offset(file_path, pos, offset, flag=0):
    if not flag:
        load_blit(file_path,
                  (pos[0] + offset[0] * g.XGAP, pos[1] + offset[1] * g.XGAP))
    if flag:
        load_blit(file_path,
                  (pos[0] + offset[0] * g.DKP, pos[1] + offset[1] * g.DKP))


def load_blit(file_path, pos):
    file_path = 'data/' + file_path + '.png'
    sizex, sizey = g.images[file_path].get_rect().size
    img = pygame.transform.smoothscale(
        g.images[file_path], (int(sizex * g.scale), int(sizey * g.scale)))
    g.screen.blit(img, pos)


def get_lives(level):
    if level in levels:
        return levels[level]
    else:
        return (0, 0)


def get_random(level):
    start = 10**(level - 1)
    end = 10**level - 1
    return random.randint(start, end)
