# pylint: disable=invalid-name, unused-argument, too-many-arguments
"""
Script that contain the creation of the YoloV3 model
"""
import numpy as np
import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import (
    Add,
    Concatenate,
    Conv2D,
    Input,
    Lambda,
    LeakyReLU,
    UpSampling2D,
    ZeroPadding2D,
)
from tensorflow.keras.regularizers import l2
from main.yolov3.utils import BatchNormalization

# maximum number of boxes per image
YOLO_MAX_BOXES = 100
# iou threshold
YOLO_IOU_THRESHOLD = 0.5
# yolo_score_threshold
YOLO_SCORE_THRESHOLD = 0.2

yolo_anchors = np.array([(10, 13), (16, 30), (33, 23), (30, 61), (62, 45),
                         (59, 119), (116, 90), (156, 198), (373, 326)],
                        np.float32) / 416
yolo_anchor_masks = np.array([[6, 7, 8], [3, 4, 5], [0, 1, 2]])


def darknet_conv(x, filters, size, strides=1, batch_norm=True):
    """
    Create a Darknet Conv Layer
    :param x: the input data
    :param filters: number of filters
    :param size: the size we want
    :param strides: size of the strides
    :param batch_norm: do we apply batch normalisation
    :return: A Darknet Conv Layer
    """
    if strides == 1:
        padding = 'same'
    else:
        x = ZeroPadding2D(((1, 0), (1, 0)))(x)  # top left half-padding
        padding = 'valid'
    x = Conv2D(filters=filters, kernel_size=size,
               strides=strides, padding=padding,
               use_bias=not batch_norm, kernel_regularizer=l2(0.0005))(x)
    if batch_norm:
        x = BatchNormalization()(x)
        x = LeakyReLU(alpha=0.1)(x)
    return x


def darknet_residual(x, filters):
    """
    Create a Darknet Residual Layer
    :param x: input data
    :param filters: the number of layers
    :return: a darknet residual layer
    """
    prev = x
    x = darknet_conv(x, filters // 2, 1)
    x = darknet_conv(x, filters, 3)
    x = Add()([prev, x])
    return x


def darknet_block(x, filters, blocks):
    """
    Crreate a Darknet Block Layer
    :param x: input data
    :param filters: number of filters
    :param blocks: number of blocks
    :return: a darknet block layer
    """
    x = darknet_conv(x, filters, 3, strides=2)
    for _ in range(blocks):
        x = darknet_residual(x, filters)
    return x


def darknet(name=None):
    """
    Create a darknet NN
    :param name:the name of the darknet
    :return:a Darknet Model
    """
    x = inputs = Input([None, None, 3])
    x = darknet_conv(x, 32, 3)
    x = darknet_block(x, 64, 1)
    x = darknet_block(x, 128, 2)  # skip connection
    x = x_36 = darknet_block(x, 256, 8)  # skip connection
    x = x_61 = darknet_block(x, 512, 8)
    x = darknet_block(x, 1024, 4)
    return tf.keras.Model(inputs, (x_36, x_61, x), name=name)


def yolo_conv(filters, name=None):
    """
    A YoloConv Layer
    :param filters:number of filters
    :param name:name we want to give to the layer
    :return:a YoloConv Layer
    """

    def yolo_conv_acc(x_in):
        """
        Yolo Conv Layer
        :param x_in: input tuple
        :return: Yolo Conv Layer
        """
        if isinstance(x_in, tuple):
            inputs = Input(x_in[0].shape[1:]), Input(x_in[1].shape[1:])
            x, x_skip = inputs

            # concat with skip connection
            x = darknet_conv(x, filters, 1)
            x = UpSampling2D(2)(x)
            x = Concatenate()([x, x_skip])
        else:
            x = inputs = Input(x_in.shape[1:])

        x = darknet_conv(x, filters, 1)
        x = darknet_conv(x, filters * 2, 3)
        x = darknet_conv(x, filters, 1)
        x = darknet_conv(x, filters * 2, 3)
        x = darknet_conv(x, filters, 1)
        return Model(inputs, x, name=name)(x_in)

    return yolo_conv_acc


def yolo_output(filters, anchors, classes, name=None):
    """
    YoloOutput Layer
    :param filters: Number of filters
    :param anchors: Number of anchors
    :param classes: Number of classes to predict
    :param name: The name we want to give to the layer
    :return: A YoloOutput Layer that needs an X argument
    """

    def yolo_output_acc(x_in):
        """
        YoloOutput Layer
        :param x_in: input data
        :return: The YoloOutput Layer
        """
        x = inputs = Input(x_in.shape[1:])
        x = darknet_conv(x, filters * 2, 3)
        x = darknet_conv(x, anchors * (classes + 5), 1, batch_norm=False)
        x = Lambda(lambda x: tf.reshape(x, (-1, tf.shape(x)[1], tf.shape(x)[2],
                                            anchors, classes + 5)))(x)
        return tf.keras.Model(inputs, x, name=name)(x_in)

    return yolo_output_acc


def yolo_boxes(pred, anchors, classes):
    """
    Function that will return the boxes according to the prediction
    :param pred: Prediction given by the Yolo algorithm
    :param anchors: anchors
    :param classes: number of classes to predict
    :return: boxes according to predictions, anchors and classes
    """
    # pred: (batch_size, grid, grid, anchors, (x, y, w, h, obj, ...classes))
    grid_size = tf.shape(pred)[1]
    box_xy, box_wh, objectness, class_probs = tf.split(
        pred, (2, 2, 1, classes), axis=-1)

    box_xy = tf.sigmoid(box_xy)
    objectness = tf.sigmoid(objectness)
    class_probs = tf.sigmoid(class_probs)
    pred_box = tf.concat((box_xy, box_wh), axis=-1)  # original xywh for loss

    # !!! grid[x][y] == (y, x)
    grid = tf.meshgrid(tf.range(grid_size), tf.range(grid_size))
    grid = tf.expand_dims(tf.stack(grid, axis=-1), axis=2)  # [gx, gy, 1, 2]

    box_xy = (box_xy + tf.cast(grid, tf.float32)) / \
             tf.cast(grid_size, tf.float32)
    box_wh = tf.exp(box_wh) * anchors

    box_x1y1 = box_xy - box_wh / 2
    box_x2y2 = box_xy + box_wh / 2
    bbox = tf.concat([box_x1y1, box_x2y2], axis=-1)

    return bbox, objectness, class_probs, pred_box


def yolo_nms(outputs, anchors, masks, classes):
    """
    Yolo Non Max Suppression to detect object only once
    :param outputs: the outputs computed from the model
    :param anchors: anchors
    :param masks: mask
    :param classes: number of classes we want to classify
    :return: the outputs after the algorithm Non Max Suppression has been done
    """
    # boxes, conf, type
    b, c, t = [], [], []

    for o in outputs:
        b.append(tf.reshape(o[0], (tf.shape(o[0])[0], -1, tf.shape(o[0])[-1])))
        c.append(tf.reshape(o[1], (tf.shape(o[1])[0], -1, tf.shape(o[1])[-1])))
        t.append(tf.reshape(o[2], (tf.shape(o[2])[0], -1, tf.shape(o[2])[-1])))

    bbox = tf.concat(b, axis=1)
    confidence = tf.concat(c, axis=1)
    class_probs = tf.concat(t, axis=1)

    scores = confidence * class_probs
    boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
        boxes=tf.reshape(bbox, (tf.shape(bbox)[0], -1, 1, 4)),
        scores=tf.reshape(
            scores, (tf.shape(scores)[0], -1, tf.shape(scores)[-1])),
        max_output_size_per_class=YOLO_MAX_BOXES,
        max_total_size=YOLO_MAX_BOXES,
        iou_threshold=YOLO_IOU_THRESHOLD,
        score_threshold=YOLO_SCORE_THRESHOLD
    )

    return boxes, scores, classes, valid_detections


