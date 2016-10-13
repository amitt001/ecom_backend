"""Conatins views that are common to all the applications"""

from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def api_endpoints(request):
    netloc = 'https//' if request.is_secure() else 'http://'
    domain = netloc + str(get_current_site(request))
    api_uri = dict(
        products=domain + reverse('products'),
        categories_list= domain + reverse('list_categories'))
    return Response(api_uri)

