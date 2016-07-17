import collections

from kivy import app, properties
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Line, Rectangle
import kivy.utils

MapCoords = collections.namedtuple('MapCoords', ['row', 'col'])


class StrategyGame(FloatLayout):
    main_map = properties.ObjectProperty(None)
    status = properties.ObjectProperty(None)
    map_rows = properties.NumericProperty(0)
    map_cols = properties.NumericProperty(0)

    def __init__(self, **kwargs):
        super(StrategyGame, self).__init__(**kwargs)

        number_of_regions = self.map_rows * self.map_cols
        for region in xrange(0, number_of_regions):
            row = region / self.map_cols
            col = region % self.map_cols

            # Add hex cells to make up the map.
            hex_cell = HexMapCell(row, col)
            self.main_map.add_widget(hex_cell)

            # Add overlay conditionally.
            if (row % 6 == 1 and col % 2 == 1) or (row % 6 == 4 and col % 2 == 0) and (col > 0):
                hex_cell.visible_on_map = True

                # Determine the location of the solid hexagon cell.  Needs to be offset from the centre of the hex.
                radius = 2 * hex_cell.height
                solid_x = hex_cell.x - hex_cell.height*2
                solid_y = hex_cell.y - hex_cell.height*2
                solid_size = (4*hex_cell.height, 4*hex_cell.height)

                with hex_cell.canvas.after:

                    # Create the outline of hexagon, based off the centre of the hex.
                    Color(*kivy.utils.get_color_from_hex('#A1A5AA'))
                    hex_cell.ell = Line(circle=(hex_cell.x, hex_cell.y, radius, 0, 360, 6), width=2)

                    # Create the solid background of the hexagon, from the bottom left coordinate of the hex.
                    hex_cell.terrain_colour = kivy.utils.get_random_color(alpha=.5)
                    Color(*hex_cell.terrain_colour)
                    hex_cell.solid = Ellipse(pos=(solid_x, solid_y), size=solid_size, segments=6)

                    Color(1, 1, 1, 1)
                    hex_cell.coord_label = Label(
                        text=hex_cell.map_display_text(),
                        center_x=hex_cell.x,
                        center_y=hex_cell.y)

                # Bind the cell code so as to update its position and size when the parent widget resizes.
                hex_cell.bind(pos=hex_cell.update_pos, size=hex_cell.update_pos)

    def update_selected_cell(self, coords, terrain_colour, *args):
        self.status.text = 'Coords: ({}, {})'.format(coords[0], coords[1])
        with self.status.canvas.before:
            Color(*terrain_colour)
            Rectangle(pos=self.status.pos, size=self.status.size)
        return True


class HexMapCell(Label):
    def __init__(self, row=0, col=0, **kwargs):
        super(HexMapCell, self).__init__(**kwargs)
        self.coords = MapCoords(row, col)
        self.selected = False
        self.visible_on_map = False
        self.terrain_colour = Color(0, 0, 0, 1)

    def map_coordinates(self):
        return self.coords.row / 3, self.coords.col / 2

    def map_display_text(self):
        map_x, map_y = self.map_coordinates()
        return "({}, {})".format(map_x, map_y)

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

        if not self.visible_on_map:
            return False

        if not self.collide_point(touch.x, touch.y):
            with self.canvas.after:
                Color(*kivy.utils.get_color_from_hex('#A1A5AA'))
                radius = 2 * self.height
                self.ell = Line(circle=(self.x, self.y, radius, 0, 360, 6), width=2)
            return False

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


class StrategyGameApp(app.App):
    def build(self):
        return StrategyGame()

if __name__ == '__main__':
    StrategyGameApp().run()
