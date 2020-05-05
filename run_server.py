# import the necessary packages
import numpy as np
import flask
from flask_restplus import Resource, Api
from werkzeug.utils import secure_filename
import io
import tensorflow as tf
from main.yolov3.models import YoloV3
from main.yolov3.dataset import transform_images
from main.yolo_transform import convert_prediction_to_tiles, assign_crowns_to_tiles, compute_matrix_from_predictions, zoning, score
from flaskutils.parsers import ImageParser


# Path to class file
CLASSES = './data/kingdomino.names'
# Path to model weight
MODEL_WEIGHT = './data/yolov3.tf'
# Image input size
MODEL_SIZE_IMAGE = 416
# Image output path
OUTPUT_IMAGE_PATH = './output.jpg'
# Number of classes in the model
MODEL_CLASS_NUM = 8

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
modelKingDomino = None

api = Api(app=app, version='0.1', title='BoardGameMate API', description='', validate=True)
IMAGE_PARSER = ImageParser.image_uploaded

def load_model():
    global modelKingDomino
    modelKingDomino = YoloV3(classes=MODEL_CLASS_NUM)
    modelKingDomino.load_weights(MODEL_WEIGHT).expect_partial()
    print("-- Weights loaded --")

    class_names = [c.strip() for c in open(CLASSES).readlines()]
    print("-- Classes loaded --")

@api.route("/predict/kingdomino/latest")
@api.expect(IMAGE_PARSER)
class KingDominoAILatest(Resource):
    """
    API Class for the last model of KingDomino
    """
    def post(self):
        data = {"success": False}

        args = IMAGE_PARSER.parse_args()
        filename = args['image_file']
        filename.save("temp.jpg")
        img_raw = tf.image.decode_image(open("temp.jpg", 'rb').read(), channels=3)

	width, height, channels = img_raw.shape
        img = tf.expand_dims(img_raw, 0)
        img = transform_images(img, MODEL_SIZE_IMAGE)

        boxes, scores, classes, _ = modelKingDomino(img)

	[boxes] = boxes.numpy()
        [scores] = scores.numpy()
        [classes] = classes.numpy()
        scores = scores[scores != 0.]
        boxes = boxes[:len(scores)] * width
        classes = classes[:len(scores)]

        print(boxes)
        print(scores)
        print(classes)

        tiles = convert_prediction_to_tiles(boxes, scores, classes)
        tiles = assign_crowns_to_tiles(tiles)
        matrix_tiles = compute_matrix_from_predictions(tiles)
        zone_matrix, _ = zoning(matrix_tiles)
        result = score(matrix_tiles, zone_matrix)
        data["result"] = result
        data["success"] = True
        
        return flask.jsonify(data)


@api.route("/test")
class Test(Resource):
    def get(self):
         return "Hello world"

if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    load_model()
    app.run(host='0.0.0.0', port=80)
