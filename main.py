from kivy import app, properties
from kivy.uix import label, floatlayout


class StrategyGame(floatlayout.FloatLayout):
    main_map = properties.ObjectProperty(None)
    map_rows = properties.NumericProperty(0)
    map_cols = properties.NumericProperty(0)

    def __init__(self, **kwargs):
        super(StrategyGame, self).__init__(**kwargs)

        number_of_regions = self.map_rows * self.map_cols
        for region in xrange(0, number_of_regions):
            row = region / self.map_cols
            col = region % self.map_cols

            # Add hex cells to make up the map.
            cell = MapHexCell()
            location_text = '({}, {})'.format(row, col)
            cell.text = location_text
            self.main_map.add_widget(cell)


class MapHexCell(label.Label):
    pass


class StrategyGameApp(app.App):
    def build(self):
        return StrategyGame()

if __name__ == '__main__':
    StrategyGameApp().run()