class Submarine:
    def __init__(self, coords):
        self.coordinates = coords

    def get_ship_size(self):
        """
        returns the size of the ship
        :return:
        """
        return len(self.coordinates)
