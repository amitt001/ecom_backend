
from django.conf.urls import include, url

import views

urlpatterns = [
    url(r'^$', views.all_products, name='products'),
    url(r'categories/?$', views.list_categories, name='list_categories'),
    url(r'(?P<category>[a-zA-Z]+)/?$', views.categories, name='categories'),
    url(r'(?P<category>[a-zA-Z]+)/(?P<_id>[0-9]+)/?$', views.category, name='list_by_id'),
]