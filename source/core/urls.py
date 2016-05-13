from django.conf.urls import url

from .views import ( home, contact, )


urlpatterns = [

    # [1] Essa linha procura a função 'home' na 'views.py'
    url(r'^$', home, name='home'),

    url(r'^contact/$', contact, name='contact'),
]
