# set base image (host OS)
FROM python:3.10 as base

# set working dir to root of the django project
WORKDIR /home/MP3API/

# install linux dependencies
RUN apt-get update && apt-get -y install sqlite3 libsqlite3-dev

# copy the requirements file to the working directory
COPY ./django_project/requirements.txt .

# install python dependencies
RUN pip install -r requirements.txt
RUN pip install django-extensions
# copy the project to the working directory
ADD ./django_project/ .

# remove logs, dev db and old env vars
RUN rm -rf .env db.sqlite3 mp3/migrations accounts/migrations logs
RUN mkdir -p media assets static audio_files logs

# setup python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# setup gunicorn environment variables:
ENV WORKERS=4
ENV TIMEOUT=240

# port exposure
EXPOSE 8000

# setup django environment variables:
RUN cp docker_env_vars .env

RUN echo "yes" | python manage.py collectstatic
# command to run on container start when nothing else is run:
CMD gunicorn -b 0.0.0.0:8000 --timeout=$TIMEOUT --workers=$WORKERS --env DJANGO_SETTINGS_MODULE=MP3AI.settings MP3AI.wsgi
