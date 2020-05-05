"""
Script that will handle the configuration depending on the environment
"""
import os

class Config:
    """
    Class that will handle common configuration for all environment
    """
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY', 'Nice try')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', 'Nice try again')
    AWS_S3_URL = os.getenv('AWS_S3_URL', 'Hihi')
    DEBUG = False
    MEDIA_ALLOWED_EXTENSIONS = {'jpg','jpeg','png'}
    MEDIA_IMAGE_PATH = os.getenv('MEDIA_IMAGE_PATH', '/app/media/')
    # Path to class file
    KINGDOMINO_V1_CLASSES_FILE_PATH = os.getenv('KINGDOMINO_V1_CLASSES_FILE_PATH', './data/kingdomino.names')
    # Path to model weight
    KINGDOMINO_V1_MODEL_WEIGHT_PATH = os.getenv('KINGDOMINO_V1_MODEL_WEIGHT_PATH', './data/yolov3.tf')
    # Image input size
    KINGDOMINO_V1_MODEL_SIZE_IMAGE = os.getenv('KINGDOMINO_V1_MODEL_SIZE_IMAGE', 416)
    # Number of classes in the model
    KINGDOMINO_V1_MODEL_CLASS_NUMBER = os.getenv('KINGDOMINO_V1_MODEL_CLASS_NUMBER', 8)

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

CONFIG_BY_NAME = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
