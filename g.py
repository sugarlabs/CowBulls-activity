import os
import pygame

app = 'CowBulls'
BG_COLOR = (220, 220, 220)
images = {}


def init():
    global redraw, screen, images
    global scale, w, h, pointer, pos
    global INPUT_SIZE, DISP_SIZE, DIALPAD
    global ATTEMPTS, XGAP, DKP

    redraw = True
    for root, subdirs, files in os.walk('data'):
        for file in files:
            load_image(os.path.join(root, file))

    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill(BG_COLOR)
    pygame.display.flip()
    w, h = screen.get_size()
    scale = min([w / 1200.0, h / 700.0])

    pos = pygame.mouse.get_pos()
    pointer = images['data/pointer.png']
    pygame.mouse.set_visible(False)

    INPUT_SIZE = 75 * scale
    DISP_SIZE = 55 * scale
    XGAP = (10 + INPUT_SIZE) * scale
    DKP = (10 + DISP_SIZE) * scale
    ATTEMPTS = (60 * scale, 25 * scale)
    DIALPAD = (900 * scale, 200 * scale)


def load_image(file_path):
    img = pygame.image.load(file_path)
    images[file_path] = img


def clear_patch(pos, size=0):
    if not size:
        pygame.draw.rect(
            screen,
            BG_COLOR,
            (pos[0],
             pos[1],
                INPUT_SIZE,
                INPUT_SIZE))
    else:
        pygame.draw.rect(screen, BG_COLOR, (pos[0], pos[1], size, size))
