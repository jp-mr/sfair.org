from django.conf.urls import url

from .views import (
            teaching,
        )

# Aqui ficam os endereços da app 'teaching'
# primeiro o django busca em '/sfair/urls.py'

urlpatterns = [

    # [teaching] Essa linha procura a função 'teaching' na 'views.py'
    url(r'^$', teaching, name='teaching'),
    #url(r'^research/publications/$', publications, name='publications'),
]
