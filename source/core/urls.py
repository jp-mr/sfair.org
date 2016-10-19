from django.conf.urls import url

from .views import (

            home,
            contact,
            formation,
            research,
            publications,
        )

# Aqui ficam os endereços da app 'core'
# primeiro o django busca em '/sfair/urls.py'

urlpatterns = [

    # [home] Essa linha procura a função 'home' na 'views.py'
    url(r'^$', home, name='home'),

    # [contact] Essa linha procura a função 'contact' na 'views.py'
    url(r'^contact/$', contact, name='contact'),

    # [formation&CV] Essa linha procura a função 'formation' na 'views.py'
    url(r'^formation&CV/$', formation, name='formation&CV'),

    # [research] Essa linha procura a função 'research' na 'views.py'
    url(r'^research/$', research, name='research'),

    # [publications] Essa linha procura a função 'publications' na 'views.py'
    # Vá para: core/models.py
    url(r'^research/publications/$', publications, name='publications'),
]
