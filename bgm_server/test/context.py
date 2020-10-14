import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main.gamecommon.yolo_transform import compute_matrix_from_predictions, assign_crowns_to_tiles, zoning, score
from main.gamecommon.tile import Tile
from main.gamecommon.constants import (
    TILE_TYPE_FOREST,
    TILE_TYPE_SWAMP,
    TILE_TYPE_WHEAT,
    TILE_TYPE_MINE,
    TILE_TYPE_LAKE,
    TILE_TYPE_CASTLE,
    MAX_TILE_NUMBER,
    TILE_TYPE_PASTURE,
    TILE_TYPE_CROWN,
    TILE_TYPE_VOID)
