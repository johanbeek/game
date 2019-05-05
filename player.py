from settler import Settler


class Player:
    def __init__(self, name, map_view_x, map_view_y):
        self.name = name
        self.map_view_x = map_view_x
        self.map_view_y = map_view_y

        self.units = []
        self.towns = []

    def add_unit(self, unit_type, x, y):
        if unit_type == 'settler':
            settler = Settler(x, y)
            self.units.append(settler)