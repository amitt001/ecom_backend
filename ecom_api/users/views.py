"""User and Authentication views.

All the user CRUD and JWT token authentication is done in this view.
All the views in this app have unrestricted `AllowAny` access.

# Permissions: http://www.django-rest-framework.org/api-guide/permissions/

NOTE:
In `User` model `username` and `email` fields can be used interchangeably.
Username field is kept for compatability with django `User` model"""

from django.db import IntegrityError
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN)

from .auth_util import generate_token
from .serializers import UserSerializer


INTEGRITY_USERNAME_MSG = "Unique constraint failed for column 'email'"
USERS_FAIL_MSG = dict(
    detail="Only admin user can access all the user's data.")

class UserRegister(APIView):
    """Get all the users(Only for admin) or register user to get API token.
        
    Allowed methods: GET, POST"""
    permission_classes = (AllowAny,)

    def get(self, request):
        # Only allow access to registered user. Because Django doesn't
        # allow method based permission in class
        if not request.user.is_superuser:
            return Response(USERS_FAIL_MSG, status=HTTP_403_FORBIDDEN)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        user_data = request.data
        user = UserSerializer(data=user_data)
        if user.is_valid():
            try:
                user.save()
            except IntegrityError as e:
                # Convert, if unique username error raised by Django `User`
                # model, to unique email error
                if 'auth_user.username' in e.args[0]:
                    e.args = (INTEGRITY_USERNAME_MSG,)
                return Response(
                    dict(error=e.args[0]), status=HTTP_400_BAD_REQUEST)
            return Response(user.data, status=HTTP_201_CREATED)
        return Response(user.errors, status=HTTP_400_BAD_REQUEST)


class UserDetails(APIView):
    """A single user views. A unique user is identified using `pk`

    Allowed Methods: GET, POST, DELETE"""

    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id):
        user = get_object_or_404(User, ok=id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data) # TODO: add status
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        user = get_object_or_404(User, pk=id)
        user.delete()
        # TODO: redirect
        return Response(status=HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    try:
        email = request.data['email']
        password = request.data['password']
    except KeyError:
        return Response(
            dict(error="Email/Password missing"), status=HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, email=email)
    # Using user object's `check_password` method
    # which compare both the password hashes
    if user.check_password(password):
        # Token metadata after authentication
        token=generate_token(user)
        return Response(token)
    return Response(status=HTTP_401_UNAUTHORIZED)