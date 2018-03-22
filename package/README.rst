========
cse_app
========

cse_app is a simple Django app based on Natural Language Processing.

INSTALLATION
------------

1. Add "cse_app" to your INSTALLED_APPS setting like this,

    INSTALLED_APPS = [
        'cse_app.apps.CseAppConfig',
			...
			...
    ]

2. Include the cse_app URLconf in your project urls.py like this,

    from django.contrib import admin
	from django.urls import include, path

	urlpatterns = [
		path('admin/', admin.site.urls),
		path('cse/', include('cse_app.urls')),
	]

3. You have to install some required modules manually with pip
		pip3 install requests
		pip3 install beautifulsoup4
		pip3 install nltk
			python shell >>> import nltk
						 >>> nltk.download()

4. Run 'python manage.py migrate' in cmd to create the models.

5. Start the development server by running 'python manage.py runserver' and visit http://127.0.0.1:8000/cse/