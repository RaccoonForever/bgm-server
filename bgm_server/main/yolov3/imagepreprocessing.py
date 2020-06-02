"""
Script that will handle all preprocessing routines for images
"""
from tensorflow.keras.preprocessing.image import img_to_array
import base64
import numpy as np


def transform_images(image, size):
    """
    Preprocess our image to fit to the model
    :param image: the image to modify
    :param size: the desire size [we are making a square]
    :return: the image modified as a tensor
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')

    image = image.resize(size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255
    return image


def base64_encode_image(a):
    """
    Encode image in base64
    :param a: the image
    """
    # base64 encode the input NumPy array
    return base64.b64encode(a).decode("utf-8")


def base64_decode_image(a, dtype, shape):
    """
    Decode image in base64
    :param a: the image encoded
    :param dtype: the type of values
    :param shape: the shape of the image
    :return: the image decoded
    """
    # convert the string to a NumPy array using the supplied data
    # type and target shape
    a = np.frombuffer(base64.decodestring(a), dtype=dtype)
    a = a.reshape(shape)
    # return the decoded image
    return a
