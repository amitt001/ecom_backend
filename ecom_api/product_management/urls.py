
from django.conf.urls import include, url

import views

urlpatterns = [
    url(r'^$', views.products),
    url(r'(?P<category>[a-zA-Z]+)/?$', views.categories),
    url(r'(?P<category>[a-zA-Z]+)/(?P<_id>[0-9]+)/?$', views.category),
]