from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)

from .models import Product, ProductManager
from .utils import (
    serializer_factory, model_factory, top_level_dict, add_hyperlink)


@api_view(['GET'])
def products(request):
    """Get all the products irrespective of the product category

    Sample URL: /api/1.0/products/?q=moto&in_stock=1&start=1&count=2

    Filters:
        q = <search str>
        start: int
        count: int
        featured: 0/1 bool
        in_stock: 0/1 bool
    """
    manager = ProductManager()
    kw = manager.validate_filters(request)
    products = manager.find(**kw)
    for category, product in products.iteritems():
        top_level_serializer = top_level_dict(product)
        products[category] = add_hyperlink(request, top_level_serializer)
    # Add hyperlink to itself each resource
    # using `build_absolute_uri` method for building url
    return Response(products)


@api_view(['GET', 'POST'])
def categories(request, category):
    """Get and create a product belonging to a specific category.

    Sample URL: /api/1.0/products/shoes?q=nik&start=1&count=1&featured=0

    Sample POST payload(with only the required fields)

        Category: Shoes

            {
                "name": "Nike T Sports", "category": "SHOE",
                "manufacturer": "Nike", "price": 1999,
                "quantity": 20, "size": 9, "colour": "Yellow",
                "shoe_type": "MOUNTAINEERING"
            }
    """
    try:
        _ProductModel = model_factory(category)
        _ProductSerializer = serializer_factory(category)
    except KeyError:
        return Response(dict(error='Invalid product category'),
                        status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        manager = ProductManager()
        kw = manager.validate_filters(request)
        category_data = manager.find_by_category(
            _ProductModel, _ProductSerializer, **kw)
        top_level_serializer = top_level_dict(category_data)
        return Response(add_hyperlink(request, top_level_serializer))

    elif request.method == 'POST':
        data = request.data
        is_anon = request.user.is_anonymous()
        # If seller info is None and set current user as seller
        if request.data.get('seller') is None and is_anon is False:
            data['seller'] = request.user.id
        # Set the product info creater data
        if is_anon is False:
            data['added_by'] = request.user.id
        # Get `Product` model specific data and put it in `product`
        # key for serialization
        product_fields = [f.name for f in Product._meta.get_fields()]
        product_data = dict((field, data.pop(field)
            ) for field in product_fields if field in data)
        data['product'] = product_data

        serializer = _ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            top_level_serializer = top_level_dict(serializer.data)
            return Response(add_hyperlink(request, top_level_serializer),
                            status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def category(request, category, _id):
    """A specific item/product details view"""
    
    _ProductModel = model_factory(category)
    _ProductSerializer = serializer_factory(category)
    product = get_object_or_404(_ProductModel, pk=_id)

    if request.method == 'GET':
        serializer = _ProductSerializer(product)
        top_level_serializer = top_level_dict(serializer.data)
        return Response(add_hyperlink(request, top_level_serializer))

    elif request.method == 'PUT':
        data = request.data
        # Get `Product` model specific data and put it in `product`
        # key for serialization
        product_fields = [f.name for f in Product._meta.get_fields()]
        product_data = dict((
            field, data.pop(
                field)) for field in product_fields if field in data)
        data['product'] = product_data

        serializer = _ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            top_level_serializer = top_level_dict(serializer.data)
            return Response(add_hyperlink(request, top_level_serializer))
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=HTTP_204_NO_CONTENT)


@api_view(['GET'])
def list_categories(request):
    netloc = 'https//' if request.is_secure() else 'http://'
    domain = netloc + str(get_current_site(request))
    manager = ProductManager()
    categories = dict(
        (u[0], domain + reverse('categories', kwargs={'category': u[0]}).lower()
            ) for u in manager.categories)
    return Response(categories)
