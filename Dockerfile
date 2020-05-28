# Pull base image
FROM tensorflow/tensorflow:latest

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV FLASK_WEB_APP run_web_server.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 80
ENV GCP_CREDENTIALS_PATH "/app/dominomate_secrets.json"
ENV MEDIA_IMAGE_PATH /app/media/
ENV KINGDOMINO_V1_CLASSES_FILE_PATH "/app/data/kingdomino.names"
ENV KINGDOMINO_V1_MODEL_WEIGHT_PATH "/app/data/yolov3.tf"
ENV KINGDOMINO_V1_MODEL_SIZE_IMAGE 416
ENV KINGDOMINO_V1_MODEL_CLASS_NUMBER 8
ENV ENVIRONMENT dev
ENV REDIS_HOST "redis"
ENV REDIS_PORT 6379
ENV REDIS_QUEUE_KINGDOMINO "kingdomino_queue"
ENV REDIS_BATCH_SIZE 32
ENV REDIS_SERVER_SLEEP 0.25
ENV REDIS_CLIENT_SLEEP 0.25

ENV WAIT_VERSION 2.7.3
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

# Set work directory
WORKDIR /app

# Install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system

COPY boot.sh /app/boot.sh
RUN chmod +x /app/boot.sh

# Copy project
COPY . /app/
