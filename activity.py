# activity.py
# my standard link between sugar and my activity
"""
    Copyright (C) 2010  Peter Hewitt
    Copyright (C) 2013  Ignacio Rodriguez

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""

import os
from gettext import gettext as _

from gi.repository import Gtk
from gi.repository import Gdk

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton, StopButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.style import GRID_CELL_SIZE
from sugar3 import profile

import pygame
import sugargame.canvas
import main


class CowBullsActivtiy(activity.Activity):
    LOWER = 0
    UPPER = 400

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        # Get user's Sugar colors
        self._sugarcolors = profile.get_color().to_string().split(',')
        colors = [[int(self._sugarcolors[0][1:3], 16),
                   int(self._sugarcolors[0][3:5], 16),
                   int(self._sugarcolors[0][5:7], 16)],
                  [int(self._sugarcolors[1][1:3], 16),
                   int(self._sugarcolors[1][3:5], 16),
                   int(self._sugarcolors[1][5:7], 16)]]

        # No sharing
        self.max_participants = 1

        # Build the activity toolbar.
        toolbox = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbox.toolbar.insert(activity_button, 0)
        activity_button.show()

        self.separator0 = Gtk.SeparatorToolItem()
        self.separator0.props.draw = False
        if Gdk.Screen.width() > 1023:
            toolbox.toolbar.insert(self.separator0, -1)
        self.separator0.show()

        cyan = ToolButton('cyan')
        toolbox.toolbar.insert(cyan, -1)
        cyan.set_tooltip(_('Reset'))
        cyan.connect('clicked', self._button_cb, 'cyan')
        cyan.set_sensitive(False)
        cyan.show()

        separator2 = Gtk.SeparatorToolItem()
        separator2.props.draw = True
        separator2.set_expand(False)
        toolbox.toolbar.insert(separator2, -1)
        separator2.show()

        item1 = Gtk.ToolItem()
        label1 = Gtk.Label()
        label1.set_text(_('Levels') + ' ')
        item1.add(label1)
        toolbox.toolbar.insert(item1, -1)

        item2 = Gtk.ToolItem()

        levels = (_('Easy'),
                  _('Medium'),
                  _('Hard'))

        combo = Combo(levels)
        item2.add(combo)
        combo.connect('changed', self.change_combo)
        toolbox.toolbar.insert(item2, -1)

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbox.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        stop_button.props.accelerator = _('<Ctrl>Q')
        toolbox.toolbar.insert(stop_button, -1)
        stop_button.show()

        toolbox.show()
        self.set_toolbar_box(toolbox)

        self._toolbar = toolbox.toolbar

        # Create the game instance.
        self.game = main.CowBulls()

        # Build the Pygame canvas.
        self.game.canvas = self._pygamecanvas = sugargame.canvas.PygameCanvas(
            self, main=self.game.run, modules=[pygame.display, pygame.font])

        # Note that set_canvas implicitly calls
        # read_file when resuming from the Journal.
        self.set_canvas(self._pygamecanvas)

        Gdk.Screen.get_default().connect('size-changed',
                                         self.__configure_cb)

    def change_combo(self, combo):
        level = combo.get_active()
        self.game.change_level(int(level))

    def get_preview(self):
        return self._pygamecanvas.get_preview()

    def __configure_cb(self, event):
        ''' Screen size has changed '''
        logging.debug(self._pygamecanvas.get_allocation())
        pygame.display.set_mode((Gdk.Screen.width(),
                                 Gdk.Screen.height() - GRID_CELL_SIZE),
                                pygame.RESIZABLE)
        self.game.save_pattern()
        self.game.g_init()
        self._speed_range.set_value(200)
        self.game.run(restore=True)

    def read_file(self, file_path):
        try:
            f = open(file_path, 'r')
        except Exception as e:
            logging.debug('Error opening %s: %s' % (file_path, e))
            return
        f.close()

    def write_file(self, file_path):
        f = open(file_path, 'w')
        f.close()

    def _button_cb(self, button=None, color=None):
        self.game.restart()


class Combo(Gtk.ComboBox):
    def __init__(self, options):

        self.liststore = Gtk.ListStore(str)

        for o in options:
            self.liststore.append([o])

        Gtk.ComboBox.__init__(self)
        self.set_model(self.liststore)
        cell = Gtk.CellRendererText()
        self.pack_start(cell, True)
        self.add_attribute(cell, 'text', 0)

        self.set_active(0)
