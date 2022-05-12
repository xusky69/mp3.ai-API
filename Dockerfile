# set base image (host OS)
FROM python:3.10 as base

# set working dir to root of the django project
WORKDIR /home/MP3API/

# install linux dependencies
RUN apt-get update && apt-get -y install sqlite3 libsqlite3-dev ffmpeg

# copy the requirements file to the working directory
COPY ./django_project/requirements.txt .

# install python dependencies
RUN pip install -r requirements.txt

# copy the cache script to the working directory & run it
# this will save the cached models to the image and
# avoids redownloading them each time a container respawns
RUN rm -rf .env
COPY ./django_project/docker_env_vars ./docker_env_vars
RUN cp docker_env_vars .env
RUN mkdir scripts/
COPY ./django_project/mp3/common.py ./mp3/common.py
COPY ./django_project/mp3/docker_cache.py ./mp3/docker_cache.py
RUN python ./mp3/docker_cache.py

# copy the project to the working directory
ADD ./django_project/ .

# remove logs, dev db and old env vars
RUN rm -rf db.sqlite3 mp3/migrations accounts/migrations logs media assets audio_files
RUN mkdir -p media assets static audio_files logs

# setup django environment variables:
# doing this again avoids us from 
# re-caching ml models each time the 
# container is built with changes in 
# any code of the server source
RUN rm -rf .env
COPY ./django_project/docker_env_vars ./docker_env_vars
RUN cp docker_env_vars .env

# setup python environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# setup gunicorn environment variables:
ENV WORKERS=1
ENV TIMEOUT=240

# port exposure
EXPOSE 8000

# command to run on container start when nothing else is run:
CMD gunicorn -b 0.0.0.0:8000 --timeout=$TIMEOUT --workers=$WORKERS --env DJANGO_SETTINGS_MODULE=MP3AI.settings MP3AI.wsgi
