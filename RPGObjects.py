class Object:
    def __init__(self, proection='@', coord=(0, 0), coliseum=False):
        self.matrix = []
        for i in proection.split('\n'):
            string = [j for j in i]
            self.matrix.append(string)
        self.coord = coord
        self.coliseum = coliseum

    def request_move(self, key):
        return None

    def set_coord(self, coord):
        self.coord = coord

    def set_proection(self, proection):
        self.matrix = []
        for i in proection.split('\n'):
            string = [j for j in i]
            self.matrix.append(string)

    def get_coliseum(self):
        coords = []
        for ind, line in enumerate(self.matrix):
            for ind2, column in enumerate(line):
                if column != " ":
                    coords.append((self.coord[0] + ind2, self.coord[1] + ind))

        return coords


class Player(Object):
    def request_move(self, key):
        coord = None

        if  key in ('w', 'H'):
            coord = (self.coord[0], self.coord[1] - 1)
        elif  key in ('s', 'P'):
            coord = (self.coord[0], self.coord[1] + 1)
        elif  key in ('a', 'K'):
            coord = (self.coord[0] - 1, self.coord[1])
        elif  key in ('d', 'M'):
            coord = (self.coord[0] + 1, self.coord[1])

        return coord


class Wall(Object):
    pass
