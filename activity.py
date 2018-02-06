# activity.py
# my standard link between sugar and my activity
"""
    Copyright (C) 2018  Rahul Bothra

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""

from gettext import gettext as _

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton, StopButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.style import GRID_CELL_SIZE

import pygame
import sugargame.canvas
import CowBulls


class CowBullsActivtiy(activity.Activity):

    def __init__(self, handle):
        activity.Activity.__init__(self, handle)

        # No sharing (Future Improvement)
        self.max_participants = 1

        # Build the activity toolbar.
        toolbox = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbox.toolbar.insert(activity_button, 0)
        activity_button.show()

        restart = ToolButton('media-playback-start')
        toolbox.toolbar.insert(restart, -1)
        restart.set_tooltip(_('Restart'))
        restart.connect('clicked', self._restart_button_cb)
        restart.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = True
        separator.set_expand(False)
        toolbox.toolbar.insert(separator, -1)
        separator.show()

        comboLabel = Gtk.ToolItem()
        label1 = Gtk.Label()
        label1.set_text(_('Level:') + ' ')
        comboLabel.add(label1)
        toolbox.toolbar.insert(comboLabel, -1)

        levels = (_('Easy'),
                  _('Moderate'),
                  _('Hard'))

        comboField = Gtk.ToolItem()
        combo = Combo(levels)
        comboField.add(combo)
        combo.connect('changed', self.change_combo)
        toolbox.toolbar.insert(comboField, -1)

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
        self.show_all()

        # Create the game instance.
        self.game = CowBulls.CowBulls()

        # Build the Pygame canvas.
        self.game.canvas = self._pygamecanvas = sugargame.canvas.PygameCanvas(
            self, main=self.game.run, modules=[pygame.display, pygame.font])

        # Note that set_canvas implicitly calls
        # read_file when resuming from the Journal.
        self.set_canvas(self._pygamecanvas)
        Gdk.Screen.get_default().connect('size-changed',
                                         self.__configure_cb)

        self.game.set_restart_button(restart)

    def change_combo(self, combo):
        level = combo.get_active()
        self.game.change_level(int(level) + 3)

    def get_preview(self):
        return self._pygamecanvas.get_preview()

    def __configure_cb(self, event):
        ''' Screen size has changed '''
        pygame.display.set_mode((Gdk.Screen.width(),
                                 Gdk.Screen.height() - GRID_CELL_SIZE),
                                pygame.RESIZABLE)
        self.game.g_init()
        self.game.run()

    def _restart_button_cb(self, event):
        self.game.restart()


class Combo(Gtk.ComboBox):
    def __init__(self, levels):

        self.liststore = Gtk.ListStore(str)
        for level in levels:
            self.liststore.append([level])

        Gtk.ComboBox.__init__(self)
        self.set_model(self.liststore)
        cell = Gtk.CellRendererText()
        self.pack_start(cell, True)
        self.add_attribute(cell, 'text', 0)
        self.set_active(0)
