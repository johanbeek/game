import tile
import numpy as np
import resources
import matplotlib.pyplot as plt

from skimage.morphology import disk
from skimage.filters import rank


class Map:

    def __init__(self, nr_tiles_x, nr_tiles_y):#, tile_size)#, screen_width, screen_height):

        self.nr_tiles_x = nr_tiles_x
        self.nr_tiles_y = nr_tiles_y

        # self.screen_width = screen_width
        # self.screen_height = screen_height
        # self.tile_size = tile_size

        self.tiles = [[0 for x in range(nr_tiles_x)] for y in range(nr_tiles_y)]

        map_matrix = self.generate_map_matrix()

        for x in range(nr_tiles_x):
            for y in range(nr_tiles_y):
                tile_type = resources.tile_converter[map_matrix[y, x]]
                self.tiles[y][x] = tile.Tile(tile_type, x, y)

    def generate_map_matrix(self):
        """
        Generates a map based on the map settings
        :return: a numpy matrix with an integer for each class:
        1: sea
        2: grass
        3: forest
        4: mountain
        """

        map_matrix = np.random.rand(self.nr_tiles_y, self.nr_tiles_x) * 100
        map_matrix = map_matrix.astype("uint8")

        """
        Determine the distance to the edge to increase likelihood sea
        """
        max_dist = min([self.nr_tiles_x, self.nr_tiles_y]) / 4

        edge_map = np.zeros((self.nr_tiles_y, self.nr_tiles_x))
        for x in range(map_matrix.shape[1]):
            for y in range(map_matrix.shape[0]):
                dist_x = min([self.nr_tiles_x - (x + 1), x])
                dist_y = min([self.nr_tiles_y - (y + 1), y])
                edge_map[y, x] = min([dist_x, dist_y])

        edge_map = np.where(edge_map < max_dist, edge_map, max_dist)

        """
        Add the edge map to the map matrix and smooth
        """
        prob_map = (edge_map + map_matrix).astype("uint8")

        selem = disk(3)
        map_smooth = rank.mean(prob_map, selem=selem)

        """
        Divide into classes
        """
        mean_map = np.mean(map_smooth)
        sd_map = np.std(map_smooth)

        water_thr = mean_map - sd_map
        grass_thr = mean_map + 0.5 * sd_map
        forest_thr = mean_map + 0.8 * sd_map

        map_smooth[map_smooth <= water_thr] = 1
        map_smooth[(map_smooth > water_thr) & (map_smooth <= grass_thr)] = 2
        map_smooth[(map_smooth > grass_thr) & (map_smooth <= forest_thr)] = 3
        map_smooth[map_smooth > forest_thr] = 4

        """
        Set edge to water
        """
        map_smooth[edge_map == 0] = 1

        """
        Post smoothing
        """
        selem = disk(2)
        map_smooth = rank.mean(map_smooth, selem=selem)


        # plt.imshow(map_smooth)
        # plt.savefig(r"d:/temp/map.png")
        # plt.close()

        return map_smooth
