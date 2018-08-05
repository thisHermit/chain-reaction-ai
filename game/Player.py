"""The Player class stores all the functions and data related to the Player."""

from pygame import Rect


class Player:
    COLORS = [
        (255, 0, 0),      # Tomato
        (0, 0, 255),        # Blue
        (60, 179, 113),     # Green
        (238, 130, 238),    # Pink
        (255, 165, 0),      # Orange
        (106, 90, 205)      # Violet
    ]

    def __init__(self, id, color=None):
        self.id = id
        if not color:
            self.color = self.COLORS[id]
        else:
            self.color = color


class Marker(Rect):
    def __init__(self, color):
        self.color = color
