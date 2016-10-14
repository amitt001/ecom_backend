"""Conatins views that are common to all the applications"""

from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@api_view(['GET'])
@permission_classes([AllowAny])
def api_redirect(request):
    return redirect(reverse('endpoints'))


@api_view(['GET'])
@permission_classes([AllowAny])
def api_endpoints(request):
    netloc = 'https//' if request.is_secure() else 'http://'
    domain = netloc + str(get_current_site(request))
    api_uri = dict(
        auth_api=dict(
            register=domain + reverse('userlist'),
            authentication=domain + reverse('token'),
            verify_token=domain + reverse('verify')
            ),
        product_api=dict(
            products=domain + reverse('products'),
            categories_list= domain + reverse('list_categories')
            ))
    return Response(api_uri)

