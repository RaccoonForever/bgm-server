"""
Script that will contain methods that can be used for inference
"""
import io
import time
from PIL import Image, ImageFile
from flask import current_app as APP
import json
from main.yolov3.imagepreprocessing import transform_images, base64_encode_image
from main import redis_client

# Initializing redis config
IMAGE_QUEUE = "kingdomino_queue"
BATCH_SIZE = 32
SERVER_SLEEP = 0.25
CLIENT_SLEEP = 0.25

ImageFile.LOAD_TRUNCATED_IMAGES = True


def predict_kingdomino_v1(filepath, uniqueid):
    """
    Function that will take the filepath of the image to predict using KINGDOMINO_V1_MODEL
    :param filepath: the path of the file
    :param uniqueid: the unique id for this image
    :return: the score predicted by the algorithm
    """
    img_raw = open(filepath).read()
    img_raw = Image.open(io.BytesIO(img_raw))
    img = transform_images(img_raw,
                           (APP.config['KINGDOMINO_V1_MODEL_SIZE_IMAGE'], APP.config['KINGDOMINO_V1_MODEL_SIZE_IMAGE']))

    img = img.copy(order="C")

    encoded_img = base64_encode_image(img)

    d = {
        "id": uniqueid,
        "image": encoded_img
    }

    redis_client.rpush(IMAGE_QUEUE, json.dumps(d))

    # keep looping until our model server returns the output
    # predictions
    while True:
        # attempt to grab the output predictions
        output = redis_client.get(uniqueid)
        # check to see if our model has classified the input
        # image
        if output is not None:
            print "output is : " + output
            # delete the result from the database and break
            # from the polling loop
            redis_client.delete(uniqueid)
            break
        # sleep for a small amount to give the model a chance
        # to classify the input image
        time.sleep(CLIENT_SLEEP)

    return output
