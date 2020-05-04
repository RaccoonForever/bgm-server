# Pull base image
FROM tensorflow/tensorflow:latest

# Set environment variables
ENV FLASK_APP run_server.py
ENV FLASK_RUN_HOST 0.0.0.0

# Set work directory
WORKDIR /app

# Install dependencies
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --system

# Copy project
COPY . /app/
