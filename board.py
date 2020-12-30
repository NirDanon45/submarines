import exceptions
NUMBER_OF_ROWS = 10
NUMBER_OF_COLUMNS = 10

class Board:
    def __init__(self, row_count, col_count, submarines=[]):
        self.row_count = row_count
        self.col_count = col_count
        self.submarines = submarines

    def is_submarine_there(self, row_index, col_index):
        """
        checks if there's a submarine in the given coords.
        """
        return True if [row_index, col_index] in self.submarines else False

    def add_submarine(self, submarine):
        """
        adds a submarine to the board
        :param submarine: the sub
        """
        for submarine_coord in submarine.coordinate:
            if self.is_submarine_there(submarine_coord):
                raise exceptions.OverlapingShipsExeption
        self.submarines.append(submarine)

    def sink_submarine(self, coords):
        """
        sinks a submarine and returns the sinking sub. doesn't check if it's there.
        :param coords: the coords to sink the sub.
        :return:
        """
        for submarine in self.submarines:
            for submarine_coord in submarine.coordinates:
                if submarine_coord == coords:
                    submarine_to_sink = submarine

        if submarine_to_sink not in self.submarines:
            raise exceptions.NoneExistentSubmarine

        self.submarines.remove(submarine_to_sink)
        return submarine_to_sink

    def get_all_ships_coords(self):
        coords = []
        for sub in self.submarines:
            coords.append(sub.coords)
        return coords

    def get_ascii_art(self):
        """"
        returns ascii representation of the board
        """
        board = []
        all_subs_coords = self.get_all_ships_coords()
        for i in range(0, NUMBER_OF_ROWS):
            row = []
            for j in range(0, NUMBER_OF_COLUMNS):
                if [i, j] in all_subs_coords:
                    row.append("S")
                else:
                    row.append("~")
            board.append(row)
        return board

