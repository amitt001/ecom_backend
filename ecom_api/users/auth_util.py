import jwt
from rest_framework_jwt.utils import jwt_payload_handler
from django.conf import settings
from django.contrib.auth.models import User


def generate_token(user):
    # Expiration time of JWT token 60 minutes
    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    return dict(
        token=token.decode('unicode_escape'),
        exp=payload['exp'],
        user_id=user.id)
