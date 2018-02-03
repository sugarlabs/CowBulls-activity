import pygame
import sys
from pygame.locals import *
import utils
import g

X = 800
Y = 200
XX = 60
YY = 25
MARGIN = 10
INPUT_SIZE = 70
DISP_SIZE = 55
XGAP = MARGIN + INPUT_SIZE
DPX = MARGIN + DISP_SIZE
BG_COLOR = (220, 220, 220)


class CowBulls:
    def __init__(self, level=3):
        self.attempts = 0
        self.num = [int(x) for x in str(utils.get_random(level))]
        self.level = level
        self.game_over = False
        self.lives, self.offset = utils.get_lives(self.level)
        self.input = []
        self.highlight = 0

    def display(self):
        for x in range(3):
            for y in range(4):
                utils.blit_offset('dialpad/' + str(1 + x + 3 * y), (X, Y), (x, y))

        for x in range(int(self.level)):
            utils.blit_offset('entries/entry-small', (XX, YY + DISP_SIZE), (x, 0), 1)
            utils.blit_offset('status/bull', (XX, YY), (self.level + .5 + x, 0), 1)
            utils.blit_offset('entries/question', (XX, YY), (x, 0), 1)

        for x in range(self.level):
            utils.blit_offset('dialpad/entry-big', (X, Y), (x + self.offset, -0.7))
        utils.blit_offset('lives/lives', (X, Y), (0, 5))
        utils.blit_offset('lives/' + str(self.lives), (X, Y), (1, 5))

    def put_num(self, valy):
        if len(self.input) < self.level:
            utils.blit_offset('dialpad/' + str(valy), (X, Y), (self.offset + len(self.input), -1.6))
            self.input.append(int(valy))

    def clear(self):
        for x in range(self.level):
            self.delete()

    def delete(self):
        if (len(self.input) != 0):
            self.clear_patch(
                (X + (self.offset + len(self.input) - 1) * (XGAP), Y - 1.6 * XGAP))
            self.input.pop()

    def do_button(self, pos):
        pos = ((pos[0] - X) / XGAP), ((pos[1] - Y) / XGAP)
        num = 3 * pos[1] + pos[0] + 1
        if num > 0 and num <= 9:
            self.put_num(num)
        elif num == 10:
            self.enter()
        elif num == 11:
            self.put_num(0)
        elif num == 12:
            self.delete()

    def clear_patch(self, pos, size=INPUT_SIZE):
        pygame.draw.rect(g.screen, BG_COLOR, (pos[0], pos[1], size, size))

    def remove_glow(self):
        if self.highlight:
            if self.highlight % 3:
                x, y = (self.highlight % 3) - 1, self.highlight / 3
            else:
                x, y = 2, self.highlight / 3 - 1
            self.clear_patch((X + x * (XGAP), Y + y * XGAP))
            utils.blit_offset('dialpad/' + str(self.highlight), (X, Y), (x, y))
            self.highlight = 0

    def glow(self, num, pos):
        utils.blit_offset('dialpad/highlight', (X, Y), pos)
        utils.blit_offset('dialpad/' + str(num), (X, Y), pos)

    def highlight_bt(self, pos):
        self.remove_glow()
        pos = ((pos[0] - X) / XGAP), ((pos[1] - Y) / XGAP)

        if pos[0] in range(3) and pos[1] in range(4):
            num = 3 * pos[1] + pos[0] + 1
            self.glow(num, pos)
            self.highlight = num
        else:
            self.highlight = 0

    def attempt_disp(self):
        for x in range(self.level):
            if self.num[x] == self.input[x]:
                status = 'bull'
            elif self.input[x] in self.num:
                status = 'cow'
            else:
                status = 'cancel'
            utils.blit_offset('status/' + status, (XX, YY), (self.level + .5 + x, self.attempts + 1), 1)
            utils.blit_offset('entries/' + str(self.input[x]), (XX, YY), (x, self.attempts + 1), 1)

    def display_answer(self):
        for x in range(self.level):
            tt = self.lives + 2
            utils.blit_offset('entries/' + str(self.num[x]), (XX, YY), (x, self.lives + 2), 1)
            utils.blit_offset('status/bull', (XX, YY), (x + 0.5 + self.level, self.lives + 2), 1)

    def enter(self):
        if len(self.input) != self.level:
            pass
        else:
            self.attempt_disp()
            self.attempts += 1
            utils.blit_offset('lives/' + str(self.lives - self.attempts)), (X, Y), (1, 5))
            status = None
            if self.input == self.num:
                status = 'won'
            elif self.attempts == self.lives:
                self.display_answer()
                status = 'lost'
            if status:
                utils.load_blit(status, (550, 300))
                self.game_over = True

            self.clear()

    def run(self):
        g.init()
        self.display()
        while True:
            for event in pygame.event.get():
                if not self.game_over:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.do_button(event.pos)
                    elif event.type == pygame.MOUSEMOTION:
                        self.highlight_bt(event.pos)
                    elif event.type == pygame.KEYDOWN:
                        value = utils.get_input(event.key)
                        if value:
                            self.put_num(value)
                        elif event.key == pygame.K_BACKSPACE:
                            self.delete()
                        elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                            self.enter()
            pygame.display.update()

    def restart(self):
        self.init(self.level)
        self.run()

    def change_level(self, level):
        self.init(level)
        self.run()



if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1200, 700))
    game = CowBulls(int(sys.argv[1]))
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
