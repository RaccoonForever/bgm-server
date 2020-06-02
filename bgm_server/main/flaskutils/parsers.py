# pylint: disable=too-few-public-methods, line-too-long
"""
Script that will contain Request parser for special requests such as Images
"""
import werkzeug
from flask_restplus import reqparse


class ImageParser(object):
    """
    Class that will handle Image request parser
    """
    image_uploaded = reqparse.RequestParser()
    image_uploaded.add_argument('image_file', type=werkzeug.datastructures.FileStorage, location='files', required=True,
                                help='Image File')
