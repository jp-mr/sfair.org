from django.conf.urls import url

from .views import (
                        home,
                        home2,
                                )


urlpatterns = [
    url(r'^home/', home, name='home'),
    url(r'^home2/', home2, name='home2'),
]
