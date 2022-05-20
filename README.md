# mp3.ai-API

**[THIS PROJECT IS A WORK IN PROGRESS]**


A **REST API** for **transcribing** and **analyzing** mp3 files with **AI**. This project is made using [Django Rest Framework](https://www.django-rest-framework.org/).

![GIF demo](https://imgur.com/DtyobLM.gif)

### Features:
- Transcripts a given **.mp3** audio file
- Given a set of words, returns a word count
- Given a set of words, returns the timestamps & confidence values for each one
- Performs a sentiment analysis of the transcript
- Token authentication
- Create, Read & Delete operations for your results
- In-DB history log for CRUD operations

### Known limitations:
- only **.mp3 files are supported**
- Your audio file will be cropped to the first minute

### To be done:
- Support longer audio files
- Support a more sofisticated auth strategy (JWT, iron-session, etc)
- Create dedicated microservices for model inference only
- Move the inference pipeline to the `save` method of the `Recording` model, *in order to keep views thin and models fat*

## Setting up dev environment

1. Clone the repo & cd to `REPO_FOLDER/django_project/`
2. Make sure you have installed a modern python 3 (>3.9) in your current environment
3. Create a `venv` or use virtual environment manager of your preference (conda, pyenv, etc...), then install dependencies. eg:
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
4. Create a symlink between `dev_env_vars` and a `.env` file (or just copy `dev_env_vars` and rename it to `.env`):
```
ln dev_env_vars .env
```
5. open `MP3AI/settings.py` and at the bottom of the file make sure that both `ENABLE_SENT` and `ENABLE_VOSK` are set to `False`:
```
# ENABLE HUGGINGFACE ROBERTA SENTIMENT MODEL
ENABLE_SENT = False

# ENABLE VOSK S2T MODEL
ENABLE_VOSK = False
```
**NOTE**: this disables ML models in order to speed up migrations
6. create & run the initial migrations
```
python manage.py makemigrations accounts
python manage.py makemigrations mp3
python manage.py makemigrations
python manage.py migrate
python manage.py populate_history --auto
```
7. open `MP3AI/settings.py` and at the bottom of the file make sure that both `ENABLE_SENT` and `ENABLE_VOSK` are set to `True`:
```
# ENABLE HUGGINGFACE ROBERTA SENTIMENT MODEL
ENABLE_SENT = True

# ENABLE VOSK S2T MODEL
ENABLE_VOSK = True
```
8. run the development server
```
python manage.py runserver
```
The API will be served at `localhost:8000/api/v1/recordings/`


**PLEASE READ**: 
a. the first time you spawn the dev server, it will take a long time to boot, as it will be downloading the sentiment transformer model
b. subsequent dev server executions will also be longer than the usual, as it will take some time to initialize the sentiment transformer model

## Setting up docker environment
1. cd to the repo root & run
```
docker-compose up --build
```
2. open another terminal and run migrations
```
docker-compose exec django python manage.py makemigrations accounts
docker-compose exec django python manage.py makemigrations mp3
docker-compose exec django python manage.py migrate
```
**NOTE**: migrations will be very slow to execute, due to ML models instanciating each time you run one of the above commands
3. take containers down and up again just to make sure the db initializes properly
```
docker-compose down
docker-compose up
```
The API will be served at `localhost:8000/api/v1/recordings/`

## Testing the API

You will find an example test script at `REPO_ROOT/test_api.py`
```
python test_api.py
```
