"""
KingDomino Controller
"""
import numpy as np
import flask
from flask import current_app as app
from flask_restplus import Resource
from namespaces import KingDominoNamespace
from parsers import ImageParser
import tensorflow as tf
from main.yolov3.models import YoloV3
from main.yolov3.dataset import transform_images
from main.yolo_transform import convert_prediction_to_tiles, assign_crowns_to_tiles, compute_matrix_from_predictions, zoning, score


API = KingDominoNamespace.api

IMAGE_PARSER = ImageParser.image_uploaded

def allowed_file(filename):
    """
    Function that will check that the file upload is of good format
    :param filename: the filename of the file to check
    :return: the file extension if is is allowed, else None
    """
    ext = filename.rsplit('.', 1)[1].lower()
    if '.' in filename and ext in app.config['MEDIA_ALLOWED_EXTENSIONS']:
        return ext
    return None

@API.route('/predict/latest')
class KingDominoLatest(Resource):
    """
    API Class for the last model of KingDomino
    """
    @API.expect(IMAGE_PARSER)
    @API.doc('Get prediction from an image file for a kingdomino board. This is the latest model')
    @API.response(404, "Error uploading the image or computing the result")
    @API.response(400, "Image validation error. Probably wrong formatting for the POST call")
    def post(self):
        data = {"success": False}

        args = IMAGE_PARSER.parse_args()
        filename = args['image_file']
        filename.save("temp.jpg")
        img_raw = tf.image.decode_image(open("temp.jpg", 'rb').read(), channels=3)

        width, height, channels = img_raw.shape
        img = tf.expand_dims(img_raw, 0)
        img = transform_images(img, int(app.config['KINGDOMINO_V1_MODEL_SIZE_IMAGE']))

        boxes, scores, classes, _ = modelKingDominoV1(img)

        [boxes] = boxes.numpy()
        [scores] = scores.numpy()
        [classes] = classes.numpy()
        scores = scores[scores != 0.]
        boxes = boxes[:len(scores)] * width
        classes = classes[:len(scores)]

        tiles = convert_prediction_to_tiles(boxes, scores, classes)
        tiles = assign_crowns_to_tiles(tiles)
        matrix_tiles = compute_matrix_from_predictions(tiles)
        zone_matrix, _ = zoning(matrix_tiles)
        result = score(matrix_tiles, zone_matrix)
        data["result"] = result
        data["success"] = True
        
        return flask.jsonify(data)

