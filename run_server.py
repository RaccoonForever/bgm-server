# import the necessary packages
import numpy as np
import flask
from flask_restplus import Resource
from werkzeug.utils import secure_filename
import io
from yolov3.models import YoloV3
from yolov3.dataset import transform_images
from flaskutils.parsers import ImageParser
from flaskutils.namespaces import KingDominoNamespace

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

KINGDOMINO_API = KingDominoNamespace.api
IMAGE_PARSER = ImageParser.image_uploaded

def load_model():
    global modelKingDomino
    modelKingDomino = YoloV3(classes=MODEL_CLASS_NUM)
    modelKingDomino.load_weights(MODEL_WEIGHT).expect_partial()
    print("-- Weights loaded --")

    class_names = [c.strip() for c in open(MODEL_CLASS_NUM).readlines()]
    print("-- Classes loaded --")

@KINGDOMINO_API.route("/predict/kingdomino/latest")
@KINGDOMINO_API.expect(IMAGE_PARSER)
class KingDominoAILatest(Resource):
    """
    API Class for the last model of KingDomino
    """
    @KINGDOMINO_API.doc("Get prediction from an Image File of a kingdomino board. This is the latest model for this AI")
    @KINGDOMINO_API.response(404,"Can't upload the image file or get de prediction corresponding")
    @KINGDOMINO_API.response(200,"Image uploaded and prediction returned")
    def post(self):
        args = IMAGE_PARSER.parse_args()
        result = args
        return flask.jsonify(result)

#@app.route("/predict/kingdomino/latest", methods=["POST"])
#def predict():
    # initialize the data dictionary that will be returned from the
    # view
#    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
#    if flask.request.method == "POST":
#        if flask.request.files.get("image"):
#            img_raw = tf.image.decode_image(
#            open(FLAGS.image, 'rb').read(), channels=3)

#            img = tf.expand_dims(img_raw, 0)
#            img = transform_images(img, FLAGS.size)

#            boxes, scores, classes, nums = model(img)

#            data["boxes"] = boxes
#            data["scores"] = scores
#            data["classes"] = classes
#            data["nums"] = nums

            # indicate that the request was a success
#            data["success"] = True

    # return the data dictionary as a JSON response
#    return flask.jsonify(data)


if __name__ == "__main__":
    print(("* Loading Keras model and Flask starting server..."
        "please wait until server has fully started"))
    load_model()
    app.run(host='0.0.0.0', port=80)

