from django.conf.urls import include, url
from django.conf import settings

from commons import api_endpoints
from product_management import urls as prod_urls
from users import urls as users_url


_API_VERSION = settings.API_VERSION

urlpatterns = [
    url(r'^api/{}/?$'.format(_API_VERSION), api_endpoints),
    # Users and authentication
    url(r'^api/{}/users/'.format(_API_VERSION), include(users_url)),
    # product management
    url(r'^api/{}/products/'.format(_API_VERSION), include(prod_urls)),
]
