# import the necessary packages
import numpy as np
import flask
from flask import Blueprint
from flask_restplus import Resource, Api
from werkzeug.utils import secure_filename
import io
import os
import tensorflow as tf
from main.yolov3.models import YoloV3
from main.yolov3.dataset import transform_images
from main.yolo_transform import convert_prediction_to_tiles, assign_crowns_to_tiles, compute_matrix_from_predictions, zoning, score
from main.flaskutils.parsers import ImageParser
from config import CONFIG_BY_NAME
from main.flaskutils.kingdominocontroller import API as kingdominons

BLUEPRINT = Blueprint('api', __name__)

# initialize our Flask application
app = flask.Flask(__name__)
app.config.from_object(CONFIG_BY_NAME[os.getenv('ENVIRONMENT', 'dev')])
print("--- Environment %s initialized ---" % (os.getenv('ENVIRONMENT')))

# Global var for models
modelKingDominoV1 = None

API = Api(BLUEPRINT, version='0.1', title='BoardGameMate API', description='', validate=True)
API.add_namespace(kingdominons, path='/kingdomino')

app.register_blueprint(BLUEPRINT)
app.app_context().push()

IMAGE_PARSER = ImageParser.image_uploaded

def load_models():
    global modelKingDominoV1
    modelKingDominoV1 = YoloV3(classes=int(app.config['KINGDOMINO_V1_MODEL_CLASS_NUMBER']))
    modelKingDominoV1.load_weights(app.config['KINGDOMINO_V1_MODEL_WEIGHT_PATH']).expect_partial()
    print("-- Weights modelKingDominoV1 loaded --")

if __name__ == "__main__":
    print(("* Loading TF models and Flask starting server..."
        "please wait until server has fully started"))
    load_models()
    app.run(host='0.0.0.0', port=80)
