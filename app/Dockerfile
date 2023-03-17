# Gemerator of images with  geometric shapes
#
# VERSION               0.1
# DOCKER-VERSION        0.3

# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

WORKDIR image_generator

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "image_generator_complex_scenarious.py"]
