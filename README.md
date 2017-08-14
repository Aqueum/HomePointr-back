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

the following was originally based on[how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04):
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
import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

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

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'homes/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'homes/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'homes/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'homes/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('homes:results', args=(question.id,)))

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
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
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

from .models import Question
from .models import Choice


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
```

## Add templates
- create file `/homes/templates/homes/index.html` with content:
```
{% load static %}

<link rel="stylesheet" type="text/css" href="{% static 'homes/style.css' %}" /> {% if latest_question_list %}

<ul>
    {% for question in latest_question_list %}
    <li><a href="{% url 'homes:detail' question.id %}">{{ question.question_text }}</a></li>
    {% endfor %}
</ul>
{% else %}
<p>No homes are available.</p>
{% endif %}
```
- create file `/homes/templates/homes/detail.html` with content:
```
<h1>{{ question.question_text }}</h1>

{% if error_message %}
<p><strong>{{ error_message }}</strong></p>{% endif %}

<form action="{% url 'homes:vote' question.id %}" method="post">
    {% csrf_token %} {% for choice in question.choice_set.all %}
    <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}" />
    <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br /> {% endfor %}
    <input type="submit" value="Vote" />
</form>
```
- create file `/homes/templates/homes/results.html` with content:
```
<h1>{{ question.question_text }}</h1>

<ul>
    {% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }} -- {{ choice.votes }} vote{{ choice.votes|pluralize }}</li>
    {% endfor %}
</ul>

<a href="{% url 'homes:detail' question.id %}">Vote again?</a>
```

## Look and feel
- add file `homes/static/homes/style.css` with content:
```
li a {
  color: green;
}

body {
  background: white url("images/python.gif") no-repeat right bottom;
}
```
- add file `homes/static/homes/images/python.gif`
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