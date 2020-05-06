# pylint: disable=global-statement
"""
File that fill handle all model loading and global variables
"""
from flask import current_app as app
from main.yolov3.models import yolov3

MODEL_KINGDOMINO_V1 = None


def load_models():
    """
    Main function to load all models to expose to the API
    :return:
    """
    global MODEL_KINGDOMINO_V1
    MODEL_KINGDOMINO_V1 = yolov3(classes=app.config['KINGDOMINO_V1_MODEL_CLASS_NUMBER'])
    MODEL_KINGDOMINO_V1.load_weights(app.config['KINGDOMINO_V1_MODEL_WEIGHT_PATH']).expect_partial()
    print "-- Weights modelKingDominoV1 loaded --"
