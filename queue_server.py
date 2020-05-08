import json
import time
import redis
import tensorflow as tf
import numpy as np
from config import Config
import main.yolov3.yolomodels as mdl
from main.gamecommon.yolo_transform import convert_prediction_to_tiles, assign_crowns_to_tiles, \
    compute_matrix_from_predictions, zoning, score
from main.yolov3.imagepreprocessing import transform_images, base64_decode_image


def queuing_process():
    print "* Loading TF models ... *"
    mdl.load_models()

    print "* Init redis client *"
    redis_client = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0)
    print "* Redis Client : OK *"

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
                    [boxes] = boxes.numpy()
                    [scores] = scores.numpy()
                    [classes] = classes.numpy()
                    scores = scores[scores != 0.]
                    boxes = boxes[:len(scores)] * batch[i].shape[0]
                    classes = classes[:len(scores)]

                    tiles = convert_prediction_to_tiles(boxes, scores, classes)
                    tiles = assign_crowns_to_tiles(tiles)
                    matrix_tiles = compute_matrix_from_predictions(tiles)
                    zone_matrix, _ = zoning(matrix_tiles)
                    result = score(matrix_tiles, zone_matrix)

                    # store the output predictions in the database, using
                    # the image ID as the key so we can fetch the results
                    redis_client.set(imageIDs[i], json.dumps(result))

                # remove the set of images from our queue
                redis_client.ltrim(Config.REDIS_QUEUE_KINGDOMINO, len(imageIDs), -1)

            # sleep for a small amount
            time.sleep(Config.REDIS_SERVER_SLEEP)


if __name__ == "__main__":
    queuing_process()
