"""
Script that will handle all preprocessing routines for images
"""
import tensorflow as tf


def transform_images(x_train, size):
    """
    Preprocess our image to fit to the model
    :param x_train: the image to modify
    :param size: the desire size [we are making a square]
    :return: the image modified as a tensor
    """
    x_train = tf.image.resize(x_train, (size, size))
    x_train = x_train / 255
    return x_train
