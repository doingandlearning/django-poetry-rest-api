# Deployment Checklist

## Environment Variables

1. Install `environs[django]`

2. Add the code in `settings.py` to load and use them.

```python
# django_project/settings.py
from pathlib import Path
from environs import Env # new
env = Env()  # new
env.read_env()  # new
```

3. Now add a `.env` and update your `.gitignore` to exclude this from source control.

## DEBUG and secret key

1. In `settings.py` we want DEBUG to be True when we are developing but False in production.

```python
DEBUG = env.bool("DEBUG", default=False)
```

2. In your local `.env` file, add `DEBUG=True`.

3. Generate a new secret key. One way to do this is run this in your terminal:

```bash
python -c "import secrets; print(secrets.token_urlsafe())"
```

4. Add to your `.env` file.

```
SECRET_KEY=KBl3sX5kLrd2zxj-pAichjT0EZJKMS0cXzhWI7Cydqc
```

5. Update your settings.py

```python
SECRET_KEY = env.str("SECRET_KEY")
```

## Allowed Hosts

This represents the host/domain names that our Django project can serve - much like the ALLOWED_CORS setting.

Update your `settings.py` to represent where your front end is going to be hosted.

```python
ALLOWED_HOSTS = [".herokuapp.com", "localhost", "127.0.0.1"]  # new
```

## Databases

You'll want to move the database URL into `.env`.

## Gunicorn

Gunicorn is a production web server and must be installed as well to replace the current Django web server which is only suitable for local development.

```
poetry add gunicorn==20.1.0
```

## Poetry build pack for Heroku

If you are deploying to Heroku, you need to let Heroku know how to install your dependencies from Poetry.

This assumes you have the heroku-cli app installed:

```
heroku buildpacks:clear
heroku buildpacks:add https://github.com/moneymeets/python-poetry-buildpack.git
heroku buildpacks:add heroku/python
```

The build pack help to create a requirement.txt file from your pyproject.lock during the build on Heroku.

## Procfil and runtime.txt

Heroku relies on a custom file called Procfile that describes how to run projects in production. This must be created in the project root directory next to the manage.py file. 

```
web: gunicorn django_project.wsgi --log-file -
```

The final step is to specify which Python version should run with `runtime.txt`.

```
python-3.10.2
```

## Checklist

We just went through a lot of steps. Too many to remember for most developers which is why deployment checklists exist. To recap, here is what we did:

- add environment variables via environs[django]
- set DEBUG to False
- set ALLOWED_HOSTS
- use environment variable for SECRET_KEY
- update DATABASES 
- install gunicorn for a production web server
- install the Heroku poetry buildpack
- create a Procfile for Heroku
- create a runtime.txt to set the Python version on Heroku