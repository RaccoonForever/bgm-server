"""
Script that will contain every constants for the server
"""

# Area constants
MIN_WIDTH = 0
MAX_WIDTH = 99999999
MIN_HEIGHT = 0
MAX_HEIGHT = 99999999

# Transform constants
TILE_ERROR_MARGIN = 0.2
MATRIX_ERROR_MARGIN = 0.05
MAX_TILE_NUMBER = 9
OVERLAPPING_THRESHOLD = 0.8

# Tile constants
TILE_TYPE_VOID = -1
TILE_TYPE_CROWN = 0
TILE_TYPE_CASTLE = 1
TILE_TYPE_LAKE = 2
TILE_TYPE_MINE = 3
TILE_TYPE_PASTURE = 4
TILE_TYPE_WHEAT = 5
TILE_TYPE_SWAMP = 6
TILE_TYPE_FOREST = 7

TRANSCO_TYPE = {
    -1: "Vide",
    0: "Crown",
    1: "Castle",
    2: "Lake",
    3: "Mine",
    4: "Pasture",
    5: "Wheat",
    6: "Swamp",
    7: "Forest"
}
