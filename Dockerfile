# Pull base image
FROM tensorflow/tensorflow:latest

# Set environment variables
ENV FLASK_APP run_server.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 80
ENV AWS_SECRET_KEY "Nice try"
ENV AWS_ACCESS_KEY "Nice try again"
ENV AWS_S3_URL "Http://hihi.tv"
ENV MEDIA_IMAGE_PATH /app/media/
ENV KINGDOMINO_V1_CLASSES_FILE_PATH "/app/data/kingdomino.names"
ENV KINGDOMINO_V1_MODEL_WEIGHT_PATH "/app/data/yolov3.tf"
ENV KINGDOMINO_V1_MODEL_SIZE_IMAGE 416
ENV KINGDOMINO_V1_MODEL_CLASS_NUMBER 8
ENV ENVIRONMENT dev

# Set work directory
WORKDIR /app

# Install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system

# Copy project
COPY . /app/
