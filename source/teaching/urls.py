from django.conf.urls import url

from .views import (
            student_login,
            student_area,
            teaching,
        )

# Aqui ficam os endereços da app 'teaching'
# primeiro o django busca em '/sfair/urls.py'

urlpatterns = [

    # [teaching] Essa linha procura a função 'teaching' na 'views.py'
    url(r'^$', teaching, name='teaching'),
    url(r'^student/login/$', student_login, name='student-login'),
    url(r'^student/area/$', student_area, name='student-area'),
    #url(r'^research/publications/$', publications, name='publications'),
]
