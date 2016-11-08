import os


if os.environ['LOGNAME'] == 'sfair':

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = os.environ['SECRET_PROJECT_KEY']

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = [
        os.environ['ALLOWED_HOST_URL'],
    ]

    # Definições para email    
    EMAIL_HOST = os.environ['HOST_EMAIL']
    EMAIL_HOST_USER = os.environ['HOST_USER_EMAIL']
    EMAIL_HOST_PASSWORD = os.environ['HOST_PASSWORD_EMAIL']
    EMAIL_PORT = 25
    EMAIL_USE_TSL = True
    EMAIL_DESTINY = os.environ['DESTINY_EMAIL']

    # Database
    # https://docs.djangoproject.com/en/1.9/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USER'],
            'PASSWORD': os.environ['DB_PASSWORD'],
            'HOST': os.environ['DB_HOST'],
            'PORT': '3306',
        }
    }
