class Submarine:
    def __init__(self, coords):
        self.coordinates = coords

    def get_ship_size(self):
        return len(self.coordinates)
