"""
Script that will handle the configuration depending on the environment
"""
import os


class Config(object):
    """
    Class that will handle common configuration for all environment
    """
    AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY', 'Nice try')
    AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY', 'Nice try again')
    AWS_S3_URL = os.getenv('AWS_S3_URL', 'Hihi')
    DEBUG = False
    MEDIA_ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    MEDIA_IMAGE_PATH = os.getenv('MEDIA_IMAGE_PATH', '/app/media/')
    # Path to class file
    KINGDOMINO_V1_CLASSES_FILE_PATH = os.getenv('KINGDOMINO_V1_CLASSES_FILE_PATH', './data/kingdomino.names')
    # Path to model weight
    KINGDOMINO_V1_MODEL_WEIGHT_PATH = os.getenv('KINGDOMINO_V1_MODEL_WEIGHT_PATH', './data/yolov3.tf')
    # Image input size
    KINGDOMINO_V1_MODEL_SIZE_IMAGE = int(os.getenv('KINGDOMINO_V1_MODEL_SIZE_IMAGE', 416))
    # Number of classes in the model
    KINGDOMINO_V1_MODEL_CLASS_NUMBER = int(os.getenv('KINGDOMINO_V1_MODEL_CLASS_NUMBER', 8))
    ENVIRONMENT = "Development"
    FLASK_RUN_HOST = os.getenv('FLASK_RUN_HOST', "0.0.0.0")
    FLASK_RUN_PORT = int(os.getenv('FLASK_RUN_PORT', 80))
    REDIS_HOST = os.getenv('REDIS_HOST', "redis")
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_QUEUE_KINGDOMINO = os.getenv('REDIS_QUEUE_KINGDOMINO', "kingdomino_queue")
    REDIS_BATCH_SIZE = int(os.getenv('REDIS_BATCH_SIZE', 32))
    REDIS_SERVER_SLEEP = float(os.getenv('REDIS_SERVER_SLEEP', 0.25))
    REDIS_CLIENT_SLEEP = float(os.getenv('REDIS_CLIENT_SLEEP', 0.25))
    REDIS_URL = "redis://" + REDIS_HOST + ":" + str(REDIS_PORT) + "/0"


class DevelopmentConfig(Config):
    DEBUG = True
    ENVIRONMENT = "Development"


class ProductionConfig(Config):
    DEBUG = False
    ENVIRONMENT = "Production"


CONFIG_BY_NAME = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
