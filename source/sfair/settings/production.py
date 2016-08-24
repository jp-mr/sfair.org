from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = [
    KW[1],
]


# Definições para email    
EMAIL_HOST = KW[2]
EMAIL_HOST_USER = KW[3]
EMAIL_HOST_PASSWORD = KW[4]
EMAIL_PORT = 25
EMAIL_USE_TSL = True


# Para testar localmente o envio de email descomente as linhas abaixo e 
# rode em outra instancia do terminal o comando: 
# $python -m smtpd -n -c DebuggingServer localhost:1025

#EMAIL_HOST = 'localhost'
#EMAIL_PORT = 1025
#EMAIL_HOST_USER = 'contact@sfair.org'
#EMAIL_HOST_PASSWORD = None


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': KW[5],
        'USER': KW[6],
        'PASSWORD': KW[7],
        'HOST': KW[8],
        'PORT': '3306',
    }
}


