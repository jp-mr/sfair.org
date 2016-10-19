from sfair.keywords import keys

import os


# Para testar localmente o envio de email rode em outra 
# instancia do terminal o comando:
# $python -m smtpd -n -c DebuggingServer localhost:1025

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = 'contact@sfair.org'
EMAIL_HOST_PASSWORD = None


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party
    'crispy_forms',
    'markdown_deux',
    'pagedown',
    # local project
    'core',
]
