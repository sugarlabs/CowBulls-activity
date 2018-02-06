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
    def __init__(self, level=3, parent=None):
        self.parent = parent
        self.level = level
        self.journal = True  # set to False if we come in via main()
        self.num = [int(x) for x in str(utils.get_random(level))]
        self.lives, self.offset = utils.get_lives(self.level)
        self.status = None
        self.input = []
        self.compare_list = []
        self.attempts_list = []
        self.score = 0
        self.parent.update_score(self.score)

    def display(self):
        g.screen.fill(g.BG_COLOR)
        for x in range(3):
            for y in range(4):
                utils.blit_offset('dialpad/' + str(1 + x + 3 * y),
                                  g.DIALPAD, (x, y))

        for x in range(int(self.level)):
            utils.blit_offset('entries/entry-small',
                              (g.ATTEMPT[0], g.ATTEMPT[1] + g.DISP_SIZE),
                              (x, 0), 1)
            utils.blit_offset('status/bull', g.ATTEMPT,
                              (self.level + .5 + x, 0), 1)
            utils.blit_offset('entries/question', g.ATTEMPT, (x, 0), 1)
            utils.blit_offset('dialpad/entry-big', g.DIALPAD,
                              (x + self.offset, -0.7))

        for x in range(len(self.input)):
            utils.blit_offset('dialpad/' + str(self.input[x]), g.DIALPAD,
                              (self.offset + x, -1.6))

        utils.blit_offset('lives/lives', g.DIALPAD, (0, 5))
        utils.blit_offset('lives/' + str(self.lives -
                          len(self.attempts_list)), g.DIALPAD, (1, 5))
        self.highlight()
        self.result()
        self.attempt_disp()
        if self.status == 'lost':
            self.display_answer()

    def result(self):
        if self.status:
            utils.load_blit(self.status, (g.w / 2, g.h / 2 - (128 * g.scale)))

    def delete(self):
        if (len(self.input) != 0):
            self.input.pop()

    def g_init(self):
        g.init()

    def do_key(self, event):
        value = utils.get_input(event.key)
        if value:
            if len(self.input) < self.level:
                self.input.append(int(value))
        elif event.key == pygame.K_BACKSPACE:
            self.delete()
        elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
            self.enter()

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

    def highlight(self):
        pos = int((g.pos[0] - g.DIALPAD[0]) /
                  g.XGAP), int((g.pos[1] - g.DIALPAD[1]) / g.XGAP)

        if pos[0] in range(3) and pos[1] in range(4):
            num = 3 * pos[1] + pos[0] + 1
            utils.blit_offset('dialpad/highlight', g.DIALPAD, pos)
            utils.blit_offset('dialpad/' + str(num), g.DIALPAD, pos)

    def attempt_disp(self):
        for num in range(len(self.attempts_list)):
            for x in range(self.level):
                utils.blit_offset('status/' + self.compare_list[num][x],
                                  g.ATTEMPT, (self.level + .5 + x, num + 1), 1)
                utils.blit_offset(
                    'entries/' + str(self.attempts_list[num][x]), g.ATTEMPT,
                    (x, num + 1.1), 1)

    def display_answer(self):
        for x in range(self.level):
            utils.blit_offset(
                'entries/' + str(self.num[x]),
                g.ATTEMPT, (x, self.lives + 2), 1)
            utils.blit_offset('status/bull', g.ATTEMPT,
                              (x + 0.5 + self.level, self.lives + 2), 1)

    def enter(self):
        if len(self.input) != self.level:
            pass
        else:
            status = []
            for x in range(self.level):
                if self.num[x] == self.input[x]:
                    status.append('bull')
                elif self.input[x] in self.num:
                    status.append('cow')
                else:
                    status.append('cancel')

            self.compare_list.append(status)
            self.attempts_list.append(self.input)
            if self.input == self.num:
                self.status = 'won'
                self.next_button.set_sensitive(True)
                self.score += (self.lives - len(self.attempts_list)) + 1
                if self.parent:
                    self.parent.update_score(self.score)
            elif len(self.attempts_list) == self.lives:
                self.status = 'lost'
            self.input = []

    def set_next_button(self, next_bt):
        self.next_button = next_bt

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
                if event.type == pygame.MOUSEMOTION:
                    g.pos = event.pos
                    g.redraw = True
                    if self.canvas is not None:
                        self.canvas.grab_focus()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.status:
                        self.do_button(event.pos)
                        g.redraw = True
                    self.flush_queue()

                elif event.type == pygame.KEYDOWN:
                    if not self.status:
                        self.do_key(event)
                        g.redraw = True
                    self.flush_queue()

                elif event.type == pygame.QUIT:
                    going = False

            if g.redraw:
                self.display()
                g.screen.blit(g.pointer, g.pos)
                pygame.display.flip()
                g.redraw = False

            pygame.display.update()

    def restart(self):
        g.screen.fill((0,0,0))
        self.change_level(self.level)

    def change_level(self, level):
        g.screen.fill((0,0,0))
        self.level = level
        self.journal = True  # set to False if we come in via main()
        self.num = [int(x) for x in str(utils.get_random(level))]
        self.lives, self.offset = utils.get_lives(self.level)
        self.status = None
        self.input = []
        self.attempts_list = []
        self.compare_list = []
        self.score = 0
        self.parent.update_score(self.score)

    def nextRound(self):
        g.screen.fill((0,0,0))
        self.next_button.set_sensitive(False)
        self.journal = True  # set to False if we come in via main()
        self.num = [int(x) for x in str(utils.get_random(self.level))]
        self.lives, self.offset = utils.get_lives(self.level)
        self.status = None
        self.input = []
        self.attempts_list = []
        self.compare_list = []


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1200, 700), pygame.FULLSCREEN)
    game = CowBulls()
    game.journal = False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
