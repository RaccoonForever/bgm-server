# pylint: disable=C0301
# Disabling "Line too long"

"""
Script with Tile class and its functions
"""

from constants import (
    MIN_WIDTH,
    MIN_HEIGHT,
    MAX_HEIGHT,
    MAX_WIDTH,
    TILE_TYPE_VOID,
    TRANSCO_TYPE,
    OVERLAPPING_THRESHOLD
)


class Tile:
    """
    Class to handle tile functions and model
    Example: a swamp / a crown / a castle etc...
    """

    def __init__(self, tiletype=TILE_TYPE_VOID, xmin=MIN_WIDTH, xmax=MAX_WIDTH, ymin=MIN_HEIGHT, ymax=MAX_HEIGHT,
                 probability=1.0):
        """
        Constructor
        :param tiletype:the type of the tile
        :param xmin:
        :param xmax:
        :param ymin:
        :param ymax:
        :param probability:
        """
        self.type = tiletype
        self.xmin = int(xmin)
        self.xmax = int(xmax)
        self.ymin = int(ymin)
        self.ymax = int(ymax)
        self.crowns = []
        self.probability = probability

    def get_width(self):
        """
        :return: the width of the tile
        """
        return self.xmax - self.xmin

    def get_height(self):
        """
        :return: the height of the tile
        """
        return self.ymax - self.ymin

    def is_overlapping(self, other_tile):
        """
        Function that gives the information if a tile is overlapping the current tile
        :param other_tile: the tile to compare
        :return: true if it is overlapping enough or false
        """
        diff_x = min(self.xmax, other_tile.xmax) - max(self.xmin, other_tile.xmin)
        diff_y = min(self.ymax, other_tile.ymax) - max(self.ymin, other_tile.ymin)
        area = (other_tile.ymax - other_tile.ymin) * (other_tile.xmax - other_tile.xmin)
        if diff_x >= 0 and diff_y >= 0 and area * OVERLAPPING_THRESHOLD <= diff_x * diff_y:
            return True

        return False

    def add_crown(self, crown):
        """
        Add a crown to the list of crowns associated to the tile
        :param crown: the crown tile to add
        """
        self.crowns.append(crown)

    def __repr__(self):
        return "Tile(tiletype=%s,xmin=%s,ymin=%s,xmax=%s,ymax=%s,crowns=%s)" % (TRANSCO_TYPE[self.type], self.xmin, self.ymin, self.xmax, self.ymax, self.crowns)
