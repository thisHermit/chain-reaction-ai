"""The Board Class stores and performs all board functions."""

from pygame import Rect


class Board:

    def __init__(self, box_size=50, epoch=20, rows=10, columns=6, board_lines_color=(255, 0, 0)):
        self.epoch = epoch
        self.box_size = box_size
        self.rows = rows
        self.columns = columns
        self.board_lines_color = board_lines_color

        self.board = []
        for i in range(rows):
            row = []
            for j in range(columns):
                unstability = 3
                if i == 0 or i == 9 or j == 0 or j == 5:
                    unstability = 2
                if i % 9 == 0 and j % 5 == 0:
                    unstability = 1

                row.append(Box(j * box_size + epoch,
                               i * box_size + epoch,
                               box_size,
                               box_size,
                               (i, j),
                               unstability))
            self.board.append(row)


    def printBoard(self):
        for row in self.board:
            for i in row:
                print("Box:", i.coordinates, "Unstability:", i.unstability)
            print()

    def unstabilities(self):
        explosions = []
        for row in self.board:
            for elem in row:
                if elem.balls > elem.unstability:
                    explosions.append(elem)
        return explosions


class Box(Rect):
    # TODO: think whether unstability boolean or number_of_balls is better for updating the game
    def __init__(self, left, top, width, height, coordinates, unstability, balls=0, color=None):
        super().__init__(left, top, width, height)
        self.balls = balls
        self.coordinates = coordinates
        self.unstability = unstability
        self.color = color
