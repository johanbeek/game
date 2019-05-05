from unit import Unit


class Settler(Unit):
    def __init__(self, x, y):
        super().__init__(x, y, 100, 4, 3)

    def build_town(self):
        pass