#!/usr/bin/python
# CowBulls.py

"""
    Copyright (C) 2018  Rahul Bothra

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
"""
"""
    Acknowledgement:
    Icons borrowed from multiple authors via FlatIcon: https://www.flaticon.com
"""

import sys
import pygame

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from sugar3.graphics.style import GRID_CELL_SIZE

import g
import utils


class CowBulls:
    def __init__(self, level=3):
        self.attempts = 0
        self.journal = True  # set to False if we come in via main()
        self.num = [int(x) for x in str(utils.get_random(level))]
        self.level = level
        self.game_over = False
        self.lives, self.offset = utils.get_lives(self.level)
        self.input = []
        self.highlight = 0
        self.status = None
        self.attempts_list = []

    def display(self):
        g.screen.fill(g.BG_COLOR)
        for x in range(3):
            for y in range(4):
                utils.blit_offset('dialpad/' + str(1 + x + 3 * y),
                                  g.DIALPAD, (x, y))

        for x in range(int(self.level)):
            utils.blit_offset('entries/entry-small',
                              (g.ATTEMPTS[0], g.ATTEMPTS[1] + g.DISP_SIZE),
                              (x, 0), 1)
            utils.blit_offset('status/bull', g.ATTEMPTS,
                              (self.level + .5 + x, 0), 1)
            utils.blit_offset('entries/question', g.ATTEMPTS, (x, 0), 1)

        for x in range(self.level):
            utils.blit_offset('dialpad/entry-big', g.DIALPAD,
                              (x + self.offset, -0.7))
        utils.blit_offset('lives/lives', g.DIALPAD, (0, 5))
        utils.blit_offset('lives/' + str(self.lives - self.attempts), g.DIALPAD, (1, 5))
        self.highlight_bt(g.pos)
        self.put_num()
        self.result()
        for num in range(len(self.attempts_list)):
            self.attempt_disp(self.attempts_list[num], num)
        self.display_answer()

    def result(self):
        if self.status:
            utils.load_blit(self.status, (g.w / 2, g.h / 2 - (128 * g.scale)))

    def put_num(self):
        for x in range(len(self.input)):
            utils.blit_offset('dialpad/' + str(self.input[x]), g.DIALPAD,
                              (self.offset + x, -1.6))

    def clear(self):
        for x in range(self.level):
            self.delete()

    def delete(self):
        if (len(self.input) != 0):
            self.input.pop()

    def g_init(self):
        g.init()

    def do_button(self, pos):
        pos = (int((pos[0] - g.DIALPAD[0]) / g.XGAP)
               ), int((pos[1] - g.DIALPAD[1]) / g.XGAP)
        num = 3 * pos[1] + pos[0] + 1

        if pos[1] >= 0 and pos[0] >= 0:
            if num in range(1, 10):
                if len(self.input) < self.level:
                    self.input.append(num)
            elif num == 10:
                self.enter()
            elif num == 11:
                if len(self.input) < self.level:
                    self.input.append(0)
            elif num == 12:
                self.delete()

    def remove_glow(self):
        if self.highlight:
            if self.highlight % 3:
                x, y = (self.highlight % 3) - 1, self.highlight / 3
            else:
                x, y = 2, self.highlight / 3 - 1
            g.clear_patch((g.DIALPAD[0] + x * (g.XGAP),
                           g.DIALPAD[1] + y * g.XGAP))
            utils.blit_offset('dialpad/' + str(self.highlight),
                              g.DIALPAD, (x, y))
            self.highlight = 0

    def glow(self, num, pos):
        utils.blit_offset('dialpad/highlight', g.DIALPAD, pos)
        utils.blit_offset('dialpad/' + str(num), g.DIALPAD, pos)

    def highlight_bt(self, pos):
        self.remove_glow()
        pos = int((pos[0] - g.DIALPAD[0]) /
                  g.XGAP), int((pos[1] - g.DIALPAD[1]) / g.XGAP)

        if pos[0] in range(3) and pos[1] in range(4):
            num = 3 * pos[1] + pos[0] + 1
            self.glow(num, pos)
            self.highlight = num
        else:
            self.highlight = 0

    def set_restart_button(self, restart):
        self.restart_button = restart

    def attempt_disp(self, attempt, attempt_no):
        for x in range(self.level):
            if self.num[x] == attempt[x]:
                status = 'bull'
            elif attempt[x] in self.num:
                status = 'cow'
            else:
                status = 'cancel'
            utils.blit_offset('status/' + status, g.ATTEMPTS,
                              (self.level + .5 + x, attempt_no + 1), 1)
            utils.blit_offset(
                'entries/' + str(attempt[x]), g.ATTEMPTS,
                (x, attempt_no + 1.1), 1)

    def display_answer(self):
        if self.status == 'lost':
            for x in range(self.level):
                utils.blit_offset(
                    'entries/' + str(self.num[x]),
                    g.ATTEMPTS, (x, self.lives + 2), 1)
                utils.blit_offset('status/bull', g.ATTEMPTS,
                                (x + 0.5 + self.level, self.lives + 2), 1)

    def enter(self):
        if len(self.input) != self.level:
            pass
        else:
            self.attempts_list.append(self.input)
            self.attempts += 1
            utils.blit_offset('lives/' + str(self.lives - self.attempts),
                              g.DIALPAD, (1, 5))
            if self.input == self.num:
                self.status = 'won'
                self.game_over = True
            elif self.attempts == self.lives:
                self.status = 'lost'
                self.game_over = True
            self.input = []

    def flush_queue(self):
        flushing = True
        while flushing:
            flushing = False
            if self.journal:
                while Gtk.events_pending():
                    Gtk.main_iteration()
            for event in pygame.event.get():
                flushing = True

    def run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode(
                    (event.size[0], event.size[1] - GRID_CELL_SIZE),
                    pygame.RESIZABLE)
                break
        g.init()
        self.display()
        if self.canvas is not None:
            self.canvas.grab_focus()
        going = True
        while going:
            # Pump Gtk messages.
            if self.journal:
                while Gtk.events_pending():
                    Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    going = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_over:
                        self.do_button(event.pos)
                    g.redraw = True
                    self.flush_queue()
                elif event.type == pygame.MOUSEMOTION:
                    g.pos = event.pos
                    g.redraw = True
                    if self.canvas is not None:
                        self.canvas.grab_focus()
                    self.highlight_bt(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if not self.game_over:
                        value = utils.get_input(event.key)
                        if value:
                            if len(self.input) < self.level:
                                self.input.append(int(value))
                        elif event.key == pygame.K_BACKSPACE:
                            self.delete()
                        elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                            self.enter()
                    g.redraw = True
                    self.flush_queue()
            if g.redraw:
                self.display()
                g.screen.blit(g.pointer, g.pos)
                pygame.display.flip()
                g.redraw = False

            pygame.display.update()

    def restart(self):
        self.change_level(self.level)

    def change_level(self, level):
        self.attempts = 0
        self.journal = True  # set to False if we come in via main()
        self.num = [int(x) for x in str(utils.get_random(level))]
        self.level = level
        self.game_over = False
        self.lives, self.offset = utils.get_lives(self.level)
        self.input = []
        self.highlight = 0
        self.status = None
        self.attempts_list = []
        self.run()


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1200, 700), pygame.FULLSCREEN)
    game = CowBulls()
    game.journal = False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
