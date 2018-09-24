# django_oauth
implementing social authentication in django using facebook, twitter, github

This is yet another Django Tutorial. In this one we will be implementing login and
signup **authentication** onto our django backed website using the popular social 
websites like **Facebook**, **Twitter** and **Github**

For this one we will be using [ngrok](https://ngrok.com/download). We will talk more about why ngrok is so important for our project.

# Installation
```
pip install -r requirements.txt
```

One new requirement for our django project this time is 

```
Django==2.1.1
social-auth-app-django==2.1.0
```

social-auth-app-django which can be installed directly if you like also using 

```
pip install social-auth-app-django
```

This module will be the backend logic for social authorizing.

# Project Setup
1. ```django-admin startproject webapp .     ```

2. ```python manage.py migrate```

3. ```python manage.py createsuperuser```

4. Adding ```social_django``` to ```INSTALLED_APPS``` of our **settings**

	```
	# Application definition
	...
	INSTALLED_APPS = [
	    'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	    'social_django',
	]
	```

5. ```.env``` containing ```SECRET_KEY=<your_secret_key>```

6. Config ```.env``` variables using ```python-decouple```

	```
	from decouple import config
	...
	SECRET_KEY = config("PROJECT_KEY")
	...
	```

7. ```migrate``` the database again.

	```
	python manage.py migrate
	...
	Applying social_django.0001_initial... OK
	Applying social_django.0002_add_related_name... OK
	Applying social_django.0003_alter_email_max_length... OK
	Applying social_django.0004_auto_20160423_0400... OK
	Applying social_django.0005_auto_20160727_2333... OK
	Applying social_django.0006_partial... OK
	Applying social_django.0007_code_timestamp... OK
	Applying social_django.0008_partial_timestamp... OK
	```

	The library will automatically handle authentication tokens and all the 
	required information to deal with OAuth and OAuth2. Generally speaking, you 
	won’t need to handle it manually nor access the user’s social profile.

8. Update the ```MIDDLEWARE_CLASSES``` classes by adding 
	```SocialAuthExceptionMiddleware``` to the end of it.

9. Update ```context_processors``` inside ```TEMPLATES``` in ```settings.py```

	```
	TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',  # oauth-settings
                'social_django.context_processors.login_redirect',  # oauth-settings
            ],
	```

10. Add the ```AUTHENTICATION_BACKENDS```: 

	```
	AUTHENTICATION_BACKENDS = (
	    'social_core.backends.github.GithubOAuth2',
	    'social_core.backends.twitter.TwitterOAuth',
	    'social_core.backends.facebook.FacebookOAuth2',
	    'django.contrib.auth.backends.ModelBackend',
	)
	```

	**Notice** the ```github``` ```twitter``` and ```facebook``` backends are new
	and ```ModelBackend``` is by default in django.

	Since here in this example we will be working with GitHub, Twitter and 
	Facebook I just added those three backends.

# Update URLS
Now we need to update our urls and add social-auth-app-django urls.

For this either you can create a ```views.py``` file where ```urls.py``` is 
locted for ```webapp``` or you can create a separate app for the project

I will cover both cases here... **Use only one case**

First ```views.py``` in single project folder

```
+ webapp
	- __init__.py
	- settings.py
	- urls.py
	- views.py
	- wsgi.py
```

Inside ```views.py``` add

```
from django.shortcuts import render

def home_view(request):
	return render(request, 'index.html')
```

Now creating a separate app

```
python manage.py startapp display
```

display/views.py
```
from django.shortcuts import render

def home_view(request):
	return render(request, 'index.html')
```

## Project URLS

**webapp/urls.py**
```
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import login, logout

# use either one as per your project
from display.views import home_view 	# for separate app
from .views import home_view 	# for views.py in webapp folder

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home')
]

urlpatterns += [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]

urlpatterns += [
    path('oauth/', include('social_django.urls', namespace='social')),
]
```

## Add Login Urls In Settings
```
...
AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


# AUTHENTICATION URLS

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'dashboard'
...
```

Let's also create a view for redirecting users after they have successfully 
logged in to our app. That is where ```'dashboard'``` comes in

**views.py**
```
def dashboard_view(request):
	return render(request, 'dashboard.html')
```

And url for **dashboard**

**urls.py**
```
from display.views import home_view, dashboard_view

...
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
```

Now create the templates ```home.html``` and ```dashboard.html``` and 
```base.html``` in templates folder, I will use bootstrap in my templates, so I 
have **static** folder also that contains all the files. You can refer my 
templates and static folder and copy paste the code from there.
