import pygame
import sys
from pygame.locals import *
from utils import *
import g
from gi.repository import Gtk
import logging
class CowBulls:
    def __init__(self, level=3):
        self.attempts = 0
        self.num = [int(x) for x in str(get_random(level))]
        self.level = level
        self.game_over = False
        self.lives, self.offset = get_lives(self.level)
        self.input = []
        self.highlight = 0
        

    def display(self):
        for x in range(3):
            for y in range(4):
                blit_offset('dialpad/' + str(1 + x + 3 * y), g.DIALPAD, (x, y))

        for x in range(int(self.level)):
            blit_offset('entries/entry-small', (g.ATTEMPTS[0], g.ATTEMPTS[1] + g.DISP_SIZE), (x, 0), 1)
            blit_offset('status/bull', g.ATTEMPTS, (self.level + .5 + x, 0), 1)
            blit_offset('entries/question', g.ATTEMPTS, (x, 0), 1)

        for x in range(self.level):
            blit_offset('dialpad/entry-big', g.DIALPAD, (x + self.offset, -0.7))
        blit_offset('lives/lives', g.DIALPAD, (0, 5))
        blit_offset('lives/' + str(self.lives), g.DIALPAD, (1, 5))

    def put_num(self, valy):
        if len(self.input) < self.level:
            blit_offset('dialpad/' + str(valy), g.DIALPAD, (self.offset + len(self.input), -1.6))
            self.input.append(int(valy))

    def clear(self):
        for x in range(self.level):
            self.delete()

    def delete(self):
        if (len(self.input) != 0):
            g.clear_patch(
                (g.DIALPAD[0] + (self.offset + len(self.input) - 1) * (g.XGAP), g.DIALPAD[1] - 1.6 * g.XGAP))
            self.input.pop()

    def do_button(self, pos):
        pos = (int((pos[0] - g.DIALPAD[0]) / g.XGAP)), int((pos[1] - g.DIALPAD[1]) / g.XGAP)
        num = 3 * pos[1] + pos[0] + 1
        logging.debug(str(pos))
        logging.debug(str(num))
        if pos[1]>= 0 and pos[0]>=0:
            if num in range(1,10):
                self.put_num(num)
            elif num == 10:
                self.enter()
            elif num == 11:
                self.put_num(0)
            elif num == 12:
                self.delete()

    def remove_glow(self):
        if self.highlight:
            if self.highlight % 3:
                x, y = (self.highlight % 3) - 1, self.highlight / 3
            else:
                x, y = 2, self.highlight / 3 - 1
            g.clear_patch((g.DIALPAD[0] + x * (g.XGAP), g.DIALPAD[1] + y * g.XGAP))
            blit_offset('dialpad/' + str(self.highlight), g.DIALPAD, (x, y))
            self.highlight = 0

    def glow(self, num, pos):
        blit_offset('dialpad/highlight', g.DIALPAD, pos)
        blit_offset('dialpad/' + str(num), g.DIALPAD, pos)

    def highlight_bt(self, pos):
        self.remove_glow()
        pos = int((pos[0] - g.DIALPAD[0]) / g.XGAP), int((pos[1] - g.DIALPAD[1]) / g.XGAP)

        if pos[0] in range(3) and pos[1] in range(4):
            num = 3 * pos[1] + pos[0] + 1
            self.glow(num, pos)
            self.highlight = num
        else:
            self.highlight = 0

    def set_cyan_button(self, cyan):
        self.cyan_button = cyan

    def attempt_disp(self):
        for x in range(self.level):
            if self.num[x] == self.input[x]:
                status = 'bull'
            elif self.input[x] in self.num:
                status = 'cow'
            else:
                status = 'cancel'
            blit_offset('status/' + status, g.ATTEMPTS, (self.level + .5 + x, self.attempts + 1), 1)
            blit_offset('entries/' + str(self.input[x]), g.ATTEMPTS, (x, self.attempts + 1), 1)

    def display_answer(self):
        for x in range(self.level):
            tt = self.lives + 2
            blit_offset('entries/' + str(self.num[x]), g.ATTEMPTS, (x, self.lives + 2), 1)
            blit_offset('status/bull', g.ATTEMPTS, (x + 0.5 + self.level, self.lives + 2), 1)

    def enter(self):
        if len(self.input) != self.level:
            pass
        else:
            self.attempt_disp()
            self.attempts += 1
            blit_offset('lives/' + str(self.lives - self.attempts), g.DIALPAD, (1, 5))
            status = None
            if self.input == self.num:
                status = 'won'
            elif self.attempts == self.lives:
                self.display_answer()
                status = 'lost'
            if status:
                load_blit(status, (550, 300))
                self.game_over = True

            self.clear()

    def flush_queue(self):
        flushing = True
        while flushing:
            flushing = False

            while Gtk.events_pending():
                Gtk.main_iteration()
            for event in pygame.event.get():
                flushing = True

    def run(self):
        g.init()
        self.display()
        while True:

            # Pump Gtk messages.
            while Gtk.events_pending():
                Gtk.main_iteration()
            for event in pygame.event.get():
                if not self.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.do_button(event.pos)
                        self.flush_queue()
                    elif event.type == pygame.MOUSEMOTION:
                        self.highlight_bt(event.pos)
                        self.flush_queue()
                    elif event.type == pygame.KEYDOWN:
                        logging.debug("Inside it")
                        value = get_input(event.key)
                        if value:
                            self.put_num(value)
                        elif event.key == pygame.K_BACKSPACE:
                            self.delete()
                        elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                            self.enter()
                        self.flush_queue()
            pygame.display.update()

    def restart(self):
        self.change_level(self.level)

    def change_level(self, level):
        self.attempts = 0
        self.num = [int(x) for x in str(get_random(level))]
        self.level = level
        self.game_over = False
        self.lives, self.offset = get_lives(self.level)
        self.input = []
        self.highlight = 0
        self.run()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1024, 768), pygame.FULLSCREEN) 
    game = CowBulls(int(sys.argv[1]))
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)