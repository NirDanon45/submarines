import exceptions


class Board:
    def __init__(self, row_count, col_count, submarines=[]):
        self.row_count = row_count
        self.col_count = col_count
        self.submarines = submarines

    def is_ship_there(self, row_index, col_index):
        return True if [row_index, col_index] in self.submarines else False

    def add_ship(self, submarine):
        for ship_coord in submarine.coordinate:
            if self.is_ship_there(ship_coord):
                raise exceptions.OverlapingShipsExeption
        self.submarines.append(submarine)

    def sink_ship(self, submarine):
        if submarine not in self.submarines:
            raise exceptions.NoneExistentSubmarine
