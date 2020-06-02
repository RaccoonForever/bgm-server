"""
Script that will handle all GCP actions
"""
from google.cloud import storage
from google.oauth2 import service_account
from config import Config


def init_gcs():
    """
    Method to call to get an initialized connection with GCS
    :return: the storage service
    """
    try:
        credentials = service_account.Credentials.from_service_account_file(Config.GCP_CREDENTIALS_PATH)
    except IOError:
        raise ValueError("No or invalid credentials for GCP account")

    service = storage.Client(project="DominoMate", credentials=credentials)

    return service


def upload_image(image_path, blob_name):
    """
    Upload an image on GCS
    :param image_path: the path of the image to copy
    :param blob_name: the name for the blob in GCS
    """
    service = init_gcs()
    bucket = service.get_bucket('server-kingdomino-bucket')
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(image_path)
