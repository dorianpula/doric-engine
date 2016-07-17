import collections

from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line

import kivy.utils
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.vector import Vector

MapCoords = collections.namedtuple('MapCoords', ['row', 'col'])


class HexMapCell(Label):
    def __init__(self, row=0, col=0, **kwargs):
        super(HexMapCell, self).__init__(**kwargs)
        self.coords = MapCoords(row, col)
        self.selected = False
        self.visible_on_map = False
        self.terrain_colour = Color(0, 0, 0, 1)
        self.terrain = ''

    def map_coordinates(self):
        return self.coords.row / 3, self.coords.col / 2

    def map_display_text(self):
        map_x, map_y = self.map_coordinates()
        return "({}, {}) \n {}".format(map_x, map_y, self.terrain)

    def update_pos(self, instance, value):
        # Determine the location of the solid hexagon cell.  Needs to be offset from the centre of the hex.
        radius = 2 * self.height
        solid_x = self.x - self.height*2
        solid_y = self.y - self.height*2
        solid_size = (4*self.height, 4*self.height)

        # Resize the outline of the cell.
        self.ell.circle = (self.x, self.y, radius, 0, 360, 6)

        # Resize the actual cell.f
        self.solid.pos = (solid_x, solid_y)
        self.solid.size = solid_size

        self.coord_label.center_x = self.x
        self.coord_label.center_y = self.y

    def on_touch_down(self, touch):
        if super(HexMapCell, self).on_touch_down(touch):
            return False

        coord_x, coord_y = self.map_coordinates()
        if not self.visible_on_map:
            return False

        with self.canvas.after:
            Color(*kivy.utils.get_color_from_hex('#000000'))
            radius = 2 * self.height
            self.ell = Line(circle=(self.x, self.y, radius, 0, 360, 6), width=2)

        if not self.collide_with_bounding_circle(touch.x, touch.y):
            return False

        Logger.debug('Selected: ({}, {})'.format(coord_x, coord_y))
        with self.canvas.after:
            if 'button' in touch.profile and touch.button == 'left':
                Color(*kivy.utils.get_color_from_hex('#00FF00'))

            if 'button' in touch.profile and touch.button == 'right':
                # TODO Will refactor to have separate on_touch_up for selected target hex instead.
                Color(*kivy.utils.get_color_from_hex('#FF0000'))
            radius = 2 * self.height
            self.ell = Line(circle=(self.x, self.y, radius, 0, 360, 6), width=2)

        self.parent.game.update_selected_cell(self.map_coordinates(), self.terrain_colour)
        return True

    def collide_with_bounding_circle(self, coord_x, coord_y):
        # Register if within bounds of circle that the hex is inscribed in.
        Logger.debug('Detected: ({}, {})'.format(coord_x, coord_y))
        radius = 2 * self.height
        dist = Vector(self.x, self.y).distance((coord_x, coord_y))
        Logger.debug('({}, {}) -> ({}, {})'.format(self.x, self.y, coord_x, coord_y))
        Logger.debug('Dist: {} Diff: {}'.format(dist, dist - radius))
        return dist - radius <= 0
