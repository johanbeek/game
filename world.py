from map import Map
from player import Player
import resources
import numpy as np
from settler import Settler

class World:

    def __init__(self, nr_tiles_x, nr_tiles_y):
        self.map = Map(nr_tiles_x, nr_tiles_y)
        self.players = {}
        self.active_player = None


    def draw(self, player_name, game_display, screen_width, screen_height, tile_size):
        """

        :param game_display:
        :param screen_width:
        :param screen_height:
        :param tile_size:
        :return:
        """
        map_view_x = self.players[player_name].map_view_x
        map_view_y = self.players[player_name].map_view_y

        nr_tiles_screen_x = int(screen_width / tile_size)
        nr_tiles_screen_y = int(screen_height / tile_size)

        left_x = map_view_x - int(nr_tiles_screen_x / 2)
        top_y = map_view_y - int(nr_tiles_screen_y / 2)

        """
        Correct start position if too far to the edge
        """
        if left_x < 0:
            left_x = 0
        if left_x > self.map.nr_tiles_x - nr_tiles_screen_x:
            left_x = self.map.nr_tiles_x - nr_tiles_screen_x

        if top_y < 0:
            top_y = 0
        if top_y > self.map.nr_tiles_y - nr_tiles_screen_y:
            top_y = self.map.nr_tiles_y - nr_tiles_screen_y

        # right_x = left_x + nr_tiles_screen_x
        # bottom_y = top_y + nr_tiles_screen_y

        """
        Draw world tiles discovered by player
        """
        player = self.players[player_name]

        for screen_x in range(nr_tiles_screen_x):
            for screen_y in range(nr_tiles_screen_y):
                screen_pixel_x = screen_x * tile_size
                screen_pixel_y = screen_y * tile_size

                world_x = left_x + screen_x
                world_y = top_y + screen_y

                if player.map_discovered[world_y][world_x]:
                    tile_type = self.map.tiles[world_y][world_x].tile_type
                else:
                    tile_type = 'undiscovered'

                img = resources.tile_dict[tile_type]["img"]
                game_display.blit(img, (screen_pixel_x, screen_pixel_y))

        """
        Draw towns
        """


        """
        Draw units
        """
        for key in self.players:
            for unit in self.players[key].units:
                if player.map_discovered[unit.y][unit.x]:

                    # get location on screen and check if it should be visible
                    unit_screen_x = unit.x - left_x
                    unit_screen_y = unit.y - top_y

                    if 0 < unit_screen_x < nr_tiles_screen_x and \
                        0 < unit_screen_y < nr_tiles_screen_y:

                        screen_pixel_x = unit_screen_x * tile_size + 8
                        screen_pixel_y = unit_screen_y * tile_size + 8

                        if isinstance(unit, Settler):
                            img = resources.unit_dict['settler']["img"]
                        else:
                            raise ValueError(f"Unknown unit class: {unit}")

                        game_display.blit(img, (screen_pixel_x, screen_pixel_y))

    def add_player(self, player_name):
        """
        Adds a new player to the game. The player starts with one unit, a settler
        :return:
        """

        """
        Find good start location
        """
        for n in range(1000):
            start_x = np.random.randint(10, self.map.nr_tiles_x-10)
            start_y = np.random.randint(10, self.map.nr_tiles_y-10)

            if self.map.tiles[start_y][start_x].tile_type == 'grass':
                break
        else:
            raise ValueError("NO VALID START POSITION FOUND")

        """
        Add player and unit to the world
        """
        player = Player(player_name, start_x, start_y, self.map)
        self.active_player = player

        unit = player.add_unit('settler', start_x, start_y)
        player.active_unit = unit     # immediately select the unit

        self.players[player_name] = player

