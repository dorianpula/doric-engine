import collections
from math import ceil

import kivy.utils
from kivy.logger import Logger
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Line
from kivy.vector import Vector

MapCoords = collections.namedtuple('MapCoords', ['row', 'col'])


class HexMapCell(Label):
    def __init__(self, row=0, col=0, **kwargs):
        super(HexMapCell, self).__init__(**kwargs)
        self.coords = MapCoords(row, col)
        ## set the cube coordinates of the hexagon
        ## as [x, y, z]
        self.cube_coords = self.even_r_to_cube(self.coords.row / 3, self.coords.col / 2)
        self.selected = False
        self.visible_on_map = False
        self.terrain_colour = Color(0, 0, 0, 1)
        self.terrain = ''

    def even_r_to_cube(self, row, col):
        '''compute cube coordinates from even-r hex coordinates'''
        x = int(col - ceil(float(row)/2))
        z = row
        y = - x - z
        return([x, y, z])

    def cube_to_even_r(self, x, y, z):
        row = int(x + ceil(z / 2))
        col = z
        return ([row, col])

    @property
    def even_r_coords(self):
        '''return even-r coordinates of the hexagon.'''
        return(self.cube_to_even_r(*self.cube_coords))

    @even_r_coords.setter
    def even_r_coords(self, value):
        self.cube_coords = self.even_r_to_cube(*value)

    def coordinate_text(self):
        return '({}, {})'.format(self.coords.row, self.coords.col)

    def even_r_coordinate_text(self):
        return '{}'.format(self.even_r_coords)

    def cube_coordinate_text(self):
        return '{}\n{}\n{}'.format(*self.cube_coords)

    def map_display_text(self):
        return "{}\n{} \n {}".format(self.even_r_coordinate_text(), self.cube_coordinate_text(), self.terrain)

    def update_pos(self, instance, value):
        # Determine the location of the solid hexagon cell.  Needs to be offset from the centre of the hex.
        radius = 2 * self.height
        solid_x = self.x - self.height*2
        solid_y = self.y - self.height*2
        solid_size = (4*self.height, 4*self.height)

        # Resize the outline of the cell.
        self.ell.circle = (self.x, self.y, radius, 0, 360, 6)

        # Resize the actual cell.
        self.solid.pos = (solid_x, solid_y)
        self.solid.size = solid_size

        self.coord_label.center_x = self.x
        self.coord_label.center_y = self.y

    def on_touch_down(self, touch):
        if super(HexMapCell, self).on_touch_down(touch):
            return False

        coord_x, coord_y = self.even_r_coords
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

        self.parent.game.update_selected_cell(self.even_r_coords, self.terrain_colour)
        return True

    def collide_with_bounding_circle(self, coord_x, coord_y):
        # Register if within bounds of circle that the hex is inscribed in.
        Logger.debug('Detected: ({}, {})'.format(coord_x, coord_y))
        radius = 2 * self.height
        dist = Vector(self.x, self.y).distance((coord_x, coord_y))
        Logger.debug('({}, {}) -> ({}, {})'.format(self.x, self.y, coord_x, coord_y))
        Logger.debug('Dist: {} Diff: {}'.format(dist, dist - radius))
        return dist - radius <= 0
