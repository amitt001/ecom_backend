from django.conf.urls import include, url
from rest_framework_jwt.views import verify_jwt_token
import views

urlpatterns = [
    url(r'^$', views.UserRegister.as_view(), name='userregister'),
    url(r'token/?$', views.get_token, name='token'),
    url(r'verify/?$', verify_jwt_token, name='verify'),
    url(r'(?P<id>[0-9]+)/?$', views.UserDetails.as_view(), name='userdetails')
]