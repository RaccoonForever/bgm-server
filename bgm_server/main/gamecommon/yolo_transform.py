# pylint: disable=line-too-long, consider-using-enumerate
"""
Script that handle every transformations to compute a score from a yolo prediction
"""
from operator import attrgetter

from main.gamecommon.tile import Tile
from main.gamecommon.constants import MAX_TILE_NUMBER, MATRIX_ERROR_MARGIN, TILE_TYPE_CROWN


def convert_prediction_to_tiles(boxes, scores, classes):
    """
    Function that will convert the 3 output from the model prediction to tiles
    :param boxes: the array containing boxes for each tile
    :param scores: the array containing probabilities for each class
    :param classes: the array containing the classes
    :return: a list of tiles
    """
    tiles = []
    for i in range(len(boxes)):
        tile = Tile(tiletype=classes[i], xmin=boxes[i][0], ymin=boxes[i][1], xmax=boxes[i][2], ymax=boxes[i][3],
                    probability=scores[i])
        tiles.append(tile)

    return tiles


def compute_matrix_from_predictions(tiles):
    """
    Function that will give the two matrixes (type matrix and crown matrix) from the tiles given by the prediction
    :param tiles: tiles given by a prediction
    :return:two matrixes (type tile matrix and crown matrix)
    """
    if tiles:
        minx_tile = min(tiles, key=attrgetter('xmin'))
        miny_tile = min(tiles, key=attrgetter('ymin'))

    matrix_tiles = [[None for i in range(MAX_TILE_NUMBER)] for y in range(MAX_TILE_NUMBER)]

    for tile in tiles:

        # For each tile
        # Find Y position in matrix
        # Retrieve tile width
        tilewidth = tile.get_width()

        # Retrieve error from tile
        errormargin = tilewidth * MATRIX_ERROR_MARGIN

        # Compute the size between most left x from all tiles and this tile.xmin
        widthremaining = tile.xmin - minx_tile.xmin

        # Becareful of 0 if same tile
        if widthremaining != 0:

            divisionmarginpositive = widthremaining / (tilewidth + int(errormargin))
            divisionmarginnegative = widthremaining / (tilewidth - int(errormargin))

            number_dec_positive = str(divisionmarginpositive - int(divisionmarginpositive))[1:]
            number_dec_negative = str(divisionmarginnegative - int(divisionmarginnegative))[1:]

            if number_dec_positive < number_dec_negative:
                y_position = int(divisionmarginpositive)
            else:
                y_position = int(divisionmarginnegative)

        else:
            y_position = 0

        # Find Y position in matrix
        # Retrieve tile height
        tileheight = tile.get_height()

        # Retrieve error from tile
        errormargin = tileheight * MATRIX_ERROR_MARGIN

        # Compute the size between most upper y from all tiles and this tile.ymin
        heightremaining = tile.ymin - miny_tile.ymin

        # Becareful of 0 if same tile
        if heightremaining != 0:
            divisionmarginpositive = heightremaining / (tileheight + int(errormargin))
            divisionmarginnegative = heightremaining / (tileheight - int(errormargin))

            number_dec_positive = str(divisionmarginpositive - int(divisionmarginpositive))[1:]
            number_dec_negative = str(divisionmarginnegative - int(divisionmarginnegative))[1:]

            if number_dec_positive < number_dec_negative:
                x_position = int(divisionmarginpositive)
            else:
                x_position = int(divisionmarginnegative)
        else:
            x_position = 0

        matrix_tiles[x_position][y_position] = tile

    return matrix_tiles


def assign_crowns_to_tiles(tiles):
    """
    Function that will assign crowns to each tile who has crown(s) in their tile
    :param tiles: all tiles from predictions including crown tiles
    :return: tiles with crowns assigned, no more crown tiles
    """
    # Retrieve tiles different from crowns

    tiles_minus_crown = [tile for tile in tiles if tile.type != TILE_TYPE_CROWN]
    crowns = [crown for crown in tiles if crown.type == TILE_TYPE_CROWN]

    treated = []
    for tile in tiles_minus_crown:
        for crown in crowns:
            if tile.is_overlapping(crown) and crown not in treated:
                tile.add_crown(crown)
                treated.append(crown)

    return tiles_minus_crown


def score(matrix_tiles, zone_matrix):
    """
    Compute the score from the tiles and the zone matrix
    :param matrix_tiles: Tiles from prediction
    :param zone_matrix: zone matrix returned by the zoning function
    :return: the score
    """
    result = 0

    # Tile number is the maximum zone number
    for k in range(1, len(matrix_tiles) * len(matrix_tiles[0]) + 1):
        crowns = 0
        nb_tiles = 0
        for i in range(len(zone_matrix)):
            for j in range(len(zone_matrix[0])):

                if zone_matrix[i][j] == k:
                    nb_tiles += 1
                    tile = matrix_tiles[i][j]
                    crowns += len(tile.crowns)

        result += crowns * nb_tiles

    return result


def zoning(matrix_tiles):
    """
    Function that will compute domains area starting from zone number 1
    :param matrix_tiles: the matrix containing tiles
    :return: a zone matrix
    """

    # Zone de depart -> 1
    zone = 1
    zone_matrix = [[-1 for j in range(len(matrix_tiles[0]))] for j in range(len(matrix_tiles))]

    for i in range(len(matrix_tiles)):
        for j in range(len(matrix_tiles[0])):

            if matrix_tiles[i][j] is None or zone_matrix[i][j] != -1:
                continue

            zone_matrix[i][j] = zone
            recursive_zoning(zone_matrix, matrix_tiles, i, j, zone)

            zone += 1

    return zone_matrix, zone - 1


def recursive_zoning(zone_matrix, matrix_tiles, i, j, zone):
    """
    The recursive function called to discover an entire zone
    :param zone_matrix: the matrix to modify
    :param matrix_tiles: the matrix of tiles
    :param i: row parameter
    :param j: column parameter
    :param zone: the current zone number
    """
    if i - 1 >= 0:
        if matrix_tiles[i - 1][j] is not None and matrix_tiles[i][j] is not None:
            if matrix_tiles[i - 1][j].type == matrix_tiles[i][j].type and zone_matrix[i - 1][j] == -1:
                zone_matrix[i - 1][j] = zone
                recursive_zoning(zone_matrix, matrix_tiles, i - 1, j, zone)

    if i + 1 < len(matrix_tiles):
        if matrix_tiles[i + 1][j] is not None and matrix_tiles[i][j] is not None:
            if matrix_tiles[i + 1][j].type == matrix_tiles[i][j].type and zone_matrix[i + 1][j] == -1:
                zone_matrix[i + 1][j] = zone
                recursive_zoning(zone_matrix, matrix_tiles, i + 1, j, zone)

    if j - 1 >= 0:
        if matrix_tiles[i][j - 1] is not None and matrix_tiles[i][j] is not None:
            if matrix_tiles[i][j - 1].type == matrix_tiles[i][j].type and zone_matrix[i][j - 1] == -1:
                zone_matrix[i][j - 1] = zone
                recursive_zoning(zone_matrix, matrix_tiles, i, j - 1, zone)

    if j + 1 < len(matrix_tiles[0]):
        if matrix_tiles[i][j + 1] is not None and matrix_tiles[i][j] is not None:
            if matrix_tiles[i][j + 1].type == matrix_tiles[i][j].type and zone_matrix[i][j + 1] == -1:
                zone_matrix[i][j + 1] = zone
                recursive_zoning(zone_matrix, matrix_tiles, i, j + 1, zone)
