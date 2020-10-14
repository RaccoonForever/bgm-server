# pylint: disable=line-too-long, too-many-locals, no-self-use
"""
Script to test from the result of a model to the result on the gameboard
"""

import unittest

from .context import Tile
from .context import (TILE_TYPE_FOREST,
                      TILE_TYPE_SWAMP,
                      TILE_TYPE_WHEAT,
                      TILE_TYPE_MINE,
                      TILE_TYPE_LAKE,
                      TILE_TYPE_CASTLE,
                      MAX_TILE_NUMBER,
                      TILE_TYPE_PASTURE,
                      TILE_TYPE_CROWN,
                      TILE_TYPE_VOID)
from .context import compute_matrix_from_predictions, assign_crowns_to_tiles, score, zoning


class TransformYoloTest(unittest.TestCase):
    """ 
    Class to test all transformations to go through a gameboard prediction to a result
    """

    def init_tiles1(self):
        """
        Tiles without crown 1
        """
        tile1 = Tile(tiletype=TILE_TYPE_FOREST, xmin=843, ymin=690, xmax=1484, ymax=1347)
        tile2 = Tile(tiletype=TILE_TYPE_FOREST, xmin=1511, ymin=682, xmax=2165, ymax=1346)
        tile3 = Tile(tiletype=TILE_TYPE_FOREST, xmin=1543, ymin=2671, xmax=2202, ymax=3345)
        tile4 = Tile(tiletype=TILE_TYPE_FOREST, xmin=870, ymin=2022, xmax=1519, ymax=2664)
        tile5 = Tile(tiletype=TILE_TYPE_FOREST, xmin=874, ymin=2681, xmax=1525, ymax=3320)
        tile6 = Tile(tiletype=TILE_TYPE_SWAMP, xmin=849, ymin=1373, xmax=1502, ymax=1983)
        tile7 = Tile(tiletype=TILE_TYPE_WHEAT, xmin=221, ymin=2036, xmax=876, ymax=2675)
        tile8 = Tile(tiletype=TILE_TYPE_WHEAT, xmin=1547, ymin=2018, xmax=2208, ymax=2668)
        tile9 = Tile(tiletype=TILE_TYPE_WHEAT, xmin=2210, ymin=2030, xmax=2867, ymax=2667)
        tile10 = Tile(tiletype=TILE_TYPE_WHEAT, xmin=250, ymin=2681, xmax=845, ymax=3350)
        tile11 = Tile(tiletype=TILE_TYPE_WHEAT, xmin=2223, ymin=2684, xmax=2884, ymax=3353)
        tile12 = Tile(tiletype=TILE_TYPE_MINE, xmin=1512, ymin=1357, xmax=2176, ymax=1988)
        tile13 = Tile(tiletype=TILE_TYPE_MINE, xmin=2189, ymin=693, xmax=2831, ymax=1345)
        tile14 = Tile(tiletype=TILE_TYPE_MINE, xmin=2189, ymin=1384, xmax=2859, ymax=1996)
        tile15 = Tile(tiletype=TILE_TYPE_LAKE, xmin=187, ymin=1375, xmax=839, ymax=2024)
        tile16 = Tile(tiletype=TILE_TYPE_CASTLE, xmin=213, ymin=698, xmax=818, ymax=1363)
        tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7, tile8, tile9, tile10, tile11, tile12, tile13, tile14,
                 tile15, tile16]
        return tiles

    def init_tiles2(self):
        """
        Tiles without crown 2
        """
        tiles = [[Tile(tiletype=TILE_TYPE_LAKE), Tile(tiletype=TILE_TYPE_LAKE), Tile(tiletype=TILE_TYPE_MINE),
                  Tile(tiletype=TILE_TYPE_PASTURE), Tile(tiletype=TILE_TYPE_PASTURE)],
                 [Tile(tiletype=TILE_TYPE_LAKE), Tile(tiletype=TILE_TYPE_WHEAT), Tile(tiletype=TILE_TYPE_WHEAT),
                  Tile(tiletype=TILE_TYPE_MINE), Tile(tiletype=TILE_TYPE_MINE)],
                 [Tile(tiletype=TILE_TYPE_LAKE), Tile(tiletype=TILE_TYPE_SWAMP), Tile(tiletype=TILE_TYPE_WHEAT),
                  Tile(tiletype=TILE_TYPE_WHEAT), Tile(tiletype=TILE_TYPE_MINE)],
                 [Tile(tiletype=TILE_TYPE_SWAMP), Tile(tiletype=TILE_TYPE_SWAMP), Tile(tiletype=TILE_TYPE_SWAMP),
                  Tile(tiletype=TILE_TYPE_PASTURE), Tile(tiletype=TILE_TYPE_MINE)],
                 [Tile(tiletype=TILE_TYPE_FOREST), Tile(tiletype=TILE_TYPE_WHEAT), Tile(tiletype=TILE_TYPE_WHEAT),
                  Tile(tiletype=TILE_TYPE_WHEAT), Tile(tiletype=TILE_TYPE_LAKE)]
                 ]

        return tiles

    def init_tiles3(self):
        """
        Tiles without crown 3
        """
        tiles = [[Tile(tiletype=TILE_TYPE_LAKE), Tile(tiletype=TILE_TYPE_LAKE), None,
                  Tile(tiletype=TILE_TYPE_PASTURE), Tile(tiletype=TILE_TYPE_PASTURE)],
                 [Tile(tiletype=TILE_TYPE_LAKE), Tile(tiletype=TILE_TYPE_WHEAT), Tile(tiletype=TILE_TYPE_WHEAT),
                  Tile(tiletype=TILE_TYPE_MINE), Tile(tiletype=TILE_TYPE_MINE)],
                 [Tile(tiletype=TILE_TYPE_LAKE), Tile(tiletype=TILE_TYPE_SWAMP), Tile(tiletype=TILE_TYPE_WHEAT),
                  Tile(tiletype=TILE_TYPE_WHEAT), Tile(tiletype=TILE_TYPE_MINE)],
                 [Tile(tiletype=TILE_TYPE_SWAMP), Tile(tiletype=TILE_TYPE_SWAMP), Tile(tiletype=TILE_TYPE_SWAMP),
                  None, Tile(tiletype=TILE_TYPE_MINE)],
                 [None, Tile(tiletype=TILE_TYPE_WHEAT), Tile(tiletype=TILE_TYPE_WHEAT),
                  Tile(tiletype=TILE_TYPE_WHEAT), Tile(tiletype=TILE_TYPE_LAKE)]
                 ]

        return tiles

    def init_tiles4(self):
        """
        Tiles without crown 4
        """
        tiles = [[Tile(tiletype=TILE_TYPE_LAKE), Tile(tiletype=TILE_TYPE_LAKE), None,
                  Tile(tiletype=TILE_TYPE_PASTURE), Tile(tiletype=TILE_TYPE_PASTURE), None, None, None, None],
                 [Tile(tiletype=TILE_TYPE_LAKE), Tile(tiletype=TILE_TYPE_WHEAT), Tile(tiletype=TILE_TYPE_WHEAT),
                  Tile(tiletype=TILE_TYPE_MINE), Tile(tiletype=TILE_TYPE_MINE), None, None, None, None],
                 [Tile(tiletype=TILE_TYPE_LAKE), Tile(tiletype=TILE_TYPE_SWAMP), Tile(tiletype=TILE_TYPE_WHEAT),
                  Tile(tiletype=TILE_TYPE_WHEAT), Tile(tiletype=TILE_TYPE_MINE), None, None, None, None],
                 [Tile(tiletype=TILE_TYPE_SWAMP), Tile(tiletype=TILE_TYPE_SWAMP), Tile(tiletype=TILE_TYPE_SWAMP),
                  None, Tile(tiletype=TILE_TYPE_MINE), None, None, None, None],
                 [None, Tile(tiletype=TILE_TYPE_WHEAT), Tile(tiletype=TILE_TYPE_WHEAT),
                  Tile(tiletype=TILE_TYPE_WHEAT), Tile(tiletype=TILE_TYPE_LAKE), None, None, None, None]
                 ]

        return tiles

    def init_tileswithcrown(self):
        """
        Tiles with crown
        """
        tiles = self.init_tiles1()
        tiles.append(Tile(tiletype=TILE_TYPE_CROWN, xmin=1296, ymin=3185, xmax=1520, ymax=3291))
        tiles.append(Tile(tiletype=TILE_TYPE_CROWN, xmin=2625, ymin=3133, xmax=2848, ymax=3312))
        tiles.append(Tile(tiletype=TILE_TYPE_CROWN, xmin=884, ymin=2058, xmax=1094, ymax=2232))
        tiles.append(Tile(tiletype=TILE_TYPE_CROWN, xmin=626, ymin=1388, xmax=790, ymax=1598))
        tiles.append(Tile(tiletype=TILE_TYPE_CROWN, xmin=2234, ymin=1380, xmax=2402, ymax=1582))
        tiles.append(Tile(tiletype=TILE_TYPE_CROWN, xmin=2244, ymin=1762, xmax=2416, ymax=1986))
        tiles.append(Tile(tiletype=TILE_TYPE_CROWN, xmin=1921, ymin=1366, xmax=2134, ymax=1538))
        tiles.append(Tile(tiletype=TILE_TYPE_CROWN, xmin=2644, ymin=1105, xmax=2818, ymax=1315))
        tiles.append(Tile(tiletype=TILE_TYPE_CROWN, xmin=1725, ymin=1368, xmax=1936, ymax=1536))
        tiles.append(Tile(tiletype=TILE_TYPE_CROWN, xmin=2233, ymin=1577, xmax=2408, ymax=1773))
        tiles.append(Tile(tiletype=TILE_TYPE_CROWN, xmin=2648, ymin=901, xmax=2817, ymax=1121))
        return tiles

    def test_computematrix1(self):
        """
        Verify that the matrix returned is as expected
        """
        tiles = self.init_tiles1()
        matrix = compute_matrix_from_predictions(tiles)
        self.assertTrue(len(matrix[0]) == MAX_TILE_NUMBER)
        self.assertTrue(len(matrix) == MAX_TILE_NUMBER)
        self.assertEqual(matrix[0][0].type, TILE_TYPE_CASTLE)
        self.assertEqual(matrix[0][1].type, TILE_TYPE_FOREST)
        self.assertEqual(matrix[0][2].type, TILE_TYPE_FOREST)
        self.assertEqual(matrix[0][3].type, TILE_TYPE_MINE)
        self.assertEqual(matrix[1][0].type, TILE_TYPE_LAKE)
        self.assertEqual(matrix[1][1].type, TILE_TYPE_SWAMP)
        self.assertEqual(matrix[1][2].type, TILE_TYPE_MINE)
        self.assertEqual(matrix[1][3].type, TILE_TYPE_MINE)
        self.assertEqual(matrix[2][0].type, TILE_TYPE_WHEAT)
        self.assertEqual(matrix[2][1].type, TILE_TYPE_FOREST)
        self.assertEqual(matrix[2][2].type, TILE_TYPE_WHEAT)
        self.assertEqual(matrix[2][3].type, TILE_TYPE_WHEAT)
        self.assertEqual(matrix[3][0].type, TILE_TYPE_WHEAT)
        self.assertEqual(matrix[3][1].type, TILE_TYPE_FOREST)
        self.assertEqual(matrix[3][2].type, TILE_TYPE_FOREST)
        self.assertEqual(matrix[3][3].type, TILE_TYPE_WHEAT)

    def test_computematrix_no_tiles(self):
        """
        A test with no tiles as a param
        """
        tiles = []
        matrix = compute_matrix_from_predictions(tiles)
        self.assertTrue(len(matrix[0]) == MAX_TILE_NUMBER)
        self.assertTrue(len(matrix) == MAX_TILE_NUMBER)
        self.assertEqual(matrix[0][0], None)

    def test_assigncrowns(self):
        """
        Test that crowns are well assigned to tile corresponding
        """
        tiles = self.init_tileswithcrown()
        result_tiles = assign_crowns_to_tiles(tiles)
        self.assertEqual(len(result_tiles), 16)
        self.assertEqual(len(tiles[0].crowns), 0)
        self.assertEqual(len(tiles[1].crowns), 0)
        self.assertEqual(len(tiles[2].crowns), 0)
        self.assertEqual(len(tiles[3].crowns), 1)
        self.assertEqual(len(tiles[4].crowns), 1)
        self.assertEqual(len(tiles[5].crowns), 0)
        self.assertEqual(len(tiles[6].crowns), 0)
        self.assertEqual(len(tiles[7].crowns), 0)
        self.assertEqual(len(tiles[8].crowns), 0)
        self.assertEqual(len(tiles[9].crowns), 0)
        self.assertEqual(len(tiles[10].crowns), 1)
        self.assertEqual(len(tiles[11].crowns), 2)
        self.assertEqual(len(tiles[12].crowns), 2)
        self.assertEqual(len(tiles[13].crowns), 3)
        self.assertEqual(len(tiles[14].crowns), 1)
        self.assertEqual(len(tiles[15].crowns), 0)

    def test_zoning1(self):
        """
        Test that the zoning is working for tiles 2
        """
        type_matrix = self.init_tiles2()

        matrix_zone, nb_zone = zoning(type_matrix)

        self.assertEqual(matrix_zone[0][0], 1)
        self.assertEqual(matrix_zone[0][1], 1)
        self.assertEqual(matrix_zone[1][0], 1)
        self.assertEqual(matrix_zone[2][0], 1)

        self.assertEqual(matrix_zone[0][2], 2)
        self.assertEqual(matrix_zone[0][3], 3)
        self.assertEqual(matrix_zone[0][4], 3)

        self.assertEqual(matrix_zone[1][1], 4)
        self.assertEqual(matrix_zone[1][2], 4)
        self.assertEqual(matrix_zone[2][2], 4)
        self.assertEqual(matrix_zone[2][3], 4)

        self.assertEqual(matrix_zone[1][3], 5)
        self.assertEqual(matrix_zone[1][4], 5)
        self.assertEqual(matrix_zone[2][4], 5)
        self.assertEqual(matrix_zone[3][4], 5)

        self.assertEqual(matrix_zone[2][1], 6)
        self.assertEqual(matrix_zone[3][1], 6)
        self.assertEqual(matrix_zone[3][0], 6)
        self.assertEqual(matrix_zone[3][2], 6)

        self.assertEqual(matrix_zone[3][3], 7)

        self.assertEqual(matrix_zone[4][0], 8)

        self.assertEqual(matrix_zone[4][1], 9)
        self.assertEqual(matrix_zone[4][2], 9)
        self.assertEqual(matrix_zone[4][3], 9)

        self.assertEqual(matrix_zone[4][4], 10)

        self.assertEqual(nb_zone, 10)

    def test_zoning2(self):
        """
        Test that the zoning is working for tiles 3
        """
        type_matrix = self.init_tiles3()

        matrix_zone, nb_zone = zoning(type_matrix)

        self.assertEqual(matrix_zone[0][0], 1)
        self.assertEqual(matrix_zone[0][1], 1)
        self.assertEqual(matrix_zone[1][0], 1)
        self.assertEqual(matrix_zone[2][0], 1)

        self.assertEqual(matrix_zone[0][2], -1)

        self.assertEqual(matrix_zone[0][3], 2)
        self.assertEqual(matrix_zone[0][4], 2)

        self.assertEqual(matrix_zone[1][1], 3)
        self.assertEqual(matrix_zone[1][2], 3)
        self.assertEqual(matrix_zone[2][2], 3)
        self.assertEqual(matrix_zone[2][3], 3)

        self.assertEqual(matrix_zone[1][3], 4)
        self.assertEqual(matrix_zone[1][4], 4)
        self.assertEqual(matrix_zone[2][4], 4)
        self.assertEqual(matrix_zone[3][4], 4)

        self.assertEqual(matrix_zone[2][1], 5)
        self.assertEqual(matrix_zone[3][1], 5)
        self.assertEqual(matrix_zone[3][0], 5)
        self.assertEqual(matrix_zone[3][2], 5)

        self.assertEqual(matrix_zone[3][3], -1)
        self.assertEqual(matrix_zone[4][0], -1)

        self.assertEqual(matrix_zone[4][1], 6)
        self.assertEqual(matrix_zone[4][2], 6)
        self.assertEqual(matrix_zone[4][3], 6)

        self.assertEqual(matrix_zone[4][4], 7)

        self.assertEqual(nb_zone, 7)

    def test_zoning3(self):
        """
        Test that the zoning is working for tiles 3
        """
        type_matrix = self.init_tiles4()

        matrix_zone, nb_zone = zoning(type_matrix)

        self.assertEqual(matrix_zone[0][0], 1)
        self.assertEqual(matrix_zone[0][1], 1)
        self.assertEqual(matrix_zone[1][0], 1)
        self.assertEqual(matrix_zone[2][0], 1)

        self.assertEqual(matrix_zone[0][2], -1)

        self.assertEqual(matrix_zone[0][3], 2)
        self.assertEqual(matrix_zone[0][4], 2)

        self.assertEqual(matrix_zone[1][1], 3)
        self.assertEqual(matrix_zone[1][2], 3)
        self.assertEqual(matrix_zone[2][2], 3)
        self.assertEqual(matrix_zone[2][3], 3)

        self.assertEqual(matrix_zone[1][3], 4)
        self.assertEqual(matrix_zone[1][4], 4)
        self.assertEqual(matrix_zone[2][4], 4)
        self.assertEqual(matrix_zone[3][4], 4)

        self.assertEqual(matrix_zone[2][1], 5)
        self.assertEqual(matrix_zone[3][1], 5)
        self.assertEqual(matrix_zone[3][0], 5)
        self.assertEqual(matrix_zone[3][2], 5)

        self.assertEqual(matrix_zone[3][3], -1)
        self.assertEqual(matrix_zone[4][0], -1)

        self.assertEqual(matrix_zone[4][1], 6)
        self.assertEqual(matrix_zone[4][2], 6)
        self.assertEqual(matrix_zone[4][3], 6)

        self.assertEqual(matrix_zone[4][4], 7)

        self.assertEqual(nb_zone, 7)

    def test_score1(self):
        """
        Test the full transformation for tiles 1
        """
        tiles = self.init_tileswithcrown()
        tiles = assign_crowns_to_tiles(tiles)
        matrix_tiles = compute_matrix_from_predictions(tiles)
        matrix_zone, _ = zoning(matrix_tiles)
        details = score(matrix_tiles, matrix_zone)

        self.assertEqual(details['result'], 31)
        self.assertEqual(details[TILE_TYPE_VOID]['result'], 0)
        self.assertEqual(details[TILE_TYPE_VOID]['nb_tiles'], 0)
        self.assertEqual(details[TILE_TYPE_VOID]['crowns'], 0)
        self.assertEqual(details[TILE_TYPE_WHEAT]['result'], 3)
        self.assertEqual(details[TILE_TYPE_WHEAT]['nb_tiles'], 5)
        self.assertEqual(details[TILE_TYPE_WHEAT]['crowns'], 1)
        self.assertEqual(details[TILE_TYPE_CASTLE]['result'], 0)
        self.assertEqual(details[TILE_TYPE_CASTLE]['nb_tiles'], 1)
        self.assertEqual(details[TILE_TYPE_CASTLE]['crowns'], 0)
        self.assertEqual(details[TILE_TYPE_FOREST]['result'], 6)
        self.assertEqual(details[TILE_TYPE_FOREST]['nb_tiles'], 5)
        self.assertEqual(details[TILE_TYPE_FOREST]['crowns'], 2)
        self.assertEqual(details[TILE_TYPE_LAKE]['result'], 1)
        self.assertEqual(details[TILE_TYPE_LAKE]['nb_tiles'], 1)
        self.assertEqual(details[TILE_TYPE_LAKE]['crowns'], 1)
        self.assertEqual(details[TILE_TYPE_MINE]['result'], 21)
        self.assertEqual(details[TILE_TYPE_MINE]['nb_tiles'], 3)
        self.assertEqual(details[TILE_TYPE_MINE]['crowns'], 7)
        self.assertEqual(details[TILE_TYPE_SWAMP]['result'], 0)
        self.assertEqual(details[TILE_TYPE_SWAMP]['nb_tiles'], 1)
        self.assertEqual(details[TILE_TYPE_SWAMP]['crowns'], 0)

    def test_score_empty(self):
        """
        Test the full transformation with no tiles recognized
        """
        tiles = []
        tiles = assign_crowns_to_tiles(tiles)
        matrix_tiles = compute_matrix_from_predictions(tiles)
        matrix_zone, _ = zoning(matrix_tiles)
        result = score(matrix_tiles, matrix_zone)

        self.assertEqual(result['result'], 0)
