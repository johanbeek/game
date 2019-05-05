import numpy as np
from settler import Settler


class Player:
    def __init__(self, name, map_view_x, map_view_y, map):
        self.name = name
        self.map = map
        self.map_view_x = map_view_x
        self.map_view_y = map_view_y

        self.map_discovered = np.zeros((self.map.nr_tiles_y, self.map.nr_tiles_x))

        self.units = []
        self.towns = []

    def add_unit(self, unit_type, x, y):
        """

        :param unit_type: 'settler'
        :param x: start map location x
        :param y: start map location y
        :return:
        """
        if unit_type == 'settler':
            new_unit = Settler(x, y)
        else:
            raise ValueError(f"Unknown unit {unit_type}")

        self.units.append(new_unit)
        self.discover_area(x, y, new_unit.sight_range)

    def discover_area(self, center_x, center_y, distance):
        """
        Add area to be discovered
        :param x: center x
        :param y: center y
        :param distance: vision distance (in map cells) to be added
        :return:
        """
        
        left = center_x - distance
        top = center_y - distance
        
        if left < 0:
            left = 0
        if left > (self.map.nr_tiles_x - distance*2+1):
            left = self.map.nr_tiles_x - distance*2+1

        if top < 0:
            top = 0
        if top > (self.map.nr_tiles_y - distance*2+1):
            top = self.map.nr_tiles_y - distance*2+1

        for x in range(left, left+2*distance+1):
            for y in range(top, top+2*distance+1):
                self.map_discovered[y][x] = 1