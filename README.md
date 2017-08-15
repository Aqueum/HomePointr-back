# HomePointr Backend
A Django back end app with PostgreSQL hosted on Ubuntu 16.04

# Method
## Setup Ubuntu 16.04
- Either follow [this guide](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04) to set up on remove server OR
- Pick box from [Vagrant](https://app.vagrantup.com/boxes/)
- I chose [ubuntu/xenial64](https://app.vagrantup.com/ubuntu/boxes/xenial64)
  - Create & navigate to new folder in terminal (I'm calling mine `HomePointr-back` cloning it from an empty GitHub & copying in the .gitignore from my [DjP](https://github.com/myprojectuser/DjP/blob/master/.gitignore))
  - `vagrant init ubuntu/xenial64`
  - edit vagrant file
    - change `# config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"`
    - to `config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"`
  - `vagrant up` if first time or `vagrant reload` to load the new vagrant file
  - `vagrant box update` to get latest version
  - `vagrant ssh` to SSH into your new box
  - `cd /vagrant` to get into the shared diectory

the following was originally based on [how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04):
## Install the Components from the Ubuntu Repositories 
- `sudo apt-get update`
- `sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib`

## Create a Database and Database User
- `sudo -u postgres psql` to log in to PostgreSQL as postgres
- enter:
    ```
    CREATE DATABASE homepointr;
    CREATE USER myprojectuser WITH PASSWORD 'jEQuV6h2uwBMG237';
    ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
    ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
    ALTER ROLE myprojectuser SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE homepointr TO myprojectuser;
    ```
- `\q` to exit PostgreSQL

## Install Django within a Virtual Environment
- `sudo -H pip3 install --upgrade pip` (because it always complains)
- `sudo -H pip3 install virtualenv` (added the -H at the prompts suggestion)
- `mkdir /vagrant/homepointr`
- `cd /vagrant/homepointr`
- `virtualenv ENV` to create virtual environment
- `source ENV/bin/activate`
- `pip install django psycopg2`
- `django-admin.py startproject homepointr .`

## Configure the Django Database Settings
- Edit `homepointr/homepointr/settings.py` to have: 
  - `ALLOWED_HOSTS = ['.localhost', '35.176.170.23', '192.168.1.65', '109.157.214.104', '127.0.0.1']` these are: local host, my lightsail ip, mu local host according to system, my public ip, standard localhost
  - `DATABASES` as:
    ```
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'homepointr',
            'USER': 'myprojectuser',
            'PASSWORD': 'jEQuV6h2uwBMG237',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    ```
  - `LANGUAGE_CODE = 'en-gb'`
  - `TIME_ZONE = 'UTC'`
    - ? still not completely sure if this should be `'UTC'` or `'Europe/London'`

## Migrate the Database and Test Project
- `cd /vagrant/homepointr`
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py createsuperuser` I used myprojectuser & jEQuV6h2uwBMG237
- `python manage.py runserver 0:8000`
- [localhost:8000](http://localhost:8000/)
- [localhost:8000/admin](http://localhost:8000/admin)

End of digitalocean setup tutorial, the following was originally based on [django polls tutorial](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)

## Create app
- ctrl-c to exit server
- `cd /vagrant/homepointr` to get to folder with manage.py
- `python manage.py startapp homes` to create homes app starter

## Create models
- Edit `homes/models.py` to:
```
from django.db import models


class Bread(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name

```
## Activate models
- add `'homes.apps.HomesConfig',` to top of `INSTALLED_APPS`. list in `homepointr/homepointr/settings.py`

## Admin
- edit `homes/admin.py` to:
```
from django.contrib import admin

from .models import Bread


class BreadAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bread, BreadAdmin)
```

## Look and feel
- add `admin.site.site_header = 'HomePointr admin'` to `homes/admin.py`


## Migrate the Database
- `python manage.py makemigrations`
- `python manage.py makemigrations homes` to create migrations for model changes
- optional `python manage.py sqlmigrate homes 0001` to see what SQL Django thinks is needed
- optional `python manage.py check` to check for project problems
- `python manage.py migrate` to create model tables in database

## Test App
- `python manage.py runserver 0:8000`
- [localhost:8000/homes](http://localhost:8000/homes)
- [localhost:8000/admin](http://localhost:8000/admin)