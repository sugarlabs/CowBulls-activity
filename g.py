import pygame
import os
import utils

app = 'CowBulls'
ver = '1'

BG_COLOR = (220, 220, 220)
images = {}


def init():
    global screen, images, scale
    global INPUT_SIZE, DISP_SIZE, DIALPAD
    global ATTEMPTS, XGAP, DKP
    
    INPUT_SIZE = 70
    DISP_SIZE  = 55
    XGAP       = 10 + INPUT_SIZE
    DKP        = 10 + DISP_SIZE

    for root, subdirs, files in os.walk('data'):
        for file in files:
            load_image(os.path.join(root, file))

    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill(BG_COLOR)
    pygame.display.flip()
    w, h = screen.get_size()
    scale = min([w/1200.0, h/700.0])
    INPUT_SIZE *= scale
    DISP_SIZE *= scale
    DIALPAD    = (800*scale, 200*scale)
    ATTEMPTS   = (60*scale, 25*scale)
    XGAP *= scale
    DKP *= scale

    pos = pygame.mouse.get_pos()
    # pointer = utils.load_image('pointer.png', True)
    # pygame.mouse.set_visible(False)


def load_image(file_path):
    img = pygame.image.load(file_path)
    images[file_path] = img


def clear_patch(pos, size=0):
    if not size:
        pygame.draw.rect(screen, BG_COLOR, (pos[0], pos[1], INPUT_SIZE, INPUT_SIZE))
    else:
        pygame.draw.rect(screen, BG_COLOR, (pos[0], pos[1], size, size))