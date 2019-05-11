class Unit:
    def __init__(self, x, y, max_hitpoints, max_movement_points, sight_range):
        self.x = x
        self.y = y
        self.max_hitpoints = max_hitpoints
        self.hitpoints = max_hitpoints
        self.sight_range = sight_range
        self.max_movement_points = max_movement_points
        self.movement_points = max_movement_points

    def move(self, dir_x, dir_y, map):
        """

        :param dir_x:
        :param dir_y:
        :param map:
        :return:
        """

        if self.movement_points <= 0:
            print("No move movement points")
            return False

        new_x = self.x + dir_x
        new_y = self.y + dir_y

        if map.tiles[new_y][new_x].tile_type in ["mountain", "water"]:
            print("Cannot move unit, new location is mountain or water")
            return False

        print("Unit moved")
        self.x = new_x
        self.y = new_y
        self.movement_points -= 1
        return True
