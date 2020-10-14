import json
import time
import redis
import numpy as np
import traceback

from config import Config
import main.yolov3.yolomodels as mdl
from main.gamecommon.yolo_transform import convert_prediction_to_tiles, assign_crowns_to_tiles, \
    compute_matrix_from_predictions, zoning, score
from main.yolov3.imagepreprocessing import base64_decode_image


def queuing_process():
    print "* Loading TF models ... *"
    mdl.load_models()

    print "* Init redis client *"
    redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)
    print "* Redis Client : OK *"
    print "* Queue is ready to handle files *"

    # continually poll for new images to classify
    while True:
        # attempt to grab a batch of images from the database, then
        # initialize the image IDs and batch of images themselves
        queue = redis_client.lrange(Config.REDIS_QUEUE_KINGDOMINO, 0, Config.REDIS_BATCH_SIZE - 1)
        imageIDs = []
        batch = None

        # loop over the queue
        for q in queue:
            # deserialize the object and obtain the input image
            q = json.loads(q.decode("utf-8"))
            image = base64_decode_image(q['image'], "float32", (
                1, Config.KINGDOMINO_V1_MODEL_SIZE_IMAGE, Config.KINGDOMINO_V1_MODEL_SIZE_IMAGE, 3))

            # check to see if the batch list is None
            if batch is None:
                batch = image
            # otherwise, stack the data
            else:
                batch = np.vstack([batch, image])
            # update the list of image IDs
            imageIDs.append(q["id"])

            # check to see if we need to process the batch
            if len(imageIDs) > 0:
                # classify the batch

                for i in range(len(imageIDs)):
                    boxes, scores, classes, _ = mdl.MODEL_KINGDOMINO_V1(np.expand_dims(batch[i], 0))

                    # postprocessing
                    # transform result to remove one array layer, and keep only probabilities higher than 0
                    scores, boxes, classes = postprocessing(batch[i], boxes, scores, classes)

                    try:
                        # Compute the score
                        result = compute_result(scores, boxes, classes)
                        result["success"] = True
                    except Exception as exc:
                        print "Error computing result ! Exception : "
                        traceback.print_exc()
                        result = {"result": 0, "success": False}

                    # store the output predictions in the database, using
                    # the image ID as the key so we can fetch the results
                    redis_client.set(imageIDs[i], json.dumps(result, sort_keys=True))

                # remove the set of images from our queue
                redis_client.ltrim(Config.REDIS_QUEUE_KINGDOMINO, len(imageIDs), -1)

            # sleep for a small amount
            time.sleep(Config.REDIS_SERVER_SLEEP)


def postprocessing(image, boxes, scores, classes):
    """
    Postprocessing is required to handle the result from the algorithm
    Removing one array layer and keeping probabilities > 0
    :param image: the image
    :param boxes: numpy array of result boxes
    :param scores: numpy array of result probabilities
    :param classes: numpy array of classes predicted for each box
    :return: scores, boxes, classes
    """
    [boxes] = boxes.numpy()
    [scores] = scores.numpy()
    [classes] = classes.numpy()
    scores = scores[scores != 0.]
    boxes = boxes[:len(scores)] * image.shape[0]
    classes = classes[:len(scores)]

    return scores, boxes, classes


def compute_result(scores, boxes, classes):
    """
    Compute the board score from the prediction
    :param scores: array of probabilities for each box
    :param boxes: array of predicted boxes
    :param classes: array of classes predicted
    :return: the result as an Int
    """
    tiles = convert_prediction_to_tiles(boxes, scores, classes)
    tiles = assign_crowns_to_tiles(tiles)
    matrix_tiles = compute_matrix_from_predictions(tiles)
    zone_matrix, _ = zoning(matrix_tiles)
    return score(matrix_tiles, zone_matrix)


if __name__ == "__main__":
    queuing_process()
