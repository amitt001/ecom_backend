from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)
from .models import Shoes
from .serializers import ShoesSerializer

@api_view(['GET', 'POST'])
def products(request):
    """Get all the products irrespective of the product category"""
    if request.method == 'GET':
        shoes = Shoes.objects.all()
        serializer = ShoesSerializer(shoes, many=True)
        return Response(serializer.data)

    
@api_view(['GET', 'POST'])
def categories(self, request):

    ProductModel = category_model[category]
    ProductSerializer = category_serializer[category]

    if request.method == 'GET':
        product = ProductModel.objects.all()
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'POST':
        # TODO: handle this
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def category(self, request, category, _id):
    
    ProductModel = category_model[category]
    ProductSerializer = category_serializer[category]

    if request.method == 'GET':
        product = get_object_or_404(ProductModel, pk=_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        product = get_object_or_404(ProductModel, pk=_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product = get_object_or_404(ProductModel, pk=_id)
        product.delete()
        # TODO redirect
        return Response(status=HTTP_204_NO_CONTENT)



def category_model(category):
    return {
        'shoes': Shoes,
    }[category]


def category_serializer(category):
    return {
        'shoes': ShoesSerializer,
    }[category]