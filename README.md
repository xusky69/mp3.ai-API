# mp3.ai-API

**(THIS PROJECT IS A WORK IN PROGRESS)**

A REST API for transcribing and analyzing mp3 files with AI. This project is made using [Django Rest Framework](https://www.django-rest-framework.org/).

## Setting up dev environment

1. Clone the repo & cd to `REPO_FOLDER/django_project/`
2. Make sure you have installed a modern python 3 (>3.7) in your current environment
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
5. create & run the initial migrations
```
python manage.py makemigrations accounts
python manage.py makemigrations mp3
python manage.py migrate
```
6. run the development server
```
python manage.py runserver
```
The api will be served at `localhost:8000`