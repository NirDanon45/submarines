import exceptions


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
