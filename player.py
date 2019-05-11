import numpy as np
import pandas as pd

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

        self.active_unit = None

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
        self.map_discovered = self.discover_area(x, y, new_unit.sight_range)
        return new_unit

    def move_unit(self, dir_x, dir_y):

        if not self.active_unit:
            print(f"WARNING: NO UNIT ACTIVE FOR PLAYER {self.name}, NO UNIT MOVED")
            return

        moved = self.active_unit.move(dir_x, dir_y, self.map)

        if moved:
            new_disc = self.discover_area(self.active_unit.x, self.active_unit.y,
                                          self.active_unit.sight_range)
            self.map_discovered += new_disc
            self.map_discovered = np.where(self.map_discovered > 1, 1, self.map_discovered)

            self.map_view_x = self.active_unit.x
            self.map_view_y = self.active_unit.y

    def discover_area(self, center_x, center_y, distance):
        """
        Add area to be discovered
        :param center_x: center x
        :param center_y: center y
        :param distance: vision distance (in map cells) to be added
        :return:
        """

        # create a map matrix: 1 for obstructed area, 0 for unobstructed
        map_matrix = np.zeros((self.map.nr_tiles_y, self.map.nr_tiles_x))

        for x in range(self.map.nr_tiles_x):
            for y in range(self.map.nr_tiles_y):
                if self.map.tiles[y][x].tile_type in ["forest", "mountain"]:
                    map_matrix[y][x] = 1

        view_matrix = np.zeros((self.map.nr_tiles_y, self.map.nr_tiles_x))

        x_list = []
        y_list = []
        dist_list = []
        view_angle_list = []
        min_block_angle_list = []
        max_block_angle_list = []

        for x in range(self.map.nr_tiles_x):
            for y in range(self.map.nr_tiles_y):

                if x == center_x and y == center_y:
                    continue

                dist_x = center_x - x
                dist_y = center_y - y
                dist = np.sqrt(np.power(dist_x, 2) + np.power(dist_y, 2))

                if dist <= distance:
                    x_list.append(x)
                    y_list.append(y)
                    dist_list.append(dist)

                    view_angle = np.arctan2(dist_y, dist_x)
                    view_angle_list.append(view_angle)

                    if map_matrix[y][x] == 1:
                        block_angle1 = np.arctan2(dist_y + 0.5, dist_x + 0.5)
                        block_angle2 = np.arctan2(dist_y + 0.5, dist_x - 0.5)
                        block_angle3 = np.arctan2(dist_y - 0.5, dist_x + 0.5)
                        block_angle4 = np.arctan2(dist_y - 0.5, dist_x - 0.5)
                        min_block_angle = np.min(
                            [block_angle1, block_angle2, block_angle3, block_angle4])
                        max_block_angle = np.max(
                            [block_angle1, block_angle2, block_angle3, block_angle4])
                        min_block_angle_list.append(min_block_angle)
                        max_block_angle_list.append(max_block_angle)
                    else:
                        min_block_angle_list.append(0)
                        max_block_angle_list.append(0)

        df = pd.DataFrame(
            {"x": x_list, "y": y_list, "dist": dist_list, "view_angle": view_angle_list,
             "min_block_angle": min_block_angle_list, "max_block_angle":
                 max_block_angle_list})

        for index, row in df.iterrows():

            df_in_range = df[df["dist"] < row.dist]

            x = int(row.x)
            y = int(row.y)

            min_block_angles = df_in_range["min_block_angle"].values
            max_block_angles = df_in_range["max_block_angle"].values
            view_angle = row.view_angle

            view_matrix[y][x] = 1

            for min_angle, max_angle in zip(min_block_angles, max_block_angles):

                if min_angle < 0 < max_angle:
                    if max_angle > 0.5 * np.pi:
                        if view_angle > max_angle:
                            view_matrix[y][x] = 0
                            break
                        elif view_angle < min_angle:
                            view_matrix[y][x] = 0
                            break
                    if max_angle < 0.5 * np.pi:
                        if 0 <= view_angle < max_angle:
                            view_matrix[y][x] = 0
                            break
                        if 0 > view_angle > min_angle:
                            view_matrix[y][x] = 0
                            break
                elif min_angle < view_angle < max_angle:
                    view_matrix[y][x] = 0
                    break

        view_matrix[center_y][center_x] = 1

        return view_matrix

        # """
        # OLD CODE SIMPLE VERSION
        # """
        # left = center_x - distance
        # top = center_y - distance
        #
        #
        # if left < 0:
        #     left = 0
        # if left > (self.map.nr_tiles_x - distance*2+1):
        #     left = self.map.nr_tiles_x - distance*2+1
        #
        # if top < 0:
        #     top = 0
        # if top > (self.map.nr_tiles_y - distance*2+1):
        #     top = self.map.nr_tiles_y - distance*2+1
        #
        # for x in range(left, left+2*distance+1):
        #     for y in range(top, top+2*distance+1):
        #         self.map_discovered[y][x] = 1