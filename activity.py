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
from gi.repository import GdkPixbuf

from sugar3.activity import activity
from sugar3.graphics.toolbarbox import ToolbarBox
from sugar3.activity.widgets import ActivityToolbarButton, StopButton
from sugar3.graphics.toolbutton import ToolButton
from sugar3.graphics.style import GRID_CELL_SIZE
from sugar3 import profile

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
        comboField.show()

        separator = Gtk.SeparatorToolItem()
        separator.props.draw = True
        separator.set_expand(False)
        toolbox.toolbar.insert(separator, -1)
        separator.show()

        restart = ToolButton('media-playback-start')
        toolbox.toolbar.insert(restart, -1)
        restart.set_tooltip(_('Restart'))
        restart.connect('clicked', self._restart_button_cb)
        restart.show()

        next_bt = ToolButton('next')
        toolbox.toolbar.insert(next_bt, -1)
        next_bt.set_tooltip(_('Next Number'))
        next_bt.connect('clicked', self._next_button_cb)
        next_bt.set_sensitive(False)
        next_bt.show()

        separator2 = Gtk.SeparatorToolItem()
        separator2.props.draw = True
        separator2.set_expand(False)
        toolbox.toolbar.insert(separator2, -1)
        separator2.show()

        comboLabel = Gtk.ToolItem()
        label1 = Gtk.Label()
        label1.set_text(_('Score:') + '  ')
        comboLabel.add(label1)
        toolbox.toolbar.insert(comboLabel, -1)

        self._score_image = Gtk.Image()
        item = Gtk.ToolItem()
        item.add(self._score_image)
        toolbox.toolbar.insert(item, -1)
        item.show()

        separator2 = Gtk.SeparatorToolItem()
        separator2.props.draw = False
        separator2.set_expand(True)
        toolbox.toolbar.insert(separator2, -1)
        separator2.show()

        stop_button = StopButton(self)
        stop_button.props.accelerator = _('<Ctrl>Q')
        toolbox.toolbar.insert(stop_button, -1)
        stop_button.show()

        toolbox.show()
        self.set_toolbar_box(toolbox)
        self.show_all()

        # Create the game instance.
        self.game = CowBulls.CowBulls(parent=self)

        # Build the Pygame canvas.
        self.game.canvas = self._pygamecanvas = sugargame.canvas.PygameCanvas(
            self, main=self.game.run, modules=[pygame.display, pygame.font])

        # Note that set_canvas implicitly calls
        # read_file when resuming from the Journal.
        self.game.set_next_button(next_bt)
        self.set_canvas(self._pygamecanvas)
        Gdk.Screen.get_default().connect('size-changed',
                                         self.__configure_cb)

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

    def update_score(self, score):
        pixbuf = self._svg_str_to_pixbuf(self._score_icon(score))
        self._score_image.set_from_pixbuf(pixbuf)
        self._score_image.show()

    def _svg_str_to_pixbuf(self, svg_string):
        ''' Load pixbuf from SVG string '''
        pl = GdkPixbuf.PixbufLoader.new_with_type('svg')
        pl.write(svg_string)
        pl.close()
        pixbuf = pl.get_pixbuf()
        return pixbuf

    def _score_icon(self, score):
        return \
            '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + \
            '<svg\n' + \
            'xmlns:dc="http://purl.org/dc/elements/1.1/"\n' + \
            'xmlns:cc="http://creativecommons.org/ns#"\n' + \
            'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n' + \
            'xmlns:svg="http://www.w3.org/2000/svg"\n' + \
            'xmlns="http://www.w3.org/2000/svg"\n' + \
            'version="1.1"\n' + \
            'width="55"\n' + \
            'height="55"\n' + \
            'viewBox="0 0 55 55">\n' + \
            '<path\n' + \
            'd="M 27.497,50.004 C 39.927,50.004 50,39.937 50,27.508 50,'\
            '15.076 39.927,4.997 27.497,4.997 15.071,4.997 5,15.076 5,27.508 '\
            '5,39.937 15.071,50.004 27.497,50.004 z"\n' + \
            'style="fill:#ffffff;fill-opacity:1" /><text\n' + \
            'style="fill:#000000;fill-opacity:1;stroke:none;font-family:Sans">'\
            '<tspan\n' + \
            'x="27.5"\n' + \
            'y="37.3"\n' + \
            'style="font-size:24px;text-align:center;text-anchor:middle">'\
            '%d' % score + \
            '</tspan></text>\n' + \
            '</svg>'

    def _restart_button_cb(self, event):
        self.game.restart()

    def _next_button_cb(self, event):
        self.game.nextRound()


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
