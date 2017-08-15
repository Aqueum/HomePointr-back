# HomePointr Backend
A Django back end app with PostgreSQL hosted on Ubuntu 16.04

# Method
## Setup Ubuntu 16.04
- Either follow [this guide](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04) to set up on remove server OR
- Pick box from [Vagrant](https://app.vagrantup.com/boxes/)
- I chose [ubuntu/xenial64](https://app.vagrantup.com/ubuntu/boxes/xenial64)
  - Create & navigate to new folder in terminal (I'm calling mine `HomePointr-back` cloning it from an empty GitHub & copying in the .gitignore from my [DjP](https://github.com/Aqueum/DjP/blob/master/.gitignore))
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
    CREATE USER Aqueum WITH PASSWORD '1P';
    ALTER ROLE Aqueum SET client_encoding TO 'utf8';
    ALTER ROLE Aqueum SET default_transaction_isolation TO 'read committed';
    ALTER ROLE Aqueum SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE homepointr TO Aqueum;
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
            'USER': 'Aqueum',
            'PASSWORD': '1P',
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
- `python manage.py createsuperuser` I used Aqueum & 1P
- `python manage.py runserver 0.0.0.0:8000`
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


class Provider(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.provider_name


class PropetyType(models.Model):
    ptype = models.CharField(max_length=31)

    def __str__(self):
        return self.property_type


class Council(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.council_name


class Support(models.Model):
    support = models.CharField(max_length=31)

    def __str__(self):
        return self.property_type


class Property(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    ptype = models.ForeignKey(PropetyType)
    name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255, default=name)
    address2 = models.CharField(max_length=255)
    address3 = models.CharField(max_length=255)
    town = models.CharField(max_length=31)
    region = models.CharField(max_length=31)
    postcode = models.CharField(max_length=31)
    lat = models.DecimalField(decimal_places=6)
    lng = models.DecimalField(decimal_places=6)
    council = models.ForeignKey(Council)
    bedrooms = models.IntegerField(default=1)
    beds = models.IntegerField(default=1)
    max_occupants = models.IntegerField(default=1)
    support = models.ManyToManyField(Support)
    wheelchair_accessible = models.BooleanField
    parking = models.BooleanField
    shared = models.BooleanField
    rent_pcm = models.DecimalField(decimal_places=2)
    deposit = models.DecimalField(decimal_places=2)
    units = models.IntegerField(default=1)
    next_available = models.DateField

    def __str__(self):
        return self.property_name


class Photo(models.Model):
    prop = models.ForeignKey(Property, on_delete=models.CASCADE)
    url = models.CharField(max_length=200)
    credit = models.CharField(max_length=200)
    description = models.CharField(max_length=800)

    def __str__(self):
        return self.photo_description

```
## Activate models
- add `'homes.apps.HomesConfig',` to top of `INSTALLED_APPS`. list in `homepointr/homepointr/settings.py`
- ? check at the end to see if homepointr/homes/apps.py includes:
    ```
    from django.apps import AppConfig


    class HomesConfig(AppConfig):
        name = 'homes'

    ```

## Add a view
- edit `homes/views.py` to: 
```
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Provider, Council, PropertyType, Support, Property, Photo


class IndexView(generic.ListView):
    template_name = 'homes/index.html'
    context_object_name = 'property_list'

    def get_queryset(self):
        return Property.objects.order_by('property_name')


class DetailView(generic.DetailView):
    model = Property
    template_name = 'homes/detail.html'

    def get_queryset(self):
        return Property.objects


class ResultsView(generic.DetailView):
    model = Property
    template_name = 'homes/results.html'
```
- Add new `homes/urls.py` with content:
```
from django.conf.urls import url

from . import views

app_name = 'homes'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$',
        views.ResultsView.as_view(), name='results'),
    url(r'^(?P<Property_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
```
- Edit `homepointr/urls.py` so we have:
```
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^homes/', include('homes.urls')),
    url(r'^admin/', admin.site.urls),
]
```

## Admin
- edit `homes/admin.py` to:
```
from django.contrib import admin

from .models import Provider
from .models import Council
from .models import PropertyType
from .models import Support
from .models import Property
from .models import Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0


class PropertyInline(admin.TabularInline):
    model = Property
    extra = 0
    inlines = [PhotoInline]


class ProviderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['provider_name']}),
    ]
    inlines = [PropertyInline]
    list_display = ('property_name')
    search_fields = ['property_name']


admin.site.register(Provider, ProviderAdmin)
```

## Add templates
- create file `/homes/templates/homes/index.html` with content:
```
{% load static %}

<link rel="stylesheet" type="text/css" href="{% static 'homes/style.css' %}" /> {% if property_list %}

<ul>
    {% for property in property_list %}
    <li><a href="{% url 'homes:detail' property.id %}">{{ property.property_name }}</a></li>
    {% endfor %}
</ul>
{% else %}
<p>No properties are available.</p>
{% endif %}
```
- create file `/homes/templates/homes/detail.html` with content:
```
<h1>{{ property.property_name }}</h1>
```
- create file `/homes/templates/homes/results.html` with content:
```
<h1>{{ property.property_name }}</h1>
```

## Look and feel
- add file `homes/static/homes/style.css` with content:
```
li a {
  color: red;
}
```
- add `admin.site.site_header = 'HomePointr admin'` to `homes/admin.py`


## Migrate the Database
- `python manage.py makemigrations`
- `python manage.py makemigrations homes` to create migrations for model changes
- optional `python manage.py sqlmigrate homes 0001` to see what SQL Django thinks is needed
- optional `python manage.py check` to check for project problems
- `python manage.py migrate` to create model tables in database

## Test App
- `python manage.py runserver 0.0.0.0:8000`
- [localhost:8000/homes](http://localhost:8000/homes)
- [localhost:8000/admin](http://localhost:8000/admin)