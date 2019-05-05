from map import Map
import resources


class World:

    def __init__(self, nr_tiles_x, nr_tiles_y):
        self.map = Map(nr_tiles_x, nr_tiles_y)

    def draw(self, game_display, screen_width, screen_height, tile_size):
        """

        :param game_display:
        :param screen_width:
        :param screen_height:
        :param tile_size:
        :return:
        """

        nr_tiles_screen_x = int(screen_width / tile_size)
        nr_tiles_screen_y = int(screen_height / tile_size)

        for x in range(nr_tiles_screen_x):
            for y in range(nr_tiles_screen_y):
                screen_loc_x = x * tile_size
                screen_loc_y = y * tile_size

                tile_type = self.map.tiles[y][x].tile_type
                img = resources.tile_dict[tile_type]["img"]
                game_display.blit(img, (screen_loc_x, screen_loc_y))
