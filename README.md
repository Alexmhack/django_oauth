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
from django.contrib.auth.views import LoginView, LogoutView

# use either one as per your project
from display.views import home_view 	# for separate app
from .views import home_view 	# for views.py in webapp folder

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home')
]

urlpatterns += [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
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
from django.contrib.auth.decorators import login_required

@login_required
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

If you now go to [127.0.0.1:8000/login](http://127.0.0.1:8000/login) you would get error saying template does not exist at ```registration/login.html```

This comes of from the ```LoginView.as_view()``` and the same would happen with
logout url so let's create a folder **registration** in templates folder.

Inside registration folder create ```login.html``` and ```logout.html``` files.

We will add html code in them. But now we will handle the social authentications.

# Github Authentication
Go to your github account and go to **settings** page. On the left side menu in 
the bottom click on **Developer settings**. In there click on **OAuth 
Applications**.

In there **Register a new application** and fill in the details. You can enter 
any details in the other fields but the most important field is the 
**Authorization callback URL**.

Since we are working on localhost we will enter 
```http://localhost:8000/oauth/complete/github/```

Hit Create and you will get the ```Client ID``` and ```Client Secret```

```
Client ID
------------

Client Secret
------------
```

This information has to be kept secret so, we will use ```.env``` file

```
SOCIAL_AUTH_GITHUB_KEY=<your id>
SOCIAL_AUTH_GITHUB_SECRET=<your secret>
```

We have our settings ready, now we will add a github login button in login template

```
<a type="button" href="{% url 'social:begin' 'github' %}" class="light-blue-text mx-2">
<i class="fa fa-github"></i>
</a>
```

Important part is ```{% url 'social:begin' 'github' %}```

Go to [127.0.0.1:8000/login](http://127.0.0.1:8000/login) url again and click on
github login url. It should give you errors mentioning ```redirect_uri```

That errors are due to ```localhost``` set at the **Authorization callback URL**
of github account. Okay the first way to solve that problem is to use **hosts**
in **windows**

Go to ```C:\Windows\System32\drivers\etc``` and open ```hosts``` file with 
notepad...

At last you should see...

```
#	127.0.0.1       localhost
#	::1             localhost
```

After this add 

```
127.0.0.1		djapp.com
127.0.0.1		www.djapp.com
```

You can change ```djapp.com``` to any other url but I am using this one.

Now we need to configure our github app and add 
```http://djapp.com:8000/oauth/complete/github/``` to **Authorization callback URL** and then **Update Seetings**

Now if you run server and  head to [http://djapp.com:8000/](http://djapp.com:8000/) you should see your homepage on the browser. So what we 
have done is redirect our localhost to ```http://djapp.com:8000/``` url on the 
local computer.

Now go to login url again and then click github login button and everything 
works fine. You can authenticate github app and after process is complete you 
should be redirected to ```dashboard``` url because we have set that in 
```settings.py``` file under ```LOGIN_REDIRECT_URL = 'dashboard'```

One more thing you can do is to display the username on the dashboard template

**templates/dashboard.html**
```
{% extends "base.html" %}

{% block title %}
	{{ block.super }}
{% endblock %}

{% block content %}

	<h1 class="mt-5 text-center">Welcome {{ request.user }}</h1>

{% endblock content %}
```

## Django [Admin](http://127.0.0.1:8000/admin/)
If you head onto admin site. You should see ```Python Social Auth``` section.
Click on it and you find the users that have logged in using github. Try 
creating more users by logging out and then again logging in with another github 
account. You should see all users onto admin site.

**The next time you logout and then again login using the github link it should 
automatically authenticate and redirect to dashboard**

# Twitter Authentication
Go to [apps.twitter.com](http://apps.twitter.com) and it should prompt you to 
setup developer account. Fill in all the details and after process is complete 
and on apps page of developer account click on **Create new App**. When asked to 
enter **callback url** enter ```http://djapp.com:8000/oauth/complete/twitter/```
or whatever you saved in ```hosts``` file.

Go to **Permissions** section and edit it and set to **Read only**. The less 
permissions we have better. This way we make our users more comfortable.

Now go to Keys and Access Tokens tab and grab the Consumer Key (API Key) and 
Consumer Secret (API Secret) and update the settings.py:

```
SOCIAL_AUTH_TWITTER_KEY = config("SOCIAL_AUTH_TWITTER_KEY")
SOCIAL_AUTH_TWITTER_SECRET = config("SOCIAL_AUTH_TWITTER_SECRET")
```

And yes don't forget to add those variables with your values in ```.env``` file.

Again add the twitter url onto login page

```
<a href="{% url 'social:begin' 'twitter' %}">Login with twitter</a>
```

On clicking this link you should get prompt to authorize application. This 
should redirect you to the dashboard and display your username on twitter.

If you visit the admin site and look at the **User social auths** and you should
see the provider and twitter username.

# Facebook Authenticaion
Go to [developers.facebook.com/](http://developers.facebook.com/) click on My 
Apps and then Add a New App. On the app page on the left menu bar click on 
**settings > basic** and copy the **App ID** and **App Secret** and add it to
```.env``` file then set them in **settings.py**

```
SOCIAL_AUTH_FACEBOOK_KEY = config("SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = config("SOCIAL_AUTH_FACEBOOK_SECRET")
...
```

Add facebook login url in login template 
```{% url 'social:begin' 'facebook' %}```