def yolov3(size=None, channels=3, anchors=yolo_anchors,
           masks=yolo_anchor_masks, classes=80, training=False):
    """
    Create a YoloV3 model
    :param size:the input size of images
    :param channels:the number of color channels in images
    :param anchors:anchors to use
    :param masks:masks to use
    :param classes:number of classes we want to classify
    :param training:are we training or infering ?
    :return: the full YoloV3 model
    """
    x = inputs = Input([size, size, channels])

    x_36, x_61, x = darknet(name='yolo_darknet')(x)

    x = yolo_conv(512, name='yolo_conv_0')(x)
    output_0 = yolo_output(512, len(masks[0]), classes, name='yolo_output_0')(x)

    x = yolo_conv(256, name='yolo_conv_1')((x, x_61))
    output_1 = yolo_output(256, len(masks[1]), classes, name='yolo_output_1')(x)

    x = yolo_conv(128, name='yolo_conv_2')((x, x_36))
    output_2 = yolo_output(128, len(masks[2]), classes, name='yolo_output_2')(x)

    if training:
        return Model(inputs, (output_0, output_1, output_2), name='yolov3')

    boxes_0 = Lambda(lambda x: yolo_boxes(x, anchors[masks[0]], classes),
                     name='yolo_boxes_0')(output_0)
    boxes_1 = Lambda(lambda x: yolo_boxes(x, anchors[masks[1]], classes),
                     name='yolo_boxes_1')(output_1)
    boxes_2 = Lambda(lambda x: yolo_boxes(x, anchors[masks[2]], classes),
                     name='yolo_boxes_2')(output_2)

    outputs = Lambda(lambda x: yolo_nms(x, anchors, masks, classes),
                     name='yolo_nms')((boxes_0[:3], boxes_1[:3], boxes_2[:3]))

    return Model(inputs, outputs, name='yolov3')
