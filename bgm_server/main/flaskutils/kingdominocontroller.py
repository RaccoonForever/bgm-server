# pylint: disable=no-self-use
"""
KingDomino Controller
"""
import os
import uuid
import flask
from flask import current_app as APP
from flask_restplus import Resource
from main.flaskutils import API
from main.flaskutils.parsers import ImageParser
from main.yolov3.predict import predict_kingdomino_v1
from main.gcp.gcs import upload_image

IMAGE_PARSER = ImageParser.image_uploaded


def allowed_file(filename):
    """
    Function that will check that the file upload is of good format
    :param filename: the filename of the file to check
    :return: the file extension if is is allowed, else None
    """
    ext = filename.rsplit('.', 1)[1].lower()
    if '.' in filename and ext in APP.config['MEDIA_ALLOWED_EXTENSIONS']:
        return ext
    return None


@API.route('/kingdomino/predict/latest')
class KingDominoLatest(Resource):
    """
    API Class for the last model of KingDomino
    """

    @API.expect(IMAGE_PARSER)
    @API.doc('Get prediction from an image file for a kingdomino board. This is the latest model')
    @API.response(404, "Error uploading the image or computing the result")
    @API.response(400, "Image validation error. Probably wrong formatting for the POST call")
    def post(self):
        """
        Post function
        :return: the score prediction
        """
        data = {"success": False}

        args = IMAGE_PARSER.parse_args()
        tempfile = args['image_file']

        extension = allowed_file(tempfile.filename)

        if extension:
            # Generate unique uuid
            unique_id = str(uuid.uuid1())

            # Save the file
            path = os.path.join(APP.config['MEDIA_IMAGE_PATH'], unique_id + "." + extension)
            upload_image(path, unique_id + "." + extension)
            tempfile.close()

            result = predict_kingdomino_v1(path, unique_id)

            data["result"] = result
            data["success"] = True

            return flask.jsonify(data)
        return {
            "success": False,
            "result": "File extension is not allowed. Only JPEG/JPG/PNG are allowed !"
        }
